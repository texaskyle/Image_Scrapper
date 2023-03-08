import os  # for making  a directory
import time  # for enabling a smooth iteration for getting the urls and downloading images from the google
import requests  # used for downloading the images from the urls
from selenium import webdriver  # selenium is used to automate the process of fetching the images from the urls
# the webdriver is used to create an instance of chrome of chrome browser
from selenium.webdriver.chrome.service import Service  # this code allows an easy way to config and launch chrome
# Service class which has been imported is used mto create an instance of chrome
from selenium.webdriver.common.by import By  # By is used to select the mechanism by which an element is located on the webpage

"""the purpose of this function is to use the given webdriver instance to automate google image search and 
extract the urls of the returned images"""
def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int=1):
    # the below code will scroll the webpage to the bottom by executing the javascript code
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query
    # the search query is template with well defined parameters
    search_url ="https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    """ load the page
    the search query is a string , the format will be used to replace the q placeholder with the variable query
    the get() method opens the specific web browser window, which allows the user to view and interact with the search results
    """
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    result_start = 0

    while image_count < max_links_to_fetch:
        scroll_to_end(wd)
        # get all the image thumbnail results
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {result_start}: {number_results}")

        for img in thumbnail_results[result_start: number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract the image urls
            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!!")
                break

        else:
            print("Found", len(image_urls), "image links, looking for more...")
            time.sleep(30)
            return
            load_more_button = wd.find_element(By.CSS_SELECTOR, 'img: mye4qd')
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd").click();

        # move the results startpoint further down
        results_start = len(thumbnail_results)
    return image_urls


def persist_image(folder_path: str, url: str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"Error could not download {url}-{e}")
    try:
        f=open(os.path.join(folder_path, 'jpg' + '_' + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"success-saved {url} as {folder_path}")
    except Exception as e:
        print(f"Error-could not save {url}-{e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    #from selenium.webdriver.chrome.service import Service
    with webdriver.Chrome(service=Service(executable_path=driver_path)) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1


DRIVER_PATH = './chromedriver.exe'
search_term = "cat"
number_images = 5
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=number_images)


