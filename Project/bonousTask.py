from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def initialize_driver():
    driver_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

def returnSoup(url, className, driver, max_retries=3):
    print("Return Soup page...")
    for _ in range(max_retries):
        driver.get(url)
        try:
            # Wait for the products to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, className)))
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            return soup
        except Exception as e:
            return f"Error loading the page: {url}\nError details: {str(e)}"
    return f"Failed to load the page after {max_retries} retries: {url}"

def findData(soup, classList, tagList):
    print("Find Data page...")
    data_list = {
        'ATR1': [],
        'ATR2': [],
        'ATR3': [],
        'ATR4': [],
    }
    
    atr1 = soup.find_all(tagList[0], class_=classList[0])
    atr2 = soup.find_all(tagList[1], class_=classList[1])
    atr3 = soup.find_all(tagList[2], class_=classList[2])
    atr4 = soup.find_all(tagList[3], class_=classList[3])

    maxLength = max(len(atr1), len(atr2), len(atr3), len(atr4))

    for i in range(maxLength):
        if len(atr1) < maxLength:
            atr1.append('N/A')
        if len(atr2) < maxLength:
            atr2.append('N/A')
        if len(atr3) < maxLength:
            atr3.append('N/A')
        if len(atr4) < maxLength:
            atr4.append('N/A')

    for i in range(maxLength):
        atr1_value = atr1[i]
        atr2_value = atr2[i]
        atr3_value = atr3[i]
        atr4_value = atr4[i]

        if isinstance(atr1_value, str):
            atr1_value = ' '.join(atr1_value.split())
        else:
            atr1_value = ' '.join(atr1_value.text.split()) if atr1_value else 'N/A'

        if isinstance(atr2_value, str):
            atr2_value = ' '.join(atr2_value.split())
        else:
            atr2_value = ' '.join(atr2_value.text.split()) if atr2_value else 'N/A'

        if isinstance(atr3_value, str):
            atr3_value = ' '.join(atr3_value.split())
        else:
            atr3_value = ' '.join(atr3_value.text.split()) if atr3_value else 'N/A'

        if isinstance(atr4_value, str):
            atr4_value = ' '.join(atr4_value.split())
        else:
            atr4_value = ' '.join(atr4_value.text.split()) if atr4_value else 'N/A'


        data_list['ATR1'].append(atr1_value)
        data_list['ATR2'].append(atr2_value)
        data_list['ATR3'].append(atr3_value)
        data_list['ATR4'].append(atr4_value)

    df = pd.DataFrame(data_list)
    return df

def scrape_page(URL, classList, tagList):
    print("Scraping page...")
    url = URL
    className = 'row'
    driver = initialize_driver() 
    result = returnSoup(url, className, driver)
    if isinstance(result, str):
        return result  # Return error message
    soup = result  # Continue with the BeautifulSoup object
    df = findData(soup, classList, tagList)
    df.to_csv('./ExtractedData/data.csv', mode='w', index=False, header=False)
    driver.quit()

def main(c1,c2,c3,c4, t1,t2,t3,t4, url):

    try:
        print("Scraping started...")
        classList = [c1, c2, c3, c4]
        tagList = [t1, t2, t3, t4]

        if not url.startswith('https://'):
            url = 'https://' + url

        url = url

        result = scrape_page(url, classList, tagList)
        if isinstance(result, str):
            print("Error incountered: ",result)  # Print error message
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    

# if __name__ == '__main__':
#     classList = ['personalized-header', '_2iOdmoZ', 'rating-count-number']
#     tagList = ['div', 'span', 'span']
#     url = 'https://www.fiverr.com/'

#     result = scrape_page(url, classList, tagList)
#     if isinstance(result, str):
#         print("Error incountered: ",result)  # Print error message
