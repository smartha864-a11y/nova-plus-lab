from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "nova_lab.db"

def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            test_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            paid INTEGER NOT NULL,
            due INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

html = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>Nova Lab System</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    margin: 0;
    direction: rtl;
}
.header {
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    color: white;
    padding: 18px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
}
.subheader {
    text-align: center;
    color: #334155;
    margin-top: 8px;
    font-size: 14px;
}
.container {
    padding: 20px;
    max-width: 1200px;
    margin: auto;
}
.cards {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    flex: 1;
    min-width: 180px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
.card .icon {
    font-size: 28px;
    margin-bottom: 8px;
}
.card .num {
    font-size: 24px;
    font-weight: bold;
    color: #0f172a;
}
.card .label {
    color: #475569;
    margin-top: 6px;
}
.actions {
    margin: 20px 0;
    text-align: center;
}
.actions a {
    display: inline-block;
    text-decoration: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    margin: 6px;
    font-size: 15px;
}
.actions a:hover {
    background: #1d4ed8;
}
.table-box {
    background: white;
    margin-top: 20px;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    overflow-x: auto;
}
.table-box h3 {
    margin-top: 0;
    color: #0f172a;
}
table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    padding: 12px;
    border-bottom: 1px solid #e5e7eb;
    text-align: right;
    font-size: 14px;
}
th {
    background: #eff6ff;
    color: #1e3a8a;
}
.empty {
    color: #64748b;
    text-align: center;
    padding: 20px;
}
.form-box {
    max-width: 550px;
    margin: 30px auto;
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
.form-box h2 {
    text-align: center;
    margin-top: 0;
    color: #0f172a;
}
label {
    display: block;
    margin-bottom: 6px;
    color: #334155;
    font-size: 14px;
}
input, select {
    width: 100%;
    padding: 12px;
    margin-bottom: 16px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    box-sizing: border-box;
    font-size: 14px;
}
button, .back-link {
    display: inline-block;
    text-decoration: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
}
.back-link {
    background: #64748b;
    margin-right: 8px;
}
.form-actions {
    text-align: center;
    margin-top: 10px;
}
.badge-paid {
    color: #166534;
    font-weight: bold;
}
.badge-partial {
    color: #b45309;
    font-weight: bold;
}
.badge-due {
    color: #b91c1c;
    font-weight: bold;
}
</style>
</head>
<body>

<div class="header">Nova Lab System</div>
<div class="subheader">نظام حسابات ومرضى وفحوصات مختبر</div>

<div class="container">

    <div class="cards">
        <div class="card">
            <div class="icon">👥</div>
            <div class="num">{{ patients_count }}</div>
            <div class="label">عدد المرضى</div>
        </div>
        <div class="card">
            <div class="icon">🧪</div>
            <div class="num">{{ tests_count }}</div>
            <div class="label">عدد الطلبات</div>
        </div>
        <div class="card">
            <div class="icon">💰</div>
            <div class="num">{{ total_paid }}</div>
            <div class="label">إجمالي المدفوع</div>
        </div>
        <div class="card">
            <div class="icon">⚠️</div>
            <div class="num">{{ total_due }}</div>
            <div class="label">إجمالي المتبقي</div>
        </div>
    </div>

    <div class="actions">
        <a href="/add_patient">➕ إضافة مريض</a>
        <a href="/add_test">🧪 طلب فحص</a>
    </div>

    <div class="table-box">
        <h3>المرضى</h3>
        {% if patients %}
        <table>
            <tr>
                <th>الاسم</th>
                <th>العمر</th>
                <th>الجنس</th>
                <th>الهاتف</th>
            </tr>
            {% for p in patients %}
            <tr>
                <td>{{ p["name"] }}</td>
                <td>{{ p["age"] }}</td>
                <td>{{ p["gender"] }}</td>
                <td>{{ p["phone"] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <div class="empty">لا يوجد مرضى بعد</div>
        {% endif %}
    </div>

    <div class="table-box">
        <h3>طلبات الفحوصات</h3>
        {% if tests %}
        <table>
            <tr>
                <th>المريض</th>
                <th>الفحص</th>
                <th>السعر</th>
                <th>المدفوع</th>
                <th>المتبقي</th>
                <th>الحالة</th>
            </tr>
            {% for t in tests %}
            <tr>
                <td>{{ t["patient_name"] }}</td>
                <td>{{ t["test_name"] }}</td>
                <td>{{ t["price"] }}</td>
                <td>{{ t["paid"] }}</td>
                <td>{{ t["due"] }}</td>
                <td>
                    {% if t["status"] == 'مدفوع' %}
                        <span class="badge-paid">{{ t["status"] }}</span>
                    {% elif t["status"] == 'جزئي' %}
                        <span class="badge-partial">{{ t["status"] }}</span>
                    {% else %}
                        <span class="badge-due">{{ t["status"] }}</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <div class="empty">لا توجد طلبات فحوصات بعد</div>
        {% endif %}
    </div>

</div>
</body>
</html>
"""

add_patient_html = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>إضافة مريض</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    direction: rtl;
    margin: 0;
}
.header {
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    color: white;
    padding: 18px;
    text-align: center;
    font-size: 24px;
}
.form-box {
    max-width: 550px;
    margin: 30px auto;
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
label {
    display: block;
    margin-bottom: 6px;
    color: #334155;
}
input, select {
    width: 100%;
    padding: 12px;
    margin-bottom: 16px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    box-sizing: border-box;
}
button, a {
    display: inline-block;
    text-decoration: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}
a {
    background: #64748b;
    margin-right: 8px;
}
.form-actions {
    text-align: center;
}
</style>
</head>
<body>
<div class="header">إضافة مريض</div>
<div class="form-box">
    <form method="POST">
        <label>اسم المريض</label>
        <input type="text" name="name" required>

        <label>العمر</label>
        <input type="number" name="age" required>

        <label>الجنس</label>
        <select name="gender" required>
            <option value="ذكر">ذكر</option>
            <option value="أنثى">أنثى</option>
        </select>

        <label>الهاتف</label>
        <input type="text" name="phone" required>

        <div class="form-actions">
            <button type="submit">حفظ</button>
            <a href="/">رجوع</a>
        </div>
    </form>
</div>
</body>
</html>
"""

add_test_html = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>طلب فحص</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    direction: rtl;
    margin: 0;
}
.header {
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    color: white;
    padding: 18px;
    text-align: center;
    font-size: 24px;
}
.form-box {
    max-width: 550px;
    margin: 30px auto;
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
label {
    display: block;
    margin-bottom: 6px;
    color: #334155;
}
input, select {
    width: 100%;
    padding: 12px;
    margin-bottom: 16px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    box-sizing: border-box;
}
button, a {
    display: inline-block;
    text-decoration: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}
a {
    background: #64748b;
    margin-right: 8px;
}
.form-actions {
    text-align: center;
}
</style>
</head>
<body>
<div class="header">طلب فحص</div>
<div class="form-box">
    <form method="POST">
        <label>المريض</label>
        <select name="patient" required>
            <option value="">اختر المريض</option>
            {% for p in patients %}
            <option value="{{ p["name"] }}">{{ p["name"] }}</option>
            {% endfor %}
        </select>

        <label>نوع الفحص</label>
        <input type="text" name="test" required>

        <label>السعر</label>
        <input type="number" name="price" required>

        <label>المدفوع</label>
        <input type="number" name="paid" required>

        <div class="form-actions">
            <button type="submit">حفظ</button>
            <a href="/">رجوع</a>
        </div>
    </form>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    conn = get_conn()
    patients = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    tests = conn.execute("SELECT * FROM tests ORDER BY id DESC").fetchall()

    total_paid = conn.execute("SELECT COALESCE(SUM(paid), 0) FROM tests").fetchone()[0]
    total_due = conn.execute("SELECT COALESCE(SUM(due), 0) FROM tests").fetchone()[0]

    conn.close()

    return render_template_string(
        html,
        patients=patients,
        tests=tests,
        patients_count=len(patients),
        tests_count=len(tests),
        total_paid=total_paid,
        total_due=total_due
    )

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        conn = get_conn()
        conn.execute(
            "INSERT INTO patients (name, age, gender, phone) VALUES (?, ?, ?, ?)",
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

@app.route("/add_test", methods=["GET", "POST"])
def add_test():
    conn = get_conn()
    patients = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()

    if request.method == "POST":
        price = int(request.form["price"])
        paid = int(request.form["paid"])
        due = price - paid

        if due <= 0:
            due = 0
            status = "مدفوع"
        elif paid == 0:
            status = "آجل"
        else:
            status = "جزئي"

        conn.execute(
            "INSERT INTO tests (patient_name, test_name, price, paid, due, status) VALUES (?, ?, ?, ?, ?, ?)",
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

init_db()

if __name__ == "__main__":
    app.run()
