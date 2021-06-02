# Python app to manipulate a MySQL database through a HTML interface
# E5 - Bases de Datos 
# Last update: 02 june 2021
# Patricia Palula Aguilar

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'stayhome'
mysql = MySQL(app)

# Settings
app.secret_key = "mysecretkey"

# Routes
@app.route('/')
def Index():
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM video_copy')
    data3 = cur3.fetchall()
    cur3.close()
    return render_template('index.html', video_copies = data3)

# Rental Order Routes
@app.route('/rental_order')
def rental_order():
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM rental_order ORDER BY rentalNo DESC')
    data1 = cur1.fetchall()
    cur1.close()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM copy_rent ORDER BY rentalNo DESC')
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('rental_order.html', rental_orders = data1, copy_rents = data2)

@app.route('/add_rental_order', methods=['POST'])
def add_rental_order():
    if request.method == 'POST':
        memberNo = request.form['memberNo']
        dateRented = request.form['dateRented']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rental_order (memberNo, dateRented) VALUES (%s, %s)", (memberNo, dateRented))
        mysql.connection.commit()
        flash('Rental order added successfully')
        return redirect(url_for('rental_order'))

@app.route('/add_copy_rent', methods=['POST'])
def add_copy_rent():
    if request.method == 'POST':
        rentalNo = request.form['rentalNo']
        catalogNo = request.form['catalogNo']
        copyNo = request.form['copyNo']
        dateReturned = request.form['dateReturned']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO copy_rent (rentalNo, catalogNo, copyNo, dateReturned) VALUES (%s, %s, %s, %s)", (rentalNo, catalogNo, copyNo, dateReturned))
        mysql.connection.commit()
        flash('Copy rent added successfully')
        return redirect(url_for('rental_order'))

@app.route('/edit_copy_rent/rentalNo-<int:rentalNo>/catalogNo-<int:catalogNo>/copyNo-<int:copyNo>')
def get_copy_rent(rentalNo, catalogNo, copyNo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM copy_rent WHERE rentalNo = %s AND catalogNo = %s AND copyNo = %s', (rentalNo, catalogNo, copyNo))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_copy_rent.html', copy_rent = data[0])

@app.route('/update/rentalNo-<int:rentalNo>/catalogNo-<int:catalogNo>/copyNo-<int:copyNo>', methods = ['POST'])
def update_copy_rent(rentalNo, catalogNo, copyNo):
    if request.method == 'POST':
        dateReturned = request.form['dateReturned']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE copy_rent
            SET dateReturned = %s
            WHERE rentalNo = %s AND catalogNo = %s AND copyNo = %s
        """, (dateReturned, rentalNo, catalogNo, copyNo))
        print(dateReturned)
        print(rentalNo)
        print(catalogNo)
        print(copyNo)
        mysql.connection.commit()
        flash('Copy rent update succesfully')
        return redirect(url_for('rental_order'))

# Member Routes
@app.route('/member')
def member():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM member ORDER BY memberNo DESC')
    data = cur.fetchall()
    cur.close()
    return render_template('member.html', members = data)

@app.route('/add_member', methods=['POST'])
def add_member():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        branchNo = request.form['branchNo']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        regDate = request.form['regDate']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO member (firstName, lastName, branchNo, street, city, state, zipCode, regDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (firstName, lastName, branchNo, street, city, state, zipCode, regDate))
        mysql.connection.commit()
        flash('Member added successfully')
        return redirect(url_for('member'))

# Video Routes
@app.route('/video')
def video():
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM video ORDER BY catalogNo DESC')
    data1 = cur1.fetchall()
    cur1.close()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM video_copy ORDER BY catalogNo DESC')
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('video.html', videos = data1, video_copies = data2)

@app.route('/add_video', methods=['POST'])
def add_video():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        year = request.form['year']
        directorNo = request.form['directorNo']
        dailyRental = request.form['dailyRental']
        cost = request.form['cost']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO video (title, category, year, directorNo, dailyRental, cost) VALUES (%s, %s, %s, %s, %s, %s)", (title, category, year, directorNo, dailyRental, cost))
        mysql.connection.commit()
        flash('Video added successfully')
        return redirect(url_for('video'))

# Actor Routes
@app.route('/actor')
def actor():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM actor ORDER BY actorNo DESC')
    data = cur.fetchall()
    cur.close()
    return render_template('actor.html', actors = data)

@app.route('/add_actor', methods=['POST'])
def add_actor():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO actor (firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        flash('Actor added successfully')
        return redirect(url_for('actor'))

# Director Routes
@app.route('/director')
def director():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM director ORDER BY directorNo DESC')
    data = cur.fetchall()
    cur.close()
    return render_template('director.html', directors = data)

@app.route('/add_director', methods=['POST'])
def add_director():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO director (firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        flash('Director added successfully')
        return redirect(url_for('director'))

# Staff Routes
@app.route('/staff')
def staff():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM staff ORDER BY staffNo DESC')
    data = cur.fetchall()
    cur.close()
    return render_template('staff.html', staffs = data)

@app.route('/add_staff', methods=['POST'])
def add_staff():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        branchNo = request.form['branchNo']
        position = request.form['position']
        salary = request.form['salary']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO staff (firstName, lastName, branchNo, position, salary) VALUES (%s, %s, %s, %s, %s)", (firstName, lastName, branchNo, position, salary))
        mysql.connection.commit()
        flash('Staff added successfully')
        return redirect(url_for('staff'))

# Branch Routes
@app.route('/branch')
def branch():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM branch ORDER BY branchNo DESC')
    data = cur.fetchall()
    cur.close()
    return render_template('branch.html', branches = data)

@app.route('/add_branch', methods=['POST'])
def add_branch():
    if request.method == 'POST':
        staffNo = request.form['staffNo']
        phoneNum = request.form['phoneNum']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zipCode']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO branch (staffNo, phoneNum, street, city, state, zipCode) VALUES (%s, %s, %s, %s, %s, %s)", (staffNo, phoneNum, street, city, state, zipCode))
        mysql.connection.commit()
        flash('Branch added successfully')
        return redirect(url_for('branch'))

# starting the app
if __name__ == '__main__':
    app.run(port = 3000, debug = True)


# \(U.U)/