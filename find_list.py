import requests
from bs4 import BeautifulSoup
from datetime import date


# находим перечень олимпиад
def find_list(headers):
    url = f'https://olimpiada.ru/search?q='
    datte = date.today().year
    if date.today().month >= 10:
        datte += 1
        params = f"Перечень олимпиад школьников и их уровней на {datte}/{str(datte)[-2:]} учебный год по профилям"
    params = f"Перечень олимпиад школьников и их уровней на {datte - 1}/{str(datte)[-2:]} учебный год по профилям"
    print(str(datte))
    url+=params
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    result = str(soup.find_all('a', class_="new_link"))
    new_url = 'https://olimpiada.ru' + result[result.find('/'):result.find('>') - 1]
    dictt = {"res": new_url}
    return dictt


def main():
    find_list()



if __name__ == "__main__":
    main()