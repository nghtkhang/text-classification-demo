import pickle  
import bai3_config
import os
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag, #VB, VBZ
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

data=input("Nhập vào text: ")

#load model
modeldir="models"
currentpath=str(os.path.abspath(os.getcwd()))
modelpath=currentpath+"\\"+modeldir
if not (os.path.exists(modelpath)):
    os.mkdir(modelpath)
modelfile="crf"
crf=pickle.load(open(modelpath+"\\"+modelfile,"rb"))

print(data)

#predict
sentence = nltk.word_tokenize(data)
print("sentence", sentence)
x = nltk.pos_tag(sentence)
print("POS tag", x)
test_sent = [i + ('-', ) for i in x]
print("test_sent",test_sent)
sentence2feature=sent2features(test_sent)
result=crf.predict([sentence2feature])[0]
for a, b in zip(sentence, result):
    print(a, "==>", b)

