from flask import Flask
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgresql://xxxxxx"

def get_conn():
    return psycopg2.connect(DATABASE_URL)
