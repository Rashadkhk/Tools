import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

login = input("Username Daxil edin: ")
password = input("Shifreni Daxil edin: ")

# Path to your Chromedriver executable
options = Options()
options.add_argument("ignore-certificate-errors")
chromedriver_path = "chromedriver-win64/chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# URL you want to visit
url = "http://lms.adnsu.az/adnsuEducation/login.jsp"

driver.maximize_window()
driver.get(url)

#                                                             LOG IN TO THE SITE

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 
                                                            "username"))).send_keys(login) # Insert Username
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 
                                                            "password"))).send_keys(password) # Insert Password
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, 
                                                            '//*[@class="btn btn-success btn-block btn-lg"]'))).click() # Click Login Button
print('Login Succesfull')

while driver.current_url != "http://lms.adnsu.az/adnsuEducation/index.jsp":
    driver.get("http://lms.adnsu.az/adnsuEducation/index.jsp")

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, 
                                                            '//*[@class="spanClass fa fa-file-text"]'))).click() # Fənn üzrə qruplar

#                                                               OPEN THE SUBJECT 
all_dfs = []  # List to store DataFrames

for subj_id in ["79994", # MikroProsessor
                "79969", # Rəqəmli idarəetmə
                "79973", # Siqnalların emalı
                "79978", # Ingilis Dili
                "80011", # SƏTƏM
                "80016"  # Kontrollerlər
                ]:

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, 
                                                                f'//*[@data-subj_id="{subj_id}"]'))).click() # Fənnə daxil ol
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, 
                                                                '//*[@data-toggle="tab"]//span[text()="Elektron materiallar"]'))).click() # Elektron Materiallar
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, 
                                                                '//*[@data-toggle="tab" and @dataattr="1000017"]'))).click() # Elektron Jurnal
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, 
                                                                '//*[@data-toggle="tab"]//span[text()="Yekun jurnal"]'))).click() # Yekun Jurnal
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, 
                                                                '//*[@class="pull-right"]'))).click() # Show Final Journal
    print('Final Journal Opened')
    time.sleep(5)

    #                                                     COPY THE TABLE DATA TO DATAFRAME
    try:
        element = WebDriverWait(driver, 70).until(EC.presence_of_element_located((By.ID, "resultJournal")))
    except TimeoutException:
        print("Table not found or took too long to load.")
        continue  # Skip to the next subject

    table = driver.find_element(By.ID, "resultJournal")
    rows = table.find_elements(By.TAG_NAME, "tr")

    data = []  # List to store extracted data

    for row in rows[1:]:  # Skip header row
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = []
        for cell in cells:
            try:
                text = cell.text.strip()
            except:
                text = None  # Handle missing values
            row_data.append(text)
        data.append(row_data)

    column_names = [cell.text.strip() for cell in rows[0].find_elements(By.TAG_NAME, "th")]

    df = pd.DataFrame(data, columns=column_names)

    # Handle data types based on column content (e.g., convert numerical values)
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Attempt conversion, replace errors with NaN
            except:
                pass

    # Handle missing values (e.g., impute or drop rows/columns)
    df.bfill(inplace=True)  # Fill missing values forward in each column

    all_dfs.append(df)  # Append DataFrame to the list
    print(df)
    print('Data Copied to DataFrame')

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn-success pull-right"]'))).click() # Fənnlər Siyahısı

# Concatenate all DataFrames into a single DataFrame if there are any DataFrames
if all_dfs:
    final_df = pd.concat(all_dfs)

    # # Write the final DataFrame to an Excel file
    # final_df.to_excel('Rashad.xlsx', index=False)
    # print(final_df)

    # Write the final DataFrame to an Excel file
    final_df.to_excel('Results.xlsx', index=False)
    print(final_df)
    
    print("Data saved successfully to the Excel file!")
else:
    print("No data collected for any subject.")

# Keep the browser window open until user input
input("Press Enter to close the browser window...")

# Close the browser window
driver.quit()
exit()
