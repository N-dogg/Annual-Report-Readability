import PyPDF2
from itertools import combinations
import math
import matplotlib.pyplot as plt

import nltk
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

stop_words = set(stopwords.words('english'))
nltk.download('wordnet')
word_l = WordNetLemmatizer()

unigrams = []
pairs = {}

def pdf_extract(no_pdf, path):
    #returns a list of unigrams for the corpus and a dict of combinations for each text
    for y in range(no_pdf):
        path = pdf_name.format(y)
        pdfFileObj = open(path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        tokens = []
        for i in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            raw = pageObj.extractText().split(' ')
            for i in raw:
                if i.isalpha():
                    i_lem = word_l.lemmatize(i)
                    if i_lem not in stop_words:
                        i_lower = i_lem.lower()
                        tokens.append(i_lower)
                        unigrams.append(i_lower)
        combo = list(combinations(set(unigrams), 2))
        pairs[y] = combo

    return pairs, unigrams

def unigram_probability(tokens):
    #returns the unigram probability of each word in the corpus
    result = {}
    denom = len(tokens)
    counter_uni = Counter(tokens)
    for i in counter_uni:
        result[i] = counter_uni[i]/denom

    return result

def pair_occurence(pairs):
    #return the occurence amount of each combination across all texts
    holding = []
    for i in pairs:
        for y in pairs[i]:
            holding.append(y)
    result = Counter(holding)

    return result

def pair_probability(pairs, occurence, no_pdf):
    #return a dict of all a text pair combinations with their probability across the corpus
    output = {}
    for i in pairs:
        holding = {}
        for y in pairs[i]:
            holding[y] = occurence[y]/no_pdf
        output[i] = holding

    return output

def lexical_tightness(uni_prob, bi_prob, pairs, pdf):
    #returns the lexical tightness (mean PNPMI) for a text
    holding = []
    for i in range(len(pairs[pdf])):
        try:
            holding.append((math.log2(bi_prob[pdf][pairs[pdf][i]]/(uni_prob[pairs[pdf][i][0]]*uni_prob[pairs[pdf][i][1]]))) /(-math.log2(bi_prob[pdf][pairs[pdf][i]])))
        except:
            holding.append(0)
    return sum(holding)/len(holding)
    

if __name__ == '__main__':

    pdf_name = 'example{0}.pdf'
    no_pdf = 3

    pairs, unigram = pdf_extract(no_pdf, pdf_name)
    uni_prob = unigram_probability(unigrams)

    pair_occ = pair_occurence(pairs)
    pair_prob = pair_probability(pairs, pair_occ, no_pdf)

    result = []
    for i in range(no_pdf):
        result.append(lexical_tightness(uni_prob, pair_prob, pairs, i))
