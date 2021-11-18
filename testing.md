# 5.0 Testing

[README]()

## 5.1 Code validator

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| HTML W3C validator | All pages pass the validator |  |
| CSS W3C validator | All pages pass the validator |  |
| JS JSHint validator | All pages pass the validator |  | 
| PEP8 | | |

## 5.2 Nav-bar

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Logo Link | Links to home page |  |
| Title Link | Links to home page |  |
| Home button | Links to home page |  |
| My Portfolio button | Links to portfolio page |  |
| Log in button | Links to log in page |  |
| Sign up button | Links to sign up page |  |
| Log out button | Logs user out returning them to log in page |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |
| Mobile drop down menu | Menu is responsive and links work |  |

## 5.3 Footer

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Facebook link | Links to Facebook page in a new tab |  |
| YouTube link | Links to YouTube page in a new tab |  |
| Instagram link | Links to Instagram page in a new tab |  |
| Twitter link | Links to Twitter page in a new tab |  |
| Home link | Links to Home page |  |
| Portfolio link | Links to Portfolio page |  |
| Log in link | Links to Log in page |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.4 Home page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Top 50 cryptocurrencies | Home page lists top 50 cryptocurrencies |  |
| Update crypto listings | When page is refreshed the listings are updated |  |
| Sign up here link | Sign up here link works and only shows when user isn't logged in |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.5 Log in page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Wrong username | If the username is incorrect a message flashing informing the user  |  |
| Wrong password | If the password is incorrect a message flashing informing the user  |  |
| Submit button works | Submit button works and signs user in to portfolio screen |  |
| Sign up link | Links to sign up page |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.6 Sign up page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Username already taken | If the username is already in use the user is notified |  |
| Emails don't match | If the emails don't match the user is notified via flash message |  |
| Passwords don't match | If the passwords don't match the user is notified via flash message |  |
| Submit button works | Submit button works and signs user in to portfolio screen |  |
| Log in link | Links to log in page |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.7 Portfolio page

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Users name is displayed | The users name is displayed on portfolio tab |  |
| Portfolio total value | The portfolio total updated value displays under the name |  |
| Portfolio accordion | The portfolio accordion is responsive |  |
| Profit / Loss | The updated profit / loss displays |  |
| Add new button | The add new button opens the transaction modal |  |
| Portfolio chart | Portfolio chart displays when tab open with updated data |  |
| Portfolio coins | Each coin in the portfolio displays on its own row |  |
| Updated coin value | When the page is reloaded the coins price, value, profit loss and 24h % change |  |
| New transactions | New transactions change the values on the portfolio page |  |
| Delete all records | Delete button when pressed will prompt the user with a message asking if they are sure they want to delete all records |  |
| View records | View button when pressed it opens the records modal |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.8 Record modal

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Relevant coin records | Only shows the records attributed to that coin |  |
| Date order | Shows record newest to oldest |  |
| Edit button | Opens the edit modal |  |
| Delete button | Prompts user with a message asking if they are sure they want to delete the record, if clicked the record is deleted |  |
| Flash delete message | User is prompted that the record was successfully deleted |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.9 Transaction modal

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Transaction tab works | Users can select buy, sell and staking changing the transaction form |  |
| Select coin | Lists top 50 crypto's |  |
| Buy order | Buy order records correct information |  |
| Sell order | Sell order records correct information |  |
| Staking order | Staking order records correct information |  |
| Orders update portfolio | Orders update correctly to the portfolio collection |  |
| Close button | Closes the modal with no transactions being recorded |  |
| Add transaction button | The record is submited |  |
| Flash transaction message | User is prompted that the transaction was successfully recorded |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |

## 5.10 Edit modal

| Test  | Expected result | Pass/Fail |
| --------------- | ------------------------------------------------------------------------- | --------- |
| Correct record being edited | The record the user clicked on is the one being edited |  |
| Cancel button | Closes the modal cancelling the changes |  |
| Submit works | When sumbit is clicked the record is updated |  |
| Flash edit message | User is prompted that the change was successful |  |
| Desktop breakpoints | Responsive on desktop |  |
| Tablet breakpoints | Responsive on tablet |  |
| Mobile breakpoints | Responsive on mobile |  |
