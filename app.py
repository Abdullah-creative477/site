from flask import Flask, render_template,request,redirect,session
from cs50 import SQL
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import secrets
print(secrets.token_hex(32))

app = Flask(__name__)
db = SQL("sqlite:///users.db")
app.secret_key = "generated_secure_key_here"

@app.route('/')
def home():
    user_id = session.get("user_id")
    if user_id:
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        return render_template('index.html', user=user[0])  # Pass user details
    return render_template('index.html')

@app.route('/explore')
def explore():
    return "Welcome to the Explore Page! More content coming soon."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        country = request.form['country']
        phone = request.form['phone']
        password = request.form['password']
        password = generate_password_hash(request.form['password'])

        # Insert user data into the database
        try:
            db.execute("INSERT INTO users (name, email, country, phone, password) VALUES (?, ?, ?, ?, ?)",
                       name, email, country, phone, password)
            return redirect('/login')  # Redirect to login after registration
        except:
            return "Error: Email already exists!"

    return render_template('register.html')
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Query database for user
        user = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(user) != 1 or not check_password_hash(user[0]["password"], password):
            return "Invalid email or password!"

        # Store user session
        session["user_id"] = user[0]["id"]

        return redirect("/")  # Redirect to a protected page after login

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()  # Remove user session
    return redirect('/')

@app.route('/paintings')
def painting():
    return render_template("paintings.html")

@app.route('/photography')
def photography():
    return render_template("photography.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/drawing')
def draw():
    return render_template("drawing.html")








if __name__ == '__main__':
    app.run( )

