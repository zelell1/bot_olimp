import requests
from bs4 import BeautifulSoup
import datetime
import json 


def news():
    url = f'http://127.0.0.1:8000/olimpix'
    response = requests.get(url=url).json()
    for i in range(len(response)):
        for val in response[i].values():
            for j in val:
                url = j["".join(list(j.keys()))][-1] + "/news"
                response1 = requests.get(url=url)
                soup = BeautifulSoup(response1.text, 'lxml')
                res1 = list(reversed(soup.find_all('a', class_="new_link new_item")))
                ls = []
                dates = {"января": 1, "февраля" : 2, "марта" : 3, "апреля" : 4, "мая": 5, 'июня': 6, 'июля': 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}
                for l in res1:
                    url1 = 'https://olimpiada.ru/' + str(l)[str(l).find('href="') + len('href="'):str(l).find(">") - 1]
                    response2 = requests.get(url=url1)
                    soup6 = BeautifulSoup(response2.text, 'lxml')
                    date = str(soup6.find("span", class_='date_time'))
                    date = date[date.find('<span class="date_time">') + len('<span class="date_time">'): date.find('</span>')].replace(', ', ' ').split()
                    day = date[0]
                    mn = date[1]
                    year = date[2]
                    tm = date[-1].split(':')
                    hour = tm[0]
                    minut = tm[-1]
                    mn = dates[mn]
                    date = datetime.datetime(int(year), int(mn), int(day), int(hour), int(minut))
                    name1 = str(soup6.find("h1", class_='headline'))
                    name1 = name1[name1.find('<h1 class="headline"') + len('<h1 class="headline"') + 1: name1.find('</h1>')]
                    if 'Утвержден Перечень олимпиад школьников и их уровней' not in name1:
                        ls.append([date, name1])
            j["".join(list(j.keys()))].append({'news': ls})  
    with open("lst.json", 'w', encoding='utf-8') as js:
        json.dump(response, js, ensure_ascii=True)
                

            
def main():
    news()



if __name__ == "__main__":
    main()