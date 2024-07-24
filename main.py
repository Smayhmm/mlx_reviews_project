import subprocess
import os
import json
import hashlib
import requests
import pyperclip
import openpyxl
import string
import time
import Credentials
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import chromedriver_autoinstaller
from random import choice, randint
from faker import Faker

API_GPT = Credentials.API_GPT
token = Credentials.AUTOMATION_TOKEN
FOLDERID = Credentials.FOLDER_ID
REVIEW_LINK = Credentials.REVIEW_LINK
MLX_BASE = "https://api.multilogin.com"
URL = "https://launcher.mlx.yt:45001/api/v2/profile" 
    #For profile create: "https://launcher.mlx.yt:45001/api/v2/profile"
    #For quick profile:  "https://launcher.mlx.yt:45001/api/v2/profile/quick"
LAUNCHER = "https://launcher.mlx.yt:45001/api/v2" #Verified!
LAUNCHERV1 = "https://launcher.mlx.yt:45001/api/v1"
LOCALHOST = "http://127.0.0.1"
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}



FAKE = Faker()
RANDOM_NAMES_LIST    = [FAKE.name() for _ in range(50)]
RANDOM_COMPANY_NAMES = [FAKE.company() for _ in range(50)]
CHARS_DIGITS_SYMBOLS = string.ascii_letters + string.digits + '!#$%&'
RANDOM_PHONE_NUMBERS = [(f"+1{randint(100, 999)}"
                        f"{randint(100, 999)}{randint(1000, 9999)}")
                        for _ in range(50)]
PASSWORD_ACCOUNT = "".join(choice(CHARS_DIGITS_SYMBOLS) for _ in range(14))
GMAIL_EMAIL_ADDITION = ''.join([choice(string.ascii_lowercase
                                       + string.digits) for _ in range(6)])
FILE_WITH_DATA = 'Google Reviews Project/folder/platform-accounts.txt'


# SMS Pool details
API_KEY = Credentials.API_KEY
SERVICE_ID = 395
endpoint_sms_order = 'https://api.smspool.net/purchase/sms'
endpoint_check_sms = 'https://api.smspool.net/sms/check'
endpoint_active_orders = 'https://api.smspool.net/request/active'
countries_ids = {
    'SE': 6,
    'US': 1,
    'TW': 54,
    'DE': 24,
    'UK': 2
}
params_order_sms = {
    'key': API_KEY,
    'country': countries_ids['UK'],
    'service': SERVICE_ID,
    'max_price': 0.60,
    'pricing_option': 1,
    'quantity': 1,
    'areacode': '',
    'exclude': ''
}
params_active_order = {
    'key': API_KEY,
}


gmail_elements = {
    'gmail_next': '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button',
    'select_day': '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[2]/div/div/div[1]/div/div[1]/input',
    'select_year': '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[3]/div/div/div[1]/div/div[1]/input',
    'select_gender': '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/select',
    'choose_full_address': '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div',
    'gmail_input_email_address': '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div[1]/div/div[1]/input',
    'gmail_skip': '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/'
                  'div/div[2]/div/div/div[2]/div/div/button',
    'gmail_next_2': '/html/body/div[1]/div[1]/div[2]/div/div[2]/'
                    'div/div/div[2]/div/div[2]/div/div/div/div/button',
    'gmail_express': '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div[2]'
                     '/div[2]/div/div[1]/div/form/span/section/div/div/'
                     'div/div/div[1]/div/span/div[1]/div/div[1]/div'
}


