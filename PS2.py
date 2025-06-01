#********************************#
# Name: Nabeel Mahmood           #
# Username: <if applicable>      #
# Problem Set: PS2               #
# Due Date: October 1st, 2024    #
#********************************#

import re
import array
import random
import math

with open("/Users/nabeelmahmood/NLP/Shakespeare.txt", "r") as i:
    doc = i.read() 
 
doc = doc.lower()

doc = re.sub(r'[0-9]', '', doc)

doc = re.sub(r'[^a-z\s!?]', '', doc)

doc_split = re.findall(r'[a-zA-Z!?]+', doc)  


#doc = "this is a test test test test hello nerd this is a test test"


# unigram frequencies
unigram_lm = dict()

for token in doc.split():
#    print(token)
    if token in unigram_lm:
        unigram_lm[token] += 1
    else:
        unigram_lm[token] = 1
        
    


# bigram frequencies
bigrams = dict() 

tokens = doc.split()
for i in range( 0, len(tokens) -1,  1 ):
    bigram = tokens[i] + " " + tokens[i+1]

    if bigram in bigrams:
        bigrams[bigram] += 1
    else:
        bigrams[bigram] = 1

#print(f"Bigrams:  {bigrams}")


# trigram frequencies
trigrams = dict() 

tokens = doc.split()
for i in range( 0, len(tokens) -2):
    trigram = tokens[i] + " " + tokens[i+1] + " " + tokens[i+2]

    if trigram in trigrams:
        trigrams[trigram] += 1
    else:
        trigrams[trigram] = 1




# laplace smoothing
def bigram_prob_smoothing(bigrams, first_word, second_word):
    V = len(unigram_lm) 
    word_size = 0  
    
    bigram_count = bigrams[bigram]
    
    for key in bigrams:
        if key.split()[0] == first_word:
            word_size += bigrams[key]  
        
            
    return (bigram_count+ 1) / (word_size + V)
    




# trigram prob
def trigram_prob(word1, word2):

    best_next_word = None
    highest_prob = 0.0
    V = len(bigrams)

    for trigram in trigrams:
        first_word = trigram.split()[0]   
        
        second_word = trigram.split()[1]   
        third_word = trigram.split()[2]


        if first_word == word1 and second_word == word2:
            trigram_count = trigrams[trigram]  

            bigram_key = word1 + " " + word2 

    
            bigram_count = bigrams.get(bigram_key)

            
            prob = (trigram_count + 1) / (bigram_count + V)
          
            if prob > highest_prob:
                highest_prob = prob
                best_next_word = third_word
                
                if highest_prob == 0:
                    return bigram_prob_smoothing(bigrams, first_word, second_word)
                
        
    if best_next_word != None:
        return best_next_word
   


 
#print( f"Bigram with the highest probability: '{highestProbkey}' with probability: {highestProb}")



#bigram log
def calc_bigram_log(w1, w2):
    total_log = 0
    prob = bigram_prob_smoothing(bigrams, w1, w2)  
    
 
    if prob > 0:
        total_log += math.log(prob) 
    else:
        total_log += math.log(1e-10)  

    return total_log
    
#trigram log
def calc_trigram_log(w1, w2):
    total_log = 0
 
    
    prob = trigram_prob(w1, w2)  

    if isinstance(prob, (int, float)):
        total_log += math.log(prob)
    else:
        total_log += math.log(1e-10)  

    return total_log




def predict_next_ten_words_trigrams(w1, w2, numwords=10):
    predictWords = []
    string = ""
    
    for i in range(numwords):
        next_word = trigram_prob(w1, w2)
        if next_word:
            predictWords.append(next_word)
            w1, w2 = w2, next_word 
        else:
            next_word = predict_next_word_bigram(w2)
            predictWords.append(next_word)
            w1, w2 = w2, next_word
    
   
    for triword in predictWords:
        string += triword + " "  
    

    return string.strip()  




def predict_next_word_bigram(w2, numwords = 10):
    predictWords = []  
    string = ""

    for i in range(numwords):
        next_word = None  
        highest_prob = 0  
        
        for bigram in bigrams:
            first_word = bigram.split()[0]  
            if first_word == w2:
                second_word = bigram.split()[1]
                
              
                prob = bigram_prob_smoothing(bigrams, first_word, second_word)
                #print(f"Checking bigram: {bigram}, Probability: {prob}")  
                
                if prob > highest_prob:
                    highest_prob = prob
                    next_word = second_word
                    break
        

        if next_word:
            predictWords.append(next_word)
            w2 = next_word 
            
        else: random.choice(list(unigram_lm))
              

    for biword in predictWords:
        string += biword + " "  
    

    return string.strip()  

