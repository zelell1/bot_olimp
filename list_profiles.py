import requests
from bs4 import BeautifulSoup


def list_profiles():
    url = f'http://127.0.0.1:8000/find_list'
    url = requests.get(url=url).json()['res']
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    result = soup.find('table', class_="note_table")
    soup1 = BeautifulSoup(str(result), 'lxml')
    result1 = soup1.find_all('a')
    result12 = []
    for i in result1:
        res = str(i)
        key = res[res.find('>') + 1: res.find('</a>')]
        result12.append(key)
    result1 = sorted(result12)
    del result1[result1.index("Остальные")]
    result1 += ["Остальные"] 
    return result1     


def main():
    list_profiles()


if __name__ == "__main__":
    main()