import os
import random
import sys
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver

browser = webdriver.Chrome('C:\\Users\\DANISH\\PycharmProject\\Examples\\venv\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe')

browser.get('https://www.linkedin.com/uas/login')

with open('config.txt') as f:
    credentials = [x.strip().split(':', 1) for x in f]

for uname, paword in credentials:
    username = uname
    password = paword

elementid = browser.find_element_by_id('username')
elementid.send_keys(username)

elementid = browser.find_element_by_id('password')
elementid.send_keys(password)

elementid.submit()


visitingprofileid = 'danish-sharma-63623b14a/'
fulllink = 'https://www.linkedin.com/in/danish-sharma-63623b14a/'+'danish-sharma-63623b14a/'

browser.get(fulllink)

visitedprofiles = []
profilequeued = []

def get_new_profile_id(soup,profile):
    prof_id = []
    pav = soup.find('section',{'class':'pv-profile-section pv-browsemap-section profile-section artdeco-container-card ember-view'})
    all_links = soup.findAll('a',{'class':'pv-browsemap-section__member ember-view'})
    for link in all_links:
        user_id = link.get('href')

        if ((user_id not in profilequeued) and (user_id not in visitedprofiles)):
            prof_id.append(user_id)

    return prof_id
get_new_profile_id(BeautifulSoup(browser.page_source),profilequeued)

profilequeued = get_new_profile_id(BeautifulSoup(browser.page_source),profilequeued)

print(profilequeued)

while profilequeued:
    try:
        visitingProfileID = profilequeued.pop()
        visitedprofiles.append(visitingProfileID)
        fullLink = 'https://www.linkedin.com' + visitingProfileID
        browser.get(fullLink)

        browser.find_element_by_class_name('pv-s-profile-actions').click()

        browser.find_element_by_class_name('mr1').click()

        customMessage = "Hola!,This message is sent to you using a python bot"
        elementID = browser.find_element_by_id('custom-message')
        elementID.send_keys(customMessage)

        browser.find_element_by_class_name('ml1').click()

        # Add the ID to the visitedUsersFile
        with open('visitedUsers.txt', 'a') as visitedUsersFile:
            visitedUsersFile.write(str(visitingProfileID)+'\n')
        visitedUsersFile.close()

        # Get new profiles ID
        soup = BeautifulSoup(browser.page_source)
        try: 
            profilequeued.extend(get_new_profile_id(soup, profilequeued))
        except:
            print('Continue')

        # Pause
        time.sleep(random.uniform(5, 8)) # Otherwise, sleep to make sure everything loads

        if(len(visitedprofiles)%50==0):
            print('Visited Profiles: ', len(visitedprofiles))

        if(len(profilequeued)>100000):
            with open('profilesQueued.txt', 'a') as visitedUsersFile:
                visitedUsersFile.write(str(visitingProfileID)+'\n')
            visitedUsersFile.close()
            print('100,000 Done!!!')
            break;
    except:
        print('error')
