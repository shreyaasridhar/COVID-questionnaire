# COVID-questionnaire

Design a web-based system with a login page and provide a questionnaire to ask if user has Covid-19 symptoms:

•	The system should include a backend database to store the credentials (username and password) and verify the login before allowing form access.

Questionnaire form:

The questionnaire is a basic form which has the following pieces 

•	Current Date

•	The following yes/no questions

  o	Are you experiencing any flu symptoms-like cold, cough?

  o	Are you experiencing any of these conditions: Stomach upset, vomiting, fatigue?

  o	Are you suffering from shortness of breath or other respiratory problems?

•	Save the questionnaire form response to a database and link it with the user who logged in. In other words, we need to know which user filled out the form 
You can use any backend server of your choice (Java preferably), and vanilla HTML5 + Bootstrap 4 for front end design of the login page and form. You can use any database which you are comfortable with (preferably MySQL).

Bonus points:

•	Provide queries to fetch the data for the users who filled out the form in a given day and who did not fill it out.



### Database

1.	User info table: Username, password, user id generation (sequential store in postgres)

2.	Questionnaire table: Current date, q1, q2, q3, user_id

If multiple entries for different users, have a different id for each questionnaire submission. the table and set the user_id as a foreign key in the database. Else it can be the primary key of the database.

### Backend
Flask 
### Models 
SQLAlchemy model representation for each of the tables in the database. Password can be hashed when storing. If required, we can also use another table to create the specific hash value for each user’s password hash.

Functions to update, insert, and delete from the db.

SQLAlchemy so that we don’t write raw sql queries. 

Migrations in flask to keep track of all the databse changes will help incase we need to modify the structure of the questionnaire

### Flask: API endpoints:
1.	to receive the endpoint of data from login and password 

  a.	Salted Hash to store the password

2.	endpoint on submit data from the questionnaire to store in the database

### QUERY:
SELECT * FROM USER WHERE USERNAME==VAL1 AND PASSWORD == VAL2

SELECT * FROM QTABLE WHERE where DATE_FORMAT(Current_date, '%d/%m/%y %T') <= now();

