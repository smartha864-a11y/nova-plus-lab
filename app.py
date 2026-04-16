from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

patients = []
tests = []

html = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>Nova Lab System</title>

<style>
body {
    font-family: Arial;
    background: #f5f7fa;
    margin: 0;
}

.header {
    background: #0f172a;
    color: white;
    text-align: center;
    padding: 15px;
    font-size: 22px;
}

.container {
    padding: 20px;
}

.cards {
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    width: 23%;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.actions {
    margin-top: 20px;
    text-align: center;
}

.actions a {
    background: #3b82f6;
    color: white;
    padding: 10px 15px;
    margin: 5px;
    border-radius: 8px;
    text-decoration: none;
    display: inline-block;
}

.table-box {
    background: white;
    margin-top: 20px;
    padding: 15px;
    border-radius: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: right;
}
</style>

</head>
<body>

<div class="header">🚀 Nova Lab System</div>

<div class="container">

<div class="cards">
<div class="card">👥<br>{{ patients_count }}<br>مرضى</div>
<div class="card">📄<br>{{ tests_count }}<br>طلبات</div>
<div class="card">💰<br>{{ total_money }}<br>دينار</div>
<div class="card">⚠️<br>0<br>متبقي</div>
</div>

<div class="actions">
<a href="/add_patient">➕ إضافة مريض</a>
<a href="/add_test">🧪 طلب فحص</a>
</div>

<div class="table-box">
<h3>آخر المرضى</h3>
<table>
<tr>
<th>الاسم</th>
<th>العمر</th>
<th>الجنس</th>
<th>الهاتف</th>
</tr>

{% for p in patients %}
<tr>
<td>{{ p.name }}</td>
<td>{{ p.age }}</td>
<td>{{ p.gender }}</td>
<td>{{ p.phone }}</td>
</tr>
{% endfor %}

</table>
</div>

<div class="table-box">
<h3>آخر الفحوصات</h3>
<table>
<tr>
<th>المريض</th>
<th>الفحص</th>
<th>السعر</th>
</tr>

{% for t in tests %}
<tr>
<td>{{ t.patient }}</td>
<td>{{ t.test }}</td>
<td>{{ t.price }}</td>
</tr>
{% endfor %}

</table>
</div>

</div>

</body>
</html>
"""

@app.route('/')
def home():
    total_money = sum(int(t["price"]) for t in tests) if tests else 0

    return render_template_string(html,
        patients=patients,
        tests=tests,
        patients_count=len(patients),
        tests_count=len(tests),
        total_money=total_money
    )

# =========================
# إضافة مريض
# =========================
@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        patients.append({
            "name": request.form["name"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "phone": request.form["phone"]
        })
        return redirect(url_for("home"))

    return render_template_string("""
    <h2 style="text-align:center;">إضافة مريض</h2>

    <form method="post" style="width:300px;margin:auto;">
        <input name="name" placeholder="اسم المريض" required><br><br>
        <input name="age" placeholder="العمر" required><br><br>

        <select name="gender">
            <option>ذكر</option>
            <option>أنثى</option>
        </select><br><br>

        <input name="phone" placeholder="الهاتف" required><br><br>

        <button type="submit">حفظ</button>
    </form>
    """)

# =========================
# طلب فحص
# =========================
@app.route("/add_test", methods=["GET", "POST"])
def add_test():
    if request.method == "POST":
        tests.append({
            "patient": request.form["patient"],
            "test": request.form["test"],
            "price": request.form["price"]
        })
        return redirect(url_for("home"))

    return render_template_string("""
    <h2 style="text-align:center;">طلب فحص</h2>

    <form method="post" style="width:300px;margin:auto;">
        <input name="patient" placeholder="اسم المريض" required><br><br>
        <input name="test" placeholder="نوع الفحص" required><br><br>
        <input name="price" placeholder="السعر" required><br><br>

        <button type="submit">حفظ</button>
    </form>
    """)

# =========================
# تشغيل السيرفر
# =========================
if __name__ == "__main__":
    app.run()
