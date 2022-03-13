# First time

cd into the Diabetes Warrior directory.
`source .env` to set the environment variables.
`pip install -r requirements.txt` to install the python libraries.
`flask db init` to initialize the database.
`flask db migrate -m 'init'`
`flask db upgrade` upgrades the database.

`flask run` to start Diabetes Warrior

In your web browser go to `http://127.0.0.1:5000/` and start using Diabetes Warrior.

export DATABASE_URL=sqlite:///${PWD}/instance/app2.db
