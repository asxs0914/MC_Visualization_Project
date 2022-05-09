#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver


# In[2]:


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# In[3]:


def get_chrome_driver():
    # 1. 크롬 옵션 세팅
    chrome_options = webdriver.ChromeOptions()
    
    # 2. driver 생성하기
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), # 가장 많이 바뀐 부분
        options=chrome_options
    )
    
    return driver


# In[42]:


driver = get_chrome_driver()
driver.maximize_window() #창이 작으면 검색버튼이 안눌리는거같아서 최대화했습니다.


# In[43]:


driver.get("https://cu.bgfretail.com/store/list.do?category=store")#해당 페이지로 들어감


# In[1]:


driver.find_element(By.XPATH,'//*[@id="sido"]/option[3]').click() #지역 선택에서 서울시 선택


# In[49]:


#GS와 다르게 시군구 다 놓고 '검색'해야 결과물이 나옴 조건문으로 잘 굴려봐야함

import pandas as pd
import time
i=2
j=2
datas = pd.DataFrame()
salist=[]

def search():#검색 버튼
    driver.find_element(By.XPATH,'//*[@id="contents"]/div[1]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/div/input[1]').click()
    return

while True:    
    try:
        driver.find_element(By.XPATH,'//*[@id="Gugun"]').click() #id로 검색
        time.sleep(1)
        driver.find_element(By.XPATH,f'//*[@id="Gugun"]/option[{i}]').click() 
        time.sleep(1)
        while True:  
            try:
                driver.find_element(By.XPATH,'//*[@id="Dong"]').click() 
                time.sleep(1)
                driver.find_element(By.XPATH,f'//*[@id="Dong"]/option[{j}]').click()
                time.sleep(1)
                search()
                time.sleep(1)
                while True: #한번더 조건을 걸어줬습니다. 이 조건이 없으니 동 선택을 하는부분에서 계속 구 선택부분으로 간 다음 다시 동 선택을 했습니다.
                    try:
                        for k in range(1,6):
                            maj = driver.find_element(By.XPATH,f'//*[@id="result_search"]/div[2]/div[1]/table/tbody/tr[{k}]/td[1]/span[1]').text#지점 이름
                            add = driver.find_element(By.XPATH,f'//*[@id="result_search"]/div[2]/div[1]/table/tbody/tr[{k}]/td[2]/div/address/a').text#주소
                            salist = [[maj, add]]#받은거 리스트로 저장
                            dff = pd.DataFrame(salist, columns=['지점명','주소'])#데이터프레임으로 만들기
                            datas = pd.concat([datas, dff])#빈 데이터프레임에 쌓기
                        print("한페이지 끝")
                        # 다음버튼이 안보여서 그런가 싶어서 스크롤을 맨 아래로 내렸봤습니다.
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                        # 다음 버튼을 xpath로 설정했더니 다음 페이지로 넘어가니 이전버튼과 다음버튼 xpath가 좀 겹쳐서 이전버튼이 눌린거같습니다.
                        driver.find_element(By.CLASS_NAME,'next').click() # CLASS 이름이 제일 정확한거같아서 바꿨습니다.
                        time.sleep(1)               
                    except Exception as g:
                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0,0);") #검색버튼이 다시 보이게 맨위로 스크롤
                        #print("남은 페이지 0, 다음 동으로",g)
                        j += 1
                        time.sleep(1)
                        break
            except Exception as k:
                driver.execute_script("window.scrollTo(0,0);") # 검색버튼이 다시 보이게 맨위로 스크롤
                i += 1
                #print("구 선택으로 복귀",k)
                continue
    except Exception as e:
        print("종료",e)
        break

print(datas)

