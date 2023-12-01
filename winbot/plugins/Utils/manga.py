import io
import os
import requests
from reportlab.pdfgen import canvas
from PIL import Image
from bs4 import BeautifulSoup


def getSearchResult(name):
    html = requests.get("https://ww6.manganelo.tv/search/"+name)
    array = []

    soup = BeautifulSoup(html.text,"html.parser")
    for i in soup.select("div.search-story-item h3"):
        title = i.find("a").get_text()
        link = "https://ww5.manganelo.tv"+i.find('a').get('href')
        array.append({
            "title":title,
            "link":link
        })
    return array

def getChapter(link):
    html = requests.get(link)
    array = []

    soup = BeautifulSoup(html.text,"html.parser")
    for i in soup.select(".row-content-chapter .a-h"):
        title = i.find("a").get_text()
        link = i.find('a').get('href').split("chapter/")[1]
        array.append({
            "title":title,
            "link":link
        })
    return array
def getImages(id):
    html = requests.get("https://ww6.manganelo.tv/chapter/"+id)
    array = []

    soup = BeautifulSoup(html.text,"html.parser")
    title = soup.select(".panel-breadcrumb")[0].select("a")[-1].get_text()
    for i in soup.select(".container-chapter-reader img"):
        link = i.get('data-src')
        array.append(link)
    return array,title
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_data = io.BytesIO(response.content)
        return Image.open(img_data)
    return None

def images_to_pdf(image_urls, pdf_filename):
    c = canvas.Canvas(pdf_filename)

    for image_url in image_urls:
        image = download_image(image_url)

        if image:
            
            img_width, img_height = image.size
            c.setPageSize((img_width, img_height))
            temp_image_filename = os.path.basename(image_url)
            image.save(temp_image_filename, format="JPEG")

            c.drawImage(temp_image_filename, 0, 0, img_width, img_height)
            c.showPage()
            os.remove(temp_image_filename)

    c.save() 
