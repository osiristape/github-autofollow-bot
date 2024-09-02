import time
import logging
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from scripts.utils import load_credentials, get_user_inputs, set_delay, click_follow_button, display_intro, get_user_agreement

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

def follow_stargazers(driver, repo_url, page, delay, follow_count):
    """Follows users on the stargazers page."""
    driver.get(f"{repo_url}/stargazers?page={page}")
    time.sleep(3)
    follow_buttons = driver.find_elements(By.XPATH, "//input[@type='submit' and @name='commit' and @value='Follow']")
    if not follow_buttons:
        return False, follow_count
    for button in follow_buttons:
        try:
            parent_element = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'd-flex')]")
            username_element = parent_element.find_element(By.XPATH, ".//a[contains(@data-hovercard-type, 'user')]")
            username = username_element.get_attribute("href").split("/")[-1]
            follow_count = click_follow_button(button, delay, username, follow_count)
        except Exception as e:
            logging.error(f"Error clicking follow button: {e}")
    return True, follow_count

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
    github_username, github_password = load_credentials()
    repo_url, start_page, speed_mode = get_user_inputs()
    delay = set_delay(speed_mode)

    logging.info("Starting now")

    driver = webdriver.Edge(service=driver_service)
    github_login(driver, github_username, github_password)

    stop_listener = threading.Thread(target=listen_for_stop)
    stop_listener.start()

    page = start_page
    follow_count = 0

    try:
        while not stop_thread:
            followed_on_page, follow_count = follow_stargazers(driver, repo_url, page, delay, follow_count)
            if not followed_on_page:
                logging.info(f"No follow buttons found on page {page}. Exiting.")
                break
            page += 1
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    finally:
        logging.info(f"Total users followed: {follow_count}")
        driver.quit()

if __name__ == "__main__":
    main()
