from flask import *
import random
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'localhost'  # Replace with your MySQL host
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'full_stack'  # Replace with your MySQL database name

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if result is None:
            error = 'Username not registered'
        else:
            password = request.form['Password']
            if password == result[0]:

               

                query = "SELECT questionid,question FROM Questions where answer='Not Answered'"
                cur.execute(query)

                results = cur.fetchall()

                cur.close()

                return render_template('Home.html', values=results, username=username)

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if result is not None:
            return render_template('Newacc.html')

        password = request.form['Password']
        phone = request.form['Phone']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, phone) VALUES (%s, %s, %s)", (username, password, phone))
        mysql.connection.commit()
        cur.close()
        return render_template('login.html')
    
@app.route('/Home')
def Home():
    cur = mysql.connection.cursor()
    
    query = "SELECT questionid,question FROM Questions where answer='Not Answered'"
    cur.execute(query)

    results = cur.fetchall()

    cur.close()
    
    return render_template('Home.html',values=results)

    
@app.route('/answer', methods=['GET','POST'])
def answers():
    if request.method == 'POST':
        answer=request.form['answer']
        id=request.form['id']

        cur = mysql.connection.cursor()
        
        if not answer.isspace() and len(answer)!=0:
            cur.execute("UPDATE questions SET answer = %s WHERE questionid = %s", (answer, id))
            mysql.connection.commit()

        query = "SELECT questionid,question FROM Questions where answer='Not Answered'"
        cur.execute(query)

        results = cur.fetchall()

        cur.close()

        return render_template('Home.html',values=results)
    
    cur=mysql.connection.cursor()
    
    query = "SELECT questionid,question FROM Questions where answer='Not Answered'"
    cur.execute(query)

    results = cur.fetchall()

    cur.close()

    return render_template('Home.html',values=results)

@app.route('/qlist', methods=['GET','POST'])
def qlist():
    if request.method=='POST':
        username = request.form['username']
        cur = mysql.connection.cursor()
        cur.execute("select questionid,question from questions where username=%s",(username,))
        res = cur.fetchall()
        print(res)
    return render_template('MyQuestions.html', values = res, username = username)
    
@app.route('/qinsert', methods=['GET' , 'POST'])
def qinsert():
    username = request.args.get('value')
    if request.method == 'POST':
        question = request.form['question']
        username = request.form['username']
        cur = mysql.connection.cursor()
        if (not question.isspace() and len(question)!=0):
            cur.execute('insert into questions(question,username) values(%s,%s)',(question,username))
            mysql.connection.commit()
        else:
            return render_template("Questions.html",error="Questions cannot contain only spaces!!")

        query = "SELECT questionid,question FROM Questions where answer='Not Answered'"
        cur.execute(query)

        results = cur.fetchall()

        cur.close()

        return render_template('Home.html', values=results)
    
    cur = mysql.connection.cursor()
    
    query = "SELECT questionid,question FROM Questions where answer='Not Answered'"
    cur.execute(query)

    results = cur.fetchall()

    cur.close()
    
    return render_template('Home.html',values=results)




@app.route('/Newacc.html')
def newacc():
    return render_template('Newacc.html')

@app.route('/Home.html')
def home():
    return render_template('Home.html')


@app.route('/MyQuestions.html')
def MyQuestions():
    return render_template('MyQuestions.html')

@app.route('/answer.html')
def answer():
    value = request.args.get('value')
    cur=mysql.connection.cursor()
    cur.execute('select questionid,question from questions where questionid=%s',(value))
    res=cur.fetchone()

    return render_template('answer.html', value=res)

@app.route('/answerdisp.html')
def answerdisp():
    value = request.args.get('res')
    cur=mysql.connection.cursor()
    cur.execute('select questionid,question,answer from questions where questionid=%s',(value))
    res=cur.fetchone()

    return render_template('answerdisp.html', value=res)

@app.route('/Questions.html')
def Questions():
    return render_template('Questions.html')

@app.route('/Profile.html')
def Profile():
    return render_template('Profile.html')




if __name__ == '__main__':
    app.run(debug=True, port=5050)
