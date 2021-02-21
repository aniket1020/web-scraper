import sqlite3
import time
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from timesjobs import jobs

if __name__ == '__main__':
    #Initialize the database
    try:
        db = sqlite3.connect('jobs.db')
        print("Connected to the database successfully")
    except:
        print("Error occurred when connecting to the database")
        quit()

    with open('job_titles.txt') as inp:
        search_queries = inp.read().split(',')

    #Initialize the driver and url
    session = HTMLSession()

    for query in search_queries:
        search_query = query[1:-1]
        print('topic - ',search_query)
        base_url = 'https://www.naukri.com/'
        url = base_url + f"{search_query.replace(' ','-')}-jobs?k={search_query}"
        print("Starting the scraper")

        #Searching Naukri.com
        print("---> On Naukri.com <---")
        jobUrls = []
        r = session.get(url)
        r.html.render()
        soup = BeautifulSoup(r.html.raw_html, 'lxml')
        print("Recieved the response for job listings")
        print("On Page 1")
        try:
            job_list = soup.find('div', class_='list')
            jb_ls_a = job_list.find_all('a', class_='title fw500 ellipsis')
            jobUrls.extend(zip(
                [it['data-job-id'] for it in job_list.find_all('article',class_='jobTuple bgWhite br4 mb-8')],
                [it['href'] for it in jb_ls_a],
                [it['title'] for it in jb_ls_a]
            ))
        except Exception as e:
            print(f"Error Occurred : {e}")
        #Iterate through all the Job URLs
        print("Iterating through job URLs")
        for job_url in jobUrls:
            r = session.get(job_url[1])
            r.html.render()
            soup = BeautifulSoup(r.html.raw_html, 'lxml')
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
                print(f"Error - Custom Webpage")
                print(f"Job url = {job_link}")
                continue
            try:
                db.execute(
                    'INSERT INTO JOBS values (?,?,?,?,?,?,?,?,?,?,?)',
                    (job_id,search_query,job_link,job_title,job_description,job_requirement,job_location,job_salary,job_qualification,job_type,job_experience)
                )
                db.commit()
            except Exception as e:
                print(f"Error Occurred while inserting into the database : {e}")
                continue
            print("Added successfully")

        #Searching Indeed
        print("---> On Indeed.com <---")
        jobUrls = []
        url = f"https://in.indeed.com/jobs?q={search_query.replace(' ','+')}&l="
        r = session.get(url)
        r.html.render()
        soup = BeautifulSoup(r.html.raw_html, 'lxml')
        print("Recieved the response for job listings")
        print("On Page 1")
        job_list = soup.find_all('div',class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
        jb_ls_loc = soup.find_all('span',class_='location')
        jb_ls_a = soup.find_all('a',class_="jobtitle turnstileLink")
        jobUrls.extend(zip(
            [it['id'] for it in job_list],
            [it['href'] for it in jb_ls_a],
            [it.text for it in jb_ls_a],
            [it.find('span',class_='salaryText').text if it.find('span',class_='salaryText') is not None else 'N/A' for it in job_list],
            [it.text for it in jb_ls_loc],
            [it.find('div',class_='summary').text for it in job_list]
        ))
        for job_url in jobUrls:
            r = session.get('https://in.indeed.com/'+job_url[1][1:])
            r.html.render()
            soup = BeautifulSoup(r.html.raw_html,'lxml')

            job_id = job_url[0]
            job_link = job_url[1]
            job_title = job_url[2]
            job_description = soup.find('div',{'id':'jobDescriptionText'}).text
            job_salary = job_url[3]
            job_location=job_url[4]
            job_requirement = job_url[5]
            
            try:
                db.execute(
                    'INSERT INTO JOBS values (?,?,?,?,?,?,?,?,?,?,?)',
                    (job_id,search_query,job_link,job_title,job_description,job_requirement,job_location,job_salary,"N/A","N/A","N/A")
                )
                db.commit()
            except Exception as e:
                print(f"Error Occurred while inserting into the database : {e}")
                continue
            print("Added successfully")

        #Searching timesjobs.com
        print("---> On timesjobs.com <---")
        jobUrls = []
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={search_query.replace(' ','-')}&txtLocation="
        r = session.get(url)
        r.html.render()
        soup = BeautifulSoup(r.html.raw_html,'lxml')
        print("Recieved the response for job listings")
        print("On Page 1")
        job_list = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
        jb_ls_header = [jb.find('header',class_='clearfix') for jb in job_list]
        jb_ls_a = [jb.find('a') for jb in jb_ls_header]
        jobUrls.extend(zip(
            [re.search(r"(?<=jobid-)(.+?(?=__))",it['href']).group() for it in jb_ls_a],
            [it['href'] for it in jb_ls_a],
            [it.text for it in jb_ls_a]
        ))

        for job_url in jobUrls:
            job_id = job_url[0]
            job_link = job_url[1]
            job_title = job_url[2]

            try:
                (
                company,
                time_period,
                job_salary,
                job_location,
                job_description,
                job_details,
                job_requirement,
                company_details_dict
                )=jobs(job_url[1])
            except:
                continue
            
            try:
                db.execute(
                    'INSERT INTO JOBS values (?,?,?,?,?,?,?,?,?,?,?)',
                    (job_id,search_query,job_link,job_title,job_description,job_requirement,job_location,job_salary,"N/A","N/A","N/A")
                )
                db.commit()
            except Exception as e:
                print(f"Error Occurred while inserting into the database : {e}")
                continue
            print("Added successfully")

        print(f"Scraper completed for query {search_query}")
    print("Scraping Completed")