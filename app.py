from init import *
from statistical_functions import StatisticalAnalyzer
import pandas as pd
from ydata_profiling import ProfileReport
# Import User model after initializing db
from models import User
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Check if the user table exists using inspect
with app.app_context():
    inspector = inspect(db.engine)
    if inspector.has_table('user'):
        print("Table exists!")
    else:
        print("Table does not exist.")
        db.create_all()


# Path to the SQLite database file
db_path = os.path.join(os.path.abspath('data'), 'users.db')  # Specify the path to your SQLite database file

# Check if the database file exists
if os.path.exists(db_path):
    print(f"Database {db_path} exists.")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path, timeout=20)
        cursor = conn.cursor()
        
        # Try fetching the list of tables to verify database is functional
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print("The following tables exist in the database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in the database.")
        
        # Close the connection
    
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")

    finally:
        conn.close()

else:
    print(f"Database {db_path} does not exist.")

# Routes

@app.route('/')
def index():
    """Home route."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        university = request.form.get('university')
        password = request.form.get('password')

        # Generate a unique username and hash the password
        username = f"{name.lower()}.{surname.lower()}"
        hashed_password = generate_password_hash(password)

        # Create a new User object
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            university=university,
            username=username,
            password=hashed_password,
            role='student' # Default role,
        )

        # Add the user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()

        
        if user and check_password_hash(user.password, password):
            login_user(user, True)
            db.session.commit()

            return redirect(url_for("dashboard"))
        else:
            return "Invalid email or password."
    
    return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
   
    return render_template("dashboard.html")


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect("login")
    
@app.route('/upload', methods=['POST','GET'])
@login_required
def upload_file():

    if request.method == "POST":
       
        file = request.files.get("file")
        
        # Save the file and generate the report
        if file and file.filename != "":
            data_path = os.path.join("uploads", file.filename)
            file.save(data_path)
            
            # Read the data and generate the profile report
            df = pd.read_csv(data_path)
            profile = ProfileReport(df)
            profile.to_file("templates/profile_report.html")
            
            return redirect(url_for("view_report"))
    # """File upload route."""
    # if 'file' not in request.files or request.files['file'].filename == '':
    #     return render_template('upload_file.html')

    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # file.save(filepath)

    # # Process file (this is just an example)
    # analyzer = StatisticalAnalyzer(filepath)
    # analyzer.describe_data()
    # analyzer.encode_categorical_data()
    # analyzer.save_cleaned_data(os.path.join('static/reports', 'report.csv'))

    return render_template('results.html', filepath=filepath)

@app.route('/download_pdf')
@login_required
def download_pdf():
    """Download PDF report route."""
    return send_file(os.path.join('static/reports', 'report.pdf'), as_attachment=True)

@app.route('/view/report')
@login_required
def view_report():
    
    return render_template('profile_report.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created before running
    app.run(debug=True)
