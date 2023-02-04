from flask import Flask,render_template,request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import googletrans
from googletrans import Translator
base_url = "https://www.nike.com/jp/w/mens-lifestyle-shoes-13jrmznik1zy7ok"
driver = webdriver.Chrome()# 같은경로라면 드라이버 경로를 안써도 된다.

alreadyLinks = list()
productCode = ""

def printLog(logMessage):
    print("==================================")
    print(logMessage)

async def getInfo(links):
    for currentLinkTag in links:
        currentLink = currentLinkTag.get_attribute("href")
        print(currentLink)
        await driver.get(currentLink)
        await time.sleep(2)
        await driver.back()


def isFindingProduct(alreadyLinks):
    printLog(base_url+"페이지로 이동")
    driver.get(base_url) 
    FoundItem = None
    # print(listItems)
    links = driver.find_elements(By.CLASS_NAME,"product-card__img-link-overlay")
    for currentLinkTag in links:
        currentLinkText = currentLinkTag.get_attribute("href")
        printLog(currentLinkText)
        currentIndex = alreadyLinks.index(currentLinkText) if currentLinkText in alreadyLinks else -1
        if(currentIndex == -1):
            print("상품 발견: " + currentLinkText + "//")
            FoundItem = currentLinkTag
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

def moveToCurrentProductDetailPage(currentProduct):
    currentProduct.click()
    time.sleep(3)
    while(waitProductDetailPageLoading()): #product
        printLog("상품 상세 페이지 로딩중...") #product
    printLog("상세 페이지 로딩완료") #product


def getCurrentProductInfo():
    time.sleep(2)

    root  = driver.find_element(By.CLASS_NAME,"css-mso6zd")
    title  = root.find_element(By.ID,"pdp_product_title")
    titleText  = title.get_attribute("textContent")
    subTitle  = root.find_element(By.XPATH,"//h2[@data-test='product-sub-title']")
    subTitleText  = subTitle.get_attribute("textContent")
    translator = Translator(service_urls=['translate.googleapis.com'])
    titleText =  translator.translate(titleText, dest='ko').text
    subTitleText =  translator.translate(subTitleText, dest='ko').text
    price  = root.find_element(By.XPATH,"//div[@data-test='product-price']")
    priceText  = price.get_attribute("textContent")
    sizes = list()
    images = list()
    sizeTagsParent  = root.find_element(By.CLASS_NAME,"css-12whm6j").find_elements(By.TAG_NAME,"div")
    for currentTag in sizeTagsParent:
        sizeInput = currentTag.find_element(By.TAG_NAME,"input")
        if(sizeInput.get_attribute("disabled") == None):
            sizeText = currentTag.find_element(By.TAG_NAME,"label").get_attribute("textContent")
            sizeText=sizeText.replace("[","").replace("'","").replace("JP","")
            if(sizeText.find(".")!=-1):
                sizeText=sizeText.replace(".","")
            else:
                sizeText=sizeText.replace(" (US 5)","").replace(" (US 6)","")+"0"
            sizes.append(sizeText)
    productCode = driver.find_element(By.CLASS_NAME,"description-preview__style-color").get_attribute("textContent").replace("スタイル： ", "")            
    # imageTags  = driver.find_element(By.CLASS_NAME,"css-1rayx7p").find_elements(By.TAG_NAME,"img")
    imageTags  = driver.find_element(By.CLASS_NAME,"css-1rayx7p").find_elements(By.XPATH,"//*[@data-sub-type='image']")
    index = 1
    for currentTag in imageTags:
        imageText = currentTag.find_elements(By.TAG_NAME,"picture")[1].find_element(By.TAG_NAME,"img").get_attribute("src")
        if(index ==5):
            urllib.request.urlretrieve(imageText, productCode  +".png")
        images.append(imageText)
        index = index +1

    productInfo = {
        "productCode": productCode,
        "title": titleText,
        "subTitle": subTitleText,
        "price": priceText,
        "sizes": sizes,
        "images": images,
    }
    return productInfo

def fileSave(productInfo):
    print(productInfo)
    file = open("result.csv", "w", encoding="utf-8-sig")
    # string = f"{productInfo['productCode']},{productInfo['title']},{productInfo['subTitle']},{productInfo['price']},{productInfo['sizes']},{productInfo['images']}"
    string = f"{productInfo['productCode']},{productInfo['title']},{productInfo['subTitle']},{productInfo['price']}"
    for currentSize in productInfo['sizes']:
        string = string+","+currentSize
    for currentImage in productInfo['images']:
        string = f"{string},{currentImage}"
    file.write(string)

while(isFindingProduct(alreadyLinks) == False):
    printLog("재등록 상품 찾는중...")

moveToCurrentProductDetailPage(isFindingProduct(alreadyLinks))


productInfo = getCurrentProductInfo()
fileSave(productInfo)

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