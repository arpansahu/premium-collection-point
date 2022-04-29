
# Premium Collection Point

This project is a working Project for Premium Collection Point. In this project there are two entities namely 
branch and manager. My father is a LIC Wealth Manager and I have built this project to help him manage his clients 
across PAN India. 

Challenges Faced By My Father during Pandemic:
- His 90% client used to pay their LIC Premiums using Cash.
- Pre Pandemic they used to visit Fathers office or LIC branch to pay their premiums which was not possible 
  due to lockdown across India.
- Penalty Charges were increasing on my fathers clients and my Fathers Income was also reducing 

Solution To The Problem:
1. Built a web portal which was looking trustworthy and was with the name of my fathers official branch name 
 i.e. Sahu Beema Kendra which was later renamed to Premium Collection Point.com
2. Customers were used to pay in Cash to Sub branches
3. Sub-branches used to earn 1% commission of the total amount paid through their branch 
4. Next day sub-branch owners used to deposit cash to their collected cash to their bank account, and they can 
    add money to their wallet using pcp-pay gateway
5. PCP-Pay gateway was a custom sub service which was built in this project to support UPI/IMPS/CASH methods
    to add money to wallet
6. Few of our branches were allowed to deposit in CASH to our Bank Account and add money to wallet. But many others 
  were only allowed to add money using UPI QR Code or IMPS

Business Opportunities:
1. Branches were able to earn 1% of the total amount of premium bills paid through their branch
2. Refer n Earn system was also introduced later which enables branches to earn 10% of the 1 st level refers Income.

Feature Scope and Improvements:
1. Initially this project was requiring some human intervention in the working of the project.
2. Money Orders can  be automated using Email Reading With Python or Sms Reading which were sent by bank for
 approving money orders
3. Selenium was used to fetch premium amount from Amazon Pay. Although LIC Official Portal for Premium Collection 
already exists, but it's access cannot be distributed with others (for security purposes). Moreover, bill was a little
hard to scrap for that portal due to a lot of captcha. While Amazon Pay was allowing to check the bill without any login 
required. Note: since jan 2022 amazon pay started hiding premium holders name if we scrap without logging into amazon pay
    - So this can be overcome using Bill-desk APIs, but it will cost hefty money
4. You can also replace this payment Gateway with Paytm Payment Gateway which provides 0% fees on UPI and Debit 
    mode of transactions. But it would require you to be a merchant, and you should have proper documentations



-Implemented Complete Auth Using Custom Auth Model.
    
1. Used built in AbstractBaseUser as parent Auth Model
2. Build Custom Manager for the same
3. Implemented custom error View for customizing Templates
4. Login. SingUp, Logout, Account Views Implemented
5. In built views of PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetView, PasswordResetCompleteView
6. Build Custom Templates for These Inbuilt Views
7. Reset Password is working 
8. If kyc is False then it will show you Get Kyc Details unless it will welcome you. By default, every user is non keyid.
9. If you want to kyc a person login to admin panel from here:  https://premiumcollectionpoint.herokuapp.com/admin/ and  modify it

-Used Heroku to Deploy Premium Collection Point 

1. For using Selenium in Heroku 
    1. https://github.com/heroku/heroku-buildpack-chromedriver (ChromeDriver)
    2. https://github.com/heroku/heroku-buildpack-google-chrome (Chrome)
    - apart from default env variables add: variables for ChromeDriver and Chrome -
    - CHROMEDRIVER_PATH: /app/.chromedriver/bin/chromedriver
    - GOOGLE_CHROME_BIN: /app/.apt/usr/bin/google-chrome
2. Postgres was used as database

_____
Note: This project is hosted in Heroku as of now. which restricts a request to be fulfilled in max 30 seconds 
otherwise requests will be terminated. If Bill Check Service don't work properly in Demo then problem is caused due to 
this reason. I have myself hosted this project in AWS when it was in use. So I highly recommend to host it on AWS if you
want to use yourself for some other purposes then demo.
_____

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)](https://www.selenium.dev/)
[![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://www.heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Demo

Available at: https://premiumcollectionpoint.herokuapp.com/

admin login details:--    url: https://premiumcollectionpoint.herokuapp.com/admin

email: admin@arpansahu.me
password: showmecode

Branch login details:--

email: branchone@arpansahu.me
password: showmecode

Manager login details:--

email: managerone@arpansahu.me
password: showmecode
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

Installing Pre requisites

```bash
  pip install -r requirements.txt

```

Making Migrations and Migrating them.

```bash
  python manage.py makemigrations
  python manage.py migrate

```

Creating Super User

```bash
  python manage.py createsuperuser

```

Run Server
```bash
  python manage.py runserver

```

## Tech Stack

**Client:** HTML, Jinja, CSS, BootStrap

**Server:** Django, Gunicorn, Heroku, Selenium


## Deployment on Heroku

Installing Heroku Cli from : https://devcenter.heroku.com/articles/heroku-cli
Create your account in Heroku.

Inside your project directory

Login Heroku CLI
```bash
  heroku login

```

Create Heroku App

```bash
  heroku create [app_name]

```

Push Heroku App
```
    git push heroku master
```

Apart from python build packs add:
```
https://github.com/heroku/heroku-buildpack-chromedriver (ChromeDriver)
https://github.com/heroku/heroku-buildpack-google-chrome (Chrome)
```

Configure Heroku App Env Variables
```bash
  heroku config:se CHROMEDRIVER_PATH= /app/.chromedriver/bin/chromedriver
  heroku config:se GOOGLE_CHROME_BIN= /app/.apt/usr/bin/google-chrome
  heroku config:set GITHUB_USERNAME=joesmith
  ...
```


Configuring Django App for Heroku

Install whitenoise 
```
pip install whitenoise 
```

Include it in Middlewares.
```
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Create Procfile and include this code snippet in it.
```
release: ./release-tasks.sh
web: gunicorn djangoProject.wsgi
```

Create release-task.sh for running multilple commands in run: section of procfile
```
python manage.py makemigrations
python manage.py migrate
```

Make relase-task.sh executable
```
chmod +x release-tasks.sh 
```
## Documentation

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)](https://www.selenium.dev/)
[![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://www.heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

SECRET_KEY=

DEBUG=

DB_HOST=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_PORT=

EMAIL_USER=

EMAIL_PASS=

ALLOWED_HOSTS=

