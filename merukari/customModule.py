from ast import IsNot
from asyncio.windows_events import NULL
from outcome import AlreadyUsedError
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from seleniumwire import webdriver 
from pyshadow.main import Shadow
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import time
import os
from mimetypes import guess_extension
import datetime
import urllib.request

#pip uninstall httpcore
#pip uninstall h11

#pip install httpcore
#pip install h11
# Download content to temp folder
asset_dir = "images"

options = Options()

# user_data = r"C:\Users\frees\AppData\Local\Google\Chrome\User Data"
# options.add_argument(f"user-data-dir={user_data}")
# options.add_argument("--profile-directory=Profile 3")

user_data = r"C:\Users\pc\AppData\Local\Google\Chrome\User Data"
options.add_argument(f"user-data-dir={user_data}")
options.add_argument("--profile-directory=Default")

options.add_experimental_option("detach", True)  # 화면이 꺼지지 않고 유지

# options.add_argument("--start-maximized")  # 최대 크기로 시작

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
selling_products_url = 'https://jp.mercari.com/mypage/listings' # 출품중
torihiki_url = 'https://jp.mercari.com/mypage/listings/in_progress' # 토리히키중
# driver.get(torihiki_url)
shadow = Shadow(driver)
action = ActionChains(driver)
# email = 'sungkuk5420@gmail.com' #메루카리 아이디
# passwd = 'a1223334444' #메루카리 비밀번호
alreadyDownloadImages = list()
''

