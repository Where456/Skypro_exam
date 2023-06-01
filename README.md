# A simple REST-based Flask application to work with the database

This tutorial provides a description and instructions for using a simple REST application on Flask that provides database functionality. The application allows you to perform read, add, update and delete operations on data.

## Routes and domains
### 1. Getting all data
Method: GET
URL: http://158.160.4.220/

Description: Gets all data from the database.

Example response:
<img width="357" alt="image" src="https://github.com/Where456/Skypro_exam/assets/119400636/1d2d220f-804b-432b-8045-5b411deb8984">
---
### 2. Adding new data
Method: POST
URL: http://158.160.4.220/add

Description: Adds new data to the database.

Request body: JSON object with a text field to specify the title and content of the note.

Example request:
![img_2.png](static/img_2.png)
---
### 3. Changing data
Method: PUT
URL: http://158.160.4.220/schedules/{id}

Description: Changes the data in the database for the specified id.

Request body: JSON object with title and content fields to specify the new title and content of the note.

Example request:
![img_3.png](static/img_3.png)
---
### 4. Deleting data
Method: DELETE
URL: http://158.160.4.220/delete/1{id}

Description: Deletes data from the database for the specified id.

Example request:
![img_5.png](static/img_5.png)
