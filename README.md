# CoinVue - Project 3

CoinVue is a cryptocurrency portfolio tracker and price tracker updating price movements to give users fast, accurate and informative data on their assets performance. The project's goal is to deliver a portfolio service where users can keep track of their assets performance through buy, sell and transfer records with live updates on the value of their portfolio as well as a feature where users can share and compare their portfolios.

## Table of contents

## 1.0 UX

### 1.1 User goals

#### 1.1.1 Target audience

CoinVue’s target audience are crypto retail investors interested in live market movements and trends broken down into easy to read data that they need to make further investments. As well as a way to track the performance of their portfolio and others if they choose to share it.      

### 1.2 User needs and goals

#### 1.2.1 User needs:

1. Accessibility for all users
2. Accurate updated data
3. Important data on assets
4. Sign up and log in
5. Password security 
6. Private and public portfolios
7. Share portfolio
8. Add, sell, transfer and staking rewards records
9. Portfolio charts

#### 1.2.2 How the user needs are met

1. All users should have equal opportunity through text transcript compatibility, color contrast that's readable, form labels, visual feedback and responsive breakpoints to support all devices
2. Fast, accurate and close to instant updated data to ensure no big price action isn't missed or inaccurate through Coinmarketcap API
3. More in depth breakdowns of individual assets when a user clicks on them such as supply, market cap, volume and price history
4. Users can sign up and log in to access and edit their portfolios with password protection 
5. To ensure account protection, users can create a password so other can log in
6. Users with accounts can create public portfolios to share and view others as well as private portfolios
7. Users can share their portfolios with others or view others to discover new assets, trends and investing strategies
8. When adding records users can pick from 4 options as to add, sell, transfer and staking rewards to contribute to their portfolio
9. When 1 record is added to a portfolio the chart will update regularly to its current value

### 1.3 Devloper and buisness goals

#### 1.3.1 Goals of the buisness

1. To deliver an accurate service with relevant data
2. The website attracts retail investors
3. User traffic can be maintained and grow through sign ups
4. Users will interact and share portfolios to improve user engagement
5. Growth in user numbers
6. Growth on listed assets

### 1.4 User stories

1. User wants to check recent performance of digital asset
2. User wants to expand their knowledge on specific asset
3. User wants to add / edit / remove a record to their portfolio
4. User wants to sign up to create a portfolio
5. User wants to share their portfolio 
6. User wants to change their password

1.4.1 The user has invested in an asset and is looking to see how it has performed for the day with either a positive or negative percentage value based on the past 24 hours. The price tracker will act as the home page/hub listing the top 50 assets so the user only has to scroll down to find their asset or use the search bar to filter them.

1.4.2 The user wants to gain more knowledge and data on a project then what is offered on the home screen. The user can click on the asset they are interested in and will direct them to a new page dedicated to the selected asset with information on its market cap, supply, price, charts and more which the user can use to make their next investing decision.

1.4.3 The user has created an account as well as a portfolio and has made a purchase which they are looking to make a record to track its future performance. On the portfolio screen the user can add / edit / delete records that have been created on their account and portfolio for each asset but cannot add / edit / delete other users' portfolios.

1.4.4 The user is looking to create an account to share their strategies, which they can do through the sign up link in the nav where they can enter a username and password to protect their account. To access their account after its creation a login page with also be linked beneath the signup page for users with account.

1.4.5 After creating an account and a portfolio the user may want to view or share their portfolio with others which they can do on their portfolio page with the option to make it private or public. Public portfolios will display on the portfolio page where users can interact with others' portfolios and learn about new projects or copy others strategies.

1.4.6 The user has forgotten or wants to change to a more secure password, users can click the forgotten password link below the login page to change their password through an email authentication link then enter their new password.

## 2.0 Design choices

### 2.1 Fonts

### 2.2 Icons

### 2.3 Colors

### 2.4 Wireframes

### 2.5 Mockups

## 3.0 Features

### 3.1 Exisiting features

### 3.2 Features left to implement

## 4.0 Technologies used

### 4.1 HTML5

### 4.2 CSS3

### 4.3 Bootstrap 4.5

### 4.4 JavaScript

### 4.5 jQuery

### 4.6 Python 3

### 4.7 Flask

### 4.8 MongoDB

## 5.0 Testing

## 6.0 Devlopment life cycle

### 6.1 Initial commit

Additions:

- Code Institute gitpod template
- .gitignore file
- app.py
- env.py
- Create Flask app

