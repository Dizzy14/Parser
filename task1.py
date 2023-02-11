from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from time import sleep
from PIL import Image

# function to load all html pages from the site
def scrape_images():
    ua = UserAgent()
    opts = Options()
    opts.add_argument(f"user-agent={ua.random}")
    browser = Chrome('/Users/stanislavrazin/UsefulDL/dls-project/chromedriver', options=opts)
    url = f'https://www.ralphlauren.nl/en/men/clothing/hoodies-sweatshirts/10204?sw1=sw-cache-me&webcat=men%7Cclothing%7Cmen-clothing-hoodies-sweatshirts&start={64}&sz=32'
    try:
        browser.get(url)
        sleep(5)

        with open(f'html_main{3}.html', 'w') as file:
            file.write(browser.page_source)

    except Exception as _ex:
        print(_ex)
    finally:
        browser.close()
        browser.quit()

#  function to download links for later use
def get_items_links(file_path):
    with open(file_path) as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    item_links = soup.find_all('div', class_='grid-tile')
    urls = []
    for item in item_links:
        try:
            item_url = item.find('div', class_='product-tile'). \
                find('div', class_='product-image'). \
                find('a').get('href')
            item_url = f'https://www.ralphlauren.nl{item_url}'
            urls.append(item_url)
        except:
            print('Error exception')
            continue

    print('Collected Successful')
    return urls


#  function to download images (example)
def load_useful_images(file_path):
    with open(file_path) as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    picture_links = soup.find_all('div', class_='grid-tile')
    global name
    for picture in picture_links:
        try:
            picture_url = picture.find('div', class_='product-tile'). \
                find('div', class_='product-image'). \
                find('a'). \
                find('picture', class_='rlc-picture') \
                .find('source', class_='rlc-image-src-desktop').get('srcset')
            photo = requests.get(str(picture_url))
            out = open(f'Useful_images/photo{name}.jpg', 'wb')
            out.write(photo.content)
            name += 1
        except:
            print('Error exception')
            continue

    print('Collected Successful')


#  function for saving links to a text file
def write_links():
    with open('links_list.txt', 'w') as file:
        for i in range(1, 6):
            urls = get_items_links(f'html_main{i}.html')
            for url in urls:
                file.write(f'{url}\n')


#  function for uploading photos to the Useful_images folder
def write_images():
    for i in range(1, 6):
        load_useful_images(f'html_main{i}.html')


# functions to change the name of the photo 
def rename_photo_cloth(photo_name_cloth):
    image = Image.open(f'Cloth/{photo_name_cloth}.jpeg')
    image.save(f'Cloth_jpg/{photo_name_cloth}.jpg')


def rename_photo_man(photo_name_man):
    image = Image.open(f'Photo_man/{photo_name_man}.jpeg')
    image.save(f'Photo_man_jpg/{photo_name_man}.jpg')


if __name__ == '__main__':
    # I ran this function manually by changing the string references and their names to save
    scrape_images()
    name = 0  # Image counter for image names
    write_links()
    write_images()