def create_profile(proxy, FOLDERID):
    url = "https://api.multilogin.com/profile/create"
    body = {
        "name": "Teste",
        "browser_type": "mimic",
        "folder_id": FOLDERID,
        "os_type": "windows",
        "parameters": {
            "proxy": {
                "host": proxy['host'],
                "type": "http",
                "port": int(proxy['port']),
                "username": proxy['username'],
                "password": proxy['password']
            },
            "flags": {
                "audio_masking": "natural",
                "fonts_masking": "mask",
                "geolocation_masking": "mask",
                "geolocation_popup": "allow",
                "graphics_masking": "natural",
                "graphics_noise": "natural",
                "localization_masking": "mask",
                "media_devices_masking": "natural",
                "navigator_masking": "mask",
                "ports_masking": "natural",
                "proxy_masking": "custom",
                "screen_masking": "natural",
                "timezone_masking": "mask",
                "webrtc_masking": "mask"
            },
            "storage": {
                "is_local": False,
                "save_service_worker": True
            },
        "fingerprint": {}
        }
    }
    
    response = requests.post(url=url, headers=HEADERS, json=body)
    response_json = response.json()
    print(response_json)
    PROFILEID = response_json['data']['ids'][0]
    print(f'ProfileID is {PROFILEID}')
    return PROFILEID
    
def get_proxy(token):
    url = "https://profile-proxy.multilogin.com/v1/proxy/connection_url"
    body = {
            "country": "uk",
            "sessionType": "sticky",
            "protocol": "http"
    }
    headers = {
        "Authorization": f'Bearer {token}'
    }
    response = requests.post(url=url, headers=headers, json=body).json()
    proxy_settings = response['data'].split(":")
    proxy = {}
    proxy['host'] = proxy_settings[0]
    proxy['port'] = proxy_settings[1]
    proxy['username'] = proxy_settings[2]
    proxy['password'] = proxy_settings[3]

    return proxy

def start_quick_profile(proxy):
    body = {
        "browser_type": "stealthfox",
        "os_type": "windows",
        "automation": "selenium",
        "is_headless": False,
        "proxy": {
            "host": proxy['host'],
            "type": "http",
            "port": int(proxy['port']),  # Ensure port is an integer
            "username": proxy['username'],
            "password": proxy['password']
        },
        "parameters": {
            "fingerprint": {
                "cmd_params": {
                    "params": [
                        {
                            "flag": "disable-notifications",
                            "value": "true"
                        }
                    ]
                }
            },
            "flags": {
                "audio_masking": "natural",
                "fonts_masking": "mask",
                "geolocation_masking": "mask",
                "geolocation_popup": "allow",
                "graphics_masking": "natural",
                "graphics_noise": "natural",
                "localization_masking": "mask",
                "media_devices_masking": "natural",
                "navigator_masking": "mask",
                "ports_masking": "natural",
                "proxy_masking": "custom",
                "screen_masking": "natural",
                "timezone_masking": "mask",
                "webrtc_masking": "mask"
            }
        }
    }
    
    print(f"Quick profile payload: {body}")
    
    response = requests.post(url=URL, headers=HEADERS, json=body)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    if response.status_code != 200:
        raise Exception(f"Failed to start quick profile: {response.text}")
    
    response_json = response.json()
    
    if "data" not in response_json:
        raise KeyError(f"'data' key not found in response: {response_json}")
    
    profile_port = response_json["data"]["port"]
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Remote(command_executor=f'{LOCALHOST}:{profile_port}', options=options)
    
    return driver

def start_profile() -> webdriver:
    if not PROFILEID:
        raise ValueError("Profile ID is required to start the profile.")
    
    r = requests.get(
        f"{LAUNCHER}/profile/f/{FOLDERID}/p/{PROFILEID}/start?automation_type=selenium",
        headers=HEADERS,
    )
    response = r.json()
    if r.status_code != 200:
        print(f"\nError while starting profile: {r.text}\n")
    else:
        print(f"\nProfile {PROFILEID} started.\n")
    selenium_port = response["data"]["port"]
    driver = webdriver.Remote(
        command_executor=f"{LOCALHOST}:{selenium_port}", options=ChromiumOptions()
    )

    return driver

def create_order():
    response_order_sms = requests.get(endpoint_sms_order, params=params_order_sms)
    if response_order_sms.status_code == 200:
        print(f'Number has been created')
    else:
        print(f'Creating order: {response_order_sms.status_code} has occurred')

