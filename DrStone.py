from selenium import webdriver
import wget
import keyboard
from PIL import Image
import glob, os
import time
import win32api


imagelist = []

chp = str(input('from what chapter '))

chrome_path = r"Chromedriver Path"
driver = webdriver.Chrome(chrome_path)
driver.get('insert manga website link' + chp + '/')
PageNo = 1

while True:
    try:
        time.sleep(6)
        print('doing')
        memes = driver.find_elements_by_tag_name('img')
        for meme in memes:
            image_url = meme.get_attribute('src')
            print(image_url)
            image_filename = wget.download(image_url)
            print('Image Successfully Downloaded: ', image_filename)
        print('done lmao')

        try:
            os.remove(r"Photo dir")
        except:
            print('sad')
        imagelist = []

        for name in glob.glob(r"photo dir"): 
            print(name) 
            photo = Image.open(name)
            pdf = photo.convert('RGB')
            imagelist.append(pdf)
            os.remove(name)
            
        photo.save(r"Directory name \name.pdf",save_all=True, append_images=imagelist)
        print('PDF made')

        for name in glob.glob(r"photo dir"): 
            os.remove(name)

        os.rename(r"Dir of file\name.pdf", r"Directory Name\\" + chp + ".pdf") 

        print('next pg')
        try:
            #chp = chp
            #chp = str(int(chp) + 1)
            #driver.get('https://spy-xfamily.com/manga/spy-x-family-chapter-1-mission-' + chp +  '/')
            driver.find_element_by_partial_link_text('Chapter ' + str(int(chp) + 1)).click()
            #driver.find_element_by_class_name('nav-next').click()
            chp = str(int(chp) + 1)
        except:
            print('try again')
    except:
        print('f')         

#
