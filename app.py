from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    news = get_news()
    return render_template('lol-news.temp', news_list = news)

@app.route('/test')
def test():
    return render_template('test.temp')


class image_element:
    def __init__(self, source, link):
        self.source = source
        self.link = link

class news_element:
    def __init__(self, title, date, image):
        self.title = title
        self.date = date
        self.image = image_element(image.source, image.link)



def get_news():
    URL = "https://wildrift.leagueoflegends.com/en-gb/news/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    tag_type = "a"
    class_to_find = "articleCardWrapper-1JIOy"

    news_title_tag = "h4"
    news_title_class = "heading-05 font-normal title--HVLV"
    news_date_tag = "span"
    news_date_class = "copy-01"
    news_image_tag = "img"
    news_image_class = "image-NeGf2" 

    news_elements = soup.find_all(tag_type, class_=class_to_find)

    output_news_list = []

    for element in news_elements:

        element_title = element.find(news_title_tag, class_=news_title_class).text
        element_date = element.find(news_date_tag, class_=news_date_class).text
        element_image_source = element.find(news_image_tag, class_=news_image_class).get('src')
        element_image_link = ''

        if element.get('href').split('/', 1)[0] == '':
            element_image_link = "https://wildrift.leagueoflegends.com" + element.get('href')
        else:
            element_image_link = element.get('href')


        output_news_list.append(news_element(element_title,element_date,image_element(element_image_source, element_image_link)))

    return output_news_list