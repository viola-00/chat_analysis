import pytz
import datetime as dt
import string
import urllib.request as ur
import re
import emoji
import pandas as pd
from collections import Counter


def read_chat(path):
    """given the json path, produces the corresponding dataframe"""
    j = pd.read_json(path, encoding='utf-8')
    chat = pd.DataFrame(j['messages'].tolist())
    return chat


def generate_words_list(chat, emojis=False):
    """generates a Counter of the most used words/emojis
    Args:
        chat (pd.DataFrame): the full dataframe of the telegram chat
        emojis (bool): set to True if you want the output for emojis instead of words; default is False

    Returns:
        words_counter (Counter): counter with all the unique words used and their occurrences

    """
    if emojis:
        column='emoji'
    else:
        column='words'
    words_complete = [st for row in chat[column] for st in row]

    words_counter = Counter(words_complete)

    return words_counter


def remove_emojis(text):
    html = str(ur.urlopen('http://www.unicode.org/Public/emoji/5.0/emoji-data.txt').read())
    codes = list(map(lambda x: '-'.join(['\\U'+a.zfill(8) for a in x.split('..')]).encode().decode('unicode-escape'),
                     re.findall(r'(?<=\\n)[\w.]+', html)))
    emoji_pattern = re.compile('['+','.join(codes)+']', flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)  # no emoji


def remove_punctuation(text):
    clean_text = text
    for c in string.punctuation:
        if (c != '\''):
            clean_text = clean_text.replace(c, "")
    clean_text = clean_text.replace("’", " ")  # sigh
    return clean_text


def find_words(s):
    return re.findall(r"[\w']+", s)


def find_emojis(s):
    return [c for c in s if c in emoji.UNICODE_EMOJI['en']]


def get_datetime(s):
    s = s[:19]  # removes milliseconds
    frmt = '%Y-%m-%dT%H:%M:%S'
    return dt.datetime.strptime(s, frmt)


def change_dates(chat, time):
    chat['date'] = chat['date'].map(lambda x: dt.strptime(x[:16], '%Y-%m-%dT%H:%M'))
    utc = pytz.utc
    chat['date'] = chat['date'].map(lambda x: utc.localize(x).astimezone(time).tz_localize(None))

    return chat
