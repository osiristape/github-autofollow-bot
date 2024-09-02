import os
import time
import random
import logging
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from dotenv import load_dotenv

# Specify the path to the EdgeDriver executable
driver_service = Service(r'C:\Path\To\Your\msedgedriver.exe')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
LOGO = r"""

   ___ _ _   _               ___    _ _                      ___      _   
  / __(_) |_| |_ _  _ __ _  | __|__| | |_____ __ _____ _ _  | _ ) ___| |_ 
 | (_ | |  _| ' \ || / _` | | _/ _ \ | / _ \ V  V / -_) '_| | _ \/ _ \  _|
  \___|_|\__|_||_\_,_\__, | |_|\___/_|_\___/\_/\_/\___|_|   |___/\___/\__|
                     |___/                                                
"""

DEFAULT_REPO_URL = "https://github.com/torvalds/linux"
DEFAULT_START_PAGE = 1
DEFAULT_SPEED_MODE = "random"

# Global variable to control the stop command
stop_thread = False

def display_intro():
    """Displays the introductory information and disclaimer."""
    print("--------------------------------------------------")
    print(LOGO)
    print("--------------------------------------------------")
    print("DISCLAIMER: This script may violate GitHub's community guidelines.")
    print("Use this script for educational purposes only.")
    print("To stop the script at any time, type 'stop' in the terminal.")
    print("--------------------------------------------------")

def get_user_agreement():
    """Ensures the user reads and agrees to the disclaimer."""
    agreement = input("Type 'agree' to continue: ").strip().lower()
    if agreement != 'agree':
        print("You did not agree to the disclaimer. Exiting...")
        exit()

def load_credentials():
    """Loads GitHub credentials from environment variables."""
    github_username = os.getenv("GITHUB_USERNAME")
    github_password = os.getenv("GITHUB_PASSWORD")
    return github_username, github_password

def get_user_inputs():
    """Prompts the user for necessary inputs."""
    repo_url = input(f"Enter the GitHub repository URL (default {DEFAULT_REPO_URL}): ").strip() or DEFAULT_REPO_URL
    start_page = int(input(f"Enter the starting page (default {DEFAULT_START_PAGE}): ").strip() or DEFAULT_START_PAGE)
    speed_mode = input(
        f"Enter speed mode (fast, medium, slow, random) (default {DEFAULT_SPEED_MODE}): ").strip().lower() or DEFAULT_SPEED_MODE
    return repo_url, start_page, speed_mode

def set_delay(speed_mode):
    """Sets delay based on the chosen speed mode."""
    if speed_mode == "fast":
        return 0.1
    elif speed_mode == "medium":
        return 1
    elif speed_mode == "slow":
        return 5
    elif speed_mode == "random":
        return random.uniform(0.1, 10)
    else:
        logging.warning("Invalid speed mode. Defaulting to random.")
        return random.uniform(0.1, 10)

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

def click_follow_button(button, delay, username, follow_count):
    """Clicks a follow button with a delay and prints user info."""
    try:
        button.click()
        follow_count += 1
        logging.info(f"{follow_count}. Followed {username}: https://github.com/{username}")
        time.sleep(delay)
    except Exception as e:
        logging.error(f"Error clicking follow button for {username}: {e}")
    return follow_count

def listen_for_stop():
    """Listens for user input to stop the script."""
    global stop_thread
    while not stop_thread:
        if input().strip().lower() == 'stop':
            stop_thread = True

def main():
    """Main function to run the script."""
    global stop_thread

    display_intro()
    get_user_agreement()
    load_dotenv()
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
