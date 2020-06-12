# Simple-ToDo-App
Simple ToDo App☑️  on Python(Django) using DRF

What can this app do?
- Authorization (using email only)
- Creating tasks
- Altering tasks
- Setting execution status (like done/undone)
- sending email about status of execution

## Requirements

- Redis
- see requirements.txt

Make sure that you've installed all packages.

Note:

In 'settings.py' configure broker and email settings.

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
$ ./manage.py runserver
```

Open `http://127.0.0.1:8000/api/` and enjoy!




P.S:

If you're faced with error "bad credentials", fix it by reducing security, for instance, allow less secure apps.

For gmail go to https://myaccount.google.com/lesssecureapps and turn on it.


## Contributors

- Developed by @rruss
