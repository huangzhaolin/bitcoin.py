from flask import Flask
from flask import render_template
from flask import request
import service
app = Flask(__name__)

parameters=request.form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/requestData',methods=['POST'])
def requestData():
    return service.trades(parameters.get("startTime",""),parameters.get("endTime",""),parameters.get("orignal",""))
if __name__ == '__main__':
    app.run()
