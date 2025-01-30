# Welcome

## Installation

To get started, clone this repo.

Create a .env.list file 
`touch .env.list`

and add your API Ninja API key:
`echo "API_NINJAS_KEY=your_key_here" >> .env.list`

## Make
`make build`
`make run`

`make rebuild` will rebuild the docker image and run it

## Docker
Build it:
`docker build -t loans .`

Run it:
`docker run -p 8000:8000 loans`

visit it: 
http://localhost:8000 

## bootstrap with pip
add back log dir:
`mkdir logs`
`touch logs/error.log`

Install the requirements (optionally create a virtualenv):
`python -m pip install -r requirements`

Run the migrations:
`python manage.py makemigrations`
`python manage.py migrate`

start the server:
`python manage.py runserver`
visit http://127.0.0.1:8000/

# Rationale

I read the specs then followed my heart.

I'd never set up Django from scratch, and I spent a few hours plunking around with boilerplates
Each of these falied with some undocumented environment variables or strange requirements: 
https://github.com/piepworks/blaze-starter
https://github.com/django-bridge/django-bridge
https://cookiecutter-django.readthedocs.io/en/latest/index.html

The only one that was actually workable, but it's missing SQLite bindings:
https://vercel.com/templates/python/django-hello-world

So I went back to Django Docs and started from scratch.
I tried out some Django Rest Framework.
I made Django Forms and got a bit carries away making the templates and UI.
I Dockerized it.

I'll be happy to discuss any decisions.

### Should dos
Let users edit and delete these. The API would support it, but I didn't make the UI for it.

### Could dos

**Auth & Rate Limiting:**
   - Implement auth & rate limiting to prevent abuse of your API endpoints, especially since they interact with an external service that might have rate limits.
**Caching:**
   - To reduce the number of external API calls, consider caching results for identical loan parameters using Django's caching framework.
**Documentation:**
     - Add more detailed documentation to the API, including information about the endpoints, parameters, and responses.
**Handle Edge Cases:**
    - Add more validations & scenarios, such as extremely high down payments or very short mortgage terms.