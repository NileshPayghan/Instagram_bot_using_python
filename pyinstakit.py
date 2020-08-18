from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
import sys

# self.profile = "https://www.instagram.com/" + self.username + "/"

class InstagramLogin:
    """
    param:
    username => username of instagram
    password => password for specified username
    logintimeout => which is generally used when login form is loading to sleep for particular time, short time of period 2 to 5, 
                    but you can give time according to your internet connection strength.
    loadingtimeout => which is used generally for page loading on instagram, waiting period long ex. 6 , 
                    but you can give any time, but give it according to internet connection strength.
                    If the internet is high then use short time otherwise give long time to wait to load page.
    turn_on_notification => To turn on notification pass the boolean True otherwise False.
                        False is default value for this parameter. It means it won't show any notification while login.
    save_password => If you want to save password then make it True otherwise False.
                    False is default value for this parameter. It means it won't save password.

    """
    def __init__(self, username=None, password=None, logintimeout=2, loadingtimeout=6, turn_on_notification=False, save_password=False):
        self.username = username
        self.password = password
        self.logintimeout = logintimeout
        self.loadingtimeout = loadingtimeout
        self.webdriver = webdriver.Firefox() # we can also go with Chrome() webdriver.
        sleep(randint(self.logintimeout, self.logintimeout + 3))
        self.webdriver.get("https://www.instagram.com/accounts/login/")

        # details of visited users and posts
        self.prev_username_list = {}
        self.posts_visited = 0


        # must run first these three methods
        self.__login()
        self.__save_password_or_not(save_password)
        self.__turn_on_off_notifications(turn_on_notification)
    
    def __login(self):
        sleep(randint(self.logintimeout, self.logintimeout + 3))
        print(f"Entered username: {self.username}")
        print(f"Entered password: {self.password}")
        try:
            username = self.webdriver.find_element_by_name('username')
            # print(f"Entered username: {self.username}")
            username.send_keys(self.username)
            sleep(randint(self.logintimeout, self.logintimeout + 3))
            password = self.webdriver.find_element_by_name('password')
            # print(f"Entered password: {self.password}")
            password.send_keys(self.password)
            sleep(randint(self.logintimeout, self.logintimeout + 3))
            button_login = self.webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button')
            button_login.click()
            sleep(randint(self.logintimeout, self.logintimeout + 3))
            print("INFO: We are logged in to instagram account")
        except:
            print("ERROR: username and password not found")
            self.webdriver.close()
    
    def __save_password_or_not(self, save_password=False):
        sleep(randint(self.logintimeout, self.logintimeout + 3))
        try:
            #If we are login first time then we will face the notnow or saveinfo button Choose your choice
            # I used only notnow button here
            #See Extract_css_selector_path.txt for more details of css selector of notnow button
            #comment following 3 lines if you don't want to save the password
            if not save_password:
                button_notnow = self.webdriver.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button")
                button_notnow.click()
                sleep(randint(self.logintimeout, self.logintimeout + 3))
            else:
                #uncomment following 3 lines if you want save the password.
                button_saveinfo = self.webdriver.find_element_by_css_selector("#react-root > section > main > div > div > div > section > div > button.sqdOP:nth-child(4)")
                button_saveinfo.click()
                sleep(randint(self.logintimeout, self.logintimeout + 3))
            print("NotNow button successfully passed.")
        except:
            print("Save Info or Not Now not worked Or it does not appear on the screen.")
            raise "Please check internet connection strength."
        sleep(randint(self.logintimeout, self.logintimeout + 3))
    
    def __turn_on_off_notifications(self, turn_on_notification=False):
        sleep(randint(self.logintimeout, self.logintimeout + 3))
        try:
            #turn off the notification by clicking Not Now button
            if not turn_on_notification:
                button_notification_off = self.webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm")
                button_notification_off.click()
                sleep(randint(self.logintimeout, self.logintimeout + 3))
            else:
                #If you want to turn on the notifications then click on Turn On button
                button_notification_on = self.webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.bIiDR")
                button_notification_on.click()
            print("Notification button successfully passed.")
            sleep(randint(self.logintimeout, self.logintimeout + 3))
        except:
            print("Notification does not on or off Or screen does not appear on the screen")
            raise "Please check internet connection strength."


    
    def open_hashtags(self, hashtag_list_search=[], number_of_posts_per_hashtags=5):
        """False
        Search every hashtag using base url of hashtags in instagram
        param:
        hashtag_list_search => list of hashtags that want to search
        number_of_posts_per_hashtags => number of posts want to visit in that hashtags
        """
        
        hashtag_base_url = "https://www.instagram.com/explore/tags/"

        for hashtag in range(len(hashtag_list_search)):
            self.webdriver.get(hashtag_base_url + hashtag_list_search[hashtag] + '/')
            sleep(randint(self.loadingtimeout, self.loadingtimeout + 4))
            try:
                first_top_posts = self.webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
            except:
                print(f"Sorry, This page doesn't available for {hashtag_list_search[hashtag]}")
                continue #continue to the next hashtag and report if it is not searched in hashtag list
            first_top_posts.click()#This will opens first thumbnail of from Top posts from opened hashtag
            sleep(randint(self.loadingtimeout, self.loadingtimeout + 4))
            for post_number in range(number_of_posts_per_hashtags):
                post_username = self.webdriver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div/header/div[2]/div[1]/div[1]/span/a")
                # print(f'{post_username.text}')
                post_username = post_username.text  #username of which found this hashtag

                if post_username not in self.prev_username_list:
                    self.prev_username_list[post_username] = 0 #initial likes starts from zero for particular user name/
                    self.webdriver.find_element_by_link_text('Next').click()
                    sleep(randint(self.logintimeout, self.logintimeout + 3)) #needs here short time
                    self.posts_visited += 1
                else:
                    self.webdriver.find_element_by_link_text('Next').click()
                    self.prev_username_list[post_username] += 1 #incrase the like of same username with another posts 
                    sleep(randint(self.logintimeout, self.logintimeout + 3)) #needs here short time
                    self.posts_visited += 1
            
            if(hashtag_list_search[-1] == hashtag_list_search[hashtag]):
                print("This is last hash tag we are going through it.!")
            else:
                print(f"Shifting towards Next hashtag {hashtag_list_search[hashtag+1]}.")

    def show_details(self, likes=True, comments=True, visited_users=True):
        print(f"Number of users visited: {len(self.prev_username_list)}")
        print(f"Number of posts visited: {self.posts_visited}")
        print(self.prev_username_list)

        

def main():
    username = input("Enter your instagram username: ")
    password = input(f"Enter your speicified '{username}' instagram password: ")
    insta = InstagramLogin(username, password,logintimeout=2, loadingtimeout=3)

    # Now to go through hashtags.
    with open("hashtags.txt","r") as open_file:
        hashtags_search_list = open_file.read().splitlines()
        print(hashtags_search_list)
    insta.open_hashtags(hashtags_search_list, number_of_posts_per_hashtags=3)
    insta.show_details()


if __name__ == '__main__':
    main()
