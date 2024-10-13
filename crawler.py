from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm 
import numpy as np 

# Đường dẫn tới ChromeDriver
chrome_driver_path = '/usr/local/bin/chromedriver'

# Tạo instance của WebDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

base_url = 'https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-tp-hcm'

def send_request(start_page, end_page):

    date_frames = []

    for page in range(start_page, end_page + 1): 
        url = f"{base_url}/p{page}" 
        driver.get(url)
        links = driver.find_elements(By.CSS_SELECTOR, 'a.js__product-link-for-product-id')
        urls = [link.get_attribute('href') for link in links]
    #Tạo danh sách để đẩy vào csv
        property_list = []

        for url in tqdm(urls):
            driver.get(url)  # Mở link chi tiết
            # Lấy tiêu đề
            items = driver.find_elements(By.CSS_SELECTOR, 'div.re__pr-short-info-item.js__pr-config-item')

            title, date = None, None

            for item in items: 
                title_element = item.find_element(By.CLASS_NAME, 'title')
                if title_element.text.strip() == "Mã tin":
                    # If title is "Mã tin", get the corresponding value
                    value_element = item.find_element(By.CLASS_NAME, 'value')
                    title = value_element.text.strip()
                elif title_element.text.strip() == "Ngày đăng": 
                    value_element = item.find_element(By.CLASS_NAME, 'value')
                    date = value_element.text.strip()
                if title and date: break 


            # Lấy địa chỉ
            address = driver.find_element(By.CSS_SELECTOR, 'span.re__pr-short-description.js__pr-address').text.strip()

            #Lấy mức giá, nội thất, diện tích
            property_details = {
                "Mức giá": np.nan,
                "Diện tích": np.nan,
                "Nội thất":"Không",
                "Số toilet": np.nan,
                "Số phòng ngủ": np.nan 
            }

            specs = driver.find_elements(By.CSS_SELECTOR, 'div.re__pr-specs-content-item')
            for spec in specs:
                title_ele = spec.find_element(By.CSS_SELECTOR, 'span.re__pr-specs-content-item-title').text.strip()
                if title_ele in ("Mức giá","Diện tích", "Số toilet", "Số phòng ngủ"):
                    value = spec.find_element(By.CSS_SELECTOR, 'span.re__pr-specs-content-item-value').text.strip()
                    value = float(value.split(' ')[0].replace(',', '.'))
                    property_details[title_ele] = value
                if title_ele == "Nội thất":
                    value = spec.find_element(By.CSS_SELECTOR, 'span.re__pr-specs-content-item-value').text.strip()
                    property_details[title_ele] = value

            property_info = {
                'ID': title,
                'Địa chỉ': address,
                'Ngày đăng tin': date
            }
            property_info.update(property_details)
            property_info.update({"Link" : url})
            property_list.append(property_info)

        # Tạo DataFrame từ danh sách thông tin bất động sản
        df = pd.DataFrame(property_list)

        # Xuất DataFrame ra file csv
        date_frames.append(df)
    
        print(f"Done: {base_url}/p{page}")

    combined_data = pd.concat(date_frames, ignore_index=True)
    column_order = ['ID', 'Địa chỉ', 'Diện tích', 'Số phòng ngủ', 'Số toilet', 'Nội thất', 
                    'Mức giá', 'Link', 'Ngày đăng tin']
    combined_data = combined_data[column_order]
    combined_data.to_csv('DSPhongTro.csv', index=False, encoding='utf-8-sig', header=True, sep='\t')
    driver.quit()
