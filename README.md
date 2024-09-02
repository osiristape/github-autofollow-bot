# github-follower-bot
This Python script automates the process of following users on GitHub stargazers pages. Designed for educational purposes, the script logs into GitHub, navigates to a repository's stargazers page, and follows users based on configurable settings.

## Features
- **Automated Following:** Automatically follows users on specified stargazer pages.
- **Configurable Settings:** Adjust speed, starting page, and repository URL.
- **Logging:** Provides detailed logs of actions performed.

## Disclaimer

This script may violate GitHub's community guidelines. Use it for educational purposes only.

## Setup

1. **Clone the repository:** 
   ```sh
   git clone https://github.com/osiristape/github-follower-bot.git
   cd github-follower-bot
   ```
   
2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
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
   python autofollow.py
   ```

## License

This project is licensed under *The Unlicense*.





