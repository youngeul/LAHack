from flask import Flask, render_template, request

import analyzer

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return 'hello'
    else:
        return render_template('main.html')


@app.route('/analyze', methods = ['POST'])
def analyze():
    print ('Start analyzing...')
    predicted = analyzer.run()

    print ('Finish analyzing!')
    print (predicted)
    print (len(predicted))

    return str(predicted)


if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
