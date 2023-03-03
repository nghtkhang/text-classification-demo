import re
import sys
itext=""
ofile=""
data=""
phnumber_patt= "[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]"
email_patt= "[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

n=len(sys.argv)
if n >2:
    itext=str(sys.argv[1])
    ofile=str(sys.argv[2])

def extractPhoneNum(pitext):
    phlist = re.findall(r'{}'.format(phnumber_patt), pitext, flags=0)
    return phlist

def extractEmail(pitext):
    emlist = re.findall(r'{}'.format(email_patt), pitext, flags=0)
    return emlist

if itext=="" and ofile=="":
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
            contents.append(line)
        except EOFError:
            break
    data=''.join([str(i)+' ' for i in contents])

    otext=extractPhoneNum(data)
    print("Phone number list=",otext)
    otext=extractEmail(data)
    print("Email list=",otext)

elif itext!="" and ofile !="":
    try:
        with open(itext, 'r') as rfile:
            data = rfile.read().replace('\n', '')
    except IOError as e:
        print("Input File error({0}): {1}".format(e.errno, e.strerror))
        
    phlist=extractPhoneNum(data)
    emlist=extractEmail(data)

    try:
        with open(ofile,'w') as wfile:
            wfile.write("Phone number list: \n")
            for i in phlist:
                wfile.write(i+"\n")
            wfile.write("Email list: \n")
            for i in emlist:
                wfile.write(i+"\n")
    except IOError as e:
        print("Output File error({0}): {1}".format(e.errno, e.strerror))
else:
    error="""To extract email and phone list from data source, please type:
    python main.py
    or
    python main.py <<input_file>> <<output_file>>
    """
    print(error)
