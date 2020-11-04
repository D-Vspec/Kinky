import requests
from bs4 import BeautifulSoup
import urllib.request
import time
from PIL import Image
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

ComicNumber = 1
pages_to_delete = [0] #First page is 0

comlink = str(input('Enter link of site '))

response = requests.get(comlink) 

soup = BeautifulSoup(response.text, 'html.parser')

first = True
issue = str(input('Enter name of download '))
keyword = str(input('Input keyword for img '))

directory = r"C:\Users\Divyansh\Desktop\STuff\Comics\Manga\\" + issue
os.makedirs(directory)
print(directory)
for links in soup.find_all('a'):
    link = links.get('href')
    print(link)
    if  '136' not in str(link):
        if 'chapter' in str(link):
            print(link)

            l = 1

            imagelist= []

            response = requests.get(link) 

            soup = BeautifulSoup(response.text, 'html.parser')

            for page in soup.find_all('img'):
                if 'ldkmanga' not in str(page.get('src')):
                    if keyword in str(page.get('src')):
                        try:
                            print(page.get('src'))
                            urllib.request.urlretrieve(page.get('src'), r"C:\Users\Divyansh\Desktop\STuff\Python Files\Tests\\" + str(l) + ".jpg")
                            photo = Image.open(r"C:\Users\Divyansh\Desktop\STuff\Python Files\Tests\\" + str(l) + ".jpg")
                            pdf = photo.convert('RGB')
                            imagelist.append(pdf)
                            os.remove(r"C:\Users\Divyansh\Desktop\STuff\Python Files\Tests\\" + str(l) + ".jpg")
                        except:
                            print('fel')
                        l = l + 1

            ComicNumber = ComicNumber + 1

            link =link.replace(link[:34], '')
            link =link.replace('/', '')
            link =link.replace('-', ' ')
            print(link)

            comicname = link
            print(directory + '\\' + link)

            photo.save(directory + '\\' +comicname + '.pdf', save_all=True, append_images=imagelist)
            print('PDF MADE')

            #issue = str(int(issue) + 1)
            infile = PdfFileReader(directory+ '\\' + comicname + '.pdf', 'rb')
            output = PdfFileWriter()

            for i in range(infile.getNumPages()):
                if i not in pages_to_delete:
                    p = infile.getPage(i)
                    output.addPage(p)

            with open(directory + '\\' + comicname + '.pdf', 'wb') as f:
                output.write(f)

            print('Spoiler Fixed')
