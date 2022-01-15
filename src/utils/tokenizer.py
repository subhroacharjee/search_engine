import nltk, re
from stop_words import get_stop_words
from nltk.corpus import stopwords

def tokenizer(string:str):
    # we are creating list of stop words which are to be excluded from the sentence
    stop_words = list(get_stop_words('en'))
    try:
        nltk_words = list(stopwords.words('english'))
    except LookupError as le:
        nltk.download("stopwords")
        nltk_words = list(stopwords.words('english'))
    stop_words.extend(nltk_words)

    output = set()
    try:
        tokens = nltk.word_tokenize(string.lower())
    except LookupError as le:
        nltk.download('punkt')
        tokens = nltk.word_tokenize(string.lower())
    for words in tokens:
        if not words in stop_words:
            output.add(words)
        
        
    return output