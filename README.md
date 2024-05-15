# xfinity-mail-scraper

Instructions to Run the Xfinity Login Checker
Clone the Repository:

bash
Copy code
git clone https://github.com/dev-Yashwant/xfinity-mail-scraper.git

<br>
Install Dependencies:
<br>
bash
<br>
Copy code
<br>
pip install pyppeteer pyppeteer-stealth gologin

Prepare Email List:

Create a file named emails.txt in the same directory as the script.
Add one Xfinity email address per line.
Run the Script:

bash
Copy code
python xfinity_login_checker.py
Check the Results:

The script will check the login status for each email address.
Results will be written to a file named results.txt in the same directory.
