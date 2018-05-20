import requests
from bs4 import BeautifulSoup
import csv
from lxml import html

cookie_header = ''
username = '<your username>'
password = '<your password>'
login_url = 'https://amritavidya1.amrita.edu:8444/cas/login?service=https%3A%2F%2Famritavidya.amrita.edu%3A8444%2Faums%2FJsp%2FCommon%2Findex.jsp'
post_url = 'https://amritavidya1.amrita.edu:8444/aums/Jsp/StudentGrade/StudentPerformanceWithSurvey.jsp?action=UMS-EVAL_STUDPERFORMSURVEY_INIT_SCREEN&isMenu=true&pagePostSerialID=0'
get_url = 'https://amritavidya1.amrita.edu:8444/aums/Jsp/StudentGrade/StudentPerformanceWithSurvey.jsp?action=UMS-EVAL_STUDPERFORMSURVEY_INIT_SCREEN&isMenu=true&pagePostSerialID=1'


def grades():
    global cookie_header
    with requests.Session() as s:
        print("Navigating to login_url...")
        result = s.get(login_url)
        tree = html.fromstring(result.text)
        token = list(set(tree.xpath("//input[@name='lt']/@value")))[0]
        submit = list(set(tree.xpath("//input[@name='submit']/@value")))[0]
        _eventId = list(set(tree.xpath("//input[@name='_eventId']/@value")))[0]

        payload = {                   # Payload sent in Post Request
            "username": username,     # username and password are normal inputs
            "password": password,     # The rest are hidden inputs. Can be found using Right Click > Page Source
            "lt": token,
            "_eventId": _eventId,
            "submit": submit
        }

        print('Validating credentials...')
        results = s.post('https://amritavidya1.amrita.edu:8444/cas/login;jsessionid='+str(dict(result.cookies).get("JSESSIONID"))+'?service=https%3A%2F%2Famritavidya.amrita.edu%3A8444%2Faums%2FJsp%2FCommon%2Findex.jsp', data=payload, headers=dict(referer=login_url))  # Authenticating the credentials
        if results.ok:
            print('Login successful!')
        if not cookie_header:                   # Store the cookie and it'll be used in attendance_headers' cookie
            cookie_header = 'JSESSIONID='+str(dict(result.cookies).get("JSESSIONID"))+'; authorized_token=true; JSESSIONID1=0029f737-2613-40cf-90b7-4ae55b93454b.localhost'

        grades_headers = {
            'Host': 'amritavidya1.amrita.edu:8444',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': get_url,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '225',
            'Cookie': cookie_header,
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        grades_body = {
            'Page_refIndex_hidden': '1',
            'htmlPageTopContainer_selectStep': '9',
            'htmlPageTopContainer_hiddentblGrades': '',
            'htmlPageTopContainer_status': '',
            'htmlPageTopContainer_action': 'UMS-EVAL_STUDPERFORMSURVEY_CHANGESEM_SCREEN',
            'htmlPageTopContainer_notify': ''
        }

        r_post = s.post(post_url, data=grades_body, headers=grades_headers) # This is required. It does not work
        r_get = s.get(get_url, headers=grades_headers)                          # if only one request is made.
    with requests.Session() as req:
        r_post = req.post(post_url, data=grades_body, headers=grades_headers)
        r_get = req.get(get_url, headers=grades_headers)
        r_soup = BeautifulSoup(r_get.text, 'lxml')
        table = r_soup.findAll('tr', {'class': ""})              # Select only <tr class =""> elements
        with open('GradesReport.csv', 'w', newline='') as csvfile:  # Store the table values into a .csv file
            count = 0
            f = csv.writer(csvfile)
            for content in table:
                rows = content.find_all('tr')[10:]  # To strip unwanted values.
                for tr in rows: 
                    data = []
                    cols = tr.find_all('td')    
                    for td in cols:
                        if td.text.strip() == '':  
                            exit()
                        data.append(' '.join((td.text.strip()).split())) 
                    f.writerow(data)
                    print(data)


if __name__ == '__main__':
    grades()