def main(driver):
    max_attempts = 10
    attempts = 0
    create_order()
    number = retrieve_number()
    name = choice(RANDOM_NAMES_LIST)
    gmail_address = ''
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()
    
    driver.get(
        "https://accounts.google.com/v3/signin/identifier?continue=https://"
        "mail.google.com/mail/&service=mail"
        "&theme=glif&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

    wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[contains(., 'Create')]"))).click()

    try:
        wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[contains(., 'personal')]"))).click()
    except:
        print("No second question")
    
    first_name = wait.until(EC.presence_of_element_located((
        By.XPATH, "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/input")))

    first_name.send_keys(name)

    wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[contains(., 'Next')]"))).click()
    
    
    #try:
    #    month_element = wait.until(EC.element_to_be_clickable((By.ID, "month")))
    #    driver.execute_script("arguments[0].click();", month_element)
    #    month = Select(month_element)
    #    month.select_by_index(randint(1, 12))
    #except Exception as e:
    #    print(f"Exception encountered: {e}")


    month_element = Select(wait.until(EC.element_to_be_clickable((
        By.ID, "month"))))
    
    time.sleep(3)
    
    month_element.select_by_index(randint(1, 12))
    

    (wait.until(EC.visibility_of_element_located((
        By.XPATH, gmail_elements['select_day'])))
     .send_keys(str(randint(1, 25))))
    

    (wait.until(EC.visibility_of_element_located((
        By.XPATH, gmail_elements['select_year'])))
     .send_keys(str(randint(1960, 2003))))

    gender = Select(wait.until(EC.visibility_of_element_located((
        By.XPATH, gmail_elements['select_gender']))))
    gender.select_by_value('3')

    wait.until(EC.element_to_be_clickable((
        By.XPATH, gmail_elements['gmail_next']))).click()
    sleep(4)

    try:
        gmail_element = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[1]/div/div[2]/div[1]/div')))
        
        gmail_address += gmail_element.text
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[1]/div/div[2]/div[1]/div'))).click()

    except TimeoutException:
        gmail_address = name.replace(' ', '') + GMAIL_EMAIL_ADDITION
        (wait.until(EC.visibility_of_element_located((
            By.XPATH, gmail_elements['gmail_input_email_address'])))
         .send_keys(gmail_address))

    wait.until(EC.element_to_be_clickable((
        By.XPATH, gmail_elements['gmail_next']))).click()

    wait.until(EC.visibility_of_element_located((
        By.NAME, 'Passwd'))).send_keys(PASSWORD_ACCOUNT)
    sleep(1)

    wait.until(EC.visibility_of_element_located((
        By.NAME, 'PasswdAgain'))).send_keys(PASSWORD_ACCOUNT)

    wait.until(EC.element_to_be_clickable((
        By.XPATH, gmail_elements['gmail_next']))).click()

    wait.until(EC.visibility_of_element_located((
        By.ID, 'phoneNumberId'))).clear()
    sleep(1)

    wait.until(EC.visibility_of_element_located((
        By.ID, 'phoneNumberId'))).send_keys(number) 
    print(f'{"+"}+{number}')

    wait.until(EC.element_to_be_clickable((
        By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div/button/span'))).click()

    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((
            By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div[2]/div/div[2]/div[2]/div')))
        #create_gmail_account(driver)
    except TimeoutException:
        pass

    code = get_code()
    while code == '0' and attempts < max_attempts:
        sleep(7)
        code = get_code()
        attempts += 1

    wait.until(EC.visibility_of_element_located((
        By.NAME, 'code'))).send_keys(code)

    wait.until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="next"]/div/button/span'))).click()
    sleep(5)
    
    wait.until(EC.element_to_be_clickable((
        By.XPATH, '//span[text()="Skip"]'))).click()  #Confirmation Email
    sleep(5)
 
    wait.until(EC.element_to_be_clickable((
        By.XPATH, '//span[text()="Next"]'))).click() #Next Button
    sleep(5)

    write_data(name, gmail_address, PASSWORD_ACCOUNT, FOLDERID, PROFILEID, proxy)

    try: #Normal Flow
        wait.until(EC.element_to_be_clickable((
            By.ID, 'selectioni6'))).click() #Express vs Manual -> Select Express
        
        wait.until(EC.element_to_be_clickable((
            By.XPATH, '//span[text()="Next"]'))).click() #Next Button after Express

        driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Accept all"]')))) #Scroll until accept all
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Accept all"]'))).click() #Click button
        
        driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Confirm"]')))) #Scroll into Confirm 
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Confirm"]'))).click()

        driver.execute_script("arguments[0].scrollIntoView(true);", wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="I agree"]'))))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="I agree"]'))).click()

        print(f'Gmail address created: {gmail_address}')
        return gmail_address
    
    except:
        print("Error during final automation - kindly proceed to creating manually")
        return gmail_address

def write_data(name, gmail_address, PASSWORD_ACCOUNT, FOLDERID, PROFILEID, proxy):
    try:
        with open(FILE_WITH_DATA, mode='a') as txt_file:
            txt_file.write(f'Name: {name}, Email: {gmail_address}@gmail.com, Password: {str(PASSWORD_ACCOUNT)} FolderID: {FOLDERID}, ProfileID: {PROFILEID}, MLP Host: {proxy['host']}, MLP Port: {proxy['port']}, MLP Username: {proxy['username']}, MLP Password: {proxy['password']}\n')
            print(f'Successfully wrote data to {FILE_WITH_DATA}')
    except Exception as e:
        print(f'Error writing to file: {e}')

def stop_profile() -> None:
    r = requests.get(f"{LAUNCHERV1}/profile/stop/p/{PROFILEID}", headers=HEADERS) #No stop profile on Launcher V2
    if r.status_code != 200:
        print(f"\nError while stopping profile: {r.text}\n")
    else:
        print(f"\nProfile {PROFILEID} stopped.\n")

def profile_update():
    url = "https://api.multilogin.com/profile/update"
    body = {
        "name": gmail_address,
        "profile_id": PROFILEID,
        "parameters": {
            "proxy": {
                "host": proxy['host'],
                "type": "http",
                "port": int(proxy['port']),
                "username": proxy['username'],
                "password": proxy['password']
            },
            "flags": {
                "audio_masking": "natural",
                "fonts_masking": "mask",
                "geolocation_masking": "mask",
                "geolocation_popup": "allow",
                "graphics_masking": "natural",
                "graphics_noise": "natural",
                "localization_masking": "mask",
                "media_devices_masking": "natural",
                "navigator_masking": "mask",
                "ports_masking": "natural",
                "proxy_masking": "custom",
                "screen_masking": "natural",
                "timezone_masking": "mask",
                "webrtc_masking": "mask"
            },
            "storage": {
                "is_local": False,
                "save_service_worker": True
            },
        "fingerprint": {}
        }
    }
    
    response = requests.request("POST", url, headers=HEADERS, json=body)
    print(response.text)

def retrieve_number():
    response_check_num = requests.get(endpoint_active_orders, params=params_active_order)
    if response_check_num.status_code == 200:
        data = response_check_num.json()
        if data:  
            phone_number = data[0].get('phonenumber')
            print(f'This the phone number {phone_number} created')
            return phone_number
        else:
            print('No data available in the response')
    else:
        print(f'Retrieving number: {response_check_num.status_code} has occurred')


def get_code():
    response_check_sms = requests.get(endpoint_active_orders, params=params_active_order)
    if response_check_sms.status_code == 200:
        data = response_check_sms.json()
        if data:  
            code = data[0].get('code')
            return code
        else:
            print('No data available in the response')
    else:
        print(f'Getting code: {response_check_sms.status_code} has occurred')


def generate_review():
    headers = {"Authorization": f"Bearer {API_GPT}", "Content-Type": "application/json"}
    link = "https://api.openai.com/v1/chat/completions"
    body = {
        'model': 'gpt-3.5-turbo',
        'messages': [{"role": "user", "content": "Write a very short and generic good review for a calm lake from the countryside"}]
    }
    body = json.dumps(body)

    try:
        response = requests.post(link, headers=headers, data=body)
        response.raise_for_status() 

        response_data = response.json()
        message = response_data['choices'][0]['message']['content']
        print(message)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        message = None
    except Exception as err:
        print(f"Other error occurred: {err}")
        message = None

    return message

def post_review(driver, message, REVIEW_LINK):
    """Post a review on Google Maps."""
    driver.get("https://www.google.com/")
    time.sleep(3)
    driver.get(REVIEW_LINK)
    time.sleep(8)

    try:
        # Wait until the reviews button is clickable
        open_reviews = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'EIgkw') and contains(@class, 'OyjIsf')])[2]"))
        )
        if open_reviews.is_displayed():
            open_reviews.click()
        else:
            driver.execute_script("arguments[0].click();", open_reviews)
    except TimeoutException:
        print("Element not found or not clickable.")
        return
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", open_reviews)

    time.sleep(2)

    try:
        # Wait until the "Review" button is clickable
        click_review = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//span[@class='DVeyrd '])[1]"))
        )
        if click_review.is_displayed():
            click_review.click()
        else:
            driver.execute_script("arguments[0].click();", click_review)
    except TimeoutException:
        print("Element not found or not clickable.")
        return
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", click_review)

    time.sleep(10)
    
    # Switch to the iframe containing the review form
    iframe = driver.find_element(By.XPATH, "//iframe[@name='goog-reviews-write-widget']")
    driver.switch_to.frame(iframe)

    try:
        # Wait until the review text area is visible
        write_review = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//label[@jsaction='click:cOuCgd; keydown:I481le' and @jsname='vhZMvf' and @for='c2'])"))
        )
        if write_review.is_displayed():
            driver.execute_script("arguments[0].click();", write_review)
            write_review.send_keys(message)
        else:
            driver.execute_script("arguments[0].click();", write_review)
            write_review.send_keys(message)
    except TimeoutException:
        print("Write element not found or not clickable.")
        return

    try:
        # Wait until the 5-star rating element is clickable
        add_starts = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='s2xyy' and @role='radio' and @aria-checked='false' and @tabindex='0' and @jsaction='click:uOnRTe; keydown:g6LwHf' and @data-rating='5'])"))
        )
        if add_starts.is_displayed():
            add_starts.click()
        else:
            driver.execute_script("arguments[0].click();", add_starts)
    except TimeoutException:
        print("Element not found or not clickable.")
        return
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", add_starts)

    time.sleep(2)

    try:
        # Wait until the post button is clickable
        post = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='VfPpkd-RLmnJb'])[4]"))
        )
        if post.is_displayed():
            post.click()
        else:
            driver.execute_script("arguments[0].click();", post)
    except TimeoutException:
        print("Element not found or not clickable.")
        return
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", post)

    time.sleep(4)

    try:
        # Wait until the done button is clickable
        done = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//span[@jsname='V67aGc' and @class='VfPpkd-vQzf8d'])[1]"))
        )
        if done.is_displayed():
            done.click()
        else:
            driver.execute_script("arguments[0].click();", done)
    except TimeoutException:
        print("Element not found or not clickable.")
        return
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", done)

    time.sleep(10)

    driver.get("http://gmail.com/")
    time.sleep(5)
    
    print("Review Posted")

base_dir = os.path.dirname(__file__)
cookie_robot_path = os.path.join(base_dir, 'cookie_robot.py')

if __name__ == "__main__":
    proxy = get_proxy(token)
    PROFILEID = create_profile(proxy, FOLDERID)
    os.environ['PROFILEID'] = PROFILEID
    driver = start_profile()
    try:
        gmail_address = main(driver)
        time.sleep(45)
        stop_profile()
        profile_update()
        time.sleep(20)
        subprocess.run(['python3', cookie_robot_path])

        time.sleep(5)
        stop_profile()
        message = generate_review()
        if message:
            driver = start_profile()
            time.sleep(2)
            post_review(driver, message, REVIEW_LINK)
        else:
            print("Failed to generate review message.")
        
    except Exception as e:
        print(e)