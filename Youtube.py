from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
from dotenv import load_dotenv
import os
import time
from abc import ABC, abstractmethod
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
import random

class YouTubeScraper(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        pass
    
    @abstractmethod
    def scrape_video(self, video_id: str, message: str) -> any:
        pass

class MyYouTubeScraper(YouTubeScraper):
    def __init__(self):
        self.logged_in = False

    def login(self, username: str, password: str, driver: webdriver) -> bool:
        self.login = username
        self.login = password
        url = "https://accounts.google.com/v3/signin/identifier?dsh=S-1929078200%3A1679940808874536&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dpt%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&ec=65620&hl=pt-BR&ifkv=AQMjQ7QPBb3xRUc94Aqv1mWGzmcSWDWV3mm0nLGcuOx9ksl00CdE9wMysXJOdm5_JmTa-0mGMIU23Q&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
        driver.get(url)
        driver.find_element(
            By.ID,
            "identifierId"
            ).send_keys(username)
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span"
            ).click()
        time.sleep(7)
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
            ).send_keys(password)
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span"
            ).click()
        time.sleep(25)
        self.logged_in = True
        return self.logged_in



    def scrape_video(self, video_url: str, driver: webdriver, message: str) -> dict:

        # Checks for login
        if not self.logged_in:
            raise Exception("Must be logged in to scrape video.")

        # navigate to the YouTube video URL
        driver.get(video_url)
        time.sleep(3)

        parent_element = driver.find_element(By.ID, "contents")
        child_elements = parent_element.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer")
        child_elements_number = len(child_elements)
        print("Number of child elements: ", child_elements_number)

        comment_number = 1
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ENTER)
        for i in range(9): body.send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        parent_element = driver.find_element(By.ID, "contents")
        child_elements = parent_element.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer")
        child_elements_number = len(child_elements)
        while comment_number <= child_elements_number:

            if comment_number == child_elements_number:
                for i in range(30): body.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                parent_element = driver.find_element(By.ID, "contents")
                child_elements = parent_element.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer")
                child_elements_number = len(child_elements)

            # Get name account
            name = driver.find_element(
                By.XPATH,
                f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_number}]/ytd-comment-renderer/div[3]/div[2]/div[1]/div[2]/h3/a/span"
                ).get_attribute("innerHTML")
            round(random.uniform(2, 3), 3)

            # Define message
            messageFinal = f"Olá {name.strip()}, tudo bem? {message}"

            # Click Like Button
            driver.find_element(
                By.XPATH,
                f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_number}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[1]/ytd-toggle-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
                ).click()
            round(random.uniform(2, 3), 3)

            # Click RESPONSE toggle
            driver.find_element(
                By.XPATH,
                f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_number}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[1]/div[4]/ytd-button-renderer/yt-button-shape/button"
                ).click()
            round(random.uniform(2, 3), 3)

            # Input for ANSWER
            driver.find_element(
                By.XPATH, 
                f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_number}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[2]/ytd-comment-reply-dialog-renderer/ytd-commentbox/div[2]/div/div[2]/tp-yt-paper-input-container/div[2]/div/div[1]/ytd-emoji-input/yt-user-mention-autosuggest-input/yt-formatted-string/div"
                ).send_keys(
                f"{messageFinal}"
                )
            round(random.uniform(2, 3), 3)

            # Click SEND RESPONSE button
            z = driver.find_element(
                By.XPATH,
                f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_number}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[2]/ytd-comment-reply-dialog-renderer/ytd-commentbox/div[2]/div/div[4]/div[5]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
                ).click()
            time.sleep(round(random.uniform(20, 24), 3))

            comment_number += 1
            dfLog = pd.read_csv('LogYoutube.csv')
            dfLog.loc[len(dfLog['VideoUrl'])]=[datetime.datetime.now(), video_url, messageFinal, name.strip()]
            os.remove('LogYoutube.csv')
            dfLog.to_csv('LogYoutube.csv', index=False)
            
            # Break while
            if comment_number == child_elements_number:
                break
        return {}

def main(video_url, message):

    driver = webdriver.Chrome()
    load_dotenv()
    scraper = MyYouTubeScraper()

    # Login youtube
    scraper.login(os.getenv('YT_LOGIN'), os.getenv('YT_PASSWORD'), driver)

    # Scrape video
    scraper.scrape_video(video_url, driver, message)

if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=KmBkEGK6Qxg"
    url = "https://www.youtube.com/watch?v=qdlD-v4V3sM"
    message = "Já ouviu falar da *SetYou* ? Entre no nosso site, preencha um questionário de saúde em cerca de 5 minutos e *receba uma recomendação personalizada de vitaminas, minerais e fitoterápicos* ."
    main(url, message)
    print("End of comments!")