email = 'uponthisrock.utr@gmail.com' #메루카리 아이디
passwd = 'a1223334444' #메루카리 비밀번호
def expandShadowElement(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root
    
def printLog(logMessage):
    print("==================================")
    print(logMessage)

def login():
    mail_login_button = driver.find_element(By.CLASS_NAME, "style_loginButton__nsWU0") #loginButoon class
    if mail_login_button:
        mail_login_button.click()
    time.sleep(2)
    email_form = driver.find_element(By.CLASS_NAME, "sc-bYMpWt").find_element(By.XPATH, "//input[@type='email']")

    if email_form:
        email_form.click()
        email_form.send_keys(email)
    passwd_form = driver.find_element(By.CLASS_NAME, "sc-bYMpWt").find_element(By.XPATH, "//input[@type='password']")

    if passwd_form:
        passwd_form.click()
        passwd_form.send_keys(passwd)
        
        
    time.sleep(1)
    login_button = driver.find_element(By.CLASS_NAME, "sc-bYMpWt").find_element(By.TAG_NAME, "mer-button")
    if login_button:
        login_button.click()


def waitToPhoneAuthentication():
    time.sleep(3)
    allSource = driver.page_source.find('___gatsby')
    if allSource != -1:
        return False
    else:
        return True

def waitToLoadingLoginPage(): #login
    time.sleep(1)
    loginbutton = driver.page_source.find('<mer-button class="style_loginButton__nsWU0')  #loginButoon class
    if loginbutton != -1:
        return False
    else:
        return True

def moveListPageForSelling(): #출품중
    driver.get(selling_products_url)
def waitToLoadingListPageForSelling(): #출품중
    time.sleep(1)
    loadingProducts = driver.page_source.find('id="my-page-main-content"')
    if loadingProducts != -1:
        return False
    else:
        return True

def waitToLoadingListPage(): # 토리히키
    time.sleep(1)
    loadingProducts = driver.page_source.find('id="inTransaction"')
    if loadingProducts != -1:
        return False
    else:
        return True

def allProductLoading(): # 출품중상품 모두 더보기 처리
    time.sleep(2)
    moreButtonText = driver.page_source.find('LoadMoreButton__StyledButton-sc-ua1bnc-0')
    if moreButtonText != -1:
        moreButton = driver.find_element(By.CLASS_NAME,"LoadMoreButton__StyledButton-sc-ua1bnc-0")
        moreButton.click()
        time.sleep(1)
        return True
    else:
        return False

def getAllProductTitles():
    time.sleep(2)
    titles = list()
    titleDoms = shadow.find_elements(driver.find_element(By.ID,"my-page-main-content"), ".item-label")

    for currentItem in titleDoms:
        print(currentItem.text)
        titles.append(currentItem.text)
    return titles

def moveToTorihiki():
    printLog("토리히키 페이지로 이동")
    driver.get(torihiki_url) 
    time.sleep(2)

def isFindingProduct(titles):
    
    moveToTorihiki()
    while(waitToLoadingListPageForSelling()):
        printLog("출품 리스트 페이지 로딩중...")
    time.sleep(2)
    listItems = shadow.find_elements(driver.find_element(By.ID,"my-page-main-content"), ".container")
    FoundItem = None
    # print(listItems)
    for currentItem in listItems:
        statusText = currentItem.find_element(By.CLASS_NAME,"information-label").text
        print(statusText)
        if (statusText == "発送待ち") or (statusText == "支払待ち") or (statusText == "公開停止中")or (statusText == "公開停止中")or (statusText == "評価待ち"): 
            titleText = currentItem.find_element(By.CLASS_NAME,"item-label").text
            print("상품 발견: " + statusText + "//" + titleText)
            # titleText = "9816 ルビス クレンジングリキッド 本体 クレンジング料 150mL"
            if(statusText == "評価待ち"):
                FoundItem = currentItem
            else:
                currentIndex = titles.index(titleText) if titleText in titles else -1
                if(currentIndex == -1):
                    FoundItem = currentItem
                    break
                else:
                    print("이미 등록된상품입니다!!")
                    print(titleText)
                    print("상품을 탐색합니다")
    if (FoundItem != None):
        return FoundItem
    else:
        return False

def waitProductDetailPageLoading():
    detailPage = driver.page_source.find('StickyNode__SimpleSticky-sc-bomsx6-1')
    if detailPage != -1:
        return False
    else:
        return True
        
def moveToCurrentProductDetailPage(currentProduct):
    currentProduct.click()
    time.sleep(2)
    while(waitProductDetailPageLoading()): #product
        printLog("상품 상세 페이지 로딩중...") #product
    
    
    commentFormString = driver.page_source.find("name='message'")
    if commentFormString != -1:
        commentForm = driver.find_element(By.XPATH,"//textarea[@name='message']")
        commentForm.send_keys("ありがとうございました。")
        submitButton = driver.find_element(By.XPATH,"//form[@class='mer-spacing-b-16']").find_element(By.TAG_NAME,"mer-button")
        submitButton.click() #product
        time.sleep(1)
        submitButton2 = driver.find_element(By.TAG_NAME,"mer-dialog").find_element(By.XPATH,"//mer-button[@data-testid='dialog-action-button']")
        submitButton2.click() #product
        driver.back()
    else:
        productLink = driver.find_element(By.CLASS_NAME,"StickyNode__SimpleSticky-sc-bomsx6-1").find_element(By.TAG_NAME,"a") # 상품 상세화면가기 전에 토리히키화면에서 왼쪽 사이드 바에서 링크찾기. #product
        productLink.click() #product
        time.sleep(2)
        productInfo = getCurrentProductInfo()
        addProduct(productInfo)

def getCurrentProductInfo():
    time.sleep(2)

    imageNextButtonString = driver.page_source.find('slick-next')
    if imageNextButtonString != -1:
        imageNextButton = driver.find_element(By.CLASS_NAME,"slick-next") # 상품이미지 다운로드 전에 전체 이미지 로딩후 다운로드
        imageNextButton.click()
        time.sleep(2)
    title = shadow.find_element(".heading.page")
    titleText = title.text
    filePaths = list()
    imagesRoot = driver.find_element(By.CLASS_NAME, "slick-list")
    images = imagesRoot.find_elements(By.TAG_NAME, "mer-item-thumbnail")
    index  = 1
    for currentImage in images:
        imgUrl  = currentImage.get_attribute("src")
        urllib.request.urlretrieve(imgUrl, str(index)  +".png")
        filePath =str(index)  +".png"
        print(filePath)
        filePaths.append(filePath)
        index = index+1
    time.sleep(1)
    printLog("제목 : "+titleText)
    price = driver.find_element(By.CLASS_NAME,"Price__StyledItemPrice-sc-1b74han-0")
    priceShadowRoot = expandShadowElement(price)
    print(price)
    priceText = price.get_attribute("value")
    print(priceShadowRoot)
    printLog("가격 : "+priceText)
    description = driver.find_element(By.TAG_NAME, "mer-show-more")
    descriptionChild = description.find_element(By.TAG_NAME,"mer-text")
    # descriptionChildShadowRoot = expandShadowElement(descriptionChild)
    descriptionText = descriptionChild.text
    printLog("상품설명 : "+descriptionText)
    categoryRoot = driver.find_element(By.ID,"item-info")
    allCategory = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.TAG_NAME,"mer-display-row").find_element(By.TAG_NAME,"mer-breadcrumb-list")
    allCategoryTextArray = allCategory.text.split("\n")
    category1 = allCategoryTextArray[0]
    category2 = allCategoryTextArray[1]
    category3 = allCategoryTextArray[2]
    printLog("카테고리 1 : "+category1)
    printLog("카테고리 2 : "+category2)
    printLog("카테고리 3 : "+category3)
    brandParent = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[2]")
    print(brandParent.text)
    
    currentIndex = brandParent.text.index("商品の状態") if "商品の状態" in brandParent.text else -1
    if(currentIndex != -1):
        brandText = NULL
        productState = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[2]")
        printLog("상품 상태 : "+productState.text.split("\n")[1])
        productStateText = productState.text.split("\n")[1]
        payPerson = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[3]")
        printLog("배송료 부담자 : "+payPerson.text.split("\n")[1])
        payPersonText = payPerson.text.split("\n")[1]
        delivery = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[4]")
        printLog("배송방법 : "+delivery.text.split("\n")[1])
        deliveryText = delivery.text.split("\n")[1]
        sendArea = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[5]")
        printLog("발송지 : "+sendArea.text.split("\n")[1])
        sendAreaText = sendArea.text.split("\n")[1]
        sendDay = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[6]")
        printLog("발송기간 : "+sendDay.text.split("\n")[1])
        sendDayText = sendDay.text.split("\n")[1]
    else:
        brand = brandParent.find_element(By.TAG_NAME,"a")
        printLog("브랜드 : "+brand.text)
        brandText = brand.text
        # brandText = NULL
        productState = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[3]")
        printLog("상품 상태 : "+productState.text.split("\n")[1])
        productStateText = productState.text.split("\n")[1]
        payPerson = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[4]")
        printLog("배송료 부담자 : "+payPerson.text.split("\n")[1])
        payPersonText = payPerson.text.split("\n")[1]
        delivery = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[5]")
        printLog("배송방법 : "+delivery.text.split("\n")[1])
        deliveryText = delivery.text.split("\n")[1]
        sendArea = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[6]")
        printLog("발송지 : "+sendArea.text.split("\n")[1])
        sendAreaText = sendArea.text.split("\n")[1]
        sendDay = categoryRoot.find_element(By.CLASS_NAME,"PsUPz").find_element(By.XPATH,"(//mer-display-row)[7]")
        printLog("발송기간 : "+sendDay.text.split("\n")[1])
        sendDayText = sendDay.text.split("\n")[1]
    # print(len(allCategory))
    productInfo = {
        "title": titleText,
        "price": priceText,
        "description": descriptionText,
        "category1": category1,
        "category2": category2,
        "category3": category3,
        "brand": brandText,
        "productState": productStateText,
        "payPerson": payPersonText,
        "delivery": deliveryText,
        "sendArea": sendAreaText,
        "sendDay": sendDayText,
        "filePaths": filePaths,
    }
    return productInfo

