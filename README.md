# Knowledge-quest
A quiz app with diverse and interesting quizzes.  
knowledge about fields that are not much talked about but are still interesting.  
the aim of this website is to spark curiosity among people of all ages. And make them interested in these field of studies.  
this helps more and more people and young minds to get atracted to some of the subjects of our quizzes and find new hobbies or passion. 
its also deployed.
## Link
https://knowledge-quest-bufo.onrender.com/

## Tools
#### Most notable:
This website is completely created on the robust fullstack web framework [Django](https://docs.djangoproject.com/en/6.0/)  
Ofcourse, Completely written in [Python](https://www.python.org/) A high-level interpreted programming language. 
For User authentication, a third-party, battle-tested and feature-rich package [Django-Allauth](https://docs.allauth.org/en/dev/introduction/index.html) is used.
not all of the features of this awesome tool are implemented in this project. notably its famous, robust and secure [Email-verification](https://docs.allauth.org/en/dev/account/configuration.html#email-verification) features.
Due to me not being able to pay for a Transactional Email Service to send varification emails to users. But it is definately consdered for future. 
as you could probably tell the project is deployed on the PaaS service [Render](https://render.com/). and the database is saperately hosted on high-quality and one of the best PostgreSQL hosting providers in 2025-2026 [Neon](https://neon.com/). 

#### Others worth mention:
* [bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/) through its CDN service for minimal styling and customization.
* [psycopg 3](https://pypi.org/project/psycopg/) for Neon support.
* [Uvicorn](https://uvicorn.dev/) for high-performance ASGI (Asynchronous Server Gateway Interface) service.
* [Gunicorn](https://gunicorn.org/#docs) for WSGI (Web Server Gateway Interface), combined with and supervising multiple Uvicorn worker processes.
* [Whitenoise](https://pypi.org/project/whitenoise/) for serving static files in production.
###### The rest is mentioned in the requirements.txt file.
