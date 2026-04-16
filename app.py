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
                <td>{{ p.name }}</td>
                <td>{{ p.age }}</td>
                <td>{{ p.gender }}</td>
                <td>{{ p.phone }}</td>
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
                <td>{{ t.patient }}</td>
                <td>{{ t.test }}</td>
                <td>{{ t.price }}</td>
                <td>{{ t.paid }}</td>
                <td>{{ t.due }}</td>
                <td>
                    {% if t.status == 'مدفوع' %}
                        <span class="badge-paid">{{ t.status }}</span>
                    {% elif t.status == 'جزئي' %}
                        <span class="badge-partial">{{ t.status }}</span>
                    {% else %}
                        <span class="badge-due">{{ t.status }}</span>
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
            <option value="{{ p.name }}">{{ p.name }}</option>
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
    total_paid = sum(int(t["paid"]) for t in tests) if tests else 0
    total_due = sum(int(t["due"]) for t in tests) if tests else 0

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
        patients.append({
            "name": request.form["name"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "phone": request.form["phone"]
        })
        return redirect(url_for("home"))

    return render_template_string(add_patient_html)

@app.route("/add_test", methods=["GET", "POST"])
def add_test():
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

        tests.append({
            "patient": request.form["patient"],
            "test": request.form["test"],
            "price": price,
            "paid": paid,
            "due": due,
            "status": status
        })
        return redirect(url_for("home"))

    return render_template_string(add_test_html, patients=patients)

if __name__ == "__main__":
    app.run()