def addProduct(productInfo):
    printLog("상품등록 페이지로 이동")
    driver.get("https://jp.mercari.com/sell/create") 
    time.sleep(3)
    mainDOM = driver.page_source.find('id="main"')
    if mainDOM != -1:
        driver.execute_script("""
        var dialog = document.querySelector("mer-dialog")
        if (dialog)
            dialog.parentNode.removeChild(dialog);
        """)

        print(productInfo['delivery'])
        currentButton = driver.find_element(By.TAG_NAME, "mer-text-link").find_element(By.TAG_NAME,"a")
        currentButton.click()
        time.sleep(4)
        if(productInfo['delivery'] == "らくらくメルカリ便"):
            currentButton = driver.find_element(By.TAG_NAME, "mer-radio-group").find_element(By.XPATH,"(//mer-radio-label)[1]")
        elif(productInfo['delivery'] == "ゆうゆうメルカリ便"):
            currentButton = driver.find_element(By.TAG_NAME, "mer-radio-group").find_element(By.XPATH,"(//mer-radio-label)[2]")
        elif(productInfo['delivery'] == "未定"):
            currentButton = driver.find_element(By.TAG_NAME, "mer-radio-group").find_element(By.XPATH,"(//mer-radio-label)[4]")
        elif(productInfo['delivery'] == "クロネコヤマト"):
            currentButton = driver.find_element(By.TAG_NAME, "mer-radio-group").find_element(By.XPATH,"(//mer-radio-label)[8]")
            
        currentButton.click()    
        submitButton = driver.find_element(By.CLASS_NAME, "fpmkAf")
        submitButton.click()
        time.sleep(2)

        photoUploadForm = driver.page_source.find('data-testid="photo-upload"')
        if photoUploadForm != -1:
            fileForm = driver.find_element(By.XPATH,"//input[@type='file']")
            allFilePath = ""
            for filePath in productInfo['filePaths']:

                print(filePath)
                allFilePath += os.getcwd()+"\\"+filePath.replace("/","\\") + " \n "
                printLog("이미지 파일 업로드 완료: " + os.getcwd()+"\\"+filePath.replace("/","\\"))
            if(allFilePath != ""):
                allFilePath = allFilePath[:-1]
                allFilePath = allFilePath[:-1]
                allFilePath = allFilePath[:-1]
                fileForm.send_keys(allFilePath)

            for filePath in productInfo['filePaths']:
                os.remove(os.getcwd()+"\\"+filePath.replace("/","\\"))
                printLog("이미지 파일 삭제 완료: " + os.getcwd()+"\\"+filePath.replace("/","\\"))

        category1 = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='category1']"))
        category1.select_by_visible_text(productInfo['category1'])
        time.sleep(1)
        category2 = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='category2']"))
        category2.select_by_visible_text(productInfo['category2'])
        time.sleep(1)
        category3 = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='category3']"))
        category3.select_by_visible_text(productInfo['category3'])
        time.sleep(1)
        if(productInfo['brand'] != NULL):
            brand = driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//mer-text-input[@label='ブランド']")
            print(brand)
            brand.click()
            brand.send_keys(productInfo['brand'])
            driver.find_element(By.TAG_NAME, "form").find_element(By.TAG_NAME, "mer-action-row").click()
            time.sleep(1)

        productState = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='itemCondition']"))
        productState.select_by_visible_text(productInfo['productState'])
        time.sleep(1)
        title = driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//mer-text-input[@label='商品名']")
        title.click()
        title.send_keys(productInfo['title'])
        time.sleep(1)
        description = driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//mer-textarea[@label='商品の説明']")
        description.click()
        description.send_keys(productInfo['description'])
        time.sleep(1)
        payPerson = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='shippingPayer']"))
        payPerson.select_by_visible_text(productInfo['payPerson'])
        time.sleep(1)

        # delivery = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='shippingMethod']"))
        # delivery.select_by_visible_text(productInfo['delivery'])
        time.sleep(1)
        sendArea = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='shippingFromArea']"))
        sendArea.select_by_visible_text(productInfo['sendArea'])
        time.sleep(1)
        sendDay = Select(driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//select[@name='shippingDuration']"))
        sendDay.select_by_visible_text(productInfo['sendDay'])
        time.sleep(1)
        price = driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//mer-text-input[@label='販売価格']")
        price.click()
        price.send_keys(productInfo['price'])
        time.sleep(1)
        completeButton = driver.find_element(By.TAG_NAME, "form").find_element(By.XPATH, "//button[@type='submit']")
        completeButton.click()
        time.sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)

