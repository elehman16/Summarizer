# -*- coding: utf-8 -*-
"""
Represents a model for summarizing text.
"""
from FindSentence import findSentence
from nltk.corpus import wordnet as wn
from ImageToText import ImageText
import operator
import inflect
p = inflect.engine()

filterWords = {'i', 'he', 'her', 'his', 'him', 'she', 'as', 'are', 'in',
               'like', 'much', 'can', 'so', 'if', 'its', 'may', 'use', 'come', 
               'or', 'a', 'at', 'it', 'be', 'no', 'has', 'an', 'should', 
               'would', 'could'}

class Model:
    
    """
    Model for summarizing text. 
    
    @param importance represents what percent of sentences to return as a summary.    
    """
    def __init__(self):
        self.importance = .25
    
    """
    Takes in the text to be summarized, and returns the summarized text and a 
    list of key words.
    
    @param text represents a string of text to be summarized 
    @return a paragraph of summarized text
    @return a list of key vocab words
    """
    def summarize(self, text):
        sentences = self.__split_sentences__(text)
        words, mapping_occurances = self.__split_words__(sentences[:])
        map_ranked_sentences = self.__rank_sentences__(sentences[:], words[:], mapping_occurances.copy())
        ordered_importances = self.__sort__(map_ranked_sentences.copy())
        summarized = self.__select_top_n__(ordered_importances[:])
        vocab_words = self.__find_key_words__(mapping_occurances.copy())
        return summarized, vocab_words
    
    """
    Added in 1/22/18. Functionality existed before, but this method did not.
    
    Takes in a picture and calls an OCR to translate it into text.
    
    @param pic represents the picture to be converted.
    @return a text version of the picture.
    """
    def picture_to_text(self, pic):
        return ImageText(pic).text()
        
    """
    Splits the text into sentences. Removes periods from sentences.
    
    @param text the text to be split into sentences
    @return a list of sentences (strings)
    """
    def __split_sentences__(self, text):
        sentences = []
        if (text.find('.') == -1):
            sentences.append(text)
            return sentences
    
        while(len(text) > 0):
            space = findSentence(text)
            if(text[0] == " " or text[0] == '.'):
                text = text[1:]
            elif(space == -1):
                sentences.append(text[:(space)])
                return sentences
            else:
                sentences.append(text[:(space)])
                text = text[(space + 1):]
                
        return sentences
        
    """
    Takes the list of sentences and parses each into a list of words. Removes commas.
    
    @param sentences represents a list of strings to be split into a list of list of words.
    @return return a list of list of words.
    @return a hashmap detailing words to their counts.
    """
    def __split_words__(self, sentences):
        all_words = []
        mapping = {}
        for s in sentences:
            all_words.append(self.__split_single_sentence__(s, mapping))
                    
        return all_words, mapping
        
    """
    Splits a single sentence into a list of words. Removes commas.
    
    @param sentence represents the sentence to parse
    @param mapping represents the mapping to add word counts to
    """
    def __split_single_sentence__(self, sentence, mapping):
        split_sentence = sentence.split(" ")
        low = []
        for word in split_sentence:
            temp = word.lower()
            if "," in temp:
                temp.replace(",", "")
                
            
            low.append(temp)
            resp = wn.synsets(word) 
            
            if (len(resp) == 0 or resp[0].pos() != 'n' or temp in filterWords):
                continue
            elif (temp in mapping):
                mapping[temp] = mapping[temp] + 1
            elif (self.__genPlural__(temp) in mapping):
                mapping[self.__genPlural__(temp)] = mapping[self.__genPlural__(temp)] + 1
            else: 
                mapping[temp] = 1
           
            
        return low
            
            
    """
    Returns the plural, or unplural version of this word.

    @param s is the word to work with.
    @return the plural/not-plural word    
    """
    def __genPlural__(self, s):
        # is not plural
        if(type(p.singular_noun(s)) == str): 
            return p.singular_noun(s)
        elif(type(p.plural(s)) == str):
            return p.plural(s)
        else:
            return ""            
        
    """
    Ranks the sentences in accordance to word counts.

    @param sentences represents the sentences to be ranked
    @param all_words represents those sentences broken down
    @param mapping is a mapping of words to number of occurances
    @return a mapping of sentences to rank
    """
    def __rank_sentences__(self, sentences, all_words, mapping):
        sentence_rankings = {}
        for i in range(len(sentences)):
            full_sentence = sentences[i] + ". "
            sentence_rankings[full_sentence] = self.__rank_single_sentence__(all_words[i], mapping)
        return sentence_rankings
        
    
    """
    Ranks a single sentence.
    
    @param words represents a sentence broken down
    @param mapping represents the mapping of words to number of occurances
    @return a rank for that sentence
    
    """
    def __rank_single_sentence__(self, words, mapping):
        rank = 0
        for w in words:
            if w in mapping:
                rank += mapping[w]
        return rank
        
    
    """
    Sorts the given hashmap, and returns the list of sentences.
    
    @param mapping represents a mapping of sentence to importance (number).
    @return a sorted list of sentences in descending order of importance.
    """
    def __sort__(self, mapping):
        sorted_x = sorted(mapping.items(), key=operator.itemgetter(1), reverse = True)
        return sorted_x
        
    """
    Takes a sub-set of the top rankings (either sentences or words) and 
    the most important ones.
    
    @param rankings represents the elements to take the sub-set of.
    @return the most important sentences (in a list format)
    """
    def __select_top_n__(self, rankings):
        top_n = []
        num_rank = min(len(rankings), int(len(rankings) * self.importance + 1))
        for i in range(num_rank):
            top_n.append(rankings[i][0])
            
        return top_n
    
    """
    Finds the key words in the passage and returns the top n percent of 
    vocab words based on importance.
    
    @param mapping represents the number of occurances for each word.
    """
    def __find_key_words__(self, mapping):
        sorted_list = self.__sort__(mapping)
        sorted_list = self.__select_top_n__(sorted_list)
        ans = []
        i = 0
        for v in sorted_list:
            i += 1
            if (i != len(sorted_list)):
                ans.append(v + ", ")
            else:
                ans.append(v)
        return ans
        