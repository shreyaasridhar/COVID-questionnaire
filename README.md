# COVID-questionnaire
Hosted on Heroku at https://vibrantamerica.herokuapp.com/
## Motivation
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

## Design

### Database

1. User info table: Username, password, user id generation (sequential store in postgres)

2. Questionnaire table: Current date, username, user_id, array of answers

3. Questions table

If multiple entries for different users, have a different id for each questionnaire submission. 

### Backend

From the backend folder run pip install requirements.txt which includes all the required packages. To run the application,

FLASK_APP=app FLASK_ENV=development flask run

This runs the application in develop and debug mode in app.py. To run on Windows please view Flask documentation.

The application is now run on http://127.0.0.1:5000/ by default.

### Models 
SQLAlchemy model representation for each of the tables in the database. Password can be hashed when storing. If required, we can also use another table to create the specific hash value for each user’s password hash.

Functions to update, insert, and delete from the db.

SQLAlchemy so that we don’t write raw sql queries. 

There are endpoints to add questions to the database. All the endpoints are listed below.

## Flask: API endpoints:

### GET /
- General
  - Returns a login page where the username and password fields are mandatory

### POST /login 
- General
  - The submitted login form is sent to the endpoint to check if the user exists by comparing the hashes and a new user is created if no such user exists.
  - Also if the passwords don't match flashes an error message.

### GET /reset
- General
  - In case the user forgot the password, this endpoint is used to help create a new password combination

### POST /reset
- General
  - New credentials of the user is stored and redirected to the questionnaire

### GET /questionnaire
- General
  - Based on the redirected user, the survey template id rendered which once submitted provides a conformation 

### POST /questionnaire_submit
- General 
  - The form submitted from the `/questionnaire` is redirected to this endpoints that populated the table with the submitted survey information.

### POST /questionnaire
- General
  - Endpoint can be used to submit new questions to store in the database. The databse is read when the questionnaire template is rendered. 
  
- Sample request: `curl -X POST "http://127.0.0.1:5000/questionnaire" -H "Content-type: application/json" -d '{ "name": "Are you suffering from shortness of breath or other respiratory problems?" }'`

- Sample Response
```
Added question
```

### GET /users_today
- General
  - Returns a list of all the users who submitted the questionnaire today (that particular day).
- Sample request: `curl http://127.0.0.1:5000/users_today`
```
{
  "success": true,
  "today": [
    {
      "Userid": 1,
      "Username": "Jane",
      "questions": [
        "false",
        "false",
        "false"
      ]
    },
    {
      "Userid": 2,
      "Username": "John",
      "questions": [
        "false",
        "false",
        "false"
      ]
    },
    {
      "Userid": 3,
      "Username": "Lydia",
      "questions": [
        "false",
        "false",
        "false"
      ]
    }
  ],
  "total_entries": 3
}
```

### GET /date-filter

- General 
  - Renders a simple html form that requires a date and it lists out all the users who submitted the form on that particular date.

### POST /users-by-date
- General 
  - Reads the form data for the date and redirects to the page with the relevant information like below.

```
{
   "date":"2020-06-23",
   "users":[
      {
         "Username":"shreyaa",
         "Userid":1,
         "questions":[
            "false",
            "false",
            "false"
         ]
      }
   ],
   "total_entries":1
}
```

## Deployment

Heroku deployed: `https://vibrantamerica.herokuapp.com`

### Authors

[Shreyaa Sridhar](https://github.com/shreyaasridhar)

### Acknowledgements

Vibrant Sciences interview :)

Great amounts of Patience with deployment! :p

### QUERY:
SQL query to select password and retrive current information. 

`SELECT * FROM USER WHERE USERNAME==VAL1 AND PASSWORD == VAL2`

`SELECT * FROM QTABLE WHERE where DATE_FORMAT(Current_date, '%d/%m/%y %T') <= now();`

