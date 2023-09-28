from flask import Flask,request,jsonify
from legitData import legit
app = Flask(__name__)
app.register_blueprint(legit)
@app.route('/')
def hello_world():
    return "Methods for Neta.."

@app.route('/submit_sample',methods=["POST"])
def submit_sample():
    input_json = request.get_json(force=True)
    dictToReturn = {'text':input_json['text']}
    return jsonify(dictToReturn)

if __name__ == "__main__":
    # app.run(host="0.0.0.0",port=8080)
    app.run(host='0.0.0.0', port=4455, debug=True)