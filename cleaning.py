import pandas as pd
import re
import util
import datetime as dt


# cleaning.py is not used in the current version of the project! only telegram chats are used
# todo update functions to current format for fb and whatsapp so that they can be added again
def clean_tg_data(conv_names_tg, actual_names):
    chat = pd.read_json(actual_names[1] + '_T.jsonl', lines=True)
    chat['from'] = chat['from'].map(lambda x: x['first_name'])
    chat['from'].replace(conv_names_tg[0], actual_names[0], inplace=True)
    chat['from'].replace(conv_names_tg[1], actual_names[1], inplace=True)

    chat = chat[['from', 'text', 'date']]
    chat.dropna(inplace=True)

    return chat


def clean_fb_data(conv_names_fb, actual_names, time):
    chat = pd.read_csv(actual_names[1] + '_F.csv')
    chat.drop('thread', axis=1, inplace=True)
    chat.rename(columns={'sender': 'from', 'message': 'text'}, inplace=True)
    chat = util.change_dates(chat, time)

    chat['from'].replace(conv_names_fb[0], actual_names[0], inplace=True)
    chat['from'].replace(conv_names_fb[1], actual_names[1], inplace=True)

    chat.dropna(inplace=True)
    return chat


def clean_wa_data(conv_names_wa, actual_names):
    dates = []
    authors = []
    messages = []
    with open(actual_names[1] + '_W.txt', 'r') as f:
        for line in f:
            if (re.match(".*, \d\d:\d\d . .*: .*", line) is not None):  # italian whatsapp has different formatting!
                split_line = line.split("- ", 1)  # 1 maxsplit argument to split only on first
                print(line)
                date = split_line[0]
                author = split_line[1].split(": ")[0]
                message = split_line[1].split(": ")[1][:-1]  # [:-1] excludes \n

                dates.append(date)
                authors.append(author)
                messages.append(message)

    chat = pd.DataFrame(columns=['date', 'from', 'text'])
    chat['date'] = dates
    chat['from'] = authors
    chat['text'] = messages
    chat['date'] = chat['date'].map(lambda x: dt.datetime.strptime(x, '%d/%m/%Y, %H:%M '))
    chat['from'].replace(conv_names_wa[0], actual_names[0], inplace=True)
    chat['from'].replace(conv_names_wa[1], actual_names[1], inplace=True)
    chat.dropna(inplace=True)
    return chat


def unite(chat_fb, chat_wa, chat_tg):
    """unites messages from facebook, whatsapp, and telegram in a single dataframe sorted by date.
    adds column ['type'] to reconstruct the single dataframes"""
    chat_fb['type'] = 'facebook'
    chat_tg['type'] = 'telegram'
    chat_wa['type'] = 'whatsapp'
    chat = chat_fb.append(chat_wa)
    chat = chat.append(chat_tg)
    chat.sort_values('date')

    return chat
