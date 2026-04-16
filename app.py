from flask import Flask
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgresql://..."

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Nova Lab System is working 🚀"
