# Link-Shortener
The application can be accessed through [this link](https://gabrielpazinatto.github.io/link-shortener/).

## How it works
This application is very simple. It uses a PostGreSQL database hosted on Neon, which is accessed through functions in [db.py](./python/db.py) and queries contained in [queries.py](./python/queries.py). In order to encapsulate the database access, a FastAPI API ([api.py](./api.py)), hosted on Vercel, is used.

## Authentication System
Currently, the authentication system is extremely simple, it just stores the user id in browser local storage and checks it every time an API call is made. Hence, it's trivial to access other accounts without using a password. This is something I intend to work on yet.

Being logged in allows users to add an URL, which is then inserted into the database in pair with a random generated string, which will act as the short url. All urls added by an user can be seen in the "User Page" when logged in.

## Redirection System

Every shortened URL generated redirects the user to a subdomain of <a>shortify.rf.gd</a>, which is a website hosted on InfinityFree. This website simply redirects the user to the correct API URL, which retrieves the full URL from the database and triggers a redirection. 

