#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install requests beautifulsoup4 pandas selenium


# In[2]:


#Q1
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# Step 1: Get the webpage
url = "https://www.shine.com/"
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in the system PATH
driver.get(url)

# Step 2: Enter search criteria and click the search button
job_title = "Data Analyst"
location = "Bangalore"

title_input = driver.find_element_by_id("qp")
location_input = driver.find_element_by_id("ql")
search_button = driver.find_element_by_class_name("srch")
title_input.send_keys(job_title)
location_input.send_keys(location)
search_button.click()

# Give some time for the page to load
time.sleep(5)

# Step 3: Scrape data for the first 10 jobs
soup = BeautifulSoup(driver.page_source, "html.parser")
job_listings = soup.find_all("div", class_="sjs")

data = []
for job in job_listings[:10]:
    job_title = job.find("h2", class_="job_title").text.strip()
    job_location = job.find("span", class_="job_loc").text.strip()
    company_name = job.find("span", class_="job_sname").text.strip()
    experience_required = job.find("li", class_="exp").text.strip()

    data.append({
        "Job Title": job_title,
        "Job Location": job_location,
        "Company Name": company_name,
        "Experience Required": experience_required
    })

# Step 4: Create a DataFrame
df = pd.DataFrame(data)

# Step 5: Display the DataFrame
print(df)

# Close the browser window
driver.quit()


# In[4]:


#Q2
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# Step 1: Get the webpage
url = "https://www.shine.com/"
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in the system PATH
driver.get(url)

# Step 2: Enter search criteria and click the search button
job_title = "Data Scientist"
location = "Bangalore"

title_input = driver.find_element_by_id("qp")
location_input = driver.find_element_by_id("ql")
search_button = driver.find_element_by_class_name("srch")
title_input.send_keys(job_title)
location_input.send_keys(location)
search_button.click()

# Give some time for the page to load
time.sleep(5)

# Step 3: Scrape data for the first 10 jobs
soup = BeautifulSoup(driver.page_source, "html.parser")
job_listings = soup.find_all("div", class_="sjs")

data = []
for job in job_listings[:10]:
    job_title = job.find("h2", class_="job_title").text.strip()
    job_location = job.find("span", class_="job_loc").text.strip()
    company_name = job.find("span", class_="job_sname").text.strip()

    data.append({
        "Job Title": job_title,
        "Job Location": job_location,
        "Company Name": company_name,
    })

# Step 4: Create a DataFrame
df = pd.DataFrame(data)

# Step 5: Display the DataFrame
print(df)

# Close the browser window
driver.quit()


# In[5]:


#Q3
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = "https://www.shine.com/"
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in the system PATH
driver.get(url)

job_title = "Data Scientist"

title_input = driver.find_element(By.ID, "qp")
search_button = driver.find_element(By.CLASS_NAME, "srch")
title_input.send_keys(job_title)
search_button.click()

time.sleep(5)

location_filter = driver.find_element(By.XPATH, "//label[@for='location_121']")
salary_filter = driver.find_element(By.XPATH, "//label[@for='sal_3-6']")

location_filter.click()
salary_filter.click()

time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
job_listings = soup.find_all("div", class_="sjs")

data = []
for job in job_listings[:10]:
    job_title = job.find("h2", class_="job_title").text.strip()
    job_location = job.find("span", class_="job_loc").text.strip()
    company_name = job.find("span", class_="job_sname").text.strip()
    experience_required = job.find("li", class_="exp").text.strip()

    data.append({
        "Job Title": job_title,
        "Job Location": job_location,
        "Company Name": company_name,
        "Experience Required": experience_required
    })

df = pd.DataFrame(data)

print(df)

driver.quit()


# In[6]:


#Q4
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_flipkart_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    sunglasses_listings = soup.find_all("div", class_="_1AtVbE")

    data = []
    for listing in sunglasses_listings:
        brand = listing.find("div", class_="_2WkVRV").text.strip()
        description = listing.find("a", class_="IRpwTa").text.strip()
        price = listing.find("div", class_="_30jeq3").text.strip()

        data.append({
            "Brand": brand,
            "Product Description": description,
            "Price": price
        })

    return data

def get_next_page_url(soup):
    next_page_button = soup.find("a", class_="_1LKTO3")
    if next_page_button:
        return "https://www.flipkart.com" + next_page_button["href"]
    else:
        return None

