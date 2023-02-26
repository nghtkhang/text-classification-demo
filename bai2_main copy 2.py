import os
import pickle
import bai2_config

print("Enter/Paste your content. Ctrl-Z ( windows ) to save it.")
contents = []
while True:
    try:
        line = input()
        contents.append(str(line).strip())
    except EOFError:
        break
#load model
modelfile='svm'
currentpath=str(os.path.abspath(os.getcwd()))
modelpath=currentpath+"\\"+bai2_config.modeldir
if not (os.path.exists(modelpath)):
    os.mkdir(modelpath)
text_clf=pickle.load(open(modelpath+"\\"+modelfile,"rb"))

#dự đoán
if len(contents)>0:
    Y_test_predict=text_clf.predict(contents)
    for a, b in zip(contents, Y_test_predict):
            print(a, "==>", b)
else:
    print("Input not found: For text classification, you have to input the text!")
