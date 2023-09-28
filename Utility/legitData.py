from flask import Blueprint
from flask import request
import json
from common_classes import JsonData as js
from common_classes import MyCustomException as ex
from sqlQuery import SqlUtility as sql

legit = Blueprint("legi",__name__)

@legit.route("/get_legit_data",methods = ['POST'])
def get_legit_data():
    if request.method == "POST":
        input_data = json.loads(request.get_data())
        if "state_id" not in input_data:
            raise ex("state id not available")
        state_id = input_data["state_id"]
        fetch_query = "select legit_name as legit,legit_id as id from legit where state_id = 2;"
        result_query = sql.select_query(fetch_query,state_id)
        if result_query is None:
            return ("legit not id availabe")
        else:
            legitDict = []
            for items in result_query:
                singleLegit = {}
                singleLegit["legit"] = items[0]
                singleLegit["id"] = items[1]
                legitDict.append(singleLegit)
            print(legitDict)
            return ("legit id availabe")

    else:
        return json.dumps(js.method_error_message)
