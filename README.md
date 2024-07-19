# NotifyTube

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/aurora-dot/NotifyTube)

A small tool to get the latest videos for a query on YouTube, a feature they have been missing, so I decided to make it!

## Dependencies

1. Install chrome and chrome driver.
2. Install python poetry
3. Install node & npm
4. Run `npm install`
5. Run `poetry install`
6. Enter it's shell with `poetry shell`
7. Setup your `.env` file, according to `.env.example`
8. Then run, develop or test

## .env

An example local config:

```env
DEBUG=True
EMAIL_HOST=smtp.domain.com
EMAIL_HOST_USER=postmaster@domain.com
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=notification@ndomain.com
HEROKU=False
```

For prod (using heroku) you will also need to change `HEROKU=False` to `True` and to set these additionally with the above:

```env
SITENAME=domain.com
EMAIL_URL_BEGINNING=domain.com
SENTRY_DSN=
```

## Running

Build the css with `npm run build`
There are two commands which need to be ran concurrently, the first being `./manage.py runserver` and the second being `./manage.py cron`.
The first is the default Django command while the second collects videos and notifies users.

## Developing

I have included several vs code debug configs for convenience for the commands you can run, you will need to also run `npm run watch` if you are developing the frontend.

## Testing

Just run `./manage.py test`, however the repo needs more tests!
