#!/usr/bin/env python
# coding: utf-8

# In[55]:


from selenium import webdriver


# In[56]:


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# In[57]:


def get_chrome_driver():
    # 1. 크롬 옵션 세팅
    chrome_options = webdriver.ChromeOptions()
    
    # 2. driver 생성하기
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), # 가장 많이 바뀐 부분
        options=chrome_options
    )
    
    return driver


# In[58]:


driver = get_chrome_driver()


# In[59]:


driver.get("http://gs25.gsretail.com/gscvs/ko/store-services/locations#;")#해당 페이지로 들어감


# In[60]:


driver.find_element_by_xpath('//*[@id="stb1"]/option[2]').click() #지역 선택에서 서울시 선택


# In[76]:


driver.find_element_by_xpath('//*[@id="searchButton"]').click() #검색 누르기


# In[77]:


driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #스크롤 맨 아래로


# In[109]:


#한페이지 긁고 넘어가고
import time
import pandas as pd
datas = pd.DataFrame()
salist=[]

#exception 날때까지 긁음
while True:
    try:
        for i in range (1,6):    
            store = driver.find_elements_by_xpath(f'//*[@id="storeInfoList"]/tr[{i}]/td[1]/a')#지점명
            address = driver.find_elements_by_xpath(f'//*[@id="storeInfoList"]/tr[{i}]/td[2]/a')#주소
            salist = [[store[0].text, address[0].text]]#받은거 리스트로 저장
            #print(store[0].text)
            #print(address[0].text)
            dff = pd.DataFrame(salist, columns=['지점명','주소'])#데이터프레임으로 만들기
            datas = pd.concat([datas, dff])#빈 데이터프레임에 쌓기
        driver.find_element_by_xpath('//*[@id="pagingTagBox"]/a[3]').click()#다음 페이지로 넘김
        #print("한페이지 끝")
        time.sleep(2) # 이거 안하면 페이지 로딩전에 긁어버려서 망함
    except Exception as e:
        print("끝이거나 오류",e)
        break
            
     
print(datas)


# In[110]:


#csv로 저장
datas.to_csv("GS편의점 지점정보.csv", mode='a', header = False, encoding='cp949')


# In[ ]:




