import collections
import math
import pickle
import string
import sys

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Make a class of inverted index in which all the process is present to find inverted index
class InvertedIndex():
    # This is an constructor which will start fetch the document word and finally will make an inverted index
    def __init__(self):
        self.exclude = list(string.punctuation)
        self.exclude.append('।')

    def make_index(self, input_file, index_filename='index.txt'):
        # open file to write
        self.index_file = open(index_filename, 'w')
        # self.indexDict is an dictionary to store the posting list
        self.indexDict = {}
        with open(input_file, 'r') as corpus:
            sentences = corpus.readlines()
            self.N = len(sentences)
            for i in range(0, len(sentences)):
                text = sentences[i]
                # call the first operation(Remove punctuation from the document) and update the value of text variable
                text = self.remove_punctuation(text)
                # call the second operation(Remove stop word from the document) and store it as array of words
                words = self.remove_stop_word(text)
                # call the operation to apply stemming on word and store it with their document name in posting list
                self.make_PostingList(words, i)
        for i in self.indexDict.keys():
            self.index_file.write(i + "\t\t\t")
            self.index_file.write(str(self.indexDict.get(i)) + "\n")
        self.index_file.close()
        return self.indexDict

    # An operation to apply stemming and store word with their document id and frequency
    def make_PostingList(self, words, doc_id):
        # appy stemming on each word and store in lsit(word)
        words = [self.stem_word(word) for word in words]
        unique_words_frequency_dict = dict(collections.Counter(words))
        for unique_word in unique_words_frequency_dict.keys():
            # if word was present in another document then
            # append the current document at that place otherwise make another row and store it there

            if str(unique_word) in self.indexDict.keys():
                self.indexDict[str(unique_word)][doc_id] = unique_words_frequency_dict[unique_word]
            else:
                self.indexDict[str(unique_word)] = {}
                self.indexDict[str(unique_word)][doc_id] = unique_words_frequency_dict[unique_word]

# An operation to remove stop word
    def remove_stop_word(self, text):
        # print("removing stop word")
        # listOut all the stop word in stopWord list
        stopWord = open("stopWord.txt", "r").read().split("\n")
        text3 = []
        # print(stopWord)
        text = text.split()
        # make condition if text are stop word then it will remove
        for c in text:
            if c not in stopWord:
                text3.append(c)
        return text3

    # An operation to remove punctuation
    def remove_punctuation(self, text):
        text = "".join(c for c in text if c not in self.exclude)
        return text

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # An operation to find the root word by doing stemming
    # (Taken from Github)
    def stem_word(self, word):
        # suffixes have all the suffixes of hindi word which mostly comes at the end of word
        suffixes = {
            1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
            2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
            3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं",
                "ाएं", "ुओं", "ुएं", "ुआं"],
            4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं",
                "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
            5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
        }

        # make condition if word will end with these suffixes then that part will remove
        for k in 5, 4, 3, 2, 1:
            if len(word) > k:
                # print('h')
                for s in suffixes[k]:
                    if word.endswith(s):
                        # print(sf)
                        return (word[:-k])

        return word


    def search(self, query, indexDict, N):
        def getkey(item):
            return temp_calc[item]
        query = self.remove_punctuation(query)
        query = self.remove_stop_word(query)
        # query1 = list(set(query))
        temp_calc = {}
        for q_term in query:
            if q_term in indexDict:
                idf = math.log(N / len(indexDict[q_term].keys()))
                for doc_id in indexDict[q_term].keys():
                    term_frequency = indexDict[q_term][doc_id]
                    if doc_id in temp_calc:
                        temp_calc[doc_id] += term_frequency * idf
                    else:
                        temp_calc[doc_id] = term_frequency * idf
        sorted_result = [(doc, temp_calc[doc]) for doc in sorted(temp_calc, key=getkey, reverse=True)]
        return sorted_result


if __name__ == "__main__":
    # finally call all the operation by making the object of the class
    import os
    
    # obj = invertedIndex()
    # obj.make_index('hindi.corpus')
    # # finally dump the posting list in wordIndex.p in binary format
    # pickle.dump(obj.indexDict, open("hindi_corpus_index.pickle", "wb"))
    if not os.path.isfile("hindi_corpus_index.pickle") or len(sys.argv) == 2:
        obj = InvertedIndex()
        # finally dump the posting list in wordIndex.p in binary format
        hindi_corpus_file_name = sys.argv[1]
        pickle.dump(obj.make_index('corpus.hi'), open("hindi_corpus_index.pickle", "wb"))
    indexDict = {}
    indexDict = pickle.load(open(hindi_corpus_file_name, "rb"))
    print(len(indexDict))
    obj = InvertedIndex()
    query = input("enter Your Query\n")
    print(search(query, indexDict, N=30010.0))
