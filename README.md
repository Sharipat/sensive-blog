# Blog named after. Yuri Grigorievich

Blog about the commercial success of Yuri Grigorievich. I share advice on business, life and raising children.

![Screenshot](screenshots/site.png)

## Launch

To run the site you will need Python version 3.

Download the code from GitHub. Install dependencies:

```sh
pip install -r requirements.txt
```

Create a SQLite Database

```sh
python3 manage.py migrate
```

Start the development server

```
python3 manage.py runserver
```

## Environment variables

Some of the project settings are taken from environment variables. To define them, create a `.env` file next to `manage.py` and write the data there in the following format: `VARIABLE=value`.

There are 3 variables available:
- `DEBUG` - debug mode. Set to `True` to see debugging information in case of an error.
- `SECRET_KEY` — secret key of the project
- `DATABASE_FILEPATH` - full path to the SQLite database file, for example: `/home/user/schoolbase.sqlite3`
- `ALLOWED_HOSTS` - see [Django documentation](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)


## Project goals

The code was written for educational purposes - for a course on Python and web development on the website [Devman](https://dvmn.org).

Specifically, the repository is used:

- In the task “Optimizing the site” of the module [Introduction to Django: ORM](https://dvmn.org/modules/django-orm/).
- In the tutorial [Preview for ImageField in the admin panel](https://devman.org/encyclopedia/django/how-to-setup-image-preview/)