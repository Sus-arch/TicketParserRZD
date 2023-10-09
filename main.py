import time

from bs4 import BeautifulSoup
from selenium import webdriver


def get_source_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url=url)
        time.sleep(5)

        with open('index_selenium.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

        with open('index_selenium.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        card = soup.find('div', class_='row card__body ng-star-inserted')
        try:
            plaz_count = card.find_all('div', class_="card-class__quantity ng-star-inserted")[0].get_text().strip()
            plaz_price = card.find_all('div', class_="card-class__price")[0].get_text().replace('\xa0', '')
        except:
            plaz_count = 0
            plaz_price = None
        try:
            kupe_count = card.find_all('div', class_="card-class__quantity ng-star-inserted")[1].get_text().strip()
            kupe_price = card.find_all('div', class_="card-class__price")[1].get_text().replace('\xa0', '')
        except:
            kupe_count = 0
            kupe_price = None
        time_vag = card.find('div', class_="card-route__date-time card-route__date-time--from").get_text() + '||' + card.find('div', class_="card-route__date-time card-route__date-time--to").get_text()

        data = {
            'time': time_vag,
            'plac': {
                'count': plaz_count,
                'price': plaz_price
            },
            'kupe': {
                'count': kupe_count,
                'price': kupe_price
            }
        }
        return data

    except Exception as _ex:
        print(_ex)
        return None
    finally:
        driver.close()
        driver.quit()


def parse_tickest(link):
    data = []
    first_data = get_source_html(link)
    if bool(first_data):
        first_data['link'] = link
        data.append(first_data)

    return data


def main():
    link = input("Введите ссылку, которой будут искаться билеты(только прямые): ")
    print(parse_tickest(link))


if __name__ == '__main__':
    main()
