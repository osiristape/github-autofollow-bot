import os
import random
import logging
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

# Constants
DEFAULT_REPO_URL = "https://github.com/gradle/gradle"
DEFAULT_USER_URL = "https://github.com/osiristape"
DEFAULT_START_PAGE = 1
DEFAULT_SPEED_MODE = "random"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_follow_or_unfollow():
    """Asks the user if they want to follow or unfollow users."""
    action = input("Would you like to 'follow' or 'unfollow' users? (default 'follow'): ").strip().lower()
    if action not in ["follow", "unfollow"]:
        logging.warning("Invalid action provided. Defaulting to 'follow'.")
        action = "follow"
    return action

def load_credentials():
    """Loads GitHub credentials from environment variables."""
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from a .env file if present
    github_username = os.getenv("GITHUB_USERNAME")
    github_password = os.getenv("GITHUB_PASSWORD")
    if not github_username or not github_password:
        logging.error("GitHub credentials are not set in the environment variables.")
        exit(1)
    return github_username, github_password

def get_user_inputs():
    """Prompts the user for necessary inputs."""
    account_url = input(f"Enter the GitHub account URL (default '{DEFAULT_USER_URL}'): ").strip() or DEFAULT_USER_URL
    try:
        start_page = int(input(f"Enter the starting page (default {DEFAULT_START_PAGE}): ").strip() or DEFAULT_START_PAGE)
    except ValueError:
        print("Invalid page number. Please enter a valid number.")
        return get_user_inputs()
    
    speed_mode = input("Enter speed mode (fast, medium, slow, random) (default 'random'): ").strip().lower() or DEFAULT_SPEED_MODE
    if speed_mode not in ["fast", "medium", "slow", "random"]:
        print("Invalid speed mode. Please try again.")
        return get_user_inputs()

    focus = input("Do you want to focus on 'stargazers' or 'followers'? (default 'stargazers'): ").strip().lower() or "stargazers"
    if focus not in ["stargazers", "followers"]:
        print("Invalid focus type. Please try again.")
        return get_user_inputs()

    return account_url, start_page, speed_mode, focus

def set_delay(speed_mode):
    """Sets delay based on the chosen speed mode."""
    delays = {
        "fast": random.uniform(0.1, 0.3),
        "medium": random.uniform(1, 2),
        "slow": random.uniform(3, 5),
        "random": random.uniform(0.1, 5)
    }
    delay = delays.get(speed_mode, delays["random"])
    logging.info(f"Using delay: {delay:.2f} seconds.")
    return delay

def click_button(driver, button, delay, count, action):
    """Clicks a button with a delay and prints user info."""
    try:
        ActionChains(driver).move_to_element(button).click().perform()
        time.sleep(random.uniform(0.5, 1.0))  # Random delay to mimic human clicking
        count += 1
        logging.info(f"Successfully {action}ed {button.get_attribute('aria-label')}. Total {action}ed: {count}")
    except StaleElementReferenceException:
        logging.error("Element reference is stale. Skipping this button.")
    except Exception as e:
        logging.error(f"Error clicking {action} button: {e}")
    return count

def display_intro(LOGO):
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
    if input("Type 'agree' to continue: ").strip().lower() != 'agree':
        print("You did not agree to the disclaimer. Exiting...")
        exit(1)

def ask_for_2fa_verification():
    """Asks if 2FA verification is needed."""
    response = input("Do you need to verify your account using 2FA? (yes/no): ").strip().lower()
    if response == 'yes':
        return True
    elif response == 'no':
        return False
    print("Invalid response. Please enter 'yes' or 'no'.")
    return ask_for_2fa_verification()
