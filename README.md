## Rates API

### Requirements:
* Python-3.6.7
* MySQL-5.7.26
* **Packages:**
    * Django-2.2.2
    * djangorestframework-3.9.4
    * mysqlclient-1.4.2.post1

### Installation:
Clone the repository.
```
$ git clone git@github.com:hamzach/ratestask.git
$ cd ratestask
```
Setup the required environment variables.
```
$ export DB_NAME=<database_schema>
$ export DB_USER=<database_username>
$ export DB_PASSWORD=<database_user_password>
$ export DB_HOST=<database_host>
$ export OER_APP_ID=<your_openexchangerate_app_id>
```
Install the required python packages.
```
$ pip install -r requirements.txt
```
Create a schema in mysql with the name that you have set in DB_NAME and run the
database migrations by executing this command.
```
$ python manage.py migrate
```
Load the required data in the database.
```
$ python manage.py loaddata rates_api/fixtures/rates_api.json
```
Finally, start the django server.
```
$ python manage.py runserver
```