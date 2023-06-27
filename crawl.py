import requests
import time
from bs4 import BeautifulSoup

def write_out(text):
        output = open("./output.tsv", "a")
        output.write(text)
        output.close()

if __name__ == '__main__':
    f = open("./data.tsv", "r")

    write_out('number\t이름\t배합목적\n')
    for line in f.readlines():
        temp = line.split('\t')
        number = temp[0]
        url = 'https://kcia.or.kr/cid/search/ingd_view.php?no=%s'%(number)
        response = requests.get(url)

        if response.status_code != 200: 
            continue

        html = response.text 
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.select(".table_list tbody tr")

        purpose = '-'

        for tr in trs:
            header = tr.select_one("th:nth-of-type(1)")

            if header == None:
                continue

            if header.get_text() == '성분명':
                name = tr.select_one("td:nth-of-type(1)").get_text()

            if header.get_text() == '배합목적':
                purpose = tr.select_one("td:nth-of-type(1)").get_text()


        write_out("%s\t%s\t%s\n"%(number, name, purpose))

        time.sleep(0.2)
