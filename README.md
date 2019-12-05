# My API

This project is a demo template to test out API development with:

* Flask
* Flask RestFul


## Current Content


### Authorization

The user must have a valid account in the database to authorize themselves via username (email) and password. Upon authorization the API returns an API Key token which must be supplied for all requests.  The token has an expiry date and a default limit of 100 requests.  When expired a new token must be requested.

### Message

A simple end point which check the current user is authorized, brings the current user into context, and returns a greeting to the name associated with the account.

### Tasks

Allows the user to view and manage tasks associated with their account.