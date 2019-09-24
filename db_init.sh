rm -rf migrations
rm app.db
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
