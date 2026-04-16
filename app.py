from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

patients = []

home_html = """
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
    direction: rtl;
}
.header {
    background: #0f172a;
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 22px;
}
.container {
    padding: 20px;
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
    border-radius: 12px;
    flex: 1;
    min-width: 140px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    text-align: center;
}
.actions a {
    display: inline-block;
    text-decoration: none;
    background: #2563eb;
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    margin: 5px;
}
.table-box {
    background: white;
    margin-top: 20px;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
<div class="header">Nova Lab System 🚀</div>

<div class="container">
    <div class="cards">
        <div class="card">👥<br>{{ patients_count }}<br>مرضى</div>
        <div class="card">📄<br>{{ tests_count }}<br>طلبات</div>
        <div class="card">💰<br>0<br>دينار</div>
        <div class="card">⚠️<br>0<br>متبقي</div>
    </div>

    <div class="actions">
        <a href="/add_patient">➕ إضافة مريض</a>
        <a href="#">🧪 طلب فحص</a>
        <a href="#">📋 الطلبات</a>
        <a href="#">💰 الحسابات</a>
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
    font-family: Arial;
    background: #f5f7fa;
    margin: 0;
    direction: rtl;
}
.header {
    background: #0f172a;
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 22px;
}
.form-box {
    max-width: 500px;
    margin: 30px auto;
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
input, select {
    width: 100%;
    padding: 12px;
    margin: 8px 0 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-sizing: border-box;
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

        <button type="submit">حفظ</button>
        <a class="back-link" href="/">رجوع</a>
    </form>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        home_html,
        patients=patients,
        patients_count=len(patients)
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

if __name__ == "__main__":
    app.run()
