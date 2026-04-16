from flask import Flask, render_template_string, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = "PUT_YOUR_SUPABASE_URL_HERE"

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = cur.fetchall()

    cur.execute("SELECT * FROM tests ORDER BY id DESC")
    tests = cur.fetchall()

    cur.execute("SELECT COALESCE(SUM(paid),0) FROM tests")
    total_paid = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(due),0) FROM tests")
    total_due = cur.fetchone()[0]

    conn.close()

    return render_template_string(html,
        patients=patients,
        tests=tests,
        patients_count=len(patients),
        tests_count=len(tests),
        total_paid=total_paid,
        total_due=total_due
    )

@app.route("/add_patient", methods=["GET","POST"])
def add_patient():
    if request.method == "POST":
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO patients (name, age, gender, phone) VALUES (%s,%s,%s,%s)",
            (
                request.form["name"],
                request.form["age"],
                request.form["gender"],
                request.form["phone"]
            )
        )

        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    return render_template_string(add_patient_html)

@app.route("/add_test", methods=["GET","POST"])
def add_test():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT name FROM patients")
    patients = cur.fetchall()

    if request.method == "POST":
        price = int(request.form["price"])
        paid = int(request.form["paid"])
        due = price - paid

        if due <= 0:
            status = "مدفوع"
            due = 0
        elif paid == 0:
            status = "آجل"
        else:
            status = "جزئي"

        cur.execute(
            "INSERT INTO tests (patient_name, test_name, price, paid, due, status) VALUES (%s,%s,%s,%s,%s,%s)",
            (
                request.form["patient"],
                request.form["test"],
                price,
                paid,
                due,
                status
            )
        )

        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    conn.close()
    return render_template_string(add_test_html, patients=patients)

# نفس HTML السابق (لا تغيّره)
html = """ضع هنا كود الواجهة القديم"""
add_patient_html = """ضع هنا كود صفحة إضافة المريض"""
add_test_html = """ضع هنا كود طلب الفحص"""

if __name__ == "__main__":
    app.run()
