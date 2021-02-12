# Procesos Web (ScraLaw) API

This is the repository for the RESTful API built for the Procesos Web (ScraLaw) application. Its code is built with Python and the Flask Web Framework. It responds to authenticated front-end requests, validated through an AWS Cognito Service, and connects to a NoSQL AWS database called DynamoDB. Some of its files contain configurations for deployment through AWS Elastic Beanstalk in a EC2 AWS instance running Amazon Linux 2 .

![enter image description here](https://i.ibb.co/n3bD7dR/RE2.png)

# Configurations

For this API to work, several settings must be defined. This includes:

- Valid AWS Cognito UserPool ID and APP Client ID.
- Valid region for the AWS Dynamo Data Base.
- Valid NGINX configuration files that define correct Timeout times for requests and responses (.platform/nginx folder).
- Valid timezone configuration (.ebextensions folder)

# Access

This API can be accessed from any origin due to it have a completely open CORS policy.
Its functioning, however, is blocked for most of its endpoints through an authentication method that validates a JWT token, provided by the front-end, and compared against an AWS Cognito User Pool.

The token must be provided through an HTTP header in the form of:

**X-MyApp-Authorization: Bearer token**

Any attempt to access an authenticated end-point without the correct header, or with an invalid JWT token will result in a response similar to the following:

![enter image description here](https://i.ibb.co/m41DGyJ/RE1.png)

# Endpoints

## Status

The API has a standard STATUS endpoint that does not require authentication and provides a response indicating whether the service is working correctly or not.

    /api/status

    GET: Returns the status of the connection to the API

## Test

There is also a couple of unauthenticated test endpoints that can be used to perform operations configured in the code.

    /api/test:

    GET: Endpoint for testing database queries


    /api/testp:

    GET: Endpoint for testing scrapper

##

Besides this, the rest of the endpoints can be divided between Users, and Processes. For each of these, the API has the four standard methods for CRUD operations, GET, POST, PUT, and DELETE.

## User Endpoints

**Users are represented in the database with the following attributes:**

    user_id: A unique identifier for each user  (String)
    tier: An attribute not used right now, but represents a payment tier (String)
    first_name: The first name of the user (String)
    last_name: The last name of the user (String)
    person_id_type: The type of personal legal identification (String)
    person_id:  The legal identification number (String)
    e_mail: The user's email (String)
    cel: The user's cellphone number (String)
    created_at: Creation date of the user in ISO Format (String)
    updated_at:  Last updated date for the user in ISO Format (String)
    processes: Legal processes belonging to a user (Object)

**The user endpoints are presented next:**

    /api/users/

    GET: Returns a json containing all users in the database with their respective information


    /api/users/<user_id>

    GET: Returns a json with all the attributes of a specific user


    /api/users/<user_id>
    POST: Creates a new user in the database with the provided user_id (personal data attributes are optional and can be given in the body of the request in json format)


    /api/users/<user_id>
    PUT: Updates attributes of a specific user except for processes (Receives the data as a json in the body of the request)


    /api/users/<user_id>
    DELETE: Deletes a specific user from the database with all of its contents

## Processes Endpoints

Legal processes have specific endpoints, and they depend on a combination of process_id and user_id.

The process id is given by the user at the moment of creating a new process, and its value is generated through legal information independent from this web application.

**In the database, a process is stored as follows:**

    radicated_at: Date of process radication (String)
    type_proc: Type of process (String)
    parties: Parties in the process (Object with values as List)
    office: (Object) Contains:
            name: Name of office (String)
            judge:  Name of the judge (String)
            city: location of the office (String)
    movements: Contains information regarding the different movements of the legal process (Array of Objects)
    location: location of the process (String)
    location_expediente: location of physical document in the office

**The processes endpoints are presented next:**

    /api/processes/<process_id>/<user_id>

    GET: Returns a json with all the information of a specific legal process belonging to a specific user.


    /api/processes/user/<user_id>

    GET: Returns a json with all the legal processes belonging to a specific user.


    /api/processes/<process_id>/<user_id>

    POST, PUT: Creates or updates a specific legal process belonging to a specific user. On creation a Web Scraper performs data extraction from a governmental website, so its response time depends on the performance of said web page.


    /api/processes/<process_id>/<user_id>

    DELETE: Deletes a specific legal process belonging to a specific user.

# Web Scraper

In order to obtain the information of a legal process on a request for creation or update, the API uses a Web Scraper built with Beautiful Soup in Python. This scraper performs all the necessary operations in order to return a dictionary data structure containing all the relevant data of a process.

![enter image description here](https://i.ibb.co/b3bnkfF/RE3.png)

This scrapper is called by the corresponding endpoint and its data is then processed to add creation or update times in ISO format as string and then create a valid json response to answer a request.

The Web Scraping function can be found in the Scraper Folder in the file LawScraperBeautifulSoup under the name "scrap_law".

# Database Functions

The API uses the boto3 library in order to perform integration with the AWS Dynamo DataBase.

![enter image description here](https://i.ibb.co/XtRGvn9/RE4.png)

All the CRUD functions for the database can be found in the Dynamo Folder, including operations with items in a table, and also tables themselves.

# Project Front-End

This is the Repo for the front-end build with ReactJS

[Click me](https://github.com/cbayonao/Frontend_Proyecto_final_HBS)

# Project Deployed

This is the deployed project with AWS

[Click me](https://procesosweb.consulting/)

# Challenges and Future Features

This was a really challenging project to develop because of the implementation of AWS services and the steep learning curve in some of them.

Still, the development was really enriching, and the knowledge obtained was definitely worth it.

In the future it would be interesting to migrate the web scraper to a more specialized tool such as Scrapy by itself or in conjunction with Selenium.

It would also be interesting to evaluate serverless alternatives to run the API.

# Authors

Jhoan Zamora [jzamora5](https://github.com/jzamora5)  
Miguel Parada [michaelAuditore](https://github.com/michaelAuditore/)  
Camilo Bayona [cbayonao](https://github.com/cbayonao)

# About Myself

🎯 I am a Fullstack developer in love with technology and keen to learn new things everyday. My strenghts reside in Python and JavaScript although I am not afraid to take on any other language.

🎯 I have experience developing both back end and front end. I have used technologies such as Bootstrap, SASS, React, Flask, Django, Express, SQL, MongoDB, AWS, among others.

🎯 I also studied Sound Engineering some years ago, and I love music, videogames, and audiovisual media.

🔹 [LinkedIn](https://www.linkedin.com/in/jhoan-stiven-zamora-caicedo/)

🔹 [Twitter](https://twitter.com/JhoanZamora10)
