import requests
import os
from seleniumbase import Driver
from config import api_url


def take_dataset(cursor=''):
    url = f'{api_url}/{cursor}'
    r_dataset = requests.get(url)
    cursor = r_dataset.json()['cursor']
    items = r_dataset.json()['items']
    return cursor, items
    

def save_dataset_on_server(items):
    if not os.path.exists("dataset"):
        os.mkdir("dataset")      
        
    driver = Driver(uc=True, headless2=True)
    i = 1
    for item in items:
        description = item["description"]
        image_url = item["image_url"]
        print(image_url)   
        if description != None:
            driver.get(image_url)  
            driver.maximize_window()
            driver.save_screenshot(f"dataset/{'_'.join(image_url.split('/')[-2:]).split('.')[0]}.png")
            print(i)
            with open(f"dataset/{'_'.join(image_url.split('/')[-2:]).split('.')[0]}.txt", "w", encoding="utf-8") as file:
                file.write(description)
        i += 1
    driver.quit()      
        

cursor, items = take_dataset()
save_dataset_on_server(items)
