# use the print statements to check the data extracted


# BeautifulSoup
import requests
from bs4 import BeautifulSoup

def jobs(url):
    r = requests.get(url, 'html.parser')
    soup = BeautifulSoup(r.content, features='lxml')

    # company
    company = soup.find("div", class_="jd-header wht-shd-bx").h2.text.strip()
    # print(company)

    # time variable(time_period)
    time_period_list = soup.find(
        "div", class_="jd-header wht-shd-bx").ul.li.text.replace('card_travel', " ").split()
    time_period = ''
    for i in time_period_list:
        time_period = time_period + i + " "
    # print(time_period)

    # stipend/salary
    salary_list = soup.find(
        "div", class_="jd-header wht-shd-bx").ul.find_all('li')[1].text.split()
    salary = ''
    for i in salary_list:
        salary = salary + i + " "
    # print(salary)

    # location
    location = soup.find(
        "div", class_="jd-header wht-shd-bx").ul.find_all('li')[2].text.replace('location_on', " ").strip()
    # print(location)

    # job description
    # Replace br tag with newline
    for br in soup.find_all("br"):
        br.replace_with("\n")
    description_list = soup.find(
        'div', class_='jd-desc job-description-main').text.replace('Job Description', "").strip().split("\n")
    description = " "
    for i in description_list:
        if(i == ""):
            description = description + "\n"
        else:
            description = description + i
    # print(description)

    # job function
    job_function = soup.find(
        'div', class_='job-basic-info').ul.find_all('li', class_='clearfix')
    job_details = {}
    for i in job_function:
        j = i.label.text
        ans = i.text.replace(j, " ").strip()
        job_details[j] = ans
    # print(job_details)

    # skills required
    skills = soup.find(
        'div', 'jd-sec job-skills clearfix').find_all('a')
    skills_required = " "
    for i in skills:
        skills_required = skills_required + i.text + " "
    # print(skills_required)

    # company details
    company_details = soup.find(
        'div', 'jd-sec jd-hiring-comp').find_all('li')
    company_details_dict = {}
    for i in company_details:
        j = i.label.text
        ans = i.text.replace(j, " ").strip()
        company_details_dict[j] = ans
    # print(company_details_dict)

    # on hold
    # facebook , linkedin, twitter
    # not really useful can add if we want to
    # facebook = soup.find('a', class_='addthis_button_facebook')
    # twitter = soup.find('a', class_='addthis_button_twitter')
    # linkedin = soup.find('a', class_='addthis_button_linkedin')
    # print(linkedin)

    # calling the database
    return (company, time_period, salary, location,
            description, job_details, skills_required, company_details_dict)
