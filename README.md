# github-autofollow-bot

This Python script automates the process of following or unfollowing users on GitHub. Designed for educational purposes, the script allows you to automate interactions with GitHub users and stargazers on repository pages, offering configurable options for a customizable experience.

## Features

- **Follow or Unfollow:** Choose between following or unfollowing users based on your preference.
- **Target Options:** 
  - **Stargazers:** Automatically follow or unfollow stargazers of a specified repository.
  - **GitHub Users:** Follow or unfollow a specific GitHub user followers.
- **Default Targets:**
  - **GitHub User:** `https://github.com/osiristape`
  - **GitHub Repository:** `https://github.com/gradle/gradle`
- **Configurable Settings:**
  - **Starting Page Number:** Specify the page number to start following or unfollowing users.
  - **Speed Mode:** Choose a speed mode for the automation process to manage anti-detection.
- **2FA Authentication:**
  - **Verification Option:** Decide whether 2FA authentication is required.
    - **If YES:** The script will pause for 60 seconds to allow manual input of the 2FA code received via email. The automation will continue once the code is provided.
    - **If NO:** The script will proceed with automation without 2FA verification.

## Logging

The script provides detailed logs of the actions performed, helping you track the status and results of the automation process.

## Disclaimer

Please use this script responsibly and abide by all relevant terms and conditions while using GitHub.

## Setup

1. **Clone the repository:** 
   ```sh
   git clone https://github.com/osiristape/github-autofollow-bot.git
   cd github-autofollow-bot
   ```
   
2. **Create a virtual environment and activate it:**
   ```sh
   # Linux
   python -m venv venv
   source venv/bin/activate 
   ```
   ```sh
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```
   
   
3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   
4. **Create a .env file and add your GitHub credentials:**
   ```sh
   GITHUB_USERNAME=your_github_username
   GITHUB_PASSWORD=your_github_password
   ```
   
5. **Run the script:**
   ```sh
   python autofollow.py # use ms_edge browser 
   ```

## License

This project is licensed under *The Unlicense*.

## Credits
This project is based on the template provided using [GitHub-Auto-Follow](https://github.com/ZigaoWang/github-auto-follow/blob/master/main.py).

I have made modifications and improvements to suit the needs of my specific use case. Please refer to the original repository for further details.


