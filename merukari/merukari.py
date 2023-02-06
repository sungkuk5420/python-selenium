import customModule

def mainFunc():

    customModule.printLog("재등록 상품 검색 시작")
    titles = list() # test
    while(customModule.isFindingProduct(titles) == False):
        customModule.printLog("재등록 상품 찾는중...")



    customModule.moveListPageForSelling()
    while(customModule.waitToLoadingListPageForSelling()):
        customModule.printLog("출품 리스트 페이지 로딩중...")

    while(customModule.allProductLoading()): #product
        customModule.printLog("출품중 상품 모두 불러오는중") #product

        
    customModule.printLog("출품중 상품 전체 로딩 완료")
    titles = customModule.getAllProductTitles() #product

    if(customModule.isFindingProduct(titles) == False):
        customModule.printLog("등록할 상품이 없습니다 모든 상품이 등록중입니다.")
        titles = list() # test
        while(customModule.isFindingProduct(titles) == False):
            customModule.printLog("재등록 상품 찾는중...")
        customModule.printLog("새로운 미등록 상품을 찾았습니다")
        mainFunc()
    else:
        customModule.moveToCurrentProductDetailPage(customModule.isFindingProduct(titles)) # 해당 상품 페이지 이동
        mainFunc()

# ============================================ main method ========================================

# while(customModule.waitToLoadingLoginPage()):
#     customModule.printLog("로그인 페이지 로딩중...")
# customModule.login()
# while(customModule.waitToPhoneAuthentication()):
#     customModule.printLog("휴대폰 인증 대기중...")

# customModule.printLog("휴대폰 인증 완료")
mainFunc()


