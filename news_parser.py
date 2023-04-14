import requests
from bs4 import BeautifulSoup
import datetime
import json 
import time 

def news():
    url = f'http://127.0.0.1:8000/find_list'
    url = requests.get(url=url).json()['res']
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find('table', class_="note_table")
    soup1 = BeautifulSoup(str(result), 'lxml')
    dates = {"января": 1, "февраля" : 2, "марта" : 3, "апреля" : 4, "мая": 5, 'июня': 6, 'июля': 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}
    result1 = soup1.find_all('a')
    result12 = []
    for i in result1:
        res = str(i)
        key = res[res.find('>') + 1: res.find('</a>')]
        result12.append(key)
    result1 = sorted(result12)
    del result1[result1.index("Остальные")]
    result1 += ["Остальные"]
    result2 = soup.find_all('table', class_="note_table")
    del result2[0]
    soup2 = BeautifulSoup(str(result2), 'lxml')
    result3 = soup2.find_all('a', class_="slim_dec")
    dic = {}
    for i in result3:
        ssilka = 'https://olimpiada.ru' + str(i)[str(i).find('href="') + len('href="'):str(i).find(">") - 1]
        name = str(i)[str(i).find('>') + 1: str(i).find('</a>')]
        url = ssilka + "/news"
        response1 = requests.get(url=url)
        soup = BeautifulSoup(response1.text, 'lxml')
        res1 = list(reversed(soup.find_all('a', class_="new_link new_item")))
        ls = []
        for l in res1:
            url1 = 'https://olimpiada.ru/' + str(l)[str(l).find('href="') + len('href="'):str(l).find(">") - 1]
            response2 = requests.get(url=url1)
            soup6 = BeautifulSoup(response2.text, 'lxml')
            date = str(soup6.find("span", class_='date_time'))
            date = date[date.find('<span class="date_time">') + len('<span class="date_time">'): date.find('</span>')].replace(', ', ' ').split()
            date[1] = dates[date[1]]
            name1 = str(soup6.find("h1", class_='headline'))
            name1 = name1[name1.find('<h1 class="headline"') + len('<h1 class="headline"') + 1: name1.find('</h1>')]
            if 'Утвержден Перечень олимпиад школьников и их уровней' not in name1:
                ls.append([date, name1])
        print(name)
        dic[ssilka] = [name, ls]
    with open("news.json", 'w', encoding='utf-8') as js:
        json.dump(dic, js, ensure_ascii=False)

                

            
def main():
    news()



if __name__ == "__main__":
    main()