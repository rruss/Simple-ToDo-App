# Simple-ToDo-App
Simple ToDo App☑️  on Python(Django) using DRF

What can this app do?
- Authorization (using email only)
- Creating tasks
- Altering tasks
- Setting execution status
- sending email about status of execution

## Requirement

- see requirements.txt

Make sure that you've installed all packages.

Note:
If you are using OS other than unix-like, just google for respective commands))

## Usage

Clone it!

```
$ git clone https://github.com/rruss/Simple-ToDo-App
```


Run RabbitMQ server:



```
$ sudo rabbitmq-server
```


Run Celery using:

```
$ celery -A djcelery worker -l info
```

Go into the project directory and:

```
$ python manage.py runserver
```

Open `http://127.0.0.1:8000/` and enjoy!


## Contributors

- Developed by @rruss
