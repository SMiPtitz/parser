#################################
# parser reviews from kinopois.ru
# S.Mirzaianova
# ptitzalone@gmail.com
# 2018
#################################
# This function get pages with reviews from users
# with depends of type of review
# and parse text of review to txt file
#################################

import bs4
from lxml import html
import requests

# make session with browser and system data
# because of kinopoisk.ru
s = requests.Session()
s.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
    })


# get page
def load_user_data(type, page, session):
    url = 'https://www.kinopoisk.ru/reviews/type/comment/status/%s/period/month/page/%d/#list' % (type, page)
    request = session.get(url)
    return request.text


# check if page contains reviews
def contain_movies_data(text):
    soup = bs4.BeautifulSoup(text, "html5lib")
    film_list = soup.find('div', {'class': 'reviewItem userReview'})
    return film_list is not None


# take page and return review text
def parse_text(request):
    parsed_body = html.fromstring(request)
    text = []
    for el in parsed_body.xpath('.//div[@class="brand_words"]'):
        for item in el.xpath('.//text()'):
            text.append(item)
    return text


# cycling for pages and parsing data to file
def get_pages(type, s):
    # loading files
    page = 1
    while True:
        data = load_user_data(type, page, s)
        if contain_movies_data(data):
            text = parse_text(data)
            with open("output", 'a') as file:
                for t in text:
                    if t != '\r\n' and t != '\n':
                        print(t)
                        file.write("%s\n" % t)
            page += 1
        else:
                break


if __name__ == '__main__':
    # type of reviews on kinopoisk.ru
    type = ['good', 'bad', 'neutral']
    for t in type:
        get_pages(t, s)
