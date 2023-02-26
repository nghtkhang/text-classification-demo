import os
import sys
import sklearn_crfsuite
from nltk.corpus.reader import ConllCorpusReader
from sklearn_crfsuite import metrics
from sklearn.metrics import make_scorer
import warnings
from sklearn.model_selection import RandomizedSearchCV
from sklearn.exceptions import UndefinedMetricWarning
import pickle
import bai3_config
import nltk

#lưu terminal output
ter_output=bai3_config.ter_output
f_ter_ouput=open(ter_output,"w")
sys.stdout=f_ter_ouput

#download thư viện nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#load dữ liệu
data_folder = "CoNLL-2003"
train_sents = ConllCorpusReader(data_folder, 'train.txt', ['words', 'pos', 'ignore', 'chunk']).iob_sents()
test_sents = ConllCorpusReader(data_folder, 'valid.txt', ['words', 'pos', 'ignore', 'chunk']).iob_sents()

# Bỏ các câu rỗng do lỗi dữ liệu
train_sents = [x for x in train_sents if len(x) > 0]
test_sents = [x for x in test_sents if len(x) > 0]

def createCrf(p_algorithm='lbfgs',p_c1=0.001,p_c2=0.01,p_max_iterations=100,p_all_possible_transitions=True):
    crf = sklearn_crfsuite.CRF(
    algorithm=p_algorithm,
    c1=p_c1,
    c2=p_c2,
    max_iterations=p_max_iterations,
    all_possible_transitions=p_all_possible_transitions,
    verbose=True
    )
    return crf

#chia train set và test set
X_train = [bai3_config.sent2features(s) for s in train_sents]
y_train = [bai3_config.sent2labels(s) for s in train_sents]

X_test = [bai3_config.sent2features(s) for s in test_sents]
y_test = [bai3_config.sent2labels(s) for s in test_sents]

crf=createCrf()
crf.fit(X_train, y_train)

#đánh giá trên test set
labels = list(crf.classes_)
print("Original label list:",labels)
labels.remove("O")
print("Label list with remove O:",labels)
y_pred = crf.predict(X_test)
score1 = metrics.flat_f1_score(y_test, y_pred,average='weighted', labels=labels)
print("F1 score:",score1)
print(metrics.flat_classification_report(y_test, y_pred,labels=labels))

# tối ưu các tham số bằng RandomizedSearchCV
param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

param_grid = {"c1": param_range,
              "c2": param_range}
#sử dụng F1 score làm tiêu chuẩn đánh giá việc tối ưu
f1_scorer = make_scorer(metrics.flat_f1_score, average='weighted', labels=labels)

rs = RandomizedSearchCV(crf,
                        param_distributions=param_grid,
                        scoring=f1_scorer,
                        cv=3,
                        verbose=1,
                        n_iter=50,
                        n_jobs=-1)

# bỏ qua các cảnh báo 'UndefinedMetricWarning'
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
    rs.fit(X_train, y_train)

# in ra kết quả tối ưu và sử dụng các tham số đã tối ưu để xây dựng model
print("Best score in train dataset=",rs.best_score_)
print("Best score in test dataset=",rs.score(X_test,y_test))
print("with best_params=",rs.best_params_)
print("Create model with best params:")
c1=rs.best_params_['c1']
c2=rs.best_params_['c2']
crf=createCrf(p_c1=c1,p_c2=c2)
crf.fit(X_train, y_train)

#lưu model
try:
    currentpath=str(os.path.abspath(os.getcwd()))
    modelpath=currentpath+"\\"+bai3_config.modeldir
    print(modelpath)
    if not (os.path.exists(modelpath)):
        os.mkdir(modelpath)
    pickle.dump(crf,open(modelpath+"\\"+bai3_config.modelfile,"wb"))
    print("The CRF model is saved in ",modelpath+"\\"+bai3_config.modelfile)
except Exception as e:
        print("Error({0}): {1}".format(e.errno, e.strerror))

for a, b in zip(test_sents[0], crf.predict([X_test[0]])[0]):
    print(a, b)

#đóng terminal output
f_ter_ouput.close()