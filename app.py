from flask import Flask, render_template, request, jsonify
import copy
import analyzer
import numpy as np

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

TOTAL_WASH_TIME = 24 # total required time for waashing hands
STEP_WASH_SEC =  4 # required time(seconds) to wash for each step TOTAL_WASH_TIME / 6
STEP_PERCENT_ROUND = 2 # decimal points rounded up to
TIME_PER_STATUS = 0.8 # seconds, time per one element in status array
TIME_PER_FRAME = 0.04 #round(33.0 / 780, 2)

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return 'hello'
    else:
        return render_template('main.html')

## fetch('/analyze', {method: "POST", body: "test"});
@app.route('/analyze', methods = ['POST'])
def analyze():
    print ('Start analyzing...')
    predicted = analyzer.run()
    predicted = np.array(predicted).tolist()

    print ('Finish analyzing!')
    print (predicted)
    print (len(predicted))

    output = createJson(predicted)
    result = jsonify(output)
    print(output)
    
    return result

def createJson(predicted):
    ## variables initialization 
    status = list() 
    current = 0
    step_time = [0, 0, 0, 0, 0, 0]
    step_percent = [0, 0, 0, 0, 0, 0]
    total_time = 0
    total_percent = 0

    ## parse the predicted data from model and create json for frontend
    len_predicted = len(predicted)
    for i in range(len_predicted):
        current = predicted[i]
        step_time[current] += TIME_PER_FRAME
        step_time[current] = round(step_time[current], 2)
        print("i: ", i, "step time: ", step_time[current])
        step_percent[current] = round((step_time[current] / STEP_WASH_SEC) * 100, STEP_PERCENT_ROUND)
        total_time = (i + 1) * TIME_PER_FRAME
        total_percent = round((total_time / TOTAL_WASH_TIME) * 100)

        ## save to json every 20 frames
        if i != 0 and (i % 19 == 0 or i == len_predicted -1) :
            print("save i: ", i)
            step = {
                "time" : copy.deepcopy(step_time),
                "percent" : copy.deepcopy(step_percent)
            }

            total = {
                "time" : total_time,
                "percent" : total_percent
            }

            status.append( {
                "current" : current,
                "steps" : step,
                "total" : total
            })
    output = {
        "time_per_status" : TIME_PER_STATUS, 
        "status" : status
    }
    return output

if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)
