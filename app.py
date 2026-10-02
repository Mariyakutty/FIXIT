from flask import Flask,render_template
from auth import auth as auth_blueprint

app = Flask(__name__)

# Register the blueprint from auth.py
app.register_blueprint(auth_blueprint)

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)