def scrape_flipkart_sunglasses():
    base_url = "https://www.flipkart.com"
    search_query = "sunglasses"
    page_count = 0
    data = []

    while len(data) < 100:
        url = f"{base_url}/search?q={search_query}&page={page_count}"

        page_data = scrape_flipkart_page(url)
        data.extend(page_data)

        page_count += 1

    df = pd.DataFrame(data[:100])

    print(df)

scrape_flipkart_sunglasses()


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_flipkart_reviews(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = soup.find_all("div", class_="_1AtVbE")

    data = []
    for review in reviews[:100]:
        rating = review.find("div", class_="_3LWZlK").text.strip()
        summary = review.find("p", class_="_2-N8zT").text.strip()
        full_review = review.find("div", class_="t-ZTKy").text.strip()

        data.append({
            "Rating": rating,
            "Review Summary": summary,
            "Full Review": full_review
        })

    return data

def scrape_flipkart_iphone_reviews():
    product_url = "https://www.flipkart.com/apple-iphone-11-black-64-gb/productreviews/itm4e5041ba101fd?pid=MOBFWQ6BXGJCEYNY&lid=LSTMOBFWQ6BXGJCEYNYZXSHRJ&marketplace=FLIPKART"

    reviews_data = scrape_flipkart_reviews(product_url)

    df = pd.DataFrame(reviews_data)

    print(df)

scrape_flipkart_iphone_reviews()


# In[7]:


#Q7
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_amazon_laptops():
    base_url = "https://www.amazon.in/"
    search_query = "Laptop"
    cpu_filter = "Intel Core i7"

    search_url = f"{base_url}s?k={search_query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    filter_url = f"{base_url}s?k={search_query}&rh=n%3A1375424031%2Cp_n_feature_three_browse-bin%3A16757432031&dc&qid=1644290170&rnid=16757422031&ref=sr_nr_p_n_feature_three_browse-bin_2"
    response = requests.get(filter_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    laptop_listings = soup.find_all("div", class_="s-include-content-margin")

    data = []
    for laptop in laptop_listings[:10]:
        title = laptop.find("span", class_="a-size-medium").text.strip()
        rating = laptop.find("span", class_="a-icon-alt")
        rating = rating.text if rating else "Not available"
        price = laptop.find("span", class_="a-offscreen").text.strip()

        data.append({
            "Title": title,
            "Ratings": rating,
            "Price": price
        })

    df = pd.DataFrame(data)

    print(df)

scrape_amazon_laptops()


# In[8]:


#Q8
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = "https://www.azquotes.com/"
driver = webdriver.Chrome()  
driver.get(url)

top_quotes_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Top Quotes')]")
top_quotes_link.click()

driver.implicitly_wait(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
quote_listings = soup.find_all("div", class_="wrap-block")

data = []
for quote in quote_listings[:1000]:
    quote_text = quote.find("a", class_="title").text.strip()
    author = quote.find("div", class_="author").text.strip()
    quote_type = quote.find("div", class_="qti").text.strip()

    data.append({
        "Quote": quote_text,
        "Author": author,
        "Type Of Quote": quote_type
    })

for i in range(min(5, len(data))):
    print(f"{i + 1}. {data[i]['Quote']} - {data[i]['Author']} ({data[i]['Type Of Quote']})")

driver.quit()


# In[9]:


#Q10
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.motor1.com/"
driver = webdriver.Chrome()  
driver.get(url)

search_bar = driver.find_element(By.XPATH, "//input[@id='search-bar']")
search_bar.send_keys("50 most expensive cars")

search_button = driver.find_element(By.XPATH, "//button[@class='search-btn']")
search_button.click()

expensive_cars_link = driver.find_element(By.XPATH, "//a[contains(text(), '50 Most Expensive Cars in the World')]")
expensive_cars_link.click()

driver.implicitly_wait(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
cars_data = []

car_container = soup.find("div", class_="slide-list")

car_listings = car_container.find_all("div", class_="slide")
for car in car_listings:
    car_name = car.find("h3").text.strip()
    car_price = car.find("span", class_="price").text.strip()

    cars_data.append({
        "Car Name": car_name,
        "Price": car_price
    })

df = pd.DataFrame(cars_data)

print(df)

driver.quit()


# In[ ]:




