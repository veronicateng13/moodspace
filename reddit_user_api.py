

class RedditUserAPI:
    # provide values for attribute name @ runtime
    def __init__(self, username):
        self.username = username
    
    # methods
    # get data from reddit api, output: df
    def get_clean_data(self):
        data = requests.get(f'https://api.pushshift.io/reddit/search/submission/?author={self.username}')
        # transform json data into a dataframe
        user_df = pd.json_normalize(data.json()['data'])
        
        # get relevant cols
        include = ['title', 'selftext', 'created_utc', 'subreddit']
        user_df = user_df[include]
        user_df = user_df.rename(columns={"selftext": "original_text", "created_utc": "pub_date"})

        # change unix time stamp to date
        local_timezone = tzlocal.get_localzone()
        user_df['pub_date'] = user_df['pub_date'].apply(lambda unix_timestamp: datetime.fromtimestamp(unix_timestamp, local_timezone).strftime("%Y-%m"))

        # combine title and original text
        na_title = ((user_df['title'].isna()) | (user_df['title'] == '[removed]') | (user_df['title'] == '[deleted]'))
        na_text = ((user_df['original_text'].isna()) | (user_df['original_text'] == '[removed]') | (user_df['original_text'] == '[deleted]'))
        user_df.loc[ na_text & ~na_title, 'full_text'] = user_df['title']
        user_df.loc[ ~na_text & na_title, 'full_text'] = user_df['original_text']
        user_df.loc[ ~na_text & ~na_title, 'full_text'] = user_df['title'] + " " + user_df['original_text']

        user_df = user_df.drop(['original_text', 'title'], axis = 1)
        
        # create a custom cleaning pipeline
        custom_pipeline = [  preprocessing.remove_brackets
                            , preprocessing.remove_urls
                            , preprocessing.remove_digits
                            , preprocessing.remove_diacritics
                            , preprocessing.remove_punctuation
                            , preprocessing.remove_whitespace
                            , preprocessing.stem
                            , preprocessing.lowercase
        ]

        # pass the custom_pipeline to the pipeline argument
        user_df['clean_text'] = hero.clean(user_df['full_text'], pipeline = custom_pipeline)

        # add a list of stopwords to the stopwords
        default_stopwords = stopwords.DEFAULT
        impt_words = ['not', 'no']
        custom_stopwords = [word for word in default_stopwords if word not in impt_words]

        #pass the custom_pipeline to the pipeline argument
        user_df['clean_text'] = hero.remove_stopwords(user_df['clean_text'], custom_stopwords)
        user_df['clean_text'] = hero.remove_whitespace(user_df['clean_text'])
        
        return user_df
    
    def get_prediction(self, clean_data):
         # prediction
        pred = lr_model.predict(clean_data['clean_text'])
        clean_data['class'] = pred

        # add category
        clean_data.loc[clean_data['class'] == 0,'category'] = 'Not Negative'
        clean_data.loc[clean_data['class'] == 1,'category'] = 'Negative'
        
        # drop original
        clean_data = clean_data.drop(['full_text'], axis = 1)

        return clean_data
    
    def get_df_by_month_and_cat(self, df):
        # with labels
        class_df = df.copy()
        class_df['pub_date'] = pd.to_datetime(class_df['pub_date'])
        class_df = class_df.groupby(by=[class_df['pub_date'].dt.to_period('M'), 'category']).size()
        class_df = class_df.to_frame().reset_index()
        class_df.columns = ['month', 'category', 'number_of_threads']
        class_df['month'] = class_df['month'].astype(dtype=str)
        return class_df
    
    def get_df_by_month(self, df):
        overall_df = df.copy()
        overall_df['pub_date'] = pd.to_datetime(overall_df['pub_date'])

        overall_df = overall_df.groupby(by=[overall_df['pub_date'].dt.to_period('M'),]).size()
        overall_df = overall_df.to_frame().reset_index()
        overall_df.columns = ['month', 'number_of_threads']
        overall_df['month'] = overall_df['month'].astype(dtype=str)
        return overall_df