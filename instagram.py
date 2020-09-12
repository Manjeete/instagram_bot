from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup
import time
import re
import csv


class InstgramBot(object):
    def __init__(self):
        self.instagram_url = "https://www.instagram.com/"
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.driver.maximize_window()
        
        self.driver.get(self.instagram_url)

    def login(self):
        self.driver.get(self.instagram_url)
        wait = WebDriverWait(self.driver, 5)
        username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        
        username.send_keys("<username>")
        time.sleep(2)
        password = self.driver.find_element_by_name('password')
        password.send_keys("<password>")
        time.sleep(2)
        login_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]')
        login_button.click()
        time.sleep(2)
        
    def write_to_csv(self,data):
        for d in data:
            profile_url = d['profile_url']
            username = d['username']
            posts = d['posts']
            followers = d['followers']
            following = d['following']
            email = d['email']
            website = d['website']
            category = d['category']
            last_post_url = d['last_post_url']
            last_post_date = d['last_post_date']
            with open("database.csv", mode='a', encoding="utf-8", newline='') as database:
                csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([profile_url,username,posts,followers,following,email,website,category,last_post_url,last_post_date])
            
    def get_followers_detail(self,profile_urls):
        data = []

        posts = ""
        followers = ""
        following = ""
        bio = ""
        website = ""
        email = ""
        category = ""
        last_post_date = ""
        last_post_url = ""

        for profile_url in profile_urls:
            username = profile_url.split('/')[3]
            try:
                self.driver.get(profile_url)
                time.sleep(2)
                wait = WebDriverWait(self.driver, 5)
                try:
                    posts = wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" posts"]/span'))).text
                except:
                    posts = wait.until(EC.presence_of_element_located((By.XPATH, '//li/span[text()=" post"]/span'))).text

                try:        
                    followers = wait.until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" followers"]/span'))).text
                except:
                    followers = wait.until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" follower"]/span'))).text
                

                try:        
                    following = wait.until(EC.presence_of_element_located((By.XPATH, '//li/a[text()=" following"]/span'))).text
                except:
                    following = ""  
                print('Posts: {}; Followers: {}; Following: {}.'.format(posts, followers, following))
                try:
                    category = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/div[2]/a[1]'))).text
                except:
                    category = ""  

                try:
                    bio = str(wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/div[2]/span'))).text)
                    email = re.findall('\S+@\S+', bio)[0]
                except:
                    bio = ""
                    email = ""    
                try:
                    website = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/div[2]/a[2]'))).text
                except:
                    website = ""
                time.sleep(2)    

                try:
                    last_post = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/div[2]/article/div/div/div[1]/div[1]/a/div[1]/div[2]')))
                    last_post.click()
                    time.sleep(5)
                    last_post_url = self.driver.current_url
                    last_post_date = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/article/div[3]/div[2]/a/time'))).get_attribute("datetime")
                    
                except:
                    last_post_date = ""
                    last_post_url = ""
                    last_post = ""    
                time.sleep(2)
            except:
                pass
            data.append({"profile_url":profile_url, "username":username, "posts":posts, "followers":followers, "following":following, "email":email,"website":website,"category":category,"last_post_url":last_post_url,"last_post_date":last_post_date})            

        return self.write_to_csv(data)                



    def follow(self,accounts):
        for account in accounts:
            self.driver.get(account)
            wait = WebDriverWait(self.driver, 5)
            try:
                # To follow someone
                try:
                    follow_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')))
                except:
                    follow_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/div[1]/button')))    
                if(follow_btn.text == "Follow"):
                    follow_btn.click()
                    time.sleep(2)
                    
                # To unfollow someone
                # try:
                #     unfollow_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button')))
                #     unfollow_btn.click()
                #     time.sleep(1)
                #     unfollow = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[1]')))
                #     unfollow.click()
                #     time.sleep(1)
                # except:
                #     unfollow_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/button')))
                #     unfollow_btn.click()
                #     time.sleep(1)
                #     unfollow = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[1]')))
                #     unfollow.click()
                #     time.sleep(1)

            except:
                pass        


    def get_followers(self,username,max):
        self.driver.get(f'https://www.instagram.com/{username}')
        followersLink = self.driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(5)
        popup = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]')))
        for h in range(10):
            print(h)
            print('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)))
            time.sleep(2)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)), popup)

        for i in range(200):
            time.sleep(1)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)

        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')

        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            try:
                userLink = user.find_element_by_css_selector('a').get_attribute('href')
                
            except:
                userLink =  f'https://www.instagram.com/manjeet_k7/'   
                
                
            print(userLink)
            followers.append(userLink)       
            if (len(followers) == max):
                break
        print(len(followers))        
        return self.follow(followers)



inst = InstgramBot()
inst.login()
inst.get_followers('<usernameoftargetuser>',100)

