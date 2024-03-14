from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Function used to validate the input JSON
def json_validation(json_data):
    if type(json_data) == str:
        return False
    if not json_data:
        return False
    if 'text' not in json_data:
        return False
    if not type(json_data['text']) is str:        
        return False
    return True

# Function used to analyze the sentiment of the input text
def sentiment_analysis(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    if(compound_score >= 0.05):
        return "positive"
    elif(compound_score <= -0.05):
        return "negative"
    else:
        return "neutral"
    
def check_input_type(input_data):
    if not type(input_data) is str:
        return False
    return True