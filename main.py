
if __name__ == '__main__':
    import fields
    import util
    import stats
    import graphs

    path_to_json='result.json'
    author_from = 'Viola'
    author_to = 'Ale'
    chat = util.read_chat(path_to_json)
    chat = fields.add_fields(chat)
    chat_from = chat[chat['from'] == author_from]
    chat_to = chat[chat['from'] == author_to]

    # call methods from stats and graphs for the desired outputs