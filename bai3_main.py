import pickle  
import bai3_config
import os
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def splitWord(plist):
    wlist=[]
    for i in range(len(plist)):
        wlist.append(str(plist[i]).split())
    return wlist

print("Enter/Paste your content. Ctrl-Z ( windows ) to save it.")
contents = []
while True:
    try:
        line = input()
        contents.append(str(line).strip())
    except EOFError:
        break

#đọc model
currentpath=str(os.path.abspath(os.getcwd()))
modelpath=currentpath+"\\"+bai3_config.modeldir
if not (os.path.exists(modelpath)):
    os.mkdir(modelpath)
crf=pickle.load(open(modelpath+"\\"+bai3_config.modelfile,"rb"))

#thực hiện dự đoán
if len(contents)>0:
    for i in range(len(contents)):
        sentence = nltk.word_tokenize(contents[i])
        x = nltk.pos_tag(sentence)
        test_sent = [i + ('-', ) for i in x]
        p2feature=bai3_config.sent2features(test_sent)
        result=crf.predict([p2feature])[0]
        for a, b in zip(sentence, result):
            print(a, "==>", b)
else:
    print("Input not found: For NER, you have to input the text!")
