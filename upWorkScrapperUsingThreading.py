from selenium import webdriver
import threading
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

file_lock = threading.Lock()

def returnSoup(url, className, max_retries=3):
    service = Service(executable_path=r'C:/Users/Lenovo/Downloads/chromedriver-win64/chromedriver.exe')
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(service=service, options=options)

    for _ in range(max_retries):
        driver.get(url)

        try:
            # Wait for the products to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, className)))
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            driver.quit()
            return soup
        except Exception as e:
            print(f"Error loading the page: {url}")
            time.sleep(5)  # Wait for a while before retrying

    print(f"Failed to load the page after {max_retries} retries: {url}")
    return None



def findData(soup):
    data_list = {
        'Name': [],
        'Title': [],
        'JobSuccess': [],
        'PerHourCharges': [],
        'Offers consultations': [],
        'Location': [],
        'Earnings': [],
        'Ratings': []
    }
    
    card = soup.find_all('div', class_='up-card-section up-card-hover')
    for i in range(len(card)):
        name = card[i].find('div', class_='identity-name')
        title = card[i].find('p', class_='my-0 freelancer-title')
        perHourCharge = card[i].find('strong', {'data-v-afba2f9e': True})
        consultaions = card[i].find('div', class_='up-skill-badge up-badge up-badge-highlight up-badge-rounded-inverse')
        rating = card[i].find('span', class_='up-badge up-badge-tagline top-rated-badge-status')
        job_Success = card[i].find('span', class_='up-job-success-text')
        location = card[i].find('span', class_='d-inline-block vertical-align-middle')
        earning = card[i].find('span', {'data-v-afba2f9e': True, 'data-test': 'earned-amount-formatted'})

        # Initialize location_text, and other variables
        location_text = 'N/A'

        # Extract the data without double quotes
        name_text = ' '.join(name.text.split()) if name else 'N/A'
        title_text = ' '.join(title.text.split()) if title else 'N/A'
        job_success_text = ' '.join(job_Success.text.split()) if job_Success else 'N/A'
        per_hour_charge_text = ' '.join(perHourCharge.text.split()) if perHourCharge else 'N/A'
        if location:
            location_text = ' '.join(location.text.split())
        earning_text = ' '.join(earning.text.split()) if earning else 'N/A'
        rating_text = ' '.join(rating.text.split()) if rating else 'N/A'
        consultation_text = 'Offers consultations' if consultaions else 'N/A'

        data_list['Name'].append(name_text)
        data_list['Title'].append(title_text)
        data_list['JobSuccess'].append(job_success_text)
        data_list['PerHourCharges'].append(per_hour_charge_text)
        data_list['Location'].append(location_text)
        data_list['Earnings'].append(earning_text)
        data_list['Ratings'].append(rating_text)
        data_list['Offers consultations'].append(consultation_text)

    df = pd.DataFrame(data_list)
    return df



def scrape_page(page_number, end):
    # Change the URL
    start = page_number
    while page_number <= end:
        url = f"https://www.upwork.com/search/profiles/?page={page_number}&q=seo"
        className = 'row'
        soup = returnSoup(url, className)
        if soup is None:
            print (f"Skipping page {page_number}")
            page_number +=1
            continue
        df = findData(soup)
        print("Current page: ", page_number)
        with file_lock:
            df.to_csv(f'upwork_3data{start}-{end}.csv', index=False, mode='a', header=False)
        page_number += 1

# ...

if __name__ == '__main__':
    t1 = threading.Thread(target=scrape_page, args=(995, 1000))
    t2 = threading.Thread(target=scrape_page, args=(251, 500))

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()

    t1.join()
    t2.join()

#change the driver path on the top function
#also change the csv file name for every url to ignore the data lose in case of any issue
# https://www.upwork.com/search/profiles/?page={page_number}&q=software%20developer
# https://www.upwork.com/search/profiles/?page={page_number}&q=seo

