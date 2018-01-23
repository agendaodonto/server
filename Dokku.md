# Dokku Setup

This a basic step by step how to deploy this app on a [Dokku instance](https://github.com/dokku/dokku)

1. Install the required plugins:
 - Postgres `sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git`
 - RabbitMQ `sudo dokku plugin:install https://github.com/dokku/dokku-rabbitmq.git`
 - Let's Encrypt `sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git`
2. Create a new app `dokku apps:create backend-staging`
3. Create a new Postgres database `dokku postgres:create staging-db`
4. Link the new db with the app `dokku postgres:link staging-db backend-staging`
5. Create a new RabbitMQ service `dokku rabbitmq:create staging-store`
6. Link the new store with the app `dokku rabbitmq:link staging-store backend-staging`
7. Configure environment variables `dokku --app backend-staging config:set [KEY]=[VALUE]`
 - DJANGO_SECRET_KEY (A new one can be generated with `tr -dc A-Za-z0-9 </dev/urandom | head -c 48`)
 - DJANGO_SETTINGS_MODULE (`app.settings.prod` or `app.settings.staging`)
 - [SMS_GATEWAY_USER](https://smsgateway.me/admin/users/login#signup)
 - [SMS_GATEWAY_PASSWORD](https://smsgateway.me/admin/users/login#signup)
 - EMAIL_HOST
 - EMAIL_HOST_PASSWORD
 - EMAIL_HOST_USER
8. Deploy the app once.
9. Setup Let's Encrypt (Optional, but recommended)
 - Add email as a global variable `dokku config:set --global DOKKU_LETSENCRYPT_EMAIL=domain@tld.com`
 - Run configuration command `dokku letsencrypt backend-staging`
