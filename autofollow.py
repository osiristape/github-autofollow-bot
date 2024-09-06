import random
import time
import logging
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from scripts.utils import load_credentials, get_user_inputs, set_delay, click_button, display_intro, get_user_agreement, ask_for_2fa_verification, get_follow_or_unfollow

# Specify the path to the EdgeDriver executable
driver_service = Service(r'C:\Path\To\Your\msedgedriver.exe')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LOGO = r"""
   ___ _ _   _               ___    _ _                      ___      _   
  / __(_) |_| |_ _  _ __ _  | __|__| | |_____ __ _____ _ _  | _ ) ___| |_ 
 | (_ | |  _| ' \ || / _` | | _/ _ \ | / _ \ V  V / -_) '_| | _ \/ _ \  _|
  \___|_|\__|_||_\_,_\__, | |_|\___/_|_\___/\_/\_/\___|_|   |___/\___/\__|
                     |___/                                                
"""

# Global variable to control the stop command
stop_thread = False

def github_login(driver, username, password):
    """Logs in to GitHub."""
    driver.get("https://github.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "login_field").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.NAME, "commit").click()
    time.sleep(2)
    logging.info("Logged in successfully.")

def handle_accounts(driver, account_url, action, focus, page, delay, count):
    """Handles the logic for following or unfollowing users based on focus."""
    target_url = f"{account_url}/{'stargazers' if focus == 'stargazers' else '?tab=followers&page='}{page}"
    
    logging.info(f"Navigating to {target_url}")
    driver.get(target_url)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @name='commit']")))
    except TimeoutException:
        logging.error("Timed out waiting for the page to load or buttons to be present.")
        with open("page_source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        logging.debug("Page source saved to page_source.html")
        return False, count

    buttons_xpath = {
        "follow": "//input[@type='submit' and @name='commit' and @value='Follow']",
        "unfollow": "//input[@type='submit' and @name='commit' and @value='Unfollow']"
    }.get(action)
    ignore_buttons_xpath = {
        "follow": "//input[@type='submit' and @name='commit' and @value='Unfollow']",
        "unfollow": "//input[@type='submit' and @name='commit' and @value='Follow']"
    }.get(action)

    if not buttons_xpath:
        logging.error(f"Unknown action type: {action}.")
        return False, count

    all_buttons = driver.find_elements(By.XPATH, buttons_xpath)
    if not all_buttons:
        logging.info(f"No {action} buttons found on page {page}.")
        if not driver.find_elements(By.XPATH, "//a[@aria-label='Next']"):
            logging.info("No pagination controls found. Exiting.")
            return False, count
        logging.info("Moving to the next page.")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.5, 2))  # Random delay to mimic human scrolling
        return True, count

    logging.info(f"Found {len(all_buttons)} {action} buttons on page {page}.")
    for button in all_buttons:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(button))
            time.sleep(random.uniform(0.1, 0.5))  # Random delay to simulate human behavior
            count = click_button(driver, button, delay, count, action)
        except (StaleElementReferenceException, TimeoutException) as e:
            logging.error(f"Error with button interaction: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    return True, count

def listen_for_stop():
    """Listens for user input to stop the script."""
    global stop_thread
    while not stop_thread:
        if input().strip().lower() == 'stop':
            stop_thread = True

def main():
    """Main function to run the script."""
    global stop_thread

    display_intro(LOGO)
    get_user_agreement()
    
    action = get_follow_or_unfollow()
    account_url, start_page, speed_mode, focus = get_user_inputs()
    delay = set_delay(speed_mode)

    github_username, github_password = load_credentials()
    if ask_for_2fa_verification():
        logging.info("2FA verification required. Waiting for 60 seconds...")
        time.sleep(60)

    logging.info("Starting now")

    driver = webdriver.Edge(service=driver_service)
    github_login(driver, github_username, github_password)

    stop_listener = threading.Thread(target=listen_for_stop)
    stop_listener.start()

    page = start_page
    count = 0

    try:
        while not stop_thread:
            action_success, count = handle_accounts(driver, account_url, action, focus, page, delay, count)
            if not action_success:
                logging.info(f"No {action} buttons found or pagination controls missing. Exiting.")
                break
            page += 1
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    finally:
        logging.info(f"Total accounts processed ({action}ed): {count}")
        driver.quit()

if __name__ == "__main__":
    main()
