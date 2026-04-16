from flask import Flask, render_template_string

app = Flask(__name__)

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
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    flex: 1;
    min-width: 120px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    text-align: center;
}

.buttons {
    margin-top: 20px;
}

button {
    padding: 12px 20px;
    margin: 5px;
    border: none;
    border-radius: 10px;
    background: #2563eb;
    color: white;
    font-size: 14px;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}
</style>
</head>

<body>

<div class="header">
    Nova Lab System 🚀
</div>

<div class="container">

<div class="cards">
    <div class="card">👥<br>0 مرضى</div>
    <div class="card">🧾<br>0 طلبات</div>
    <div class="card">💰<br>0 ريال</div>
    <div class="card">⚠️<br>0 متبقي</div>
</div>

<div class="buttons">
    <button>➕ إضافة مريض</button>
    <button>🧪 طلب فحص</button>
    <button>📋 الطلبات</button>
    <button>💰 الحسابات</button>
</div>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

if __name__ == "__main__":
    app.run()
