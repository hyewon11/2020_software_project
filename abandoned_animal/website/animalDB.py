import os
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import urllib.request
import ssl

from django.shortcuts import render
from django.utils import timezone

ssl._create_default_https_context = ssl._create_unverified_context
import sqlite3
import pandas as pd
from .models import Post

# 본인 serviceKey 입력
serviceKey = "718617iI2GVV0AWrip1dEkJMt3Jl9GPvl%2Flz28ktLjA7EYSXhYwCFjFlH9LovIRqzDDkAeUy29%2FaugkKim%2Fa%2Fw%3D%3D"


# SQLite3 이용
def sqlite_append(animalDf):
    # C드라이브에 projectDB 폴더 생성 animalInfo.db 파일 생성
    con = sqlite3.connect("c:/projectDB/animalInfo.db")
    animalDf.to_sql('animalInfo', con, if_exists='append', index=False) # 저장
    con.close()


# API 데이터 파싱 후 sqlite_append 함수 불러오기

def collect_info():
    url = "http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?serviceKey="
    url = url + serviceKey

    request = urllib.request.urlopen(url)
    xml = request.read()
    soup = BeautifulSoup(xml, "html.parser")
    name = soup.find_all("item")

    totalCount = soup.find("totalcount").text

    url = "http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?" \
            "&numOfRows=" + totalCount + "&ServiceKey="
    url = url + serviceKey

    request = urllib.request.urlopen(url)
    xml = request.read()
    soup = BeautifulSoup(xml, "html.parser")

    item = soup.find_all("item")

    # item에 있는 정보들 불러오기
    for info in item:
        age = info.find("age").text
        careaddr = info.find("careaddr").text
        carenm = info.find("carenm").text
        caretel = info.find("caretel").text
        kindcd = info.find("kindcd").text
        happendt = info.find("happendt").text
        date = timezone.datetime.strptime(happendt, "%Y%m%d")
        happenplace = info.find("happenplace").text
        specialmark = info.find("specialmark").text
        poster_src = info.find("popfile").text

        # urlretrieve(poster_src, "popfile/" + careaddr[:4] + ".png")

        Post(menu=True, species=kindcd, miss_date=date, miss_loc=happenplace, feature=specialmark, image=None,
             shelter=carenm, shelter_phone=caretel).save()
    '''
        # 데이터프레임으로 넣기
        animalInfo = pd.DataFrame(([[age, careaddr, caretel, kindcd, happendt, happenplace, specialmark, poster_src]]),
                                  columns=["age", "careaddr", "caretel", "kindcd", "happendt", "happenplace",
                                           "specialmark", "poster_src"])

        # sqlite_append 함수 호출
        sqlite_append(animalInfo)
    '''

def db(request):
    collect_info()
    return render(request, 'db.html')
