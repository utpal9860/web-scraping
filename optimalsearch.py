import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

jsonf = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}


def getlink(url):
    try:
        source = requests.get(url, headers=headers)
        return source
    except:
        time.sleep(1)
        return getlink(url)


def square(source):

    plaintext = source.text
    soup = BeautifulSoup(plaintext, "html.parser")
    data = {}  # {'name': [], 'magnet':[],'size':[], 'seed': [],'leech':[],'ss':[] }
    name = soup.find(
        'div', attrs={'class': 'box-info-heading clearfix'}).next_element

    print(name)
    # data["id"] = ids+1
    # ids += 1
    data["name"] = (name.get_text())
    fname = name.get_text()

    data["sname"] = fname[:20] + '...'
    magnet = soup.find_all('a')
    x = magnet[31:32]

    data["magnet"] = (x[0].get('href'))
    postertag = soup.find_all(
        'img', attrs={'class': 'img-responsive descrimg lazy'})
    posters = []
    for poster in postertag:
        posters.append(poster.get('data-original'))
#           print(posters)
    data["ss"] = (posters)
    type(posters)
    size = soup.find(
        string='Total size').next_element.next_element.get_text()
    print(size)
    data["size"] = (size)
    seeds = soup.find(
        string='Seeders').next_element.next_element.get_text()
    print(seeds)
    data["seed"] = (seeds)
    leeches = soup.find(
        string='Leechers').next_element.next_element.get_text()
    print(leeches)
    data["leech"] = (leeches)
    lang = soup.find(
        string='Language').next_element.next_element.get_text()
    print(lang)
    data["lang"] = (lang)
    return data


if __name__ == '__main__':
    # pool = multiprocessing.Pool()
    pool = Pool(cpu_count() * 2)
    all_link = []

    temp = 0
    total = 0
    query = "bootstrap studio"
    url1 = "https://1337x.to/search/" + str(query) + "/1/"

    source_code1 = getlink(url1)

    plain_text1 = source_code1.text
    soup1 = BeautifulSoup(plain_text1, "html.parser")
    links = soup1.findAll('a')

    links = links[31:len(links)-7]

    for link in links:
        href = link.get('href')
        if temp % 3 == 1:
            print("https://1337x.to"+href)
            all_link.append("https://1337x.to"+href)
            total += 1
        temp += 1
    start_time = time.time()
    all_link = pool.map(getlink, all_link)
    print("..............................")
    output = pool.map(square, all_link)
    print(output)
    print("--- %s seconds ---" % (time.time() - start_time))
