from preprocess import *
import pickle
import os

def lm_train(data_dir, language, fn_LM):
    """
	This function reads data from data_dir, computes unigram and bigram counts,
	and writes the result to fn_LM
	
	INPUTS:
	
    data_dir	: (string) The top-level directory continaing the data from which
					to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
	language	: (string) either 'e' (English) or 'f' (French)
	fn_LM		: (string) the location to save the language model once trained
    
    OUTPUT
	
	LM			: (dictionary) a specialized language model
	
	The file fn_LM must contain the data structured called "LM", which is a dictionary
	having two fields: 'uni' and 'bi', each of which holds sub-structures which 
	incorporate unigram or bigram counts
	
	e.g., LM['uni']['word'] = 5 		# The word 'word' appears 5 times
		  LM['bi']['word']['bird'] = 2 	# The bigram 'word bird' appears 2 times.
    """
	
	# TODO: Implement Function
    unigrams = {}
    bigrams = {}

    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            data_files = os.path.join(subdir, file)
            #check langunage
            if data_files.endswith(language):
                ofile = open(data_files)
                for line in ofile.readlines():
                    unigrampop(unigrams, line, language)
                    bigrampop(bigrams,line,language)
                ofile.close()
    language_model = {"uni": unigrams, "bi": bigrams}

    #Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("checkdog")
        
    return language_model


#DO MAGIC
    #populate bigram
def bigrampop(bigrams, line, language):
    #processed line
    proc_line = preprocess(line,language)
    prevword = ""
    for word in proc_line.split():
        if prevword in bigrams:
            if word in bigrams[prevword]:
                bigrams[prevword][word] += 1
            else:
                bigrams[prevword][word] = 1
        else:
            bigrams[prevword] = {}
            bigrams[prevword][word] = 1
        prevword = word


    #populate unigram
def unigrampop(unigrams, line, language):
    #processed line
    proc_line = preprocess(line,language)
    for word in proc_line.split():
        if word in unigrams:
            unigrams[word] += 1
        else:
            unigrams[word] = 1


