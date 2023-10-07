from flask import Flask
 
app = Flask(__name__)
 login_manager = LoginManager(app)

@app.route('/')
def index():
	return '<h1>Mashimo</h1>'
 
if __name__ == '__main__':
	app.run(debug=True)