import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm 

url = 'http://www.pkumdl.cn:8000/PSPredictor/all_scripts/runprediction.php'

def parse_html(in_seq,count=10):
    myobj = {'filenamedir': 'user_sess/user','inseq': in_seq,"taskid":'1'}
    results = requests.post(url, data = myobj)
    text = eval(results.text)[0]
    print(text)
    soup = BeautifulSoup(text, "lxml")
    
    tables=soup.find_all('table')
    for i in range(len(tables)):
        df_tables=pd.read_html(str(tables[i]))
        for j in range(len(df_tables)):
            df=df_tables[j]
            csv_name=os.path.join('tables',str(count)+'.csv')
            df.to_csv(csv_name,index=False,header=False)

with open('output.txt','r') as f:
    in_seqs = f.readlines()
    count = 0
    frenquency = 100
    in_seq=""
    flag=False
    for i in tqdm(range(0,len(in_seqs),2)):
        if(in_seqs[i].strip()=='>LOC_Os01g01010.1'):
            flag=True
        count+=1
        if(flag):
            in_seq +=in_seqs[i]+in_seqs[i+1]
            if(count %frenquency==0):
                parse_html(in_seq,count=count)
                in_seq=""