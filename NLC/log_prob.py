from preprocess import *
from lm_train import *
from math import log2

def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
    """
	Compute the LOG probability of a sentence, given a language model and whether or not to
	apply add-delta smoothing
	
	INPUTS:
	sentence :	(string) The PROCESSED sentence whose probability we wish to compute
	LM :		(dictionary) The LM structure (not the filename)
	smoothing : (boolean) True for add-delta smoothing, False for no smoothing
	delta : 	(float) smoothing parameter where 0<delta<=1
	vocabSize :	(int) the number of words in the vocabulary
	
	OUTPUT:
	log_prob :	(float) log probability of sentence
	"""
	
	#TODO: Implement by student.

    word_list = sentence.split()
    init_prob = 1
    token = word_list[0]
    for next_token in word_list[1:]:
        if LM['uni'][token] == 0:
            return 0
        else:
            #get numerator and denominator
            oneword_count = LM['uni'][token]
            twoword_count = LM['bi'][token][next_token]
            token = next_token

        # maaaaaaaaath
        # if smoothing ==  true then this function returns a δ-smoothed estimate of the sentence. In the case of smoothing, the arguments delta and
        # vocabSize must also be specified (where 0 < δ ≤ 1).
        # if smoothing == False , # returns the maximum-likelihood estimate of the sentence
        log_prob = mle(twoword_count, init_prob, oneword_count, delta, vocabSize, smoothing)


    return log_prob


def mle(num, init_prob, den, delta, vocabSize, bool):
    if bool:
        return log2((init_prob * ((num + delta)) / (den + (delta * vocabSize))))
    else:
        return log2((init_prob * (num / den)))
