from flask import Flask,flash,redirect,render_template,url_for,request,jsonify,session,send_file
import mysql.connector
from io import BytesIO
mydb=mysql.connector.connect(host='localhost',user='root',password='anusha@1999',db='ors')

app=Flask(__name__)
app.secret_key='A@Bullela@_3'
app.config["SESSION_TYPE"] = "filesystem"
@app.route('/')
def home():
    return render_template('title.html')
@app.route('/signup')#user signup
def login():
    return render_template('signup.html')
@app.route('/adminlogin',methods=['GET','POST'])#admin login
def admin():
    if request.method=="POST":
        user=int(request.form['username'])
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT adminid from admin')
        users=cursor.fetchall()            
        password=request.form['password']
        cursor.execute('select password from admin where adminid=%s',[user])
        data=cursor.fetchone()
        cursor.close() 
        if (user,) in users:
            if password==data[0]:
                session['admin']=user
                return redirect(url_for('adminpanel',adminid=user))
            else:
                flash('Invalid Password')
                return render_template('adminlogin.html')
        else:
            flash('Invalid user id')
            return render_template('adminlogin.html')      
    return render_template('adminlogin.html')
@app.route('/userlogin',methods=['GET','POST'])#userlogin
def aspirentlogin():
    if session.get('aspirent'):
        return redirect(url_for('userhome',aspirent_id=session['user']))
    if request.method=="POST":
        user=int(request.form['username'])
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT aspirentid from aspirent')
        users=cursor.fetchall()
        password=request.form['password']
        cursor.execute('select password from aspirent where aspirentid=%s',[user])
        data=cursor.fetchone()[0]
        cursor.close()
        if (user,) in users:
            if password==data:
                session["user"] =user
                return redirect(url_for('userhome',aspirent_id=user))
            else:
                flash('Invalid Password')
                return render_template('login.html')
        else:
            flash('Invalid id')
            return render_template('login.html') 
    return render_template('login.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="POST":
        print(request.form)
        cursor=mydb.cursor(buffered=True)
        id1=request.form['Id']
        cursor.execute('SELECT aspirentid from aspirent')
        data=cursor.fetchall()
        cursor.close()
        if (int(id1),) in data:
            flash('user Id already exists')
            return render_template('signup.html')
        Name=request.form['Name']
        Age=request.form['Age']
        Experience=request.form['Experience']
        Company=request.form['Company']
        Email_id=request.form['Email id']
        Phone_no=request.form['Phone']
        Address=request.form['Address']
        Gender=request.form['Gender']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into aspirent values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[id1,Name,Age,Experience,Company,Email_id,Phone_no,Address,Gender,Password])
        mydb.commit()
        cursor.close()
        flash('Signup successful')
        return render_template('signup.html')
    return render_template('signup.html')
@app.route('/adminsignup',methods=['GET','POST'])#adminsignup
def adminsignup():
    if request.method=="POST":
        cursor=mydb.cursor(buffered=True)
        id1=request.form['Admin Id']
        cursor.execute('SELECT adminid from admin')
        data=cursor.fetchall()
        cursor.close()
        if (int(id1),) in data:
            flash('user Id already exists')
            return render_template('adminsignup.html')
        Name=request.form['Name']
        Gender=request.form['Gender']
        Email_id=request.form['Email Id']
        Password=request.form['Password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into admin values(%s,%s,%s,%s,%s)',[id1,Name,Gender,Email_id,Password])
        mydb.commit()
        cursor.close()
        flash('Signup successful')
        return render_template('adminsignup.html')
    return render_template('adminsignup.html')
@app.route('/userhome/<aspirent_id>')#usershome page
def userhome(aspirent_id):
    return render_template('userpanel.html')                
@app.route('/adminpanel/<adminid>')#admin panel
def adminpanel(adminid):
    if session.get('admin'):
        return render_template('adminpanel.html')
    return redirect(url_for('admin'))
