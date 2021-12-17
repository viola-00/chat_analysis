import util


def add_start_and_delay(chat, delay_max=3600):
    """adds the column ['start'] which keeps track of the person who started the conversation,
    and the column ['delay'] that calculates the delay in answering between messages by different persons

    Args:
        chat (pd.DataFrame): the telegram chat dataframe
        delay_max (int): the max number of seconds between messages for a conversation to count as the same
        (e.g., if delay_max=3600 and a person says hi after waking up,
        and the previous message is from the other person 8 hours before, the delay will be count as 0, not 8 hours)

    Returns:
        the chat dataframe given in input enriched with the ['start'] and ['delay'] columns
    """

    delay = [0]
    start = [1]
    last = chat.iloc[0]
    for i in range(1, chat.shape[0]):
        row = chat.iloc[i]
        if last['from'] != row['from']:
            d = abs(last['date'] - row['date']).total_seconds()
            if d < delay_max:
                delay.append(d)
                start.append(0)
            else:
                delay.append(0)
                start.append(1)
        else:
            delay.append(0)
            start.append(0)
        last = row
    chat['delay'] = delay
    chat['start'] = start
    return chat


def add_combo(chat, delay_max=3600):
    """adds the column [combo] to chat.
    used to count the number of consecutive messages in stats.py.
    e.g., if a person sent four consecutive messages
    the first one will have the value 4 in chat['combo']

    Args:
        chat (pd.DataFrame): the telegram chat dataframe
        delay_max (int): the max number of seconds between messages for a conversation to count as the same
        (e.g., if 7 consecutive messages are sent by the same person but only the first 3 are sent
        during the same day (and delay_max=3600), ['combo'] will display 3 not 7)

    Returns:
        the chat dataframe given in input enriched with the ['combo'] column
        """
    chat['idx'] = range(0, chat.shape[0])
    chat.index = chat['idx']
    chat['combo'] = 0
    i = 0
    while i < chat.shape[0] - 1:
        tot = 0
        k = 1
        while chat.iloc[i]['from'] == chat.iloc[i + k]['from'] and \
                (abs(chat.iloc[i + k - 1]['date'] - chat.iloc[i + k]['date']).total_seconds() < delay_max):
            tot = tot + 1
            k = k + 1
        chat.at[chat.iloc[i].idx, 'combo'] = tot
        i = i + k
    return chat


def add_lowercase_text(srs):
    return srs.map(lambda x: str(x).lower())


def add_message_words(text_srs):
    """given a series of messages (text), returns a list of all the words used in each message"""
    return text_srs.map(
        lambda x: util.find_words(x.lower()) + util.find_emojis(x.lower()) if isinstance(x, str) else list())


def add_message_emojis(text_srs):
    """given a series of messages (text), returns a list of all the emojis used in each message"""
    return text_srs.map(lambda x: util.find_emojis(x))


def add_datetime(date_srs):
    return date_srs.map(lambda x: util.get_datetime(str(x)))


def add_n_words(words_srs):
    """given a series of lists of words, returns the length of each list"""
    return words_srs.map(lambda x : len(x))


def add_call_duration(chat):
    return chat.apply(lambda x: 0 if x['type'] != 'service' else x['duration_seconds'], axis=1)


def set_index(chat, date_field_str):
    """sets the date as the dataframe index (takes as arguments the dataframe and the label for the date column)"""
    chat = chat.sort_values(by='date')
    chat = chat.set_index('date')
    chat[date_field_str] = chat.index
    return chat


def count_specific_word(words_srs, word):
    """counts the occurrences of a specific word for each message (used to add this information as a dataframe column)

    Args:
        words_srs (pd.Series): series representing the words per each message
        word (str): the word we want to know the occurrences of

    Returns:
          series with the occurrences of word for each message (to add as chat dataframe column)
        """
    return words_srs.map(lambda x: x.count(word) if isinstance(x, list) else 0)


def add_fields(chat):
    """adds all the necessary fields to the initial dataframe"""
    chat['text_original'] = chat['text']
    chat['date_original'] = chat['date']
    chat['text'] = add_lowercase_text(chat['text'])
    chat['words'] = add_message_words(chat['text'])
    chat['n_words'] = add_n_words(chat['words'])
    chat['emoji'] = add_message_emojis(chat['text'])
    chat['date'] = add_datetime(chat['date'])
    chat['call_duration'] = add_call_duration(chat)
    chat = add_start_and_delay(chat=chat, delay_max=3600)
    chat = add_combo(chat= chat, delay_max= 3600)
    chat = set_index(chat, 'date')
    return chat