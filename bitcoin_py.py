from flask import Flask
from flask import render_template
from flask import request
import json
import service
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/queryData.htm',methods=['POST'])
def requestData():
    parameters=request.form
    print parameters
    print request.args
    return json.dumps(service.trades(parameters.get("startTime",""),parameters.get("endTime",""),parameters.get("orignal","")),indent=6)
if __name__ == '__main__':
    app.run()
