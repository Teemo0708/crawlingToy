# -- coding: utf-8 --
from fastapi import FastAPI
import requests, json
from pprint import pprint
from bs4 import BeautifulSoup as bs
from pydantic import BaseModel
from elastic import ElasticPost
from collections import defaultdict


class Item(BaseModel):
    cat_list : list = [{"name" : "건강식품", "param" : ["50000023"]}]
    
ID = "2955"  
KEY = "c18025a9-bc77-4084-8017-164977caffa9"

ELASTIC_HOST = "34.64.205.41"
ELASTIC_PORT = 9200

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
        
        
@app.post("/items/select")
async def selectC(parameter: Item):

    ####################################
    client_id = "SOmSP6p7sz6n7sSYB2GZ"
    client_secret = "asqHDSqHK9"
    ####################################

    url = "https://openapi.naver.com/v1/datalab/shopping/categories"
    
    print(parameter)

    payload = {"startDate": "2022-10-01",
            "endDate": "2022-11-13",
            "timeUnit": "month",
            "category": parameter.cat_list,
            "device": "pc"
                }

    headers = {"X-Naver-Client-Id": ID, "X-Naver-Client-Secret": SECRET, "Content-Type": "application/json"}
    res = requests.post(
        url, 
        data=json.dumps(payload), 
        headers=headers
        ).json()
    
    return res
    
@app.get("/items/daily")
async def selectItem():
    
    index_name = "simple_index"
    
    elastic_object = ElasticPost(ELASTIC_HOST ,ELASTIC_PORT, index_name)
    
    url = f"http://www.kamis.co.kr/service/price/xml.do?action=dailySalesList&p_cert_key={KEY}&p_cert_id={ID}&p_returntype=json"
    
    query_res = requests.get(url).json()
    
    elastic_res_code = defaultdict(int)
    
    for items in query_res["price"]:
        elastic_res_code[elastic_object.sendPost(items)] += 1
        
    return elastic_res_code
    

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
