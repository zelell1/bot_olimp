import requests
from bs4 import BeautifulSoup


# функция пробегает по сайту и берет полседенюю новость по передаваемой олимпиаде
def newss(ssilka):
    dates = {"января": 1, "февраля" : 2, "марта" : 3, "апреля" : 4, "мая": 5, 'июня': 6, 'июля': 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}
    url = "https://olimpiada.ru/activity/" + str(ssilka) + "/news"
    response1 = requests.get(url=url)
    url = "https://olimpiada.ru/activity/" + str(ssilka) 
    response2 = requests.get(url=url)
    soup0 = str(BeautifulSoup(response2.text, 'lxml').find('h1'))
    name = soup0[soup0.find('>') + 1: soup0.find('/') - 1]
    soup = BeautifulSoup(response1.text, 'lxml')
    res1 = list(reversed(soup.find_all('a', class_="new_link new_item")))[-1]
    ls = []
    if res1 != '':
        url1 = 'https://olimpiada.ru' + str(res1)[str(res1).find('/'):str(res1).find(">") - 1]
        response2 = requests.get(url=url1)
        soup6 = BeautifulSoup(response2.text, 'lxml')
        date = str(soup6.find("span", class_='date_time'))
        date = date[date.find('<span class="date_time">') + len('<span class="date_time">'): date.find('</span>')].replace(', ', ' ').split()
        date[1] = str(dates[date[1]])
        name1 = str(soup6.find("h1", class_='headline'))
        name1 = name1[name1.find('<h1 class="headline"') + len('<h1 class="headline"') + 1: name1.find('</h1>')]
        news = str(soup6.find("div", class_='full_text').find('p'))
        news = news[news.find('>') + 1: news.find('</p>') - len('p>')]
        if 'Утвержден Перечень олимпиад школьников и их уровней' not in name1:
            ls.append(date)
            ls.append(news)
            ls.append(name)
    return ls

            
def main():
    print(newss(397))



if __name__ == "__main__":
    main()