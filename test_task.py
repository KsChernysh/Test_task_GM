from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
import logging
import sys
import time  # Для пауз
import requests

logging.basicConfig(filename='out.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def login_to_facebook():
    driver = None
    try:
        username = input("Enter your login (email): ")
        password = input("Enter your password: ")

        driver = webdriver.Chrome()
        driver.get("https://www.facebook.com/")
        logging.info("Facebook opened.")

        # Enter email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(username)

        # Enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pass"))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
      
        logging.info("Login submitted.")

        try:
            captcha = driver.find_element(By.CLASS_NAME, "captcha")
            if captcha:
                print("CAPTCHA found. Please solve it.")
                time.sleep(30) 
        except Exception as e:
            logging.info("CAPTCHA not found.")

        photo_url = driver.execute_script("""
            let imageElement = document.querySelector('svg image');
            return imageElement ? imageElement.getAttribute('xlink:href') : null;
        """)
        
        if photo_url:
            logging.info(f"Photo URL: {photo_url}")
            # Download the photo
            download_photo(photo_url)
        else:
            logging.error("Unable to find the photo URL.")
   
        # Download the photo
        download_photo(photo_url)

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

def download_photo(photo_url):
    try:
        response = requests.get(photo_url)
        with open("profile_picture.jpg", "wb") as file:
            file.write(response.content)
        logging.info("Profile picture downloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to download photo: {e}")

if __name__ == "__main__":
    login_to_facebook()
