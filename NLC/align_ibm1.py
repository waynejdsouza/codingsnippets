from lm_train import *
from log_prob import *
from preprocess import *
from math import log
import os
import glob

def align_ibm1(train_dir, num_sentences, max_iter, fn_AM):
    """
	Implements the training of IBM-1 word alignment algoirthm.
	We assume that we are implemented P(foreign|english)

	INPUTS:
	train_dir : 	(string) The top-level directory name containing data
					e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
	num_sentences : (int) the maximum number of training sentences to consider
	max_iter : 		(int) the maximum number of iterations of the EM algorithm
	fn_AM : 		(string) the location to save the alignment model

	OUTPUT:
	AM :			(dictionary) alignment model structure

	The dictionary AM is a dictionary of dictionaries where AM['english_word']['foreign_word']
	is the computed expectation that the foreign_word is produced by english_word.

			LM['house']['maison'] = 0.5
	"""
    AM = {}

    # Read training data
    train_data = read_hansard(train_dir, num_sentences)
    eng = train_data[0]
    fre = train_data[1]
    AM = initialize(eng,fre)
    # Initialize AM uniformly
    for i in range(max_iter):






    # Iterate between E and M steps



    return AM


# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences):
    """
	Read up to num_sentences from train_dir.

	INPUTS:
	train_dir : 	(string) The top-level directory name containing data
					e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
	num_sentences : (int) the maximum number of training sentences to consider


	Make sure to preprocess!
	Remember that the i^th line in fubar.e corresponds to the i^th line in fubar.f.

	Make sure to read the files in an aligned manner.
	"""
    # TODO
    train_data = {"eng": {}, "fre": {}}
    AM = {}
    counter = 0
    #from lm_train
    '''for subdir, dirs, files in os.walk(train_dir):
        for file in files:
            data_files = os.path.join(train_dir, file)
            # check langunage
                '''
    for file in glob.glob(train_dir + '.e'):
        if counter < num_sentences:
            eng_file = open(file)
            eng_line = eng_file.readline()
            fre_file = open(file[:-2] + '.f')
            fre_line = fre_file.readline()
            while eng_line != "" and counter < num_sentences:
                eng_line = preprocess(eng_line, 'e')
                fre_line = preprocess(fre_line, 'f')
                train_data['eng'][counter] = eng_line
                train_data['fre'][counter] = fre_line

                eng_line = eng_file.readline()
                fre_line = fre_file.readline()
                counter += 1

            eng_file.close()
            fre_file.close()

    return train_data

def initialize(eng, fre):
    """
	Initialize alignment model uniformly.
	Only set non-zero probabilities where word pairs appear in corresponding sentences.
	"""

    # TODO

    AM = {}
    AM["SENTSTART"] = {}
    AM["SENTEND"] = {}
    AM["SENTSTART"]["SENTSTART"] = 1
    AM["SENTEND"]["SENTEND"] = 1

    length = len(eng) + 1
    for i in range(length):
        eng_sent = eng[i].split()
        fre_sent = fre[i].split()
        #store
        AM = store_am(AM, eng_sent, fre_sent)
        #align
        AM = align_am(AM, eng_sent, fre_sent)

    return AM


def store_am(AM, eng_sent, fre_sent):
    length = len(eng_sent) - 1
    for i in range(length):
        eng_word = eng_sent[i]
            #if dict exists
        if eng_word in AM:
            AM = store_helper(AM, eng_word, fre_sent)
        else:
            #create the dict for the word
            AM[eng_word] = {}
            AM = store_helper(AM, eng_word, fre_sent)
    return AM


def align_am(AM, eng_sent, fre_sent):
    length = len(eng_sent) - 1
    for i in range(length):
        fre_dict = AM[eng_sent[i]]
        for word in fre_dict:
            total = float(len(fre_dict))
            if total != 0:
                # AM[‘e’][‘f’] = 1/∥VF ∥, where ∥VF ∥ is the size of the French vocabulary.
                fre_dict[word] = 1/total
            else:
                fre_dict[word] = 0
    return AM

#sync
def store_helper(AM,eng_word, fre_sent):
    for j in range(len(fre_sent) - 1):
        fre_word = fre_sent[j]
        AM[eng_word][fre_word] = 1
    return AM


def em_step(t, eng, fre):
    """
	One step in the EM algorithm.
	Follows the pseudo-code given in the tutorial slides.
	"""
    # TODO


