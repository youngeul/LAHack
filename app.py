from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS, cross_origin
import analyzer
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# app.config['JSON_SORT_KEYS'] = False
# app.config['UPLOAD_FOLDER'] = 'static/uploaded'
# app.config['ALLOWED_EXTENTIONS'] = {'mp4'}

def allowed_video(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.', 1)[1]
    if ext.upper() in app.config['ALLOWED_EXTENTIONS']:
        return True
    else:
        return False

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.files:
            video = request.files['video']

            if video.filename == '':
                print('Video must have a filename')
                return redirect(request.url)
            else:
                filename = secure_filename(video.filename)
                video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('Video saved')
        return redirect(request.url)
    # return render_template('main.html')
    return render_template('main.html')


@app.route("/m")
def mobile():
    return render_template('mobile.html')


@app.route('/analyze', methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def analyze():
    print('Start analyzing...')
    output = analyzer.run()
    print('Finish analyzing!')

    response = jsonify(output)

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    response.headers.add("Access-Control-Allow-Headers", '*');
    response.headers.add("Status", "200 OK")
    response.headers.add("Vary", "Accept")
    response.headers.add('Content-Type', 'application/octet-stream')

    return response


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
