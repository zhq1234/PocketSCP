from flask import Blueprint, request
from flask_cors import CORS
from pocket_service import chordPlotService

chordPlot = Blueprint("chordPlot", __name__)
CORS(chordPlot, resource=r"/*")



@chordPlot.route("/chordPlot/index", methods=["GET", "POST"])
def chordPlot_index():
    print("/chordPlot/index  ")
    return chordPlotService.chordPlotIndex(eval(request.get_data(as_text=True)))
