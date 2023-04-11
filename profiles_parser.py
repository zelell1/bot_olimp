import requests
from bs4 import BeautifulSoup
import random



def profiles(headers):
    url = f'https://olimpiada.ru/activities'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all("div", class_=["sc_pop_sub", "sc_pop_sub popular"])
    dictt = {}
    for elem in cards:
        num = str(elem)[str(elem).find('[') + 1:str(elem).find(']')]
        name = str(elem)[str(elem).find('</span>') + len('</span>') + 1:str(elem).find('</font>')]
        if '\xa0язык' not in name:
            dictt[str(name)] = num
    return dictt
        


def main():
    profiles()



if __name__ == "__main__":
    main()