
# import requests
# from bs4 import BeautifulSoup

# def search_datasets(query):
#     url = f"https://datasetsearch.research.google.com/search?query={query}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Example: Extract dataset titles and URLs
#     datasets = []
#     for result in soup.find_all('div', class_='kCClje'):
        
#         title = result.find('h1').text
#         print(title)

#         # # print('title',title)
#         # link = result.find('a')['href']
#         # # print('link',link)
#         # datasets.append({'title': title, 'link': link})

#     # return datasets


# query = "crop disease"
# datasets = search_datasets(query)
# print(datasets)
# print('hhh')
# for dataset in datasets:
#     # print('here')
#     print(dataset['title'], dataset['link'])



# **********************************
# import requests
# from bs4 import BeautifulSoup

# def search_datasets(query):
#     url = f"https://datasetsearch.research.google.com/search?query={query}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     datasets = []
#     # Update this based on the actual class or tags on the page
#     for result in soup.find_all('div', class_='kCClje'):
#         title_tag = result.find('h1')
#         if title_tag:
#             title = title_tag.text
#             datasets.append({'title': title})

#             # Print each title
#             print(title)

#     return datasets

# query = "crop disease"
# datasets = search_datasets(query)



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Function to search datasets dynamically using Selenium
def search_datasets(query):
    # Specify the path to the webdriver (e.g., ChromeDriver) here
    # PATH="/usr/bin/geckodriver"
    driver = webdriver.Firefox()

    # Open Google Dataset Search
    url = f"https://datasetsearch.research.google.com/search?query={query}"
    driver.get(url)
    
    time.sleep(3)  # Wait for page to load

    # List to store dataset results
    datasets = []

    # Find all dataset result elements dynamically loaded on the page
    results = driver.find_elements(By.CLASS_NAME, 'kCClje')  # Update the class if it changes
    for result in results:
        try:
            # Extract the title for each dataset result
            title = result.find_element(By.TAG_NAME, 'h1').text
            datasets.append({'title': title})

            # Print the dataset title
            print(title)
        except:
            pass

    driver.quit()
    return datasets

# Example usage
query = "crop disease"
datasets = search_datasets(query)
