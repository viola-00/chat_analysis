# chat_analysis
Collection of methods to retrieve statistics from a given chat.  
More specifically:  
`fields.py` include methods that add fields to (Telegram) chats that will be useful to generate stats and graphs (the method `add_fields` add all the main ones),  
`util.py` includes utility methods that are called in `stats.py` and `graphs.py`,  
`stats.py` includes methods that generate statistics based on the chat given in input,  
`graphs.py` includes methods that generate plots based on the chat given in input,  
`cleaning.py` includes methods to clean Telegram, WhatsApp, and Facebook chats (but note that the latest version of the other files focuses on Telegram chats).  
## Examples
An example of the type of outputs generated by this project can be found [here](https://github.com/viola-00/chat_analysis/blob/main/output.pdf).
