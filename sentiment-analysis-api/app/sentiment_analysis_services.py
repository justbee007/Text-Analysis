from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Function used to validate the input JSON
def json_validation(json_data):
    '''
    This function checks if the input JSON is valid
    :param json_data: JSON input
    Function returns True if the input JSON is valid
    '''
    if type(json_data) == str:
        return False
    if not json_data:
        return False
    if "text" not in json_data:
        return False
    if not type(json_data["text"]) is str:
        return False
    return True


# Function used to analyze the sentiment of the input text
def sentiment_analysis(text):
    '''
    This function checks the sentiment of the input text
    :param text: input text
    Function returns the sentiment of the input text
    '''
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound_score = scores["compound"]
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Function used to check the input type
def check_input_type(input_data):
    '''
    This function checks the type of the input data
    :param input_data: input data
    Function returns True if the input data is a string'''
    if not type(input_data) is str:
        return False
    return True
