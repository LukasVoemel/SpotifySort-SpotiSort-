from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,  template_folder='../Frontend/templates')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login (authenticate user)
        # If successful, redirect to home page
        return redirect(url_for('home'))
    # Show login form
    return render_template('login.html')

@app.route('/login')
def home():
    # Home page after successful login
    # Display user's liked songs, or other relevant info
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
