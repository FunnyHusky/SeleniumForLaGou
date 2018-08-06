# -*- coding:UTF-8 -*-
'''
Created on 2018年4月1日

@author: Administrator
'''
import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from selenium.common.exceptions import TimeoutException
import time
jobs_urls =set()
browser = webdriver.Firefox(executable_path="C:\\Users\\liangzi\\Desktop\\SeleniumWebDriver\\geckodriver.exe") #这里填的是你本机下载的geckodriver.exe的真实路径
#browser = webdriver.Chrome(executable_path="C:\\Users\\liangzi\\Desktop\\SeleniumWebDriver\\chromedriver.exe")
browser.get("https://passport.lagou.com/login/login.html")
wait = WebDriverWait(browser,10)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"form.active > div:nth-child(5) > input:nth-child(1)")))    
def sendKeys(browser):
    username="用户名"
    password="用户密码"
    user = browser.find_element_by_css_selector("form.active > div:nth-child(1) > input:nth-child(1)")
    user.send_keys(username)
    browser.implicitly_wait(3)
    password = browser.find_element_by_css_selector("form.active > div:nth-child(2) > input:nth-child(1)")
    password.send_keys(password)
def clickLoginButton(browser,selector):
    login=browser.find_element_by_css_selector(selector)
    login.click()
    
def searchJobs(keyword,browser): #keyword是要找的工作类型，如python开发工程师,java开发工程师,android等等
    search = browser.find_element_by_css_selector("#search_input")
    search.send_keys(keyword)
    browser.implicitly_wait(2)
    clickLoginButton(browser, "#search_button")
    
def getJobs(result):
    try:
        selector = Selector(text=result)
        links = selector.xpath('//div[@class="p_top"]/a/@href').extract()
        print(links)
        lens = len(links)
        if lens >0:
            for x in links:
                jobs_urls.add(x)
    except Exception as e:
        print("GetJobs",e)
def isNextButtonClickable(browser):
    isable =EC.element_to_be_clickable((By.CSS_SELECTOR,".pager_next"))
    return isable
def getAndNext(browser):
    for x in range(17):
            browser.implicitly_wait(10)
            clickLoginButton(browser, ".pager_next")
            browser.implicitly_wait(5)
            getJobs(browser.page_source)
            browser.implicitly_wait(3)
#         else:
#             break 
def sendResume(browser,jobsUrl):
    try:
        browser.get(jobsUrl)
        browser.implicitly_wait(10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".send-CV-btn")))
        sendButton = browser.find_element_by_css_selector(".send-CV-btn")
        company = browser.find_element_by_css_selector(".company").text
        jobname = browser.find_element_by_css_selector("span.name:nth-child(2)").text
        print("当前的公司是",company)
#         print("sendButton Text ",sendButton.text)        
        if sendButton.text =="已投递":
            return
        else:   
            clickLoginButton(browser, ".send-CV-btn") 
            browser.implicitly_wait(2)
            if EC.visibility_of_element_located((By.CSS_SELECTOR,"#delayConfirmDeliver")) :
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#delayConfirmDeliver")))
#                 print("确认投递按钮出现")
                clickLoginButton(browser, "#delayConfirmDeliver")
                browser.implicitly_wait(5)
#                 if EC.visibility_of_element_located((By.CSS_SELECTOR,".upper_msg")):
#                     print("当天投递次数已经用完，明天继续投递")
#                     raise Exception("当天投递次数已经用完")
#                     return
                if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#knowed"))):
                    print("投递简历成功")
                    writeLaGou(company, jobname)
                  
    except TimeoutException as e:
        print(e)
    except Exception as e:
        raise e

def writeLaGou(company,jobname):
     with open("C:\\Users\\Administrator\\Desktop\\spiderHistory\\lagou"+str(time.strftime("%Y-%m-%d"))+".txt","a+",encoding="utf-8") as f:
                    f.write(time.strftime("%H-%M-%S")+":投递"+company+" "+jobname+"  成功 ")
                    f.write("\n")
def Main():
    sendKeys(browser)
    clickLoginButton(browser,"form.active > div:nth-child(5) > input:nth-child(1)")    
    keyword ="工作岗位"
    searchJobs(keyword, browser) 
    browser.implicitly_wait(10)
    getJobs(browser.page_source)
    browser.implicitly_wait(5)
#     getAndNext(browser) 
    for url in jobs_urls:
        try:
            sendResume(browser, url)
            browser.implicitly_wait(10)
        except Exception as e:
            if e.__str__() =="当天投递次数已经用完":
                print("Exception",e)
if __name__ =="__main__":
      Main()