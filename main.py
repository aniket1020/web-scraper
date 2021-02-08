import sqlite3
import requests
import time
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

if __name__ == '__main__':

    #Initialize the database
    try:
        db = sqlite3.connect('jobs.db')
        print("Connected to the database successfully")
    except:
        print("Error occurred when connecting to the database")
        quit()

    #Initialize the driver and url
    #search_query = 'nvidia corporation'
    search_query = input('Search Query : ')
    base_url = 'https://www.naukri.com/'
    url = base_url + f"{search_query.replace(' ','-')}-jobs?k={search_query}"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path='./geckodriver')
    print("Driver Initialized")
    jobUrls = []

    #Scrape the first page

    # headers = {
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding':'gzip, deflate, br',
    # 'Accept-Language':'en-US,en;q=0.5',
    # 'Cache-Control':'max-age=0',
    # 'Connection':'keep-alive',
    # 'Host':'www.naukri.com',
    # 'Referer':'https://www.naukri.com/python-jobs?k=python',
    # 'TE':'Trailers',
    # 'Upgrade-Insecure-Requests':'1',
    # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
    # }
    #
    # response = requests.get(url,headers=headers)
    # soup = BeautifulSoup(response.content, 'lxml')
    # print(soup.body.prettify())
    # quit()

    driver.get(url)
    time.sleep(2)
    print("Recieved the response for job listings")
    print(f"On Page 1")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    job_list = soup.find('div', class_='list')
    jobUrls.extend(zip(
        [it['data-job-id'] for it in job_list.find_all('article',class_='jobTuple bgWhite br4 mb-8')],
        [it['href'] for it in job_list.find_all('a', class_='title fw500 ellipsis')],
        [it['title'] for it in job_list.find_all('a', class_='title fw500 ellipsis')]
    ))

    #Search for the first 3 pages
    for page in range(2,4):
        print(f"On Page {page}")
        url = base_url + f"{search_query.replace(' ','-')}-jobs-{page}?k={search_query}"
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        job_list = soup.find('div', class_='list')
        jobUrls.extend(zip(
            [it['data-job-id'] for it in job_list.find_all('article',class_='jobTuple bgWhite br4 mb-8')],
            [it['href'] for it in job_list.find_all('a', class_='title fw500 ellipsis')],
            [it['title'] for it in job_list.find_all('a', class_='title fw500 ellipsis')]
        ))

    cnt = 1

    #Iterate through all the Job URLs
    print("Iterating through job URLs")
    for job_url in jobUrls:
        driver.get(job_url[1])
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        try :
            job_id = job_url[0]
            job_link = job_url[1]
            job_title = job_url[2]
            job_description = soup.find('div',class_='dang-inner-html').text
            job_requirement = ', '.join([it.find('span').text for it in soup.find('div',class_='key-skill').findChildren('a')])
            job_location = soup.find('span',class_='location').find('a').text
            job_salary = soup.find('div',class_='salary').find('span').text
            job_qualification = soup.find('div',class_='education').text
            job_type = soup.find('div',class_='other-details').select('div.details:nth-child(4) > span:nth-child(2) > span:nth-child(1)')[0].text
            job_experience = soup.find('div', class_='exp').find('span').text
        except Exception as e:
            print(f"Error Occurred {e}")
            print(f"Job url = {job_link}")
            traceback.print_exc()
            continue
        try:
            db.execute(
                'INSERT INTO JOBS values (?,?,?,?,?,?,?,?,?,?)',
                (job_id,job_link,job_title,job_description,job_requirement,job_location,job_salary,job_qualification,job_type,job_experience)
            )
            db.commit()
        except Exception as e:
            print(f"Error Occurred while inserting into the database : {e}")
            continue
        print("Added successfully")
    driver.close()
