from bs4 import BeautifulSoup
import time
from time import sleep
from datetime import datetime
import requests
import csv

print(" Initializing ...")
print(" Loading Keywords")
with open("pcodes.txt") as pcodes:
    postkeys = []
    for line in pcodes:
        postkeys.append(line.strip())

with open("pcodnum.txt") as pcodnum:
    postkeynum = []
    for line in pcodnum:
        postkeynum.append(line.strip())

print(" Welcome to YellScrape v1.0")
print(" You ar searching yell.com ")

comtype = input(" Please enter a Company Type (e.g Newsagent, Barber): ")
pagesnum = 0
listinnum = 0
comloc = " "
f = csv.writer(open(datetime.today().strftime('%Y-%m-%d') + '-' + comtype + '-' + 'yelldata.csv', 'w'))
f.writerow(['Business Name', 'Business Type', 'Phone Number', 'Street Address', 'Locality', 'Region', 'Website'])

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

data_list = []
for x in postkeys:
    print(" Searching " + x + " for " + comtype + " companies")
    for y in postkeynum:
        url = 'https://www.yell.com/ucs/UcsSearchAction.do?keywords=' + comtype + '&pageNum=' + str(y) + '&location=' + x
        data_list.append(url)
        for item in data_list:
            site = requests.get(item, headers=headers)
            soup = BeautifulSoup(site.content, 'html.parser')
            questions = soup.select('.businessCapsule--mainContent')
            for question in questions:
                listinnum += 1
                busname = question.find(class_='businessCapsule--name').get_text()
                bustype =   question.find(class_='businessCapsule--classification').get_text()
                busnumber = question.select_one('span.business--telephoneNumber')
                if busnumber is None:
                    busnumber = 'None'
                else:
                    busnumber = busnumber.text
                busadd = question.find('span', attrs={"itemprop": "streetAddress"})
                if busadd is None:
                    busadd = 'None'
                else:
                    busadd = busadd.text.replace(',',' ')
                buslocal = question.find('span', attrs={"itemprop": "addressLocality"})
                if buslocal is None:
                    buslocal = 'None'
                else:
                    buslocal = buslocal.text
                buspost = question.find('span', attrs={"itemprop": "postalCode"})
                if buspost is None:
                    buspost = 'None'
                else:
                    buspost = buspost.text
                busweb = question.find('a', attrs={"rel": "nofollow noopener"})
                if busweb is None:
                    busweb = 'None'
                else:
                    busweb = busweb.attrs['href']
                print(busweb)
                f.writerow([busname, bustype, busnumber, busadd, buslocal, buspost, busweb])
            data_list = []

        pagesnum += 1
        print(" Finsihed Page " + str(y) + ". For " + x + " . " + str(listinnum) + " listings so far. Moving To Next Page")
    print(" Waiting 30 seconds for security reasons.")
    sleep(30)
print(" Finished. \n Total: " + str(pagesnum) + " pages with " + str(listinnum) + " listings. \n Please look for file: " + datetime.today().strftime('%Y-%m-%d') + '-' + comtype + '-' + 'yelldata.csv')
