import os
import sys
import pickle
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import bai2_config

def preproccess_data(str):
    X_data=[]
    Y_data=[]
 
    with open(str,encoding="utf8") as f:
        for line in f:
            l=line.split(":")
            clstxts=l[0].split(".")
            Y_data.append(clstxts[0].upper())
            X_data.append(l[1].replace("?\n","").strip())
    return X_data,Y_data

def createPipeline(C=1.0,use_idf=True,ngram_range=(1, 2)):
    text_clf = Pipeline([
    ('vect', CountVectorizer(ngram_range=ngram_range)),
    ('tfidf', TfidfTransformer(use_idf=use_idf)),
    ('clf', svm.LinearSVC(C=C)),
    ])
    return text_clf

X_data,Y_data=preproccess_data(bai2_config.train_path)


print("Class:",set(Y_data))


text_clf = createPipeline()


X_train,X_test,Y_train,Y_test=train_test_split(X_data,Y_data,test_size=0.2,random_state=0)


text_clf.fit(X_train,Y_train)
Y_predict=text_clf.predict(X_test)

ncorrect = sum([y_pred == y for y_pred, y in zip (Y_predict, Y_test)])
accurracy = ncorrect / len(Y_test)
print("Accuracy:",accurracy)

modeldir="models"
modelfile="svm"
currentpath=str(os.path.abspath(os.getcwd()))
modelpath=currentpath+"\\"+modeldir
if not (os.path.exists(modelpath)):
    os.mkdir(modelpath)
pickle.dump(text_clf,open(modelpath+"\\"+modelfile,"wb"))

