import requests
from bs4 import BeautifulSoup


def profiles():
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
    result2 = soup.find_all('table', class_="note_table")
    del result2[0]
    lisst = []
    for i in range(len(result1)):
        soup2 = BeautifulSoup(str(result2[i]), 'lxml')
        result3 = soup2.find_all('tr')
        soup3 = BeautifulSoup(str(result3), 'lxml')
        result4 = soup3.find_all('p')
        key = result1[i]
        book = {key: []}
        lst = str(result4)[str(result4).find('Уровень</strong></p>') + len('Уровень</strong></p>') + 2:].split('<p style="text-align: left;"><a class="slim_dec" ')[1:]
        for j in lst:
            ssilka = 'https://olimpiada.ru' + j[j.find('"') + 1: j.find('>') - 1]
            name = j[j.find('>') + 1: j.find('</a>')]
            num = j[j.find('<p>'):]
            num1 = num[num.find('>') + 1: num.find('</p>')]
            pred = list(reversed(num[num.find(', ') + 2:].split('</p>,')))
            if pred[0] == " ":
                del pred[0]
            if len(pred) == 3:
                del pred[-1]
            pred = ", ".join(list(reversed(pred))) 
            pred1 = pred[pred.find('>') + 1: pred.find(',  <p>')]
            lvl = pred[pred.find(',  <p>') + len(',  <p>'):]
            if len(lvl) > 1:
                lvl = lvl[0]
            dictt = {name: [num1, pred1, lvl, ssilka]}
            book[key].append(dictt)
        lisst.append(book)
    return lisst

            
        
        

def main():
    profiles()



if __name__ == "__main__":
    main()