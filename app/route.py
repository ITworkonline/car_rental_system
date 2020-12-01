from flask import render_template, flash, redirect, url_for, request

from flask_login import login_user, login_required, current_user, logout_user
from app import app, bcrypt, db, mysql
from app.forms import RegisterForm, LoginForm, ManagerForm, CarForm
from app.models import User


@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registeration success! Book the car now!', category='success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # user exist and password matched
            login_user(user, remember=remember)
            flash('Login success', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('User not exists or password not match', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/customer')
def customer():
    return render_template('customer.html')


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    form = ManagerForm()
    password = form.password.data
    if password != '12345':
        flash('password not match', category='danger')
    else:
        return render_template('admin.html')
    return render_template('manager.html', form=form)


@app.route('/modify', methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM cars")
    info = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', cars=info)
    else:
        msg = 'No car Found'
        return render_template('dashboard.html', msg=msg)

    # Close connection
    cur.close()


# add car into database
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    form = CarForm(request.form)
    if request.method == 'POST' and form.validate():
        car_type = form.car_type.data
        car_level = form.car_level.data
        price = form.price.data

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cars(car_type, car_level, price) VALUES(%s, %s, %s)", (car_type, car_level, price))
        mysql.connection.commit()
        cur.close()
        flash('Car added', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_car.html', form=form)


# edit car into database
@app.route('/edit_car/<string:id>', methods=['GET', 'POST'])
def edit_car(id):
    cur = mysql.connection.cursor()

    # Get car by id
    result = cur.execute("SELECT * FROM cars WHERE id = %s", [id])
    info = cur.fetchone()
    cur.close()
    form = CarForm(request.form)
    # get the data
    form.car_type.data = info['car_type']
    form.car_level.data = info['car_level']
    form.price.data = info['price']
    form.availibity.data = info['availibity']
