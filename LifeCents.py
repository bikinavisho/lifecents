import flask
import dataBaser
import base64, os, bcrypt, re

from init import db, app, socket_io
from api import check_request


@app.before_request
def setup_user():
    """
    Figure out if we have an authorized user, and look them up.
    This runs for every request, so we don't have to duplicate code.
    """
    if 'auth_user' in flask.session:
        user = dataBaser.User.query.get(flask.session['auth_user'])
        if user is None:
            # old bad cookie, no good
            del flask.session['auth_user']
        # save the user in `flask.g`, which is a set of globals for this request
        flask.g.user = user


@app.before_request
def setup_csrf():
    # make a cross-site request forgery preventing token
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


# This signifies that when you navigate to the URL / on our homepage (lcents.com/) it will run this function
@app.route('/')
def render_homepage():
    # This signifies that at the end of the function it will render the index.html template.
    # We can add additional arguments to it if we want to pass data
        # Ex: flask.render_template('index.html', var1, var2)
        #       and in the html file you would put {{ var1 }} to print its value
    return flask.render_template('index.html')


@app.route('/budget')
def render_budget_page():
    if 'auth_user' in flask.session:
        # Get user data (if any)
        budgets = dataBaser.Budget.query.filter_by(user_id=flask.g.user.id).all()
        # Separate them into income category and expense category
        incomes = []
        expenses = []
        for budget in budgets:
            if budget.type:
                expenses.append(budget)
            else:
                incomes.append(budget)

        return flask.render_template('budget.html', incomes=incomes, expenses=expenses)
    else:
        return flask.redirect(flask.url_for('login_page2', error='You must log in first!'), code=303)


@app.route('/budget/edit')
def edit_budget_form():
    if 'auth_user' in flask.session:
        # Get User Data (if any)
        budgets = dataBaser.Budget.query.filter_by(user_id=flask.g.user.id).all()
        # Separate them into income category and expense category
        incomes = []
        expenses = []
        for budget in budgets:
            if budget.type:
                expenses.append(budget)
            else:
                incomes.append(budget)
        return flask.render_template('edit_budget.html', incomes=incomes, expenses=expenses)
    else:
        return flask.redirect(flask.url_for('login_page2', error='You must log in first!'), code=303)


@app.route('/budget/edit', methods=['POST'])
def submit_edit_budget():
    if 'auth_user' in flask.session:
        check_request()
        user = flask.g.user
        # Iterate through incomes
        income_total = flask.request.form['income-count']
        i = 1
        while i <= int(income_total):
            inc_name = flask.request.form['income'+str(i)]
            i_v = flask.request.form['income-value'+str(i)]
            # is there data in there?
            if inc_name is not "" and i_v is not "":
                inc_value = 0.0 + float(i_v)
                new_income = dataBaser.Budget()
                new_income.name = inc_name
                new_income.value = inc_value
                new_income.type = False
                new_income.user_id = user.id
                user.budgetData.append(new_income)

                db.session.add(new_income)

            i += 1
        # Iterate through expenses
        expense_total = flask.request.form['expense-count']
        i = 1
        while i <= int(expense_total):
            exp_name = flask.request.form['expense'+str(i)]
            e_v = flask.request.form['expense-value'+str(i)]

            if exp_name is not "" and e_v is not "":
                exp_value = 0.0 + float(e_v)
                new_expense = dataBaser.Budget()
                new_expense.name = exp_name
                new_expense.value = exp_value
                new_expense.type = True
                new_expense.user_id = user.id
                user.budgetData.append(new_expense)

                db.session.add(new_expense)

            i += 1

        # save database changes
        db.session.commit()

    # Test to make sure everything is saving to database
    # budgets = dataBaser.Budget.query.all()
    # print(budgets)

    # TODO redirect to budget page (doesn't exist yet)
    return flask.redirect(flask.url_for('render_homepage'))


# ================================
#           LOGIN LOGIC
# ================================
@app.route('/login')
def login_page():
    return flask.render_template('login.html')


@app.route('/login/?<error>')
def login_page2(error):
    return flask.render_template('login.html', error_msg=error)


@app.route('/register')
def register_page():
    return flask.render_template('register.html')


@app.route('/login', methods=['POST'])
def handle_login():
    # POST request to /login - check user
    name = flask.request.form['username']
    password = flask.request.form['password']
    # try to find user
    user = dataBaser.User.query.filter_by(name=name).first()

    if user is not None:
        # hash the password the user gave us
        # for verifying, we use their real hash as the salt
        pw_hash = bcrypt.hashpw(password.encode('utf8'), user.pw_hash)
        # is it good?
        if pw_hash == user.pw_hash:
            # yay!
            flask.session['auth_user'] = user.id
            # And redirect to '/', since this is a successful POST
            return flask.redirect(flask.url_for('render_homepage'), code=303)

    # if we got this far, either username or password is no good
    # For an error in POST, we'll just re-show the form with an error message
    return flask.render_template('login.html', error_msg="Invalid username or password")


@app.route('/create_user', methods=['POST'])
def create_user():
    name = flask.request.form['username']
    password = flask.request.form['password']

    # do the passwords match?
    error = None
    if password != flask.request.form['confirm_password']:
        error = "Passwords don't match"
    # is the login ok?
    if len(name) > 60:
        error = "Username too long"
    if not re.match(r"^[A-Za-z0-9\.\+_-]*$", name):
        error = "Username contains invalid characters"

    # search for existing user
    existing = dataBaser.User.query.filter_by(name=name).first()

    if existing is not None:
        # oops, found your doppelganger
        error = "Username already taken"

    if error:
        return flask.render_template('register.html', error_msg=error)

    # create user
    user = dataBaser.User()
    user.name = name
    # hash password
    user.pw_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(15))

    # save user
    db.session.add(user)
    db.session.commit()

    flask.session['auth_user'] = user.id

    # It's all good!
    return flask.redirect(flask.url_for('render_homepage'), 303)


@app.route('/logout')
def handle_logout():
    # user wants to say goodbye, just forget about them
    del flask.session['auth_user']
    del flask.g.user
    # redirect to specified source URL, or / if none is present
    return flask.redirect(flask.url_for('render_homepage'), code=303)


# ================================
#         END LOGIN LOGIC
# ================================


# This runs the application which is our website
if __name__ == '__main__':
    # app.run()
    socket_io.run(app)
