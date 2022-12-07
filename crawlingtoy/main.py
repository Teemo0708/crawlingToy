from fastapi import FastAPI
import requests, json
from pprint import pprint
from bs4 import BeautifulSoup as bs
from pydantic import BaseModel
from elastic import ElasticPost
from collections import defaultdict


ID = "2955"
KEY = "c18025a9-bc77-4084-8017-164977caffa9"


ELASTIC_HOST = "34.64.205.41"
ELASTIC_PORT = 9200
ELASTIC_INDEX = "simple_index"

app = FastAPI()

# 데코레이션
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/daily")
async def selectItem():
    # elasticsearch class 호출
    elastic_object = ElasticPost(ELASTIC_HOST ,ELASTIC_PORT, ELASTIC_INDEX)

    # api 요청 url
    url = f"http://www.kamis.co.kr/service/price/xml.do?action=dailySalesList&p_cert_key=%7BKEY%7D&p_cert_id=%7BID%7D&p_returntype=json"

    # api에 get요청 보냄
    query_res = requests.get(url).json()

    # elasticsearch 응답코드를 저장하기 위한 dict
    elastic_res_code = defaultdict(int)

    # elasticsearch에 요청
    for items in query_res["price"]:
        elastic_res_code[elastic_object.sendPost(items)] += 1
        
        print(elastic_res_code)

    # 결과값 리턴
    return elastic_res_code