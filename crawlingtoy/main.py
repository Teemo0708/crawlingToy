# -- coding: utf-8 --
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup as bs
import json
import pprint



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test/{input}")
async def crawling(input):
    
    try:
        
        page = requests.get("https://library.gabia.com/")
        
        soup = bs(page.content, 'html.parser',from_encoding='utf-8')
        
        elements = soup.select('div.esg-entry-content a.eg-grant-element-0')
        list_ele = list(elements)
        
        res_dict= {}

        for index, elements in enumerate(list_ele):
            
            res_dict[index] = elements.text, elements.attrs['href']
        
        json_val = json.dumps(res_dict, ensure_ascii=False) # ensure_ascii=False 붙여넣기
        
        print(json_val)
        
        return json_val
    
    except Exception as e :
        print(e)
        
@app.get("/items/select/{select_cat}")
async def selectC(select_cat):

    ####################################
    client_id = "SOmSP6p7sz6n7sSYB2GZ"
    client_secret = "asqHDSqHK9"
    ####################################

    url = "https://openapi.naver.com/v1/datalab/shopping/categories"

    payload = {"startDate": "2022-10-01",
            "endDate": "2022-11-13",
            "timeUnit": "month",
            "category": [
                {"name": "식품",
                    "param": ["50000006"]},
                {"name": "건강식품",
                    "param": ["50000023"]}],
            "device": "pc",
            #"ages": [],
            #"gender": 
                }

    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret, "Content-Type": "application/json"}
    res = requests.post(url, data=json.dumps(payload), headers=headers)

    print(res.status_code)
    aaa = json.loads(res.text)

    json_val2 = json.dumps(aaa, ensure_ascii=False)

    pprint.pprint(json_val2)
    #print(type(aaa))
    
    return json_val2
    

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
