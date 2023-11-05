import requests
import os
from seleniumbase import Driver
from PIL import Image
import numpy as np
from config import api_url


import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} выполнилась за {execution_time:.2f} секунд")
        return result
    return wrapper


def take_dataset(cursor=''):
    url = f'{api_url}/{cursor}'
    r_dataset = requests.get(url)
    cursor = r_dataset.json()['cursor']
    items = r_dataset.json()['items']
    return cursor, items
    

@timing_decorator
def save_dataset(items):
    if not os.path.exists("dataset"):
        os.mkdir("dataset")      
        
    driver = Driver(uc=True, headless2=True)
    i = 1
    for item in items:
        description = item["description"]
        image_url = item["image_url"]
        path_img = f"dataset/{'_'.join(image_url.split('/')[-2:]).split('.')[0]}"
        print(image_url)   
        if description != None:
            driver.get(image_url)  
            driver.maximize_window()
            driver.save_screenshot(f"{path_img}.png")
            img_without_background(f"{path_img}.png")
            print(i)
            with open(f"{path_img}.txt", "w", encoding="utf-8") as file:
                file.write(description)
        i += 1
    driver.quit()      
   
@timing_decorator    
def img_without_background(image_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    data = np.array(image)
    background_color = data[0, 0]

    non_background_indices = np.where(np.any(data != background_color, axis=-1))
    x, y = non_background_indices[1], non_background_indices[0]

    left, top, right, bottom = x.min(), y.min(), x.max(), y.max()

    image = image.crop((left, top, right + 1, bottom + 1))
    image.save(image_path)
    image.close()

    

cursor, items = take_dataset()
save_dataset(items)

  