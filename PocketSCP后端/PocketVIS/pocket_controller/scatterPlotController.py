from flask import Blueprint, request
from flask_cors import CORS
from util import message

scatterPlot = Blueprint("scatterPlot", __name__)
CORS(scatterPlot, resource=r"/*")

@scatterPlot.route("/scatterPlot/index", methods=["GET", "POST"])
def scatterPlot_index():
    print("/scatterPlot/index", request.get_data(as_text=True))
    # return "Demo"

    return message.success_message("success")
