

from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__, template_folder='templates')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kkale'
app.config['MYSQL_DB'] = 'form'

db = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS REGISTER (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        FIRST_NAME VARCHAR(30),
        LAST_NAME VARCHAR(30),
        DATE_OF_BIRTH VARCHAR(10),
        EMAIL VARCHAR(30),
        PHONE_NUMBER INT(10),
        GENDER VARCHAR(10),
        ADDRESS VARCHAR(30),
        CITY VARCHAR(20),
        PINCODE INT,
        STATE VARCHAR(20),
        COUNTRY VARCHAR(20)
    )
""")


@app.route('/')
def index():
    return render_template('collegeregistration.html')

@app.route('/home1')
def home1():
    return render_template('home1.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        
        first_name = request.form['First_Name']
        last_name = request.form['Last_Name']
        date_of_birth = request.form['date']
        email = request.form['Email']
        mobile = request.form['Mobile']
        gender = request.form['Gender']
        address = request.form['Address']
        city = request.form['City']
        pin_code = request.form['Pin_Code']
        state = request.form['State']
        country = request.form['Country']

        
        cursor.execute("""
            INSERT INTO REGISTER (
                FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, EMAIL, PHONE_NUMBER,
                GENDER, ADDRESS, CITY, PINCODE, STATE, COUNTRY
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, date_of_birth, email, mobile, gender, address, city, pin_code, state, country))

        db.commit()

        return render_template('collegeregistration.html')#"Data added successfully"

    return "Invalid request"


@app.route('/delete_student', methods=['POST'])
def delete_student():
    id = request.form["student_id"]
    if request.method == 'POST':



       cursor.execute("DELETE FROM REGISTER WHERE ID=%s",(id,))
       db.commit()
       return redirect('/view')
    return render_template("home1.html")


@app.route('/search_student_by_name', methods=['POST'])
def search_student_by_name():
    if request.method == 'POST':
     
        student_name = request.form['update_id']
        if student_name == "all":
            cursor.execute("SELECT * FROM REGISTER")
            register = cursor.fetchall()
        
        else:
            cursor.execute("SELECT * FROM REGISTER WHERE FIRST_NAME LIKE %s", ('%' + student_name + '%',))
            register = cursor.fetchall()

        return render_template('home1.html', register=register)

    return "Invalid request"






def view_info():
    cursor.execute("SELECT * FROM REGISTER")
    register = cursor.fetchall()
    return register


@app.route('/view')
def view():
    register = view_info()
    print(register)
    return render_template('home1.html', register=register)

# @app.route('/view1')
# def view1():
#     register = view_info()
#     print(register)
#     return render_template('home1.html', register=register)


if __name__ == '__main__':
    app.run(debug=True)
