from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import googletrans
from googletrans import Translator
from selenium.webdriver.chrome.options import Options
import csv
import random

# python.exe -m pip install --upgrade pip
# pip install googletrans==3.1.0a0
#pip install httpx==0.19.0

base_url = "https://kream.co.kr/brands/Human%20Made?quick&immediate_delivery_only" # 신발
options = Options()

user_data = r"C:\Users\pc\AppData\Local\Google\Chrome\User Data"
options.add_argument(f"user-data-dir={user_data}")
options.add_argument("--profile-directory=Default")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지
driver = webdriver.Chrome(options=options)# 같은경로라면 드라이버 경로를 안써도 된다.
def printLog(logMessage):
    print("==================================")
    print(logMessage)

def waitProductListPageLoading():
    detailPage = driver.page_source.find('search_content')
    if detailPage != -1:
        return False
    else:
        return True

def isFindingProduct(alreadyLinks,proceed):
    while(waitProductListPageLoading()): #product
        printLog("상품 리스트 페이지 로딩중...") #product
    printLog("리스트 페이지 로딩완료") #product
    FoundItem = None
    links = driver.find_elements(By.CLASS_NAME,"item_inner")
    for currentLinkTag in links:
        # transactionCount = currentLinkTag.find_element(By.CLASS_NAME,"status_value").get_attribute("textContent").replace("거래 ", "")
        transactionCount = ''
        currentLinkText = currentLinkTag.get_attribute("href")
        currentIndex = alreadyLinks.index(currentLinkText) if currentLinkText in alreadyLinks else -1
        if(currentIndex == -1):
            print("상품 발견: " + currentLinkText + "//")
            FoundItem = currentLinkText
            break
        else:
            print("이미 등록된상품입니다!!")
            print(currentLinkText)
        
    if (FoundItem != None):
        return [FoundItem,transactionCount]
    else:
        return False
    

def waitProductDetailPageLoading():
    detailPage = driver.page_source.find('column_bind')
    if detailPage != -1 :
        return False
    else:
        return True
    
def moveToCurrentProductDetailPage(currentLinkText):
    driver.get(currentLinkText)
    time.sleep(1)
    while(waitProductDetailPageLoading()): #product
        printLog("상품 상세 페이지 로딩중...") #product
    printLog("상세 페이지 로딩완료") #product

allProduct = list()
def getCurrentProductInfo(link,transactionCount):
    allSizeData = list()
    root  = driver.find_element(By.CLASS_NAME,"column_bind")

    addProductInfo(root,link,transactionCount,allSizeData)
    allSizeButtonCheck = driver.page_source.find('product_figure_wrap')
    if allSizeButtonCheck != -1 : # 있으면 
        allSizeButton  = root.find_element(By.CLASS_NAME,"product_figure_wrap") # 모든 사이즈 버튼 누르기
        allSizeButton.click()
        time.sleep(1)

        allSizeLinks = driver.find_elements(By.CLASS_NAME,"select_item")
        print(allSizeLinks)
        index = 1
        for currentLink in allSizeLinks:
            allSizeLinksTemp = driver.find_element(By.CLASS_NAME,"select_list")
            trueCurrentLink = allSizeLinksTemp.find_element(By.XPATH,"(//li[@class='select_item'])["+str(index)+"]");
            trueCurrentLink.click()
            index = index+1
            addProductInfo(root,link,transactionCount,allSizeData)
            time.sleep(1)
            if(len(allSizeLinks) == index):
                addProductInfo(root,link,transactionCount,allSizeData)
                break
            allSizeButton.click()
            time.sleep(1)


    return allSizeData
