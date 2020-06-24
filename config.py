import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# DONE IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = "postgres://dkluuncfcsvasb:d7b7c37214917c1895b06adf3e73f2f57575f1935b105e3390d4744c5190392a@ec2-52-0-155-79.compute-1.amazonaws.com:5432/ddn59k3b73e2f8"