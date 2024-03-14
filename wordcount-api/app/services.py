import re
# Function used to calculate the word count of the input text
def calculate_word_count(input_text):
    '''
    Function to calculate the word count of the input text
    :param input_text: The input text
    :return: The word count of the input text
    '''

    if not input_text.strip():
        return 0
    cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', input_text)
    word_count = len(cleaned_sentence.split())
    return word_count

# Function used to validate the input JSON
def json_validation(json_data):
    '''
    Function to validate the input JSON
    :param json_data: The input JSON
    :return: True if the input JSON is valid, False otherwise'''
    if not json_data:
        return False
    if 'text' not in json_data:
        return False
    if not type(json_data['text']) is str:        
        return False
    return True
