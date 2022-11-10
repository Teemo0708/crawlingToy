# -- coding: utf-8 --
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup as bs
import json


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

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
