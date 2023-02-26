import os
import pickle
import sklearn_crfsuite
import pandas as pd
from nltk.corpus.reader import ConllCorpusReader
from sklearn_crfsuite import metrics

data_folder = "CoNLL-2003"
train_sents = ConllCorpusReader(data_folder, 'train.txt', ['words', 'pos', 'ignore', 'chunk']).iob_sents()
test_sents = ConllCorpusReader(data_folder, 'valid.txt', ['words', 'pos', 'ignore', 'chunk']).iob_sents()

# Bỏ các câu rỗng do lỗi dữ liệu
train_sents = [x for x in train_sents if len(x) > 0]
test_sents = [x for x in test_sents if len(x) > 0]

# Xem một số câu ví dụ 
print(train_sents[:3])

ll = []
for s in train_sents:
    for t in s: 
        ll.append({'token': t[0], 'postag': t[1], 'label': t[2]})
    ll.append({'token': '', 'postag': '', 'label': ''})

pd.set_option('display.max_columns', None)
pd.set_option("max_rows", 100)
df = pd.DataFrame(ll)
print(df)

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

def sent2tokens(sent):
    return [token for token, postag, label in sent]


# Xem kết quả của việc rút trích đặc trưng
print(sent2features(train_sents[0]))

X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]

X_test = [sent2features(s) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents]

#print(len(X_train[0]))
#print(len(y_train[0]))
#print(X_train[0][2])
#print(y_train[0][2])


crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.0001,
    c2=0.01,
    max_iterations=100,
    all_possible_transitions=True,
    verbose=True
)
crf.fit(X_train, y_train)

labels = list(crf.classes_)
#print(labels)

y_pred = crf.predict(X_test)
score1 = metrics.flat_f1_score(y_test, y_pred,
                      average='weighted', labels=labels)

print(score1)
labels.remove('O')
score2 = metrics.flat_f1_score(y_test, y_pred,
                      average='weighted', labels=labels)
#print(labels)
print(score2)

count=0
sum=0
for i in range(len(test_sents)):
    sum=sum+len(test_sents[i])
    for a, b in zip(test_sents[i], crf.predict([X_test[i]])[0]):
        if a[2]!=b:
            #print(a, b)
            count=count+1

#print(str(count)+"/"+str(sum)+":",count/sum*100)

#save model
modeldir="models"
currentpath=str(os.path.abspath(os.getcwd()))
modelpath=currentpath+"\\"+modeldir
print(modelpath)
if not (os.path.exists(modelpath)):
    os.mkdir(modelpath)
modelfile="crf"
pickle.dump(crf,open(modelpath+"\\"+modelfile,"wb"))