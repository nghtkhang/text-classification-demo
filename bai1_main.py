import re
import sys

data=""

n=len(sys.argv)
if n <2:
    data=input("Nhập vào test cần extract: ")

    outtext = re.findall(r'{}'.format("[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]"), data, flags=0)
    print("Phone number list=",outtext)
    outtext = re.findall(r'{}'.format("[a-z0-9]+@[a-z0-9]+\.[a-z]+"), data, flags=0)
    print("Email list=",outtext)

else:
    inputtext=str(sys.argv[1])
    outputtext=str(sys.argv[2])
    with open(inputtext, 'r') as rfile:
        data = rfile.read().replace('\n', '')
    phonelist = re.findall(r'{}'.format("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"), data, flags=0)
    emaillist = re.findall(r'{}'.format("[a-z0-9]+@[a-z0-9]+\.[a-z]+"), data, flags=0)
    with open(outputtext,'w') as wfile:
        wfile.write("Phone number list: \n")
        for i in phonelist:
                wfile.write(i+"\n")
        wfile.write("Email list: \n")
        for i in emaillist:
                wfile.write(i+"\n")
