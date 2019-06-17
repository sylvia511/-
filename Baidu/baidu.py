import requests
from bs4 import BeautifulSoup
import re 
import time

time1=time.time()
exist_url=[]
g_writecount=0

def scrappy(url,depth=1):
    global g_writecount
    try:
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        r=requests.get("https://baike.baidu.com/item/"+url,headers=headers)
        html=r.content.decode('utf-8')
    except Exception as e:
        print('Fail downloading and saving',url)
        print(e)
        exist_url.append(url)
        return None

    exist_url.append(url)
    link_list=re.findall('<a href="/([^:#=<>]*?)".*?</a>',html)
    unique_url=list(set(link_list)-set(exist_url))

    for eachone in unique_url:
        g_writecount+=1
        output="No."+str(g_writecount)+"\t Depth:"+str(depth)+"\t"+url+"->"+eachone+"\n"
        print(output)
        with open('title.txt',"a+") as f:
            f.write(output)
            f.close()
        if depth<2:
            scrappy(eachone,depth+1)

scrappy("百度")
time2=time.time()
print("Total time",time2-time1)