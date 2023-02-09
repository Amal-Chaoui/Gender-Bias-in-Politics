""" module for preprocessing questions text """
import re
from bs4 import BeautifulSoup

def remove_tags(corpus):
    """ Remove html tags"""
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


def remove_q_heading(text_str):
    """ Detects positions of 'mr' and /or 'mme' in text and returns stripped text """
    text_lst = text_str.split()
    list_mr_mme=["mr", "mme", "demr", "mmme", "demme", "mmr", "interrogemme"]
    if text_lst[0][0]=='"':
        text_lst[0] = text_lst[0][1:]
    i = 0
    while i<len(list_mr_mme):
        try:
            idx1 = text_lst.index(list_mr_mme[i])
            if idx1 > 20: i+=1
            else: break
        except:
            i+=1

    i = 0
    while i<len(list_mr_mme):
        try:
            idx2 = (text_lst[:idx1] + ['xx'] + text_lst[idx1+1:] ).index(list_mr_mme[i])
            if idx2 > 20: i+=1
            else: break
        except:
            i+=1

    (idx1, idx2) = (idx1, idx2) if idx1 < idx2 else (idx2, idx1)
    return ' '.join(text_lst[:idx1] + text_lst[idx2+3:])

   
def remove_anomalies(corpus, rmv_heading=True):
    """ replace apostrophy inconsistencies \ ' with real apostrophies. ' 
        remove \xa0 signs.
        remove urls.
    """
    cln_corpus = []
    for i, sentence in enumerate(corpus):
        sentence = sentence.replace("M.", "Mr")
        sentence = sentence.replace(u'\xa0', u' ')
        sentence = sentence.replace("\'", "' ")
        sentence = re.sub(r'http\S+', '', sentence)
        sentence = sentence.lower()
        sentence = sentence.replace("m.", "mr")

        # put space between words and punctuation 
        sentence = re.sub('([.,!?()])', r' \1 ', sentence)
        sentence = re.sub('\s{2,}', ' ', sentence)
        cln_corpus.append(remove_q_heading(sentence))
    return cln_corpus