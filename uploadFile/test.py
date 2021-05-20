import os 
import flask
from werkzeug import secure_filename

UPLOAD_FOLDER = 'tempfile'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg'])
if not os.path.exists(UPLOAD_FOLDER):
	dir = os.getcwd()
	print(dir)
	os.chdir(dir)
	os.mkdir(UPLOAD_FOLDER)
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/',methods=['POST','GET'])
def upload_file():
	if flask.request.method == "POST":
		file = flask.request.files['file']
		if  file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			return flask.redirect(flask.url_for('uploaded_file',filename=filename))
	return '''
	<!doctype html>
		<head>
		<title> upload new file </title>
		</head>
		<body>
		<h1> upload new file</h1>
		<form action=""  method="POST" enctype="multipart/form-data">
			<p><input type="file" name="file"/></p>
			<input type="submit" value="upload"/>
		</form>
		</body>
	'''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return flask.send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
	app.run(debug=True)
			