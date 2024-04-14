from bs4 import BeautifulSoup  # импортируем библиотеку BeautifulSoup
import requests  # импортируем библиотеку requests
import csv # импортируем библиотеку csv
CSV = "auto.csv" # Название файла
url = 'https://auto.drom.ru/all'  # передаем необходимы URL адрес
headers = { # Создание видимости обычного пользователя
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def get_html(url, Params = ""):
    page = requests.get(url, headers=headers, params=Params)  # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
    return page

def get_content(html):
    soup = BeautifulSoup(html,"lxml")  # передаем страницу в bs4
    items = soup.find_all("div", class_="ftldj64 css-flpniz")
    advert_block = []  # словарь для удобной записи в результата в файл csv
    a = 0
    for item in items:
        while a < 20:
            advert_block.append(
                {
                    "Название": item.find_all(class_="css-16kqa8y e3f4v4l2")[a].text,
                    "Полное описание": item.find_all(class_="css-jlnpz8 e1icyw250")[a].text,
                    "Цена": item.find_all(class_="css-1dv8s3l eyvqki91")[a].text.replace('\ха', ""),
                    "Качество цены": item.find_all(class_="css-1femo5v evjskuu0")[a].text,
                    "Город, время": item.find_all(class_="css-19qeydu e162wx9x0")[a].text.replace('', " "),
                    "Ссылка": item.find(class_="css-1173kvb eojktn00").find_all("a")[a].get("href")
                }
            )
            a +=1
    return advert_block

def save_csv(items, path): # Функция сохранения файла в csv
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['Название', 'Полное описание', "Цена", "Качество цены", "Город, время", "Ссылка"])
            for item in items:
                writer.writerow([item["Название"], item['Полное описание'], item["Цена"], item["Качество цены"], item["Город, время"], item["Ссылка"]])

def parser(): # Функция выбора страниц, т.е сколько страниц спарсить
    Page = input("Кол-во страниц:")
    Page = int(Page.strip())
    html = get_html(url)
    if html.status_code == 200: # Если ответ от сайта есть, то парсер продолжает работу
        advert_block = []
        for p in range(1, Page):
            print("Парсим:", Page)
            html = get_html(url, Params={"page":Page})
            advert_block.extend(get_content(html.text))
            save_csv(advert_block, CSV)

    else:
        print("Ошибка")

parser()
