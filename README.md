# My API

This project is a demo template to test out API development with:

* Python3
* Flask
* Flask RESTful
---
## Current Content

### Authorization

The user must have a valid account in the database to authorize themselves via username (email) and password. Upon authorization the API returns an API Key token which must be supplied for all requests.  The token has an expiry date and a default limit of 100 requests.  When expired a new token must be requested.

### Message

A simple end point which check the current user is authorized, brings the current user into context, and returns a greeting to the name associated with the account.

### Tasks

Allows the user to view and manage tasks associated with their account.
---
## Installation

1. Clone
2. Create config.py add the following variables to automatically create a default account (set variable values)
	2.1 initial_password = ''
	2.2 initial_username = ''
	2.3 initial_email = ''
3. Run init_databases.py to creat the databases


---
... more to follow ...