def addProductInfo(root,link,transactionCount,allSizeData):
    brand  = root.find_element(By.CLASS_NAME,"brand-shortcut").find_element(By.CLASS_NAME,"title-text")
    brandText  = brand.get_attribute("textContent")
    date  = root.find_element(By.CLASS_NAME,"detail-product-container").find_element(By.XPATH,"(//div[@class='detail-box'])[3]").find_element(By.CLASS_NAME,"product_info")
    dateText  = date.get_attribute("textContent")
    productNumber  = root.find_element(By.CLASS_NAME,"detail-product-container").find_element(By.XPATH,"(//div[@class='detail-box'])[2]").find_element(By.CLASS_NAME,"product_info")
    productNumberText  = productNumber.get_attribute("textContent")
    color  = root.find_element(By.CLASS_NAME,"detail-product-container").find_element(By.XPATH,"(//div[@class='detail-box'])[4]").find_element(By.CLASS_NAME,"product_info")
    colorText  = color.get_attribute("textContent")
    title  = root.find_element(By.CLASS_NAME,"title")
    titleText  = title.get_attribute("textContent")
    subTitle  = root.find_element(By.CLASS_NAME,"sub-title")
    subTitleText  = subTitle.get_attribute("textContent")
    buyPrice  = root.find_element(By.XPATH,"(//button[@class='btn_action'])[1]").find_element(By.CLASS_NAME,"amount")
    buyPriceText  = buyPrice.get_attribute("textContent").replace(",","").replace("원","")
    sellPrice  = root.find_element(By.XPATH,"(//button[@class='btn_action'])[2]").find_element(By.CLASS_NAME,"amount")
    sellPriceText  = sellPrice.get_attribute("textContent").replace(",","").replace("원","")
    koreaPrice  = root.find_element(By.CLASS_NAME,"detail-product-container").find_element(By.XPATH,"(//div[@class='detail-box'])[1]").find_element(By.CLASS_NAME,"product_info")
    koreaPriceText  = koreaPrice.get_attribute("textContent")
    print(koreaPriceText)
    
    premium = "-"
    if(koreaPriceText.find("-") == -1):
        if(koreaPriceText.find("약") != -1):
            koreaPriceIndex = koreaPriceText.index("약")
            koreaPriceText = koreaPriceText[koreaPriceIndex:len(koreaPriceText)].replace("약","").replace("원","").replace(")","").replace(",","")
        else:
            koreaPriceText = koreaPriceText.replace("약","").replace("원","").replace(")","").replace(",","")
        
        if(sellPriceText.find("-") == -1):
            premium = ((int(sellPriceText)/int(koreaPriceText))-1 )*100
    
    allSizeButtonCheck = driver.page_source.find('product_figure_wrap')
    if allSizeButtonCheck != -1 : # 있으면 
        allSizeButton  = root.find_element(By.CLASS_NAME,"product_figure_wrap") # 모든 사이즈 버튼 누르기
        size  = allSizeButton.find_element(By.CLASS_NAME,"title")
        sizeText  = size.get_attribute("textContent")
    else:
        sizeText = '-'
    
    productInfo = {
        "link": link,
        "brand": brandText,
        "date": dateText,
        "title": titleText,
        "subTitle": subTitleText,
        "productNumber": productNumberText,
        "color": colorText,
        "size": sizeText,
        "buyPrice": buyPriceText,
        "sellPrice": sellPriceText,
        "transactionCount": transactionCount,
        "koreaPriceText": koreaPriceText,
        "premium": premium,
    }
    
    allSizeData.append(productInfo)

def fileSave(productInfo):
    print(productInfo)
    file = open("result.csv", "a", encoding="utf-8-sig")
    # string = f"{productInfo['productCode']},{productInfo['title']},{productInfo['subTitle']},{productInfo['price']},{productInfo['sizes']},{productInfo['images']}"
    string = f'{productInfo["link"]},{productInfo["brand"]},{productInfo["date"]},{productInfo["title"]},{productInfo["subTitle"]},{productInfo["productNumber"]},{productInfo["color"]},{productInfo["size"]},{productInfo["buyPrice"]},{productInfo["sellPrice"]},{productInfo["transactionCount"]},{productInfo["koreaPriceText"]},{productInfo["premium"]}'
    # for currentImage in productInfo['images']:
    #     string = f'{string},"{currentImage}"'
    string = f'{string}\n'
    file.write(string)

alreadyLinks = list()
def mainFunc():
    scrollPosition = 0
    printLog(base_url+"페이지로 이동")
    driver.get(base_url) 
    
    file = open("./result.csv", 'r', encoding="utf-8-sig")
    csvreader = csv.reader(file)
    for row in csvreader:
        print(row)
        if(row!=[]):
            alreadyLinks.append(row[0])

    while(isFindingProduct(alreadyLinks,False) == False):
        printLog("재등록 상품 찾는중...")
        scrollPosition= scrollPosition+4000
        driver.execute_script("window.scrollTo(0, "+str(scrollPosition)+")") 
        time.sleep(1)
    result = isFindingProduct(alreadyLinks,True)
    link = result[0]
    transactionCount = result[1]
    moveToCurrentProductDetailPage(link)
    
    productInfo = getCurrentProductInfo(link,transactionCount)
    for row in productInfo:
        allProduct.append(row)
        fileSave(row)
        print(row)
    mainFunc()

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