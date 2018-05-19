# AUMS Automator

A python script which allows you to fetch your Attendance and grades from AUMS, and store it in a csv file.

#### Status: 
Attendance Fetcher: Done!

Grades Fetcher: Done!

## Getting Started



### Prerequisites

Things you need before you start with the script


* [Python 3](https://www.python.org/download/releases/3.0/) (Preferably >= 3.4)
* [pip](https://pypi.org/project/pip/)
* [Requests module](http://docs.python-requests.org/en/master/)
* [Beautiful Soup module](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)



### Installing

#### Ubuntu/Debian OS:

1. If you are using Linux based systems, chances are high that Python3 is already installed in your system.
Check if it is installed by using:
```
python3 --version
```


2. Next install pip.
```
sudo apt install python3-pip
```
If that doesn't work, try using curl
```
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
```

3. Next, install all the required modules for running the scripts. Pre-requisites can be found above.
```
pip3 install requests
pip3 install BeautifulSoup4
```

#### Windows OS:

1. If you are using Windows, download the installer from [here](https://www.python.org/downloads/windows/).

	[Python and pip installation for Windows](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)
    
2. Install the required modules for running the script
```
pip install requests
pip install BeautifulSoup4
```

#### Mac OS:
1. Mac already comes with Python installed in it. You can check if it is installed in your system by using
```
python --version
```

2. Install pip by using easy_install.

```
sudo easy_install pip

```

or
1. Install [Homebrew](https://brew.sh/) and run the following command to get install the latest Python, pip and setuptools.

```
brew install python

```



## Deployment

Before running this script, there are few changes to be made in the script.

1. Open the script with your favorite text editor.
2. There are two variables namely 'username' and 'password' where you have to input your respective credentials for authentication.
3. Now, you can run the script by double clicking it (or) running it in the IDE of your choice. (PyCharm was my favorite) (or) 
```
python3 StudentAttendanceSummary.py
python3 GradesSummary.py
```

4. Just wait for the script to finish. Once it is completed, a csv file with the name 'AttendanceReport.csv' will be generated. Open the file with LibreOffice Calc or Microsoft Excel to view your Attendance (or) Grades. 

If you want to change the semester of your Attendance (or) Grade, make changes to 'htmlPageTopContainer_selectSem' field in 'attendance_body' or 'grades_body' respectively.

```
'htmlPageTopContainer_selectSem': '7'	->	First Semester
'htmlPageTopContainer_selectSem': '8'	->	Second Semester
'htmlPageTopContainer_selectSem': '9'	->	Third Semester
'htmlPageTopContainer_selectSem': '10'	->	Fourth Semester
'htmlPageTopContainer_selectSem': '11'	->	Fifth Semester
'htmlPageTopContainer_selectSem': '12'	->	Sixth Semester
'htmlPageTopContainer_selectSem': '13'	->	Seventh Semester
'htmlPageTopContainer_selectSem': '14'	->	Eight Semester
```

Sometimes, the college uses different domains for the website. So, there'll be a problem of not getting response from the server. In those situations, try changing hostname of 'login_url', 'post_url', 'get_url' to either of these

```
'https://amritavidya.amrita.edu:8444/...
'https://amritavidya1.amrita.edu:8444/...
'https://amritavidya2.amrita.edu:8444/...
```



## Built With

* [Python](https://www.python.org/download/releases/3.0/) - The programming language used
* [Pycharm Community](https://maven.apache.org/) - IDE for Python


## Authors

* **Viswanath M**  - [viswanathm97](https://github.com/viswanathm97)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thanks to the folks at [stackoverflow](https://stackoverflow.com/) for helping me when I was in desperate need for solution and [Google](https://www.google.com/) for bringing me the appropriate search results.


