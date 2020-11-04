import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
import time

ComicNumber = 1
pages_to_delete = [0] #First page is 0

first = True
issue = str(input('Which issue '))
directory = r'C:\Users\Bob\Desktop\STuff\Comics\Manga\opm\\'
while ComicNumber <= 134:

    l = 1

    imagelist= []
    
    response = requests.get('https://readpunchmanga.com/one-punch-man-chapter-' + issue + '/')

    soup = BeautifulSoup(response.text, 'html.parser')


    for page in soup.find_all('img'):
        if 'imgur' or 'blogspot' in str(page.get('src')):
            print(page.get('src'))
            try:           
                urllib.request.urlretrieve(page.get('src'), r"C:\Users\Divyansh\Desktop\STuff\Python Files\Tests\\" + str(l) + ".jpg")
            except:
                continue            
            photo = Image.open(r"C:\Users\Divyansh\Desktop\STuff\Python Files\Tests\\" + str(l) + ".jpg")
            pdf = photo.convert('RGB')
            imagelist.append(pdf)
            os.remove(r"C:\Users\Divyansh\Desktop\STuff\Python Files\Tests\\" + str(l) + ".jpg")
            l = l + 1
    

    ComicNumber = ComicNumber + 1

    comicname = 'NAME_' + str(issue)

    photo.save(directory + comicname + '.pdf', save_all=True, append_images=imagelist)
    print('PDF MADE')

    issue = str(int(issue) + 1)
    infile = PdfFileReader(directory + comicname + '.pdf', 'rb')
    output = PdfFileWriter()

    for i in range(infile.getNumPages()):
        if i not in pages_to_delete:
            p = infile.getPage(i)
            output.addPage(p)

    with open(directory + comicname + '.pdf', 'wb') as f:
        output.write(f)

    print('Spoiler Fixed')
