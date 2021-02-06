import time
from collections import deque
from threading import Thread

from selenium import webdriver


def save_both():
    update_fetched_data()
    update_remaining_q()


def update_fetched_data():
    import json
    res = json.dumps(fetched_articles)
    f = open("fetched_data.txt", "w")
    f.write(res)


def update_remaining_q():
    import json
    res = json.dumps(list(q))
    f = open("q.txt", "w")
    f.write(res)


def fetch_article_data_with_link(link, browser):
    def execute_until_done(function, wait_till_now=0.0):
        now = time.time()
        if wait_till_now >= 4:
            print("Time out")
            raise Exception()
        try:
            return function()
        except:
            time.sleep(0.5)
            print("wait:", wait_till_now)
            return execute_until_done(function, wait_till_now=wait_till_now + time.time() - now)

    def wait_until_load(driver):
        while True:
            x = driver.execute_script("return document.readyState")
            if x == "complete":
                return True
            print("here:", link)

    browser.get(link)
    browser.implicitly_wait(10)
    b = wait_until_load(browser)
    # ID
    id = link.split("/")[-1]
    # Title
    title = execute_until_done(lambda: browser.find_element_by_class_name("name").text)

    # Abstract
    abstract = execute_until_done(lambda: browser.find_elements_by_tag_name("p")[2].text)

    # Year
    year = execute_until_done(lambda: browser.find_element_by_class_name("year").text)

    # Authors
    all_authors_tag = browser.find_elements_by_xpath("//*[@data-appinsights-key.bind='author.id']")
    authors = []
    for auth in all_authors_tag:
        if auth.get_attribute("href").split("paperId=")[-1] == id:
            authors.append(auth.text)

    # References
    ref_count = int(execute_until_done(lambda: browser.find_element_by_class_name("count").text))
    references_ids = []

    if ref_count != 0:
        temp = execute_until_done(lambda: browser.find_element_by_class_name("primary_paper"))

        all_references_tag = browser.find_elements_by_class_name("primary_paper")
        for ref in all_references_tag:
            try:
                ref_id = ref.find_element_by_xpath(".//*").get_attribute("href").split("/")[-2]
                references_ids.append(ref_id)
            except:
                pass
            if len(references_ids) >= 10:
                break

    return {
        "id": id,
        "title": title,
        "abstract": abstract,
        "date": year,
        "authors": authors,
        "references": references_ids
    }


def open_browser_crawler(index):
    browser = webdriver.Firefox()

    while len(fetched_articles) < n:
        try:
            if len(q) != 0:
                browsers_empty_q_flags[index] = False
                id = q.popleft()
                if id not in fetched_articles.keys():
                    d = fetch_article_data_with_link("https://academic.microsoft.com/paper/" + id, browser)
                    fetched_articles[id] = d
                    for ref in d['references']:
                        if ref not in fetched_articles.keys():
                            q.append(ref)
                    print("#########", len(fetched_articles))
                    print(len(q))
                if len(fetched_articles) % 20 == 1:
                    save_both()
            else:
                browsers_empty_q_flags[index] = True
            if sum(browsers_empty_q_flags) == len(browsers_empty_q_flags):
                break
        except:
            q.append(id)
    browser.close()


if __name__ == '__main__':
    n = 5000
    n = int(input("Enter Article's Count to be fetched:"))
    q = deque(['2981549002', '3105081694', '2950893734'], maxlen=3500)
    fetched_articles = {}
    b_count = 3
    browsers_empty_q_flags = [False for i in range(b_count)]
    for i in range(b_count):
        thread = Thread(target=open_browser_crawler, args=(i,))
        thread.start()
