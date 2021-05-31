import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

#Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'stayhome'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

#routes
@app.route('/')
def Index():
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM rental_order')
    data1 = cur1.fetchall()
    cur1.close()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM can_rent ORDER BY rentalNo')
    data2 = cur2.fetchall()
    cur2.close()
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM video_copy')
    data3 = cur3.fetchall()
    cur3.close()
    return render_template('index.html', rental_orders = data1, can_rents = data2, video_copies = data3)

@app.route('/add_rental_order', methods=['POST'])
def add_rental_order():
    if request.method == 'POST':
        memberNo = request.form['memberNo']
        dateRented = request.form['dateRented']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rental_order (memberNo, dateRented) VALUES (%s,%s)", (memberNo, dateRented))
        mysql.connection.commit()
        flash('Rental order added successfully')
        return redirect(url_for('Index'))

@app.route('/add_can_rent', methods=['POST'])
def add_can_rent():
    if request.method == 'POST':
        rentalNo = request.form['rentalNo']
        catalogNo = request.form['catalogNo']
        copyNo = request.form['copyNo']
        dateReturned = request.form['dateReturned']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO can_rent (rentalNo, catalogNo, copyNo, dateReturned) VALUES (%s, %s, %s, %s)", (rentalNo, catalogNo, copyNo, dateReturned))
        mysql.connection.commit()
        flash('Copy rent added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/rentalNo-<int:rentalNo>/catalogNo-<int:catalogNo>/copyNo-<int:copyNo>')
def get_can_rent(rentalNo, catalogNo, copyNo):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM can_rent WHERE rentalNo = %s AND catalogNo = %s AND copyNo = %s', (rentalNo, catalogNo, copyNo))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_can_rent.html', can_rent = data[0])

@app.route('/update/rentalNo-<int:rentalNo>/catalogNo-<int:catalogNo>/copyNo-<int:copyNo>', methods = ['POST'])
def update_can_rent(rentalNo, catalogNo, copyNo):
    if request.method == 'POST':
        dateReturned = request.form['dateReturned']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE can_rent
            SET dateReturned = %s
            WHERE rentalNo = %s AND catalogNo = %s AND copyNo = %s
        """, (dateReturned, rentalNo, catalogNo, copyNo))
        print(dateReturned)
        print(rentalNo)
        print(catalogNo)
        print(copyNo)
        mysql.connection.commit()
        flash('Can rent update succesfully')
        return redirect(url_for('Index'))

# starting the app
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
