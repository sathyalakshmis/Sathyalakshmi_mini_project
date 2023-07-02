from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL connection
db = mysql.connector.connect(
    host='localhost',
    user='sathya',
    password='linux',
    database='medical'
)

# Create cursor
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Create cursor and execute login query
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(sql, values)

        # Check if user exists
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Store user in session
            session['username'] = user[0]
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid credentials")
    else:
        return render_template('login.html')
        
@app.before_request        
def require_login():
    allowed_routes = ['login','serve_css','serve_image','serve_background']  # List of routes that can be accessed without login
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/static/css/login.css')
def serve_css():
    return app.send_static_file('css/login.css')
    
@app.route('/static/images/login.jpg')
def serve_image():
    return app.send_static_file('images/login.jpg')

@app.route('/static/images/background.jpg')
def serve_background():
    return app.send_static_file('images/background.jpg')    

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect('/')

@app.route('/home')
def home():
    # Check if user is logged in
    if 'username' in session:
        return render_template('layout.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/view')
def view():
    # Execute a query
    cursor.execute("SELECT id,name FROM medicines")
    posts = cursor.fetchall()
    
    # Render template with the query results
    return render_template('view.html', posts=posts)
  
@app.route('/insert', methods=['GET', 'POST'])
def insert_data():
    inserted_id = None
    inserted_name = None
    if request.method == 'POST':
    	
        # Get data from the request form
        id = request.form['id']
        name = request.form['name']
        
        # Prepare the SQL query
        sql = "INSERT INTO medicines (id, name) VALUES (%s, %s)"
        values = (id, name)
        
        # Execute the query
        cursor.execute(sql, values)
        
        # Commit the changes
        db.commit()
        
        inserted_id = id
        inserted_name = name
    return render_template('insert.html', inserted_id=inserted_id, inserted_name=inserted_name)
    
@app.route('/delete', methods=['GET', 'POST'])
def delete_data():
    deleted_id = None
    if request.method == 'POST':
        # Get data from the request form
        name = request.form['name']
        
        # Prepare the SQL query
        sql = "DELETE FROM medicines WHERE name = %s"
        values = (name,)
        
        # Execute the query
        cursor.execute(sql, values)
        
        # Commit the changes
        db.commit()
        deleted_id = name
    return render_template('delete.html',deleted_id = deleted_id )

@app.route('/update', methods=['GET', 'POST'])
def update_data():
    updated_id = None
    updated_name = None
    if request.method == 'POST':
        # Get data from the request form
        id = request.form['id']
        name = request.form['name']
        
        # Prepare the SQL query
        sql = "UPDATE medicines SET name = %s WHERE id = %s"
        values = (name, id)
        
        # Execute the query
        cursor.execute(sql, values)
        
        # Commit the changes
        db.commit()
        
        updated_id = id
        updated_name = name
    return render_template('update.html',updated_id = updated_id, updated_name = updated_name)
    
@app.route('/search', methods=['GET', 'POST'])
def search_data():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        # Create cursor and execute search query
        cursor = db.cursor()
        sql = "SELECT * FROM medicines WHERE name LIKE %s"
        values = ("%" + name + "%",)
        cursor.execute(sql, values)

        # Fetch search results
        results = cursor.fetchall()

        # Close cursor
        cursor.close()

        # Render template with search results
        return render_template('search.html', results=results)
    else:
        return render_template('search.html')

@app.route('/message', methods=['GET', 'POST'])
def insert_message():
    msg_name=None
    if request.method == 'POST':
    	
        # Get data from the request form
        cust_name = request.form['cust_name']
        query = request.form['query']
        contact = request.form['contact']
        
        # Prepare the SQL query
        sql = "INSERT INTO message (cust_name, query, contact) VALUES (%s, %s, %s)"
        values = (cust_name, query, contact)
        
        # Execute the query
        cursor.execute(sql, values)
        
        # Commit the changes
        db.commit()
        
        msg_name = cust_name
    return render_template('message.html',msg_name=msg_name)
    
if __name__ == '__main__':
    app.run(debug=True)
