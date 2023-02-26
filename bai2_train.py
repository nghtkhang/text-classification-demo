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
    #đọc và phân tách data và class trong dataset
    with open(str,encoding="utf8") as f:
        for line in f:
            l=line.split(":")
            #do dataset nhỏ nên chỉ lọc phân lớp lớn
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

#lưu terminal output
ter_output=bai2_config.ter_output
f_ter_ouput=open(ter_output,"w")
sys.stdout=f_ter_ouput

#tiền xử lý dữ liệu
X_data,Y_data=preproccess_data(bai2_config.train_path)

#lấy danh sách class
print("Class:",set(Y_data))

#khởi tạo pipline
text_clf = createPipeline()

#chia train và test set
X_train,X_test,Y_train,Y_test=train_test_split(X_data,Y_data,test_size=0.2,random_state=0)

#phân lớp với SVM
text_clf.fit(X_train,Y_train)
Y_predict=text_clf.predict(X_test)

#tính accuracy
ncorrect = sum([y_pred == y for y_pred, y in zip (Y_predict, Y_test)])
accurracy = ncorrect / len(Y_test)
print("Accuracy:",accurracy)

#tối ưu tham số bằng GridSearchCV
parameters = {
    'vect__ngram_range': [(1,1),(1,2),(1,3),(2,2),(2, 3),(3,3)],
    'tfidf__use_idf': (True, False),
    'clf__C': (1.0, 2.0, 3.0,4.0,5.0)
}
gs_clf = GridSearchCV(text_clf, parameters, cv=5, n_jobs=-1)
gs_clf = gs_clf.fit(X_train, Y_train)
print("Best score=",gs_clf.best_score_)
print("with parameter:")
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))

#dùng tham số đã tối ưu để tạo ra model tốt nhất
C=gs_clf.best_params_["clf__C"]
use_idf=gs_clf.best_params_["tfidf__use_idf"]
ngram_range=gs_clf.best_params_["vect__ngram_range"]
text_clf=createPipeline(C,use_idf,ngram_range)
text_clf.fit(X_train,Y_train)

#lưu model
try:
    currentpath=str(os.path.abspath(os.getcwd()))
    modelpath=currentpath+"\\"+bai2_config.modeldir
    if not (os.path.exists(modelpath)):
        os.mkdir(modelpath)
    pickle.dump(text_clf,open(modelpath+"\\"+bai2_config.modelfile,"wb"))
    print("The SVM model is saved in ",modelpath+"\\"+bai2_config.modelfile)
except Exception as e:
        print("Error({0}): {1}".format(e.errno, e.strerror))

#đóng terminal output
f_ter_ouput.close()