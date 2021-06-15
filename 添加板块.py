#Python3
#从财联社，东方财富，中证指数以及申万行业读取股票列表

import re, json, time
import requests
import numpy as np
import pandas as pd
from diy.stock import writeebk

html = "ths"  #  cls,  dfcf,  zz,  sw
bk = "881121"


def getlist(html, bk):

    if html == "cls":
        api = "https://x-quote.cls.cn/web_quote/plate/stocks?app=CailianpressWeb&os=web&rever=1&secu_code="+bk+"&sv=7.5.5&way=cmc&sign=a5d404220e9a7d0752e8bb91c76b4fa8"
        data = json.loads(requests.get(api).text)['data']['stocks']
        codelist = [term['secu_code'][2:] for term in data]
        print([term['secu_name'] for term in data])
        return codelist

    elif html == "dfcf":
        t = str(int(time.time()*1000))
        api = "http://31.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409671394462169416_"+t+"&pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f6&fs=b:BK"+bk+"+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_="+t
        data = json.loads((re.findall(r'\((.*)\)', requests.get(api).text))[0])['data']['diff']
        codelist = [term['f12'] for term in data]
        print([term['f14'] for term in data])
        return codelist

    elif html == "zz":
        api = "http://www.csindex.com.cn/uploads/file/autofile/cons/"+bk+"cons.xls?t="+str(int(time.time())-100)
        code = pd.read_excel(api,usecols = [4,5],dtype={"成分券代码Constituent Code":str,"成分券名称Constituent Name":str})
        print(code["成分券名称Constituent Name"])
        return code["成分券代码Constituent Code"]
        
    elif html == "sw":
        code = []
        for i in range(20):
            api = "http://www.swsindex.com/handler.aspx?tablename=SwIndexConstituents&key=id&p="+str(i)+"&where=SwIndexCode ='"+bk+"'  and IsReserve ='0' and    NewFlag=1&orderby=StockCode ,BeginningDate_0&fieldlist=stockcode,stockname&pagecount=200&timed="+str(int(time.time()*1000))
            data = eval(requests.get(api).text)['root']
            code = code + data
            if len(data) <20:
                print([term['stockname'] for term in code])
                return [term['stockcode'] for term in code]
        print("数据未加载完全")
        return [term['stockcode'] for term in code]
    
    else:
        print("请在财联社、东方财富、中证指数、申万行业中选择一个！")
        
    return None

getlist(html, bk)
