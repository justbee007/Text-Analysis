# Function used to calculate the word count of the input text
def calculate_word_count(inputText):
    
    if not inputText.strip():
        return 0
    word_count = len(inputText.split())
    return word_count

# Function used to validate the input JSON
def json_validation(json_data):
   
    if not json_data:
        return False
    if 'text' not in json_data:
        return False
    if not type(json_data['text']) is str:        
        return False
    return True