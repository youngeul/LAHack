from flask import Flask, render_template, request, jsonify
import analyzer

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return 'hello'
    else:
        return render_template('main.html')


@app.route('/analyze', methods = ['POST'])
def analyze():
    print('Start analyzing...')
    output = analyzer.run()
    print('Finish analyzing!')

    return jsonify(output)


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
