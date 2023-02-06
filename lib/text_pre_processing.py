""" module for preprocessing questions text """
import re
from bs4 import BeautifulSoup




# Function to remove tags
def remove_tags(corpus):
    cln_corpus = []
    for sentence in corpus:
        # parse html content
        soup = BeautifulSoup(sentence, "html.parser")

        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()
        cln_corpus.append(' '.join(soup.stripped_strings)) # return data by retrieving the tag content
    # return clean corpus
    return cln_corpus

     
            
def remove_anomalies(corpus):
    """ replace apostrophy inconsistencies \ ' with real apostrophies. ' 
        remove \xa0 signs.
        remove urls.
    """
    cln_corpus = []
    for sentence in corpus:
        sentence = sentence.replace("M.", "Mr")
        sentence = sentence.replace(u'\xa0', u' ')
        sentence = sentence.replace("\'", "' ")
        sentence = re.sub(r'http\S+', '', sentence)
        sentence = sentence.lower()
        sentence = sentence.replace("m.", "mr")

        # put space between words and punctuation 
        sentence = re.sub('([.,!?()])', r' \1 ', sentence)
        sentence = re.sub('\s{2,}', ' ', sentence)
        cln_corpus.append(sentence)
    return cln_corpus