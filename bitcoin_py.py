from flask import Flask
from flask import render_template
from flask import request
import service
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/queryData.htm',methods=['POST'])
def requestData():
    parameters=request.form
    return service.trades(parameters.get("startTime",""),parameters.get("endTime",""),parameters.get("orignal",""))
if __name__ == '__main__':
    app.run()
