SonarQube Issues Exporter

A lightweight Python script to extract all issues (bugs, vulnerabilities, and code smells) from a SonarQube instance and export them into an Excel file for analysis or reporting.

Overview

This script connects to your SonarQube server using a personal access token, fetches all issues for a specific project (or all projects if desired), and saves them into an easy-to-read Excel file (sonarqube_issues.xlsx).

It’s useful for:
•	Security or QA engineers who need offline issue reports
•	Managers generating summaries or audit logs
•	Developers analyzing code quality metrics across projects

Features
•	Fetches all projects and issues via SonarQube REST API
•	Exports issue data (severity, rule, message, line, etc.) to Excel
•	Handles pagination automatically (up to thousands of issues)
•	Easy to configure — just set your token, URL, and project key
•	Supports both public and local SonarQube instances

Requirements

Python 3.8+

The following libraries:

pip install requests pandas openpyxl

Setup & Usage

Clone this repository

git clone https://github.com/Laiba-Asad/sonarqube-exporter.git
cd sonarqube-exporter


Edit the configuration in the script

Open sonarqube-export.py and update these variables:

SONAR_URL = "http://localhost:9000"     # Your SonarQube server URL
SONAR_TOKEN = "your_sonarqube_token"    # Your personal access token
PROJECT_KEY = "FinTechApp"              # Optional: specific project key


To find your project key:
In SonarQube, open your project dashboard - the URL contains the key:

http://localhost:9000/dashboard?id=ProjectKey


Run the script

python sonarqube-export.py

Check the output

Once complete, a file named sonarqube_issues.xlsx will appear in the same directory.

