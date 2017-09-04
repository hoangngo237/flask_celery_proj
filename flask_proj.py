from flask import Flask, render_template, request
import sqlite3 as sql
from celery import Celery


app = Flask(__name__, template_folder= "D:\\Working\\Projects\\flask\\flask_celery_proj")
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@celery.task
def students_add_task(nm, addr, city, pin):
    error = 0
    try:
        with sql.connect("D:\\Working\\Projects\\flask\\flask_celery_proj\\database.db") as con:
            cur = con.cursor()
        
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
        
            con.commit()
    except:
        error = 1
        con.rollback()
    finally:
        con.close()
    if error == 1:
        raise Exception("Some error when insert")
    

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            students_add_task.apply_async(args=[nm, addr, city, pin])
            msg = "Record successfully added"
        except:
            
            msg = "error in insert operation"
    
        finally:
            return render_template("result.html",msg = msg)
            
@app.route('/list')
def get_list():
    con = sql.connect("D:\\Working\\Projects\\flask\\flask_celery_proj\\database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall();
    return render_template("list.html",rows = rows)


if __name__ == '__main__':
    app.run(debug = True, threaded=True)