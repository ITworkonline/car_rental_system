"""learning flask material https://www.youtube.com/watch?v=RWviEK1Si68&list=PLDFBYdF-BxV1G4FBpG1EMyFtbsbZuJOvD
 https://www.youtube.com/watch?v=addnlzdSQs4"""
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from app import app, bcrypt, db, mysql
from app.forms import RegisterForm, LoginForm, ManagerForm, CarForm, EditForm
from app.models import User
"""
Design patterns and ooad items we used:  
           decorator: "@app.route", "@login_required"
           MVC: "Model: Mysql, sqlalchemy", 
                "view: customer, manager's page", 
                "controller: add, edit, and delete car(manager side), choose and confirm car(customer side)"
           ORM: "sqlalchemy as user info storage"

"""
"""In this route.py, we used @app.route as our decorator since it's flask web requirement.
In addition, we added a login as the decorator. To protect data security and administrative rights, 
we require users to log in and enter a password before entering any page. In this way, 
even if the user directly input the corresponding suburl in the url bar, 
also can not directly enter. """



#base page
#example of decorator
@app.route('/')
@login_required
def index():
    return render_template('index.html')

#introduction page
@app.route('/about')
def about():
    return render_template('about.html')

#register the user info
@app.route('/register', methods=['GET', 'POST'])
def register():
    #if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)#hash to project password
        user = User(username=username, email=email, password=password)
        #sqlalchemy
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registeration success! Book the car now!', category='success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

#login the username and password
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if the user is authenticated, direct to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        #check with the database
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

#logout methods
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#base customer page
@app.route('/customer')
@login_required
def customer():
    return render_template('customer.html')

#base manager page
@app.route('/manager', methods=['GET', 'POST'])
@login_required
def manager():
    form = ManagerForm()
    password = form.password.data
    #super user password
    if password != '12345':
        flash('password not match', category='danger')
    else:
        return redirect(url_for('admin'))
    return render_template('manager.html', form=form)

#manager sub page
@app.route('/admin',methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')

#manager dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM cars")
    info = cur.fetchall()
    #see if there is some car in database
    if result > 0:
        return render_template('dashboard.html', cars=info)
    else:
        msg = 'No car Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

#add car into database
@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    form = CarForm(request.form)
    if request.method == 'POST' and form.validate():
        car_type = form.car_type.data
        car_level = form.car_level.data
        price = form.price.data
        availability = 'yes'
        #add car with availability as 'yes'
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cars(car_type, car_level, price, availability) VALUES(%s, %s, %s, %s)",
                    (car_type, car_level, price, availability))
        mysql.connection.commit()
        cur.close()
        flash('Car added', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_car.html', form=form)


#edit car into database
@app.route('/edit_car/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_car(id):
    cur = mysql.connection.cursor()

    # Get car by id
    cur.execute("SELECT * FROM cars WHERE id = %s", [id])
    info = cur.fetchone()
    cur.close()
    form = EditForm(request.form)
    # get the data
    form.car_type.data = info['car_type']
    form.car_level.data = info['car_level']
    form.price.data = info['price']
    form.availability.data = info['availability']
    
    if request.method == 'POST' and form.validate():
        car_type = request.form['car_type']
        car_level = request.form['car_level']
        price = request.form['price']
        availability = request.form['availability']
        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE cars SET car_type=%s, car_level=%s,price=%s,availability=%s,modification_time=now() WHERE id=%s",
            (car_type, car_level, price, availability, id))
        mysql.connection.commit()
        cur.close()
        flash('Car Updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_car.html', form=form)


#delete car
@app.route('/delete_car/<string:id>', methods=['POST'])
@login_required
def delete_car(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cars WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Car Deleted', 'success')

    return redirect(url_for('dashboard'))


#choose car
@app.route('/customer/<string:car_type>', methods=['GET', 'POST'])
@login_required
def choose_car(car_type):
    availability = 'yes'
    cur = mysql.connection.cursor()
    #show the certain car if availability is 'yes'
    cur.execute("SELECT * FROM cars WHERE car_type = %s and availability = %s", (car_type, availability))
    info = cur.fetchall()
    return render_template('choose_car.html', cars=info)
    cur.close()

#booking car
@app.route('/customer/pay/<string:id>', methods=['GET', 'POST'])
@login_required
def book_car(id):
    cur = mysql.connection.cursor()
    #double check page(buffer page)
    cur.execute("SELECT * FROM cars WHERE id = %s", [id])
    info = cur.fetchall()

    return render_template('book_car.html', cars=info)
    cur.close()

#successful booking
@app.route('/successful/<string:id>', methods=['GET', 'POST'])
@login_required
def successful(id):
    cur = mysql.connection.cursor()
    availability = 'no'
    #after booking, update the certain car be NONE availability
    cur.execute("UPDATE cars SET availability=%s WHERE id=%s", (availability, id))
    cur.execute("SELECT * FROM cars WHERE id = %s", [id])
    info = cur.fetchall()
    mysql.connection.commit()
    return render_template('successful.html', cars=info)
    cur.close()

#show the statistic for every type car
@app.route('/statistic', methods=['GET', 'POST'])
@login_required
def statistic():
    return render_template('statistic.html')

#show the summary for all booked car
@app.route('/statistic/<string:car_type>', methods=['GET', 'POST'])
@login_required
def statistic_car(car_type):
    availability = 'no'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cars WHERE car_type = %s and availability = %s", (car_type, availability))
    info = cur.fetchall()
    count = 0
    for i in range(len(info)):
        count += info[i]['price']
    return render_template('statistic_car.html', cars=info, counts=count)
    cur.close()