### 6.2 Updated README Section 1 UX

Additions:

- README Section 1 UX

### 6.3 Updated README Sections 2 to 5

Additions:

- README Section 2 Design Choices
- README Section 3 Features
- README Section 4 Technologies used
- README Section 5 Testing

### 6.4 Updated README Section 6 Devlopment life cycle

Additions:

- README Section 6 Devlopment life cycle

### 6.5 Updated README Sections 7 to 8

Additions:

- README Section 7 Deployment
- README Section 8 Credits

### 6.6 Add requirments.txt

Additions:

- Add requirments.txt

### 6.7 Add Procfile

Additions:

- Add Procfile

### 6.8 Deploy to heroku

Additions:

- Deployed to heroku

### 6.9 Add basic file structure

Additions:

- static file
- css file
- style.css
- js file
- script.js
- templates file
- index.html
- base.html

### 6.10 Added bootstrap and jQuery

Additions:

- Added Bootstrap
- Added jQuery
- Base template structure

### 6.11 Added basic nav-bar

Additions:

- Added nav bar

### 6.12 Added basic footer

Additions:

- Added footer

### 6.13 Added log in, sign up page and links to nav and footer

Additions:

- Added log in page
- Added sign up page
- Added links to nav-bar
- Added links to footer

### 6.14 Log in and sign up page css

Additions:

- Log in and sign up page css
- Sign up page form

### 6.15 Added CoinMarketCap API

Additions:

- Added CoinMarketCap API

### 6.16 Registration functional and flash messages added

Additions:

- Added flash messages to sign up
- Sign up page fully functional

### 6.17 Log in functionality, portfolio and profile page

Additions:

- Flash messages appear for users when signed in
- Added portfolio.html
- Added profile.html

### 6.18 Nav-bar changes based on if user is signed in or not

Additions:

- Sign up button on nav bar
- Sign out button on nav bar
- Logged in users have access to profile, my portfolio and log out
- Logged out users have access to log in and sign up on nav-bar

### 6.19 Basic portfolio page structure and crypto record modal

Additions:

- Basic portfolio page structure
- Crypto record modal

### 6.20 Crypto record form POST's to mongodb

Additions:

- Crypto record form POST's to mongodb

### 6.21 Crypto record POST's username and total cost to mongodb

Additions:

- Crypto record POST's username
- Crypto record POST's total cost

### 6.22 Portfolio page table basic structure

Additions: 

- Portfolio grid table basic structure

### 6.23 Home page crypto tracker updates when reloaded

Additions:

- Home page Crypto price tracker
- Tracker updates when user reloadeds page
- Home page basic structure

### 6.24 Issues with get_price, get_name functions and updates to front page

Additions:

- coinvue.py get_price function
- coinvue.py get_name function
- Portfolios record progress
- Update to home page

Issues #1 - (get_name) Unable to make list of names for crypto options for users to pick

Issues #2 - (portfolio collection) Unable to find records with the same crypto currency name to total up the users holdings / grand total, the value of there crypto and their profits / loses

Issues #3 - (get_price) Unable to get the cryptos current price as well as way to get price for the correct crypto

### 6.25 More Crypto options for users to pick from

Additions:

- Users can now pick from more cryptos as the options are tacken from CoinMarketCap dictionairy
- Issue #1 resolved was calling from add_record rather then portfolio

Issue RESOLVED #1 - (get_name) Unable to make list of names for crypto options for users to pick

### 6.26 Changes to my_portfolio functionality 

Additions:

- Updates to app.py
- my_portfolio collection

### 6.27 Changes to home page, nav-bar and footer css

Additions:

- Home page background color
- Nav-bar links curved, hover animation and changes to color
- Footer CSS changes to color

### 6.28 Mobile nav bar breakpoints

Additions:

- My portfolio css changes
- Nav bar breakpoints mobile

### 6.29 Mobile footer breakpoints and updates to nav-bar mobile

Additions:

- Mobile nav-bar drop down menu appears infront of the text
- Changed the order of logo, title and drop down menu
- Footer mobile and small mobile responsive breakpoints
- Mobile home page crypto table scrolls horizontally

### 6.30 Responsive home page and removal of profile page

Additions:

- Home page is responsive on all devices
- Removing of profile page, when user logs in they will be redirected to their portfolio

## 7.0 Deployment

### 7.1 Local deployment

### 7.2 GitHub page deployment

### 7.3 Heroku deployment

## 8.0 Credits

### 8.1 Content

### 8.2 Code