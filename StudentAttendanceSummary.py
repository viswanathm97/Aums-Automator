import requests
from bs4 import BeautifulSoup
import csv
from lxml import html

cookie_header = ''
username = '<your username>'
password = '<your password'
login_url = 'https://amritavidya1.amrita.edu:8444/cas/login?service=https%3A%2F%2Famritavidya.amrita.edu%3A8444%2Faums%2FJsp%2FCommon%2Findex.jsp'
post_url = 'https://amritavidya1.amrita.edu:8444/aums/Jsp/Attendance/AttendanceReportStudent.jsp?action=UMS-ATD_INIT_ATDREPORTSTUD_SCREEN&isMenu=true&pagePostSerialID=0'
get_url = 'https://amritavidya1.amrita.edu:8444/aums/Jsp/Attendance/AttendanceReportStudent.jsp?action=UMS-ATD_INIT_ATDREPORTSTUD_SCREEN&isMenu=true&pagePostSerialID=1'


def attendance():
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
        jsessionid = str(dict(result.cookies).get("JSESSIONID"))
        print(jsessionid)
        print('Validating credentials...')
        results = s.post('https://amritavidya1.amrita.edu:8444/cas/login;jsessionid='+jsessionid+'?service=https%3A%2F%2Famritavidya.amrita.edu%3A8444%2Faums%2FJsp%2FCommon%2Findex.jsp', data=payload, headers=dict(referer=login_url))  # Authenticating the credentials
        if results.ok:
            print('Login successful!')
        if not cookie_header:                   # Store the cookie and it'll be used in attendance_headers' cookie
            cookie_header = 'JSESSIONID='+jsessionid+'; authorized_token=true; JSESSIONID1=0029f737-2613-40cf-90b7-4ae55b93454b.localhost'

        attendance_body = {                     # To be attached with Post request(For attendance fetching)
            'htmlPageTopContainer_txtrollnumber': '',
            'Page_refIndex_hidden': '',
            'htmlPageTopContainer_selectSem': '9',
            'htmlPageTopContainer_selectCourse': '0',
            'htmlPageTopContainer_selectType': '1',
            'htmlPageTopContainer_hiddentSummary': '',
            'htmlPageTopContainer_status': '',
            'htmlPageTopContainer_action': 'UMS-ATD_SHOW_ATDSUMMARY_SCREEN',
            'htmlPageTopContainer_notify': '',
            'htmlPageTopContainer_hidrollNo': 'Student'
        }

        attendance_headers = {                  # To be attaached with Post request(Cookie is key element here)
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Length': '355',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie_header,
            'DNT': '1',
            'Host': 'amritavidya1.amrita.edu:8444',
            'Referer': get_url,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        r_post = s.post(post_url, data=attendance_body, headers=attendance_headers) # This is required. It does not work
        r_get = s.get(get_url, headers=attendance_headers)                          # if only one request is made.

    with requests.Session() as req:
        r_post = req.post(post_url, data=attendance_body, headers=attendance_headers)
        r_get = req.get(get_url, headers=attendance_headers)
        r_soup = BeautifulSoup(r_get.text, 'lxml')
        table = r_soup.findAll('tr', {'class': ""})              # Select only <tr class =""> elements

        with open('AttendanceReport.csv', 'w', newline='') as csvfile:  # Store the table values into a .csv file
            count = 0
            f = csv.writer(csvfile)
            for content in table:
                rows = content.find_all('tr')[6:]
                for tr in rows:
                    if count % 2 != 0 or count == 0:    # Table has 'total' value. This is used to avoid those.
                        if tr is None:
                            continue
                        else:
                            data = []
                            cols = tr.find_all('td')    # Select all the <td> tags within <tr class ="">
                            for td in cols:
                                if td.text.strip() == '':  # When empty string is encountered, stop the code
                                    exit()
                                data.append(' '.join((td.text.strip()).split()))  # Else, append and add the data to csv
                            f.writerow(data)
                            print(data)
                    count += 1


if __name__ == '__main__':
    attendance()
