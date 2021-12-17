library(syuzhet)
r_algo <- myfunction(my_df,friend_df, lang='english'){
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()

    from rpy2.robjects.packages import importr

    base = importr('base')
    # call an R function on a Pandas DataFrame
    base.summary(my_df,friend_df)

    my_values = get_nrc_sentiment(my_df[,1],lang=lang)
    friend_values = get_nrc_sentiment(friend_df[,1],lang=lang)

    return(my_values,friend_values)
}