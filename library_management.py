from flask import *
from flask_login import current_user, login_required
from flask_login import logout_user


app = Flask(__name__)




class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.access = ["maintenance", "reports", "transactions"]

class Membership:
    def __init__(self, membership_number, duration="6 months"):
        self.membership_number = membership_number
        self.duration = duration

class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.memberships = {}

    def register_user(self, username, password, is_admin=False):
        if username in self.users:
            return False
        if is_admin:
            self.users[username] = Admin(username, password)
        else:
            self.users[username] = User(username, password)
        return True

    def login(self, username, password):
        if username not in self.users:
            return False
        if self.users[username].password != password:
            return False
        return True

    def add_membership(self, membership_number, duration="6 months"):
        if membership_number in self.memberships:
            return False
        self.memberships[membership_number] = Membership(membership_number, duration)
        return True

    def update_membership(self, membership_number, new_duration="6 months"):
        if membership_number not in self.memberships:
            return False
        self.memberships[membership_number].duration = new_duration
        return True

    def extend_membership(self, membership_number, extension="6 months"):
        if membership_number not in self.memberships:
            return False
        # Extend membership
        # Code to extend membership for the given duration
        return True

    def cancel_membership(self, membership_number):
        if membership_number not in self.memberships:
            return False
        del self.memberships[membership_number]
        return True

library_system = LibrarySystem()

@app.route('/')
def index():
    return render_template('lib_index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'on'
        if library_system.register_user(username, password, is_admin):
            return redirect(url_for('login'))
    return render_template('lib_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if library_system.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('lib_login.html')

@app.route('/dashboard')
def dashboard():
    # Render dashboard template based on user type (admin or user)
    return render_template('lib_dashboard.html',current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
