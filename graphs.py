import fields
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud, STOPWORDS


def plot_words(chat, word_list, freq=False):
    """plots the occurrences of the words in word_list through time

    Args:
        chat (pd.DataFrame): the telegram chat dataframe
        word_list (list): list of the words we want to plot the occurrences of
        freq (bool): if True, returns the frequency of the word vs other words rather than the absolute number of occurrences

    Returns:
        plots generated
    """
    chat_list = [chat] * len(word_list)
    for word, chat in zip(word_list, chat_list):
        chat[word] = fields.count_specific_word(chat['words'], word)

        if freq:
            df = chat.groupby(pd.Grouper(freq='M')).agg({word: 'sum', 'text': 'count'})
            (df[word]/df['text']).plot()
        else:
            chat.groupby(pd.Grouper(freq='M')).sum()[word].plot()
    plt.title('Words over time')
    plt.xlabel('date')
    plt.ylabel('occurrences')
    plt.legend(loc="upper left", prop={'size': 18})


def messages_over_time(chat):
    """plots the number of messages over time"""
    chat.groupby(pd.Grouper(freq='D')).count()['text'].plot()
    plt.xlabel('date')
    plt.ylabel('number of messages')
    plt.title('Messages over time')


def calls_over_time(chat):
    """plots the seconds in calls over time"""
    chat.groupby(pd.Grouper(freq='d')).sum()['call_duration'].plot()
    plt.xlabel('date')
    plt.ylabel('seconds in call')
    plt.title('Calls over time')


def weekly_messages(chat):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    chat.groupby(chat.index.day_name()).count()['text'].reindex(days).plot(kind='bar')


def hourly_messages(chat, color='blue', label=''):
    chat.groupby(chat.index.hour).count()['text'].plot(color=color, label=label)


def messages_heatmap(chat):
    """creates a heatmap of messages over time by hour and weekday"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    plt.figure(figsize=(20, 5))
    pivot = chat.pivot_table(index=chat['date'].dt.day_name(),
                             columns=chat['date'].dt.hour,
                             values='text',
                             aggfunc='count').reindex(days)
    pivot.fillna(0, inplace=True)
    ax = sns.heatmap(pivot)
    plt.xlabel('hour')
    plt.ylabel('weekday')
    plt.title('Heatmap')

    plt.ylim(top=0, bottom=len(pivot))


def media_types(chat, title='Media types'):
    """pie chart of media types (stickers, audio messages, GIFs...)"""
    n = chat['media_type'].value_counts().shape[0]
    explode = (0.01, 0.05, 0.073, 0.1, 0.15)[:n]
    chat['media_type'].value_counts().plot(kind='pie', explode=explode, title=title)


def create_wordcloud(chat, additional_stopwords=[]):
    """creates a wordcloud with the most commonly used words.
    additional_stopwords can be used to add words to be ignored"""
#   stopwords = STOPWORDS.union(set(get_stop_words('en')).union(set(get_stop_words('it')))).union(additional_stopwords)
    stopwords = STOPWORDS.update(additional_stopwords)

    words = [word.lower() for sublist in chat['words'].values for word in sublist]
    wordcloud = WordCloud(stopwords=stopwords, max_font_size=60, width=500, height=250,
                          background_color='#f0efeb', colormap='viridis', min_word_length=2,
                          min_font_size=10).generate(' '.join(words))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()


def language_ratio(chat):
    # todo rewrite using current algorithm for language
    (chat.groupby(pd.Grouper(freq='m'))['en'].sum() / chat.groupby(pd.Grouper(freq='m'))['it'].sum()).plot(
        label='En to It ratio')
    plt.title('English to Italian ratio over time')
    plt.xlabel('date')
    plt.ylabel('En:It ratio')
    plt.legend(loc="upper left", prop={'size': 18})


def mood_graph(chat):
    # todo rewrite with new r algorithm
    chat.groupby(pd.Grouper(freq='m'))['total_mood'].sum().plot()
    plt.title('Mood over time')
    plt.xlabel('date')
    plt.ylabel('mood')
