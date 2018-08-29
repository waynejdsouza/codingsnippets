import sys
import argparse
import os
import json
import re
import spacy

indir = '/u/cs401/A1/data/';
nlp = spacy.load('en', disable = ['parser', 'ner'])
f = open('/u/cs401/Wordlists/StopWords','r')
stop_words = f.read().splitlines()
stop_words = list(stop_words)

def preproc1( comment , steps=range(1,10)):
    ''' This function pre-processes a single comment

    Parameters:                                                                      
        comment : string, the body of a comment
        steps   : list of ints, each entry in this list corresponds to a preprocessing step  

    Returns:
        modComm : string, the modified comment 
    '''

    modComm = comment
    if 1 in steps:
        modComm = modComm.replace("\n", "")

    if 2 in steps:
        modComm = re.sub('&amp;', '&', modComm)

        modComm = re.sub('&quot;', '"', modComm)

        modComm = re.sub('&lt;', '>', modComm)

        modComm = re.sub('&gt;', '<', modComm)

    if 3 in steps:
        #https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
        modComm = re.sub('((https?:\\/\\/)|(www.))[A-z./?=]+', '', modComm)

    if 4 in steps:
        #comma
        modComm = re.sub(',', ' , ', modComm)

        #colon
        modComm = re.sub(': ', ' : ', modComm)

        #semicolon
        modComm = re.sub('; ', ' ; ', modComm)

        #quotes
        modComm = re.sub('\'', ' \' ', modComm)
        modComm = re.sub('\"', ' \" ', modComm)


        #special cases for periods, exclamation, and question marks
        modComm = re.sub('(\\. )|(\\.$)', ' . ', modComm)
        modComm = re.sub('(\\? )|(\\?$)', ' ? ', modComm)
        modComm = re.sub('(\\! )|(\\!$)', ' ! ', modComm)

        #deal with the trples.

        re.sub('\\!\\!\\!+', ' !!! ', modComm)
        re.sub('\\?\\?\\?+', ' ??? ', modComm)
        re.sub('\\.\\.\\.+', ' ... ', modComm)

        #TODO Abreviations
    if 5 in steps:
        re.sub("n't", " n't", modComm)
        re.sub(" 's", " 's", modComm)
        re.sub(" s'", " s'", modComm)

    if 6 in steps:

        utt = nlp(modComm)
        modComm = ' '.join([((token.text).lower() +"/"+token.tag_) for token in utt])

    if 7 in steps:
        correct_words = []
        for check_word in modComm.split(' '):
            #check if word is in stop words, gotta check without the spacy tag
            if check_word.split('/')[0] not in stop_words:
                correct_words.append(check_word)
        modComm = " ".join(correct_words)

    if 8 in steps:
        '''
        text = []
        tag = []
        modComm2 = modComm.split(" ")
        modComm = [x for x in modComm2 if ((len(x)!= 0) or (x != ['/']))]
        for frag in modComm:
            if len(frag) != 0:
                text.append(frag.split("/")[0])
                tag.append(frag.split("/")[1])
        print(tag,text)
        tag_doc = spacy.tokens.Doc(nlp.vocab,words= text)
        utt_lemma = nlp.tagger(tag_doc)

        for token in utt_lemma:
            lemmas_needed = []
            lemma = token.lemma_[0]
            if lemma != "-":
                lemmas_needed.append(token.lemma_)
            else:
                lemmas_needed.append(token.text)
        tag_len = len(tag)
        for i in range(tag_len):
            modComm += lemmas_needed[i] + "/" + tag[i]
            print(modComm)

        #TODO
        '''
    if 9 in steps:
        splitmod = modComm.split()
        for frag in splitmod:
            EOS = ['./.', '?/.', '!/.']
            if frag in EOS:
                splitmod[splitmod.index(frag)] = frag + ' \\n'

        modComm = ' '.join(splitmod)


    #if 10 in steps DONE IN STEP 6:


    return modComm


def main( args ):

    allOutput = []
    for subdir, dirs, files in os.walk(indir):
        for file in files:
            fullFile = os.path.join(subdir, file)
            print("Processing " + fullFile)

            data = json.load(open(fullFile))

            # TODO: select appropriate args.max lines
            for line in data:
                # TODO: read those lines with something like `j = json.loads(line)`
                # TODO: choose to retain fields from those lines that are relevant to you
                j = json.loads(line)

                # TODO: add a field to each selected line called 'cat' with the value of 'file' (e.g., 'Alt', 'Right', ...)
                output_dic = {'cat':file, 'id': j['id']}

                # TODO: process the body field (j['body']) with preproc1(...) using default for `steps` argument
                # TODO: replace the 'body' field with the processed text

                output_dic['body'] = preproc1(j['body'])
                temp = json.dumps(output_dic)
                # TODO: append the result to 'allOutput'
                allOutput.append(temp)

    fout = open(args.output, 'w')
    fout.write(json.dumps(allOutput))
    fout.close()

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument('ID', metavar='N', type=int, nargs=1,
                        help='your student ID')
    parser.add_argument("-o", "--output", help="Directs the output to a filename of your choice", required=True)
    parser.add_argument("--max", help="The maximum number of comments to read from each file", default=10000)
    args = parser.parse_args()

    if (args.max > 200272):
        print ("Error: If you want to read more than 200,272 comments per file, you have to read them all.")
        sys.exit(1)

    main(args)


