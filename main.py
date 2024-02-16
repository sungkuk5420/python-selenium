from flask import Flask,render_template,request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import googletrans
from googletrans import Translator
import csv

# base_url = "https://jp.shein.com/flash-sale.html" # 신발
base_url = "https://www.naver.com" # 신발
# base_url = "https://www.nike.com/jp/w/mens-jackets-vests-50r7yznik1" # 옷
imageIndex = 5


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(chrome_options=options)# 같은경로라면 드라이버 경로를 안써도 된다.

alreadyLinks = list()
productCode = ""

def printLog(logMessage):
    print("==================================")
    print(logMessage)

def waitProductListPageLoading():
    detailPage = driver.page_source.find('experience-wrapper')
    if detailPage != -1:
        return False
    else:
        return True

def isFindingProduct(alreadyLinks):
    while(waitProductListPageLoading()): #product
        printLog("상품 리스트 페이지 로딩중...") #product
    printLog("리스트 페이지 로딩완료") #product
    FoundItem = None
    # print(listItems)
    links = driver.find_elements(By.CLASS_NAME,"product-card__img-link-overlay")
    for currentLinkTag in links:
        currentLinkText = currentLinkTag.get_attribute("href")
        printLog(currentLinkText)
        currentIndex = alreadyLinks.index(currentLinkText) if currentLinkText in alreadyLinks else -1
        if(currentIndex == -1):
            print("상품 발견: " + currentLinkText + "//")
            FoundItem = currentLinkText
            break
        else:
            print("이미 등록된상품입니다!!")
            print(currentLinkText)
            print("상품을 탐색합니다")
    if (FoundItem != None):
        return FoundItem
    else:
        return False
        

def waitProductDetailPageLoading():
    detailPage = driver.page_source.find('experience-wrapper')
    if detailPage != -1:
        return False
    else:
        return True

def moveToCurrentProductDetailPage(currentLinkText):
    driver.get(currentLinkText)
    time.sleep(3)
    while(waitProductDetailPageLoading()): #product
        printLog("상품 상세 페이지 로딩중...") #product
    printLog("상세 페이지 로딩완료") #product


def getCurrentProductInfo(link):
    root  = driver.find_element(By.CLASS_NAME,"css-mso6zd")
    title  = root.find_element(By.ID,"pdp_product_title")
    titleText  = title.get_attribute("textContent")
    subTitle  = root.find_element(By.XPATH,"//h2[@data-test='product-sub-title']")
    subTitleText  = subTitle.get_attribute("textContent")
    translator = Translator(service_urls=['translate.googleapis.com'])
    titleText =  translator.translate(titleText, dest='ko').text
    subTitleText =  translator.translate(subTitleText, dest='ko').text
    price  = root.find_element(By.XPATH,"//div[@data-test='product-price']")
    priceText  = price.get_attribute("textContent").replace("￥","")
    sizes = list()
    counts= list()
    images = list()
    if(driver.page_source.find('css-12whm6j') != -1):
        sizeTagsParent  = root.find_element(By.CLASS_NAME,"css-12whm6j").find_elements(By.TAG_NAME,"div")
    if(driver.page_source.find('css-1j3x2vp') != -1):
        sizeTagsParent  = root.find_element(By.CLASS_NAME,"css-1j3x2vp").find_elements(By.TAG_NAME,"div")
    for currentTag in sizeTagsParent:
        sizeInput = currentTag.find_element(By.TAG_NAME,"input")          
        sizeText = currentTag.find_element(By.TAG_NAME,"label").get_attribute("textContent")
        sizeText=sizeText.replace("[","").replace("'","").replace("JP","").replace("US","")
        if(sizeText.find(".")!=-1):
            sizeText=sizeText.replace(".","")
        else:
            sizeText=sizeText.replace(" ","").replace("(US5)","").replace("(US6)","")
            if(sizeText.isnumeric() == True):
                sizeText = sizeText+"0"
        sizeText=sizeText.replace(" ","").replace("(US5)","").replace("(US6)","")
        sizeText = sizeText.replace(" ","")
        print(sizeText)
        if(sizeInput.get_attribute("disabled") == None):
            sizes.append(sizeText)
            counts.append("5")
        else:
            sizes.append(sizeText)
            counts.append("0")
    productCode = driver.find_element(By.CLASS_NAME,"description-preview__style-color").get_attribute("textContent").replace("スタイル： ", "")            
    origin = driver.find_element(By.CLASS_NAME,"description-preview__origin").get_attribute("textContent")
    origin =  translator.translate(origin, dest='ko').text
    # imageTags  = driver.find_element(By.CLASS_NAME,"css-1rayx7p").find_elements(By.TAG_NAME,"img")
    imageTags  = driver.find_element(By.CLASS_NAME,"css-1rayx7p").find_elements(By.XPATH,"//*[@data-sub-type='image']")
    index = 1
    for currentTag in imageTags:
        imageText = currentTag.find_elements(By.TAG_NAME,"picture")[1].find_element(By.TAG_NAME,"img").get_attribute("src")
        if(index ==imageIndex):
            urllib.request.urlretrieve(imageText, productCode  +".png")
        # if(index ==6):
        #     urllib.request.urlretrieve(imageText, productCode  +"(1).png")
        if(imageText!=None):
            imageText = f"<img src='{imageText}'/>"
            images.append(imageText)
        index = index +1

    productInfo = {
        "link": link,
        "productCode": productCode,
        "title": titleText,
        "subTitle": subTitleText,
        "price": priceText,
        "sizes": sizes,
        "counts": counts,
        "images": images,
        "origin": origin,
    }
    return productInfo

