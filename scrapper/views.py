import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
# Create your views here.


def get_html_content(city):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(' ', '+')

    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content


def home(request):
    weather_data = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_content = get_html_content(city)
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup.find('div', attrs={'class': 'wob_loc'}).text)
        weather_data = dict()
        weather_data['region'] = soup.find('div', attrs={'id': 'wob_loc'}).text
        weather_data['daytime'] = soup.find('div', attrs={'id': 'wob_dts'}).text
        weather_data['status'] = soup.find('span', attrs={'id': 'wob_dc'}).text
        weather_data['temp'] = soup.find('span', attrs={'id': 'wob_tm'}).text

    return render(request, 'scrapper/home.html', {'weather': 'weather_data'})

'''
weather_data = {
            'region': soup.find('div', attrs={'id': 'wob_loc'}).text,
            'daytime': soup.find('div', attrs={'id': 'wob_dts'}).text,
            'status': soup.find('span', attrs={'id': 'wob_dc'}).text,
            'temp': soup.find('span', attrs={'id': 'wob_tm'}).text
        }
'''


def movie_home(request):
    url = "https://www.imdb.com/chart/moviemeter/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table',  {'class': 'chart full-width'})
    rows = table.find_all('tr')
    movies = []
    for row in rows:
        image = row.find('img')
        if image:
            movies.append(image['alt'])
            movies.append(image['src'])
    return render(request, "scrapper/movies.html", {'movies': movies})


def naija_news(request):
    try:
        res_list = []
        url = 'https://www.nairaland.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find_all('table', {'class': 'boards'})
        data = table[1].find('td', {'class': 'featured'})
        #print(data('a'))
        data_links = data('a')  # get all <a></a> tags as elements of a single link
        nested_lists = []
        elem = []
        x = ''
        for link in data_links:
            elem.append(link)
            #nested_lists.append(link('b'))
        #print(elem)
        for each in elem[:65]:
            res = list(map(lambda x: "".join(x), each))
            res = ''.join(res)
            res_list.append(res)
        context = {
            'res_list': res_list
        }
        return render(request, 'scrapper/naija_news.html', context)
    except:
        return render(request, 'scrapper/naija_news.html')


def weather_app(request):
    if 'city' in request.GET:
        city_name = request.GET.get('city')
        city = city_name.replace(' ', '+')
        url = f'https://www.google.com/search?q=weather+in+{city}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        name = soup.find('div', {'class': 'VQF4g'})
        print(name)
    return render(request, 'scrapper/home.html', {'weather': 'weather_data'})