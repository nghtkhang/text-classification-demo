import os
import pickle
data=[]
print("Nhập vào test cần extract: ")
line=input()
data.append(str(line).strip())
print(type(data))
#load model
modeldir="models"
currentpath=str(os.path.abspath(os.getcwd()))
modelpath=currentpath+"\\"+modeldir
if not (os.path.exists(modelpath)):
    os.mkdir(modelpath)
modelfile="svm"
text_clf=pickle.load(open(modelpath+"\\"+modelfile,"rb"))

#dự đoán
Y_test_predict=text_clf.predict(data)
for a, b in zip(data, Y_test_predict):
    print(a, "==>", b)

