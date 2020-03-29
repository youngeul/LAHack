from flask import Flask, render_template, request, jsonify
import copy
import analyzer

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

STEP_WASH_SEC = 15 # required time(seconds) to wash for each step
TOTAL_WASH_TIME = 60 # total required time for waashing hands
STEP_PERCENT_ROUND = 2 # decimal points rounded up to
TIME_PER_STATUS = 0.01 # seconds, time per one element in status array
TIME_PER_FRAME = round(33.0 / 780, 2)
NUM_FRAME_TO_STATUS = int(TIME_PER_FRAME / TIME_PER_STATUS) # number of status array per one frame

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

    ## variables initialization 
    status = list()
    current = 0
    step_time = [0, 0, 0, 0, 0, 0]
    step_percent = [0, 0, 0, 0, 0, 0]
    total_time = 0
    total_percent = 0

    ## parse the predicted data from model and create json for frontend
    for i in range(len(predicted)):
        current = predicted[i]
        step_time[current] += 1
        step_percent[current] = round((step_time[current] / STEP_WASH_SEC) * 100, STEP_PERCENT_ROUND)
        total_time = i + 1
        total_percent = round((total_time / TOTAL_WASH_TIME) * 100)

        step = {
            "time" : copy.deepcopy(step_time),
            "percent" : copy.deepcopy(step_percent)
        }

        total = {
            "time" : total_time,
            "percent" : total_percent
        }

        for i in range(NUM_FRAME_TO_STATUS):
            status.append( {
                "current" : current,
                "steps" : step,
                "total" : total
            })

    result = jsonify({
        "time_per_status" : TIME_PER_STATUS, 
        "status" : status
    })
    print("num status: ", len(status))
    return result


if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
