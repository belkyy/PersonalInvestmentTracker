from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    investments = conn.execute("""
    SELECT * FROM investments
    WHERE user_id = ?
    """, (session["user_id"],)).fetchall()

    conn.close()

    prices = {
    "BTC": 80000,
    "ETH": 2300,
    "SOL": 110,
    "XRP": 1.4,
    "BNB": 1250
    }
    
    investment_list = []
    for inv in investments:

        current_price = prices[inv["coin"]]

        percentage = (
            (
                current_price - inv["buy_price"]
            )
            /
            inv["buy_price"]
        ) * 100

        profit_loss = (
            inv["amount"] * percentage /100
        ) 

        investment_list.append({
            "id": inv["id"],
            "coin": inv["coin"],
            "amount": inv["amount"],
            "buy_price": inv["buy_price"],
            "current_price": current_price,
            "profit_loss": round(profit_loss, 2),
            "percentage": round(percentage, 2)
     })

    return render_template(
        "dashboard.html",
        investments=investment_list
    )

@app.route("/delete/<int:id>")
def delete(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    conn.execute("""
    DELETE FROM investments
    WHERE id = ?
    AND user_id = ?
    """, (
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        user = cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["user_id"] = user["id"]   
            return redirect(url_for("dashboard"))
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        (username, password))
            conn.commit()
        except:
            return render_template(
            "register.html",
            error="This username already exists"
            )

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/create')
def getCreate():
    return render_template('create.html')

@app.route("/add", methods=["GET", "POST"])
def add():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        coin = request.form["coin"]

        valid_coins = [
            "BTC",
            "ETH",
            "SOL",
            "XRP",
            "BNB"
        ]

        if coin not in valid_coins:
            return "Invalid coin!"

        try:
            amount = float(request.form["amount"])
            buy_price = float(request.form["buy_price"])

        except:
            return "Invalid number!"

        conn = get_connection()

        conn.execute("""
        INSERT INTO investments
        (user_id, coin, amount, buy_price)
        VALUES (?, ?, ?, ?)
        """, (
            session["user_id"],
            coin,
            amount,
            buy_price
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add.html")

"Bu endpoint sadece debug amaçlıdır, gerçek uygulamada böyle bir endpoint bulunmamalıdır!"
"Unutmaaaaaaaaaaaaaaaaaaaaaaaa"

@app.route("/debug")
def debug():

    conn = get_connection()

    users = conn.execute(
        "SELECT * FROM users"
    ).fetchall()

    investments = conn.execute(
        "SELECT * FROM investments"
    ).fetchall()

    conn.close()

    return {
        "users": [dict(x) for x in users],
        "investments": [dict(x) for x in investments]
    }

def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS investments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    coin TEXT,
    amount REAL,
    buy_price REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

if __name__ == "__main__":
    app.run(debug=True)

