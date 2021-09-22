from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape():
    #todaysprice data nepalstock
    #dateformat=2021-4-1(yyyy-m-d)
    url='http://www.nepalstock.com/todaysprice/?startDate&stock-symbol=&_limit=300'
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')

    names=soup.select("tr.unique td")
    columnlist=[]
    for i in names:
        columnlist.append(i.text)
    df=pd.DataFrame(columns=columnlist)

    rows=soup.find("table", attrs={"class":"table"}).find_all("tr")[2:-4]
    number=len(rows)

    for i in range (2,number+2):
        rows=soup.find("table", attrs={"class":"table"}).find_all("tr")[i]
        l=[]
        td=rows.find_all('td')
        for i in td:
            l.append(i.text.strip())
        a_series = pd.Series(l, index = df.columns)
        df = df.append(a_series, ignore_index=True)

    js = df.to_json(orient = 'records')
    return js
def index(request):
    return HttpResponse("http://nepshareapi.herokuapp.com/todayprice")
def todayprice(request):
    js=scrape()
    return HttpResponse(js,content_type="application/json")