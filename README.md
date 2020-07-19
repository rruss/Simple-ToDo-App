# Simple-ToDo-App
Simple ToDo App☑️  on Python(Django) using DRF

What can this app do?
- Authorization (using email only) [Registration is under process]
- Creating tasks
- Altering tasks
- Setting execution status (like done/undone)
- sending email about status of execution


## Requirements

- docker-compose

Make sure that you've installed it properly from https://docs.docker.com/compose/install.

Note:

In 'settings.py' configure email settings.

## Usage

Clone it!

```
$ git clone https://github.com/rruss/Simple-ToDo-App
```


Build containers:



```
$ docker-compose build
```


Run the builded containers:

```
$ docker-compose up
```



Open `http://0.0.0.0:8000` and enjoy!




P.S:

If you're faced with error "bad credentials", fix it by reducing security of mailing system, for instance, allow less secure apps.

For gmail, go to https://myaccount.google.com/lesssecureapps and turn on it.


## Contributors

- Developed with 💚
