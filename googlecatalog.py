from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Firefox()



def scroll_left_pane(query, scroll_pause_time):

    url = f"https://datasetsearch.research.google.com/search?query={query}"
    driver.get(url)

    time.sleep(3)  # Wait for page to load
    # Identify the scrollable container (Left search result pane)
    scrollable_div = driver.find_element(By.CLASS_NAME, "bwmXfe")  # Update class name if needed

    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

    while True:
        items = driver.find_elements(By.CLASS_NAME, "UnWQ5")  # Refresh items list each cycle
        
        if len(items) == 0:
            print("No items found, stopping.")
            break

        total_items = len(items)
        start_index = max(0, total_items - 20)  # Get last 20 items

        for i in range(start_index, total_items, 4):  # Process in chunks of 4
            chunk = driver.find_elements(By.CLASS_NAME, "UnWQ5")[i:i+4]  # Refresh chunk dynamically

            for j, item in enumerate(chunk):
                try:
                    # Scroll the element into view before clicking
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                    time.sleep(1)  # Allow time for scrolling
                    
                    result = item.find_element(By.TAG_NAME, 'h1').text
                    print(f"Processing item {i+j+1}: {result}")

                    item.click()  # Direct click instead of ActionChains

                    time.sleep(2)  # Allow content to load

                    # Extract links from the clicked item
                    get_url_classes = driver.find_elements(By.CLASS_NAME, 'jqqkc')
                    for get_url_class in get_url_classes:
                        link = get_url_class.get_attribute('data-source-url')
                        print(f"Extracted Link: {link}")
                    # Find the "Dataset updated" div first
                    updated_div = driver.find_element(By.XPATH, "//div[contains(text(), 'Dataset updated')]")
                    # Get the corresponding date (following sibling span)
                    date_updated = updated_div.find_element(By.XPATH, "./following-sibling::span").text
                    print("Dataset updated on:", date_updated)
                    time.sleep(2)  # Allow content to load
                    # Find the "Dataset updated" div first
                    find_auth = driver.find_element(By.XPATH, "//div[contains(text(), 'Authors') or contains(text(), 'authored')]")

                    # Get the corresponding date (following sibling span)
                    authors = find_auth.find_element(By.XPATH, "./following-sibling::span").text

                    print("Authors:", authors)
                    print('---------------------------------------------------------------------------')


                except Exception as e:
                    print(f"Error processing item {i+j+1}: {e}")

            # Scroll after processing a chunk
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(scroll_pause_time)

        # Refresh the item list after scrolling
        time.sleep(2)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        
        if new_height == last_height:  # Stop if no new content appears
            break
        last_height = new_height

scroll_left_pane("crop disease", 2)

