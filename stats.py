import pandas as pd
import fields
import util


def starting_probability(chat_from, chat_to):
    """returns the probability of starting the conversation for each person"""
    from_frac = chat_from[chat_from['start'] == 1].shape[0] / chat_from.shape[0]
    to_frac = (chat_to[chat_to['start'] == 1].shape[0] / chat_to.shape[0])

    from_prob = ( from_frac/ (from_frac + to_frac))
    to_prob = (to_frac / (from_frac + to_frac))

    return from_prob, to_prob


def average_delay(chat):
    """returns the average time that passes between answering the other person (use with dataframe filtered by author)"""
    return chat.delay.mean()


def most_likely_words(chat_from, chat_to, min=0, len=0):
    """calculates the conditional probability P(author|word) and returns the characterising words for each person

    Args:
        chat_from (pd.DataFrame): telegram chat for author 1
        chat_to (pd.DataFrame): telegram chat for author 2
        min (int): minimum number of occurrences of word (both persons) for it to be added to the result
        lin (int): minimum length of word for it to be added to the result

    Returns:
        from_characterising_words (pd.Series): sorted series with characterising words for author 1
        to_characterising_words (pd.Series): sorted series with characterising words for author 2
    """
    # todo add the option to only returns words with probability <1 (i.e., used by both persons at least once)
    from_probabilities = dict()
    to_probabilities = dict()
    words_from_counter = util.generate_words_list(chat=chat_from, emojis=False)
    words_to_counter = util.generate_words_list(chat=chat_to, emojis=False)
    words_counter = words_from_counter + words_to_counter
    words_from = list(words_from_counter.keys())
    words_to = list(words_to_counter.keys())
    words = words_from + words_to
    chat_from.index = chat_from.idx  # Indexing a DataFrame with a datetimelike index error with '2021'!
    chat_to.index = chat_to.idx  # Indexing a DataFrame with a datetimelike index error with '2021'!
    for word in words:
        word = str(word)
        if (word not in chat_from.columns) & (word not in chat_to.columns) & (word != '2021') & len(word > len):

            chat_from[word] = fields.count_specific_word(words_srs=chat_from['words'], word=word)
            chat_to[word] = fields.count_specific_word(words_srs=chat_to['words'], word=word)

            if words_counter[word] > min:
                from_probabilities[word] = (chat_from[word].sum() / words_counter[word])
                to_probabilities[word] = (chat_to[word].sum() / words_counter[word])

    from_characterising_words = pd.Series(from_probabilities).sort_values(ascending=False)
    to_characterising_words = pd.Series(to_probabilities).sort_values(ascending=False)

    return from_characterising_words, to_characterising_words


def monologues(chat, n_monologues=5):
    """returns a list of the n_monologues (default=5) longest monologues in the conversation"""
    monologues_list = []
    chat.index = chat.idx
    for i in range(0, n_monologues):
        idx = chat.sort_values(['combo'], ascending=False).idx.values[0]
        n_messages = chat.sort_values(['combo'], ascending=False).combo.values[0]
        temp_string = ''
        for j in range(0, n_messages):
            current_idx = idx + j
            current_message = chat[chat.idx == current_idx]['text'].values[0]
            temp_string += (current_message + '\n')
            chat = chat.drop([current_idx])
        temp_string += ('\n\n\n')
        print(temp_string)
        monologues_list.append(temp_string)
    return monologues_list


def average_word_length(chat, cutoff):
    return sum([len(st) for row in chat['words'] for st in row if len(st) > cutoff]) / len(
        [st for row in chat['words'] for st in row if len(st) > cutoff])


def questions_and_statements(chat):
    statements = chat['text'].map(lambda x: x[-1] == '?' if len(x) > 0 else False).value_counts()[0]
    questions = chat['text'].map(lambda x: x[-1] == '?' if len(x) > 0 else False).value_counts()[1]
    return statements, questions


def most_common_words(chat, n=20):
    words_counter = util.generate_words_list(chat, False)
    return words_counter.most_common(n)


def most_common_emojis(chat, n=20):
    emojis_counter = util.generate_words_list(chat, True)

    return emojis_counter.most_common(n), len(emojis_counter)


def average_words_per_message(chat):
    return chat['n_words'].mean()


def total_messages(chat):
    return chat.shape[0]


def total_words(chat):
    return chat['n_words'].sum()


def average_consecutive_messages(chat):
    return chat['combo'].mean() + 1


def n_specific_word(chat, word):
    """counts the occurrences of a specific word (needs fields.count_specific_word to be called first to add the
    column [word] to chat"""
    return chat[word].sum()


