from flask import Flask,render_template,request
import time
import urllib.request
import googletrans
from googletrans import Translator
import csv
from requests import get
from bs4 import BeautifulSoup

base_url = "https://www.nike.com/jp/w/mens-lifestyle-shoes-13jrmznik1zy7ok"
alreadyLinks = list()
productCode = ""
response = get(base_url)

def printLog(logMessage):
    print("==================================")
    print(logMessage)

def isFindingProduct(alreadyLinks):
    FoundItem = None
    # print(listItems)
    soup = BeautifulSoup(response.text,"html.parser")
    links = soup.find_all("a",class_="product-card__img-link-overlay")
    for currentLinkTag in links:
        currentLinkText = currentLinkTag['href']
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
        

def getCurrentProductInfo(link):
    response = get(link)
    if(response.status_code != 200):
        print('getCurrentProductInfo 응답 없음 ')
    else:
        time.sleep(5)
        soup = BeautifulSoup(response.text,"html.parser")
        root  =  soup.find_all("div",class_="css-mso6zd")
        title  =  soup.find("h1",{"id":"pdp_product_title"})
        titleText  = title.getText()
        subTitle  =  soup.find("h2",{"data-test":"product-sub-title"})
        subTitleText  = subTitle.getText()
        translator = Translator(service_urls=['translate.googleapis.com'])
        titleText =  translator.translate(titleText, dest='ko').text
        subTitleText =  translator.translate(subTitleText, dest='ko').text
        price  =  soup.find("div",{"data-test":"product-price"})
        priceText  = price.getText().replace("￥","")
        sizes = list()
        counts= list()
        images = list()
        print(soup)
        print(soup.find("div",class_="css-12whm6j"))
        if(soup.find("div",{"class":"mt2-sm css-12whm6j"}) != []):
            sizeTagsParent  = soup.find("div",{"class":"mt2-sm css-12whm6j"}).find_all("div")
        if(soup.find("div",{"class":"css-1j3x2vp"}) != []):
            sizeTagsParent  = soup.find("div",{"class":"css-1j3x2vp"}).find_all("div")
        print(sizeTagsParent)
        for currentTag in sizeTagsParent:
            sizeInput = currentTag.find_element(By.TAG_NAME,"input")          
            sizeText = currentTag.find_element(By.TAG_NAME,"label").getText()
            sizeText=sizeText.replace("[","").replace("'","").replace("JP","")
            if(sizeText.find(".")!=-1):
                sizeText=sizeText.replace(".","")
            else:
                sizeText=sizeText.replace(" ","").replace("(US5)","").replace("(US6)","")+"0"
            sizeText=sizeText.replace(" ","").replace("(US5)","").replace("(US6)","")
            sizeText = sizeText.replace(" ","")
            print(sizeText)
            if(sizeInput.get_attribute("disabled") == None):
                sizes.append(sizeText)
                counts.append("5")
            else:
                sizes.append(sizeText)
                counts.append("0")
        productCode = driver.find_element(By.CLASS_NAME,"description-preview__style-color").getText().replace("スタイル： ", "")            
        origin = driver.find_element(By.CLASS_NAME,"description-preview__origin").getText()
        # imageTags  = driver.find_element(By.CLASS_NAME,"css-1rayx7p").find_elements(By.TAG_NAME,"img")
        imageTags  = driver.find_element(By.CLASS_NAME,"css-1rayx7p").find_elements(By.XPATH,"//*[@data-sub-type='image']")
        index = 1
        for currentTag in imageTags:
            imageText = currentTag.find_elements(By.TAG_NAME,"picture")[1].find_element(By.TAG_NAME,"img").get_attribute("src")
            if(index ==5):
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
    string = string+","+productInfo['origin']
    # for currentImage in productInfo['images']:
    #     string = f'{string},"{currentImage}"'
    string = f'{string}\n'
    file.write(string)
    
allProduct = list()
def mainFunc():
    
    printLog(base_url+"페이지로 이동")
    if(response.status_code != 200):
        print('응답 없음 ')
    else:
        while(isFindingProduct(alreadyLinks) == False):
            printLog("재등록 상품 찾는중...")
        link = isFindingProduct(alreadyLinks)
        productInfo = getCurrentProductInfo(link)
        allProduct.append(productInfo )


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