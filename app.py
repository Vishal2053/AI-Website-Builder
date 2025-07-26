from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
from utils.llama_codegen import generate_code

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ====================== SQLAlchemy Models =======================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(1000))
    language = db.Column(db.String(100))
    code = db.Column(db.Text)

# =================== Login Manager loader ======================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ========================= Routes ==============================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for('register'))
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if 'chat_history' not in session:
        session['chat_history'] = []
    if 'code_files' not in session:
        session['code_files'] = {'html': '', 'css': '', 'js': '', 'py': ''}

    chat_history = session['chat_history']
    code_files = session['code_files']
    code = ""

    if request.method == 'POST':
        if request.form.get('chat') == '1':
            user_msg = request.form['description']
            language = request.form['language']

            # Determine which file to update
            file_type = ''
            if language == "HTML/CSS/JS":
                file_type = 'html'
                pre_code = code_files['html']
            elif language.lower().startswith("python"):
                file_type = 'py'
                pre_code = code_files['py']
            else:
                file_type = 'html'
                pre_code = code_files['html']

            chat_history.append({'role': 'user', 'content': user_msg})

            # Generate code with previous code as context
            new_code = generate_code(user_msg, language, pre_code)
            code_files[file_type] = new_code

            # Save code to static/generated_files
            base_path = os.path.join(app.static_folder, "generated_files")
            os.makedirs(base_path, exist_ok=True)

            # Save HTML
            with open(os.path.join(base_path, "generated.html"), "w", encoding="utf-8") as f:
                f.write(code_files['html'])

            # Optionally save CSS and JS if available
            if code_files['css']:
                with open(os.path.join(base_path, "style.css"), "w", encoding="utf-8") as f:
                    f.write(code_files['css'])

            if code_files['js']:
                with open(os.path.join(base_path, "script.js"), "w", encoding="utf-8") as f:
                    f.write(code_files['js'])

            # Save Python file if generated
            if code_files['py']:
                with open(os.path.join(base_path, "script.py"), "w", encoding="utf-8") as f:
                    f.write(code_files['py'])

            chat_history.append({'role': 'assistant', 'content': new_code})
            session['chat_history'] = chat_history
            session['code_files'] = code_files

    # For dashboard preview, combine HTML, CSS, JS for iframe
    preview_html = code_files['html']
    if code_files['css']:
        preview_html = f'<style>{code_files["css"]}</style>\n' + preview_html
    if code_files['js']:
        preview_html += f'\n<script>{code_files["js"]}</script>'

    # Show last generated code in code view
    if chat_history and chat_history[-1]['role'] == 'assistant':
        code = chat_history[-1]['content']

    return render_template(
        'dashboard.html',
        chat_history=chat_history,
        code=code,
        preview_html=preview_html,
        code_files=code_files
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Automatically creates tables if not exist
    app.run(debug=True, use_reloader=False)
