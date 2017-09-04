# Step to run flask-celery example project
1. download redis server or rabitmq
2. run redis/rabitmq server
3. Start celery server with follow command:
    celery -A flask_proj.celery worker --loglevel=info
4. Run flask app
    Export(Set if window) FLASK_APP=flask_proj.py
    python -m flask run

# Now you can test your app with flask and celery