def fileSave(productInfo):
    print(productInfo)
    file = open("result.csv", "a", encoding="utf-8-sig")
    # string = f"{productInfo['productCode']},{productInfo['title']},{productInfo['subTitle']},{productInfo['price']},{productInfo['sizes']},{productInfo['images']}"
    string = f'{productInfo["link"]},{productInfo["productCode"]},{productInfo["productCode"]}.png,{productInfo["title"]},{productInfo["subTitle"]},"{productInfo["price"]}"'
    sizeString=""
    countString=""
    imageString=""
    for currentSize in productInfo['sizes']:
        sizeString  =sizeString + currentSize + ","
    sizeString = '"'+sizeString+'"'
    for currentCount in productInfo['counts']:
        countString  =countString + currentCount + ","
    countString = '"'+countString+'"'
    print(countString)
    string = string+","+sizeString
    string = string+","+countString
    for currentImage in productInfo['images']:
        imageString  =imageString + currentImage + ","
    imageString = '"'+imageString+'"'
    string = string+","+'"'+productInfo['images'][4]+'"'
    string = string+","+imageString
    string = string+","+'"'+productInfo['origin']+'"'
    # for currentImage in productInfo['images']:
    #     string = f'{string},"{currentImage}"'
    string = f'{string}\n'
    file.write(string)
    
allProduct = list()

def mainFunc():
    
    printLog(base_url+"페이지로 이동")
    driver.get(base_url) 

    # file = open("./result.csv", 'r', encoding="utf-8-sig")
    # csvreader = csv.reader(file)
    # print(csvreader)
    # for row in csvreader:
    #     print(row)
    #     if(row!=[]):
    #         alreadyLinks.append(row[0])
    # # while(isFindingProduct(alreadyLinks) == False):
    # #     printLog("재등록 상품 찾는중...")

    link = isFindingProduct(alreadyLinks)
    moveToCurrentProductDetailPage(link)


    productInfo = getCurrentProductInfo(link)
    allProduct.append(productInfo )
    # print(productInfo)
    print(alreadyLinks)
    fileSave(productInfo)
    mainFunc()
    
# fileSave(productInfo)

# app = Flask("JobScrapper")

# @app.route("/")
# def home():
#     return render_template("home.html",name="nico")

# @app.route("/search")
# def search():
#     # url=request.args.get("url")
    
#     # base_url = url
#     base_url = "https://www.nike.com/jp/w/mens-lifestyle-shoes-13jrmznik1zy7ok"
#     driver = webdriver.Chrome()# 같은경로라면 드라이버 경로를 안써도 된다.

#     driver.get(base_url)
#     links = driver.find_elements(By.CLASS_NAME,"StickyNode__SimpleSticky-sc-bomsx6-1")
#     for currentLink in links:
#         print(currentLink)
    
#     # return render_template("search.html")

# app.run("127.0.0.1")