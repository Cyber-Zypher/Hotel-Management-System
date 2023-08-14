
# Hotel Management System with Python and MySQL database
A simple Hotel Management system with Python and MySQL database with TKinter GUI.
Easily customizable with flexible syntax.


## Install the required Libraries.

Clone the project

```
pip install pymysql
```
or
```
python -m pip install pymysql
```
## Screenshots

![App Screenshot](https://github.com/Cyber-Zypher/Hotel-Management-System/blob/main/WhatsApp%20Image%202023-08-14%20at%206.33.42%20AM.jpeg))

## Initialize the database
```
CREATE DATABASE hotel_booking;

USE hotel_booking;

CREATE TABLE bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    guest_name VARCHAR(100),
    check_in DATE,
    check_out DATE,
    room_type VARCHAR(50)
);
```

## Instructions

- After installing the needed libraries. Edit the `data.csv` file to load the questions and its answers.

- Then, run the `load_data.py` script to load the questions and answers to the SQL database.

- Don't run the `load_data.py` more than once, It will cause duplicate questions and cause clutter on your database.

- Then Finally, run the `app.py` to play the quiz.


## Authors

- [@sidharth_everett](https://github.com/Cyber-Zypher)
- [@sindhu_vaibhav_KL](https://www.instagram.com/sindhuvaibhav2007/)
- [And our friends @Medusa Infosystems International](https://www.instagram.com/themedusaclan_official/)

