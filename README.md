# Simple-ToDo-App
Simple ToDo App☑️  on Python(Django) using DRF

What can this app do?
- Authorization (using email only)
- Creating tasks
- Altering tasks
- Setting execution status
- sending email about status of execution

## Requirements

- Redis
- see requirements.txt

Make sure that you've installed all packages.

Note:
In 'settings.py' configure broker and email settings
If you are using OS other than unix-like, just google for respective commands))

## Usage

Clone it!

```
$ git clone https://github.com/rruss/Simple-ToDo-App
```


Run Redis server:



```
$ redis-server
```


Run Celery using:

```
$ celery -A ToDo worker -l info
```

Go into the project directory and after migrating everything:

```
$ python manage.py runserver
```

Open `http://127.0.0.1:8000/api/` and enjoy!


## Contributors

- Developed by @rruss
