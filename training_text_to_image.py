import requests
import os
from seleniumbase import Driver
from PIL import Image
import numpy as np
from config import api_url, TOKEN, telegram_id


url_telegram = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={telegram_id}&text='


def take_dataset():
    url = f'{api_url}/{cursor}'
    r_dataset = requests.get(url)
    if r_dataset.status_code == 200:
        cursor = r_dataset.json()['cursor']
        items = r_dataset.json()['items']
        return cursor, items
    else:
        text = f'take_dataset() status code: {r_dataset.status_code}, cursor = {cursor}'
        requests.get(f'{url_telegram}{text}')
    

def create_folder(name_folder):
    folder = name_folder
    if not os.path.exists(folder):
        os.mkdir(folder)  
    return folder


def save_dataset(items, img_counter=0):
    dataset = create_folder('dataset')         
    driver = Driver(uc=True, headless2=True)
    for item in items:
        description = item["description"]
        image_url = item["image_url"]
        if description != None:
            img_counter += 1
            folder_picture = create_folder(f'{dataset}/picture_{img_counter}')   
            path_img = f"{folder_picture}/{'_'.join(image_url.split('/')[-2:]).split('.')[0]}"
            driver.get(image_url)  
            driver.maximize_window()
            driver.save_screenshot(f"{path_img}.png")
            img_without_background(f"{path_img}.png")
            with open(f"{path_img}.txt", "w", encoding="utf-8") as file:
                file.write(description)
            
    driver.quit()      
    text = f'save_dataset(), img_counter = {img_counter}'
    requests.get(f'{url_telegram}{text}')

    
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

 
def main():    
    cursor = ''
    cursor, items = take_dataset(cursor)
    save_dataset(items)
    

main()
  