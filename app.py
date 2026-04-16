from flask import Flask
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgresql://postgres:password@aws-xxx.pooler.supabase.com:6543/postgres"

def get_conn():
    return psycopg2.connect(DATABASE_URL)
