from flask import Flask, render_template_string, request, redirect, url_for
import psycopg2
import psycopg2.extras
import os
from datetime import datetime

app = Flask(__name__)

# ضع رابط قاعدة البيانات هنا إذا تريد مباشرة
# أو الأفضل خليه في Environment Variable باسم DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "PUT_YOUR_SUPABASE_DATABASE_URL_HERE")

# لوجو نوفا
LOGO_URL = "https://i.imgur.com/placeholder.png"
# إذا ما تريد رابط خارجي، تقدر بعدين تبدله بأي رابط مباشر للوجو

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        notes TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS test_catalog (
        id SERIAL PRIMARY KEY,
        test_name TEXT NOT NULL UNIQUE,
        category TEXT DEFAULT '',
        sell_price INTEGER NOT NULL DEFAULT 0,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
        patient_name TEXT NOT NULL,
        total_price INTEGER NOT NULL DEFAULT 0,
        paid_amount INTEGER NOT NULL DEFAULT 0,
        due_amount INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'آجل',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
        test_id INTEGER REFERENCES test_catalog(id) ON DELETE SET NULL,
        test_name TEXT NOT NULL,
        price INTEGER NOT NULL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id SERIAL PRIMARY KEY,
        item_name TEXT NOT NULL,
        qty INTEGER NOT NULL DEFAULT 0,
        unit_cost INTEGER NOT NULL DEFAULT 0,
        total_cost INTEGER NOT NULL DEFAULT 0,
        supplier TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def fetch_all(query, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params or ())
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_one(query, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params or ())
    row = cur.fetchone()
    conn.close()
    return row

def execute(query, params=None, returning=False):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params or ())
    row = cur.fetchone() if returning else None
    conn.commit()
    conn.close()
    return row

def month_summary():
    revenue = fetch_one("""
        SELECT COALESCE(SUM(paid_amount), 0) AS total
        FROM orders
        WHERE date_trunc('month', created_at) = date_trunc('month', CURRENT_DATE)
    """)["total"]

    purchases = fetch_one("""
        SELECT COALESCE(SUM(total_cost), 0) AS total
        FROM purchases
        WHERE date_trunc('month', created_at) = date_trunc('month', CURRENT_DATE)
    """)["total"]

    return int(revenue), int(purchases), int(revenue) - int(purchases)

base_css = """
<style>
*{box-sizing:border-box}
body{
    font-family:Arial,sans-serif;
    background:#f3f4f6;
    margin:0;
    direction:rtl;
    color:#111827;
}
.topbar{
    background:linear-gradient(90deg,#0f172a,#1d4ed8);
    color:#fff;
    padding:14px 18px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
}
.topbar .brand{
    display:flex;
    align-items:center;
    gap:12px;
}
.topbar img{
    width:82px;
    height:auto;
    background:white;
    border-radius:8px;
    padding:4px;
}
.topbar .title{
    font-size:24px;
    font-weight:bold;
}
.topbar .subtitle{
    font-size:12px;
    opacity:.9;
}
.container{
    max-width:1200px;
    margin:auto;
    padding:20px;
}
.cards{
    display:grid;
    grid-template
