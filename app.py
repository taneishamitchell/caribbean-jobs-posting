from datetime import datetime
import requests
from bs4 import BeautifulSoup as bSoup
import os

baseurl = "https://www.caribbeanjobs.com"
myurl = "{}{}".format(baseurl, "/ShowResults.aspx")
posting_path = os.getcwd() + '/'

# Query for all IT jobs in any location in the Caribbean and international
querystring = {"Keywords":"","Location":"","Category":"3","Recruiter":"All","btnSubmit":"%20","PerPage":"100","SortBy":"MostRecent"}

# Headers identified in Mozilla Web tools required to get to all rececnt job posting
headers = {
    'Host': "www.caribbeanjobs.com",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "en-US,en;q=0.5",
    'Accept-Encoding': "gzip, deflate, br",
    'Referer': "https://www.caribbeanjobs.com/ShowResults.aspx?Keywords=&Location=&Category=3&Recruiter=Company%2cAgency&btnSubmit=+&PerPage=50",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Cache-Control': "no-cache"
}

# save all result from CaribbeanJobs
response = requests.get(myurl, params=querystring)

# HTML parsing using BeautifulSoup package
doc = bSoup(response.text, 'html.parser')

# find all DIV tag with class MODULE JOB-RESULT
containers = doc.findAll("div",{"class":"module job-result"})


def jobpostfile():
    # open text file
    with open('posts.txt', 'w') as txtFile:

        # # cycle through the array & pull out job title, the     date it was posted and job post URL
        for container in containers:
            # strip job posting date and confirm if posted within the past week
            dateContainer = container.findAll("li", {"itemprop":"datePosted"})
            datePosted = (dateContainer[0].text).split(' ', 1)[1]
            fmtDate = datetime.strptime(datePosted, '%d/%m/%Y')
            checkAge = datetime.now() - fmtDate
            # print only postings less than 7 days old
            if checkAge.days <= 7:
                titleContainer = container.findAll('h2', {'itemprop':'title'})
                locationContainer = container.findAll('li', {'itemprop':'jobLocation'})
                txtFile.write('**Job Title:  ' + titleContainer[0].text + '**\n')
                txtFile.write('**Location:**  ' + locationContainer[0].text.strip('\n') + '\n')   # text was coming up with newline when printing include strip to eliminate
                txtFile.write('**Job Posting:**  ' + "{}{}".format(baseurl, container.h2.a['href']) + '\n')
                txtFile.write('**Date Posted:**  ' + datePosted + '\n')
                txtFile.write(47 * '-' + '\n')
