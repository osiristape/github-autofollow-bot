import os
import random
import logging
import time  # Ensure this is imported
from dotenv import load_dotenv

# Constants
DEFAULT_REPO_URL = "https://github.com/torvalds/linux"
DEFAULT_START_PAGE = 1
DEFAULT_SPEED_MODE = "random"

def load_credentials():
    """Loads GitHub credentials from environment variables."""
    load_dotenv()  # Load environment variables from a .env file if present
    github_username = os.getenv("GITHUB_USERNAME")
    github_password = os.getenv("GITHUB_PASSWORD")
    return github_username, github_password

def get_user_inputs():
    """Prompts the user for necessary inputs."""
    repo_url = input(f"Enter the GitHub repository URL (default {DEFAULT_REPO_URL}): ").strip()
    if repo_url.lower() == "default":
        repo_url = DEFAULT_REPO_URL

    start_page = input(f"Enter the starting page (default {DEFAULT_START_PAGE}): ").strip()
    if start_page.lower() == "default":
        start_page = DEFAULT_START_PAGE
    else:
        try:
            start_page = int(start_page)
        except ValueError:
            print("Invalid page number. Please try again.")
            return get_user_inputs()

    speed_mode = input(
        f"Enter speed mode (fast, medium, slow, random) (default {DEFAULT_SPEED_MODE}): ").strip().lower()
    if speed_mode == "default":
        speed_mode = DEFAULT_SPEED_MODE
    elif speed_mode not in ["fast", "medium", "slow", "random"]:
        print("Invalid speed mode. Please try again.")
        return get_user_inputs()

    return repo_url, start_page, speed_mode

def set_delay(speed_mode):
    """Sets delay based on the chosen speed mode."""
    if speed_mode == "fast":
        return 0.1  # Increased delay for fast mode
    elif speed_mode == "medium":
        return 1  # Increased delay for medium mode
    elif speed_mode == "slow":
        return 5  # Increased delay for slow mode
    elif speed_mode == "random":
        return random.uniform(0.1, 10) 
    else:
        logging.warning("Invalid speed mode. Defaulting to random.")
        return random.uniform(0.1, 10)  # Default random delay

def click_follow_button(button, delay, username, follow_count):
    """Clicks a follow button with a delay and prints user info."""
    try:
        button.click()
        follow_count += 1
        logging.info(f"{follow_count}. Followed {username}: https://github.com/{username}")
        time.sleep(delay)  # Apply delay after each click
        # Additional random delay to simulate human behavior
        time.sleep(random.uniform(0.1, 2))
    except Exception as e:
        logging.error(f"Error clicking follow button for {username}: {e}")
    return follow_count

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
    agreement = input("Type 'agree' to continue: ").strip().lower()
    if agreement != 'agree':
        print("You did not agree to the disclaimer. Exiting...")
        exit()

def ask_for_2fa_verification():
    """Asks if 2FA verification is needed."""
    response = input("Do you need to verify your account using 2FA? (yes/no): ").strip().lower()
    if response == 'default':
        return False
    elif response == 'yes':
        return True
    elif response == 'no':
        return False
    else:
        print("Invalid response. Please try again.")
        return ask_for_2fa_verification()
