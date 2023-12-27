from flask import Flask, g, redirect, request, url_for, render_template, session


class User():
    """docstring for ClassName"""

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "user, %s." % self.username


users = []
users.append(User(id=1, username="Aryagami", password="ARI$899"))
users.append(User(id=2, username="Prasanth", password="PR$899"))

app = Flask(__name__)
app.secret_key = 'D36926Eewt87813DEq12916926'


@app.before_request
def before_reqiest():
    g.user = None
    # print session
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']]
        g.user = user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        if username == "":
            return redirect(url_for('login'))
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/warehouse')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('warehouse.html')


@app.route('/tickets')
def tickets():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('tickets.html')


@app.route('/registration')
def registration():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('registration.html')


@app.route('/recharges')
def recharges():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('recharges.html')


@app.route('/voucher')
def voucher():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('vouchers.html')


@app.route('/voice')
def voice():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('voice.html')


@app.route('/data')
def data():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('data.html')


@app.route('/event')
def event():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('event.html')


@app.route('/recharge_cancel')
def recharge_cancel():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('recharge_cancel.html')


@app.route('/integration')
def integration():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('intigration_log_checker.html')


@app.route('/application')
def application():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('application.html')


@app.route('/document_issues')
def document_issues():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('document_issues.html')


@app.route('/debug_logs')
def debug_logs():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('debug.html')


@app.route('/ussd')
def ussd():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('ussd.html')


@app.route('/hlr')
def hlr():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('hlr.html')