@app.route('/addnotifications',methods=['GET','POST'])
def add():
    if session.get('admin'):
        if request.method=='POST':
            id1=request.form['Notifid']
            File=request.files['File']
            filename=File.filename
            Notifname=request.form['Notifname']
            From_date=request.form['From']
            To_date=request.form['To']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into notifications values(%s,%s,%s,%s,%s,%s,%s)',[id1,session.get('admin'),File.read(),Notifname,From_date,To_date,filename])
            mydb.commit()
            cursor.close()
            return redirect(url_for('adminpanel',adminid=session['admin']))
        return render_template('add.html')
    return redirect(url_for('admin'))
@app.route('/editnotification',methods=['GET','POST'])
def edit():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select notifid from notifications')
    data=cursor.fetchall()
    if session.get('admin'):
        if request.method=='POST':
            id1=request.form['choice']
            name=request.form['name']
            File=request.files['File']
            filename=File.filename
            From_date=request.form['From']
            To_date=request.form['To']
            cursor=mysql.connection.cursor()
            cursor.execute('update notifications set Fileupload=%s,notifname=%s,From_date=%s,To_date=%s,filename=%s where notifid=%s',[File.read(),name,From_date,To_date,filename,id1])
            mydb.commit()
            cursor.close()
            return redirect(url_for('adminpanel',adminid=session['admin']))
        return render_template('edit.html',data=data)
    return redirect(url_for('admin'))
@app.route('/allnotification')
def allnotifications():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT Notifid,notifname,from_date,to_date from notifications')
    notifications=cursor.fetchall()
    cursor.close()
    return render_template('allnotifications.html',notifications=notifications)
@app.route('/viewfileadmin/<id1>')
def view(id1):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT fileupload from notifications where notifid=%s',[id1])
    data=cursor.fetchone()[0]
    cursor.execute('select filename from notifications where notifid=%s',[id1])
    filename=cursor.fetchone()[0]
    #mention as_attachment=True to download the file--remove it to display the file
    return send_file(BytesIO(data),download_name=filename)
@app.route('/apply',methods=['GET','POST'])
def apply():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select notifid from notifications')
        data=cursor.fetchall()
        if request.method=='POST':
            user=session.get('user')
            notifid=request.form['choice']
            File=request.files['File']
            filename=File.filename
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert ignore into applicants (aspirentid,notifid,filename,fileupload) values(%s,%s,%s,%s)',[user,notifid,filename,File.read()])
            mydb.commit()
            cursor.close()
        return render_template('apply.html',data=data)
    return redirect(url_for('userlogin'))
@app.route('/view-delete')
def dview():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT Notifid,notifname,from_date,to_date from notifications')
    notifications=cursor.fetchall()
    cursor.close()
    return render_template('delete.html',notifications=notifications)
@app.route('/delete/<id1>')
def delete(id1):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('delete from notifications where Notifid=%s',[id1])
    mydb.commit()
    return redirect(url_for('dview'))
@app.route('/status')
def status():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT aspirentid,notifid,filename,applied_date,status from applicants')
    applicants=cursor.fetchall()
    return render_template('status.html',applicants=applicants)
@app.route('/viewfilestats/<id1>')
def view31(id1):
    print(type(id1))
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT fileupload from applicants where filename=%s',(id1,))
    data=cursor.fetchone()[0]
    return send_file(BytesIO(data),download_name=id1)
@app.route('/applicants')
def applicants():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT aspirentid,notifid,filename,applied_date,status from applicants')
    applicants=cursor.fetchall()
    return render_template('applicants.html',applicants=applicants)
@app.route('/update/<aspid>/<notid>',methods=['GET','POST'])
def update(aspid,notid):
    if request.method=='POST':
        print(request.form)
        update_status=request.form['updatestatus']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('UPDATE applicants set status=%s where aspirentid=%s and notifid=%s',[update_status,aspid,notid])
        mydb.commit()
        return redirect(url_for('applicants'))
    return render_template('update.html')        
app.run(debug='True')


