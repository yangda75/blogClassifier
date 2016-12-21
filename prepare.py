"""
description: process the text for further use.

containing functions:

rmTags(filePath)        : filePath.noTag
rmPunct(filePath)       : filePath.noPunct
wordsFreq(filePath)     : wordsVec, wordsCount
lenFreq(wordsVec)       : lenVec
hotWords(wordsVec,n)    : hotWordsVec

"""

import re
import os
import operator
import string


def rmTags(filePath):
    """
    # description: remove HTML tags in the given file, and returns a new
    file without the tags#
    input: the file(e.g. post.txt) with unwanted HTML tags
    output: "post.txt.tagFree" with no HTML tags
    """
    f = open(filePath, 'r')
    html = f.readlines()
    f.close()
    opPath = filePath + ".noTag"
    if os.path.isfile(opPath):
        os.remove(opPath)
    out = open(opPath, 'a')

    tags = re.compile(r'<[^>]+>', re.S)
    for line in html:
        line = tags.sub(' ', line)
        out.write(line)
    out.close()

    return opPath


def rmPunct(filePath):
    """
    similar to rmTags, this time remove punctuations
    """
    f = open(filePath, 'r')
    text = f.readlines()
    f.close()
    opPath = filePath + '.noPunct'
    if os.path.isfile(opPath):
        os.remove(opPath)
    opFile = open(opPath, 'a')

    for line in text:
        opLine = line.replace('-', ' ')
        opLine = ''.join(c for c in opLine if c not in string.punctuation)
        opFile.write(opLine)
    opFile.close()

    return opPath


# no word form detection, eg. 'go' and 'went' regarded as two words
def wordsFreq(filePath):
    """
    # description: calculate the vector of given file(e.g. post.txt) #
    input: path to a file
    output: 1. the vector of this text document, with each element in the from of
            "word":times appeared, in the form of a dict
            2. the numbers of words in this document, which is an integer
    """
    f = open(filePath)
    text = f.readlines()
    f.close()

    tokens = []
    freqVocab = {}

    # get words
    for line in text:
        newLine = line
        newLine = newLine.replace('\t', '')
        newLine = newLine.replace('\n', ' ')
        newLine = newLine.lower()
        words = [i for i in newLine.split(' ') if i != '']
        tokens.extend(words)
    wordsCount = len(tokens)
    vocab = list(set(tokens))
    freqVocab = dict(zip(vocab, [0] * len(vocab)))
    # get frequency of each word
    for t in tokens:
        freqVocab[t] += 1
    wordsVec = sorted(freqVocab.items(), key=operator.itemgetter(1), reverse=1)

    return wordsVec, wordsCount


def lenFreq(wordsVec):
    lenVec = [0] * 20
    for i in range(len(wordsVec)):
        lenVec[len(i[0])] += i[1]
    return lenVec


def hotWords(wordsVec, n):
    return [t[0] for t in wordsVec[:n]]


def prepare(filePath):
    f1 = rmTags(filePath)
    f = rmPunct(f1)
    wordsVec, wordsCount = wordsFreq(f)
    hotWords = hotWords(wordsVec)

    return wordsVec, wordsCount, hotWords
