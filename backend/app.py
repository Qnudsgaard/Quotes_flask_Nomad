"""
Backend flask app, provides an API for retrieving and
storing quotes, can connect to an external database
to persist quotes.
"""
import random
import os
from flask import Flask, jsonify, request
from flask_healthz import healthz
import db
from quotes import default_quotes


# create the flask app
app = Flask(__name__)

# add flask-healthz config to flask config
app.config["HEALTHZ"] = {"live": "healthz.liveness", "ready": "healthz.readiness"}
# create the healthz endpoints
app.register_blueprint(healthz, url_prefix="/healthz")


# host for the backend, if not set default to False
DATABASE_HOST = os.environ.get("db_host", False)
DATABASE_USER = os.environ.get("db_user", False)
DATABASE_PASSWORD = os.environ.get("db_password", False)
DATABASE_NAME = os.environ.get("db_name", False)

DB_CONN = {
    "host": DATABASE_HOST,
    "user": DATABASE_USER,
    "password": DATABASE_PASSWORD,
    "name": DATABASE_NAME,
}

# the list of quotes
QUOTES = default_quotes


def check_db_creds_are_set() -> bool:
    """Checks if the user has set all env vars needed for connecting to the db, and warns them otherwise"""
    all_set = True
    if not DATABASE_HOST:
        print("WARNING: 'db_host' environment variable not set, set this to connect to the database.", flush=True)
        all_set = False

    if not DATABASE_USER:
        print("WARNING: 'db_user' environment variable not set, set this to connect to the database.", flush=True)
        all_set = False

    if not DATABASE_PASSWORD:
        print("WARNING: 'db_password' environment variable not set, set this to connect to the database.", flush=True)
        all_set = False

    if not DATABASE_NAME:
        print("WARNING: 'db_name' environment variable not set, set this to connect to the database.", flush=True)
        all_set = False

    return all_set


def check_if_db_is_available() -> bool:
    """Check if the db is reachable and should be used"""
    print("Checking connection to the database ...", flush=True)

    if check_db_creds_are_set():
        return db.check_connection(DB_CONN)
    else:
        print("WARNING: database connection environment variables not set, cannot test connection.", flush=True)
        return False


@app.route("/check-db-connection")
def check_db_connection():
    """Other services can ask if the db is connected."""
    if check_if_db_is_available():
        return jsonify({"db-connected": "true"})
    else:
        return jsonify({"db-connected": "false"})


@app.route("/add-quote", methods=["POST"])
def add_quote():
    """add quote to list of quotes"""
    if request.method == "POST":
        request_json = request.get_json()

        if "quote" in request_json:
            quote = request_json["quote"]
            QUOTES.append(quote)

            if check_if_db_is_available():
                inserted = db.insert_quote(quote, DB_CONN)
                if inserted:
                    print(f"Successfully inserted '{quote}' into db.", flush=True)
                else:
                    print(f"ERROR: could insert '{quote}' into db.", flush=True)
        else:
            # TODO propper logging
            print("Error: could not find 'quote' in request", flush=True)
            return "No 'quote' key in JSON", 500

        return "Quote received", 200
    return "Could not parse quote", 500


@app.route("/quotes")
def quotes():
    """return all quotes as JSON"""
    if check_if_db_is_available():
        quotes = db.get_quotes(DB_CONN)
        if quotes:
            return jsonify(quotes)
        return jsonify([])
    return jsonify(QUOTES)


@app.route("/quote")
def quote():
    """return single random quote"""
    return random.choice(QUOTES)
