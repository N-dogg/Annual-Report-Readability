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

def unigram_prob(tokens):
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

def pair_prob(pair, occurence, pdf, no_pdf):
    #returns the co-occurence probability

    return occurence[pdf][pair]/no_pdf

def lexical_tightness(uni_prob, bi_prob, pdf):
    #returns the lexical tightness (mean PNPMI) for a text
    holding = []
    for i in range(len(bi_prob[pdf])):
        holding.append((math.log2(bi_prob[i]/(uni_prob[i][0]*uni_prob[i][1]))) / (-math.log2(bi_prob[i])))

    return sum(holding)/len(holding)

if __name__ == '__main__':

    pdf_name = 'example{0}.pdf'
    no_pdf = 3

    uni_prob = unigram_prob(unigrams)
    bi_ouput = formatting(pairs)
