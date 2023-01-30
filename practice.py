from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()# 같은경로라면 드라이버 경로를 안써도 된다.
browser.get("http://naver.com")

# find_element(By.ID, "id")
# find_element(By.NAME, "name")
# find_element(By.XPATH, "xpath")
# find_element(By.LINK_TEXT, "link text")
# find_element(By.PARTIAL_LINK_TEXT, "partial link text")
# find_element(By.TAG_NAME, "tag name")
# find_element(By.CLASS_NAME, "class name")
# find_element(By.CSS_SELECTOR, "css selector")

element = browser.find_element(By.CLASS_NAME, "link_login")
element.click()
browser.back()
searchElement = browser.find_element(By.ID, "query")
searchElement.send_keys("나도코딩")
searchElement.send_keys(Keys.ENTER)
# browser.find_elements(By.TAG_NAME,"a")  


# browser.forward()
# browser.refresh()