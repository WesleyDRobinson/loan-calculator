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

I started this project from scractch using the Django Docs.
It evolved to using some Django Rest Framework.
I used Django Forms and got a bit carried away making the templates and UI.
I choose plain HTML and tachyons.io for the markup and styling.
I Dockerized it, and added a Makefile to make it easier to run.

I am looking forward to discussing my decisions and trade-offs.

### Should do next:
Create functionality for users to edit and delete these loans. 
The DRF API supports it already, but I didn't make the UI for it.

### Could dos

**Auth & Rate Limiting:**
   - Implement auth & rate limiting to prevent abuse of your API endpoints, especially since they interact with an external service that might have rate limits.
**Caching:**
   - To reduce the number of external API calls, consider caching results for identical loan parameters using Django's caching framework.
**Documentation:**
     - Add more detailed documentation to the API, including information about the endpoints, parameters, and responses.
**Handle Edge Cases:**
    - Add more validations & scenarios, such as extremely high down payments or very short mortgage terms.