from flask import Blueprint, request
from flask_cors import CORS
from pocket_service import parallelService

parallelPlot = Blueprint("parallelPlot", __name__)
CORS(parallelPlot, resource=r"/*")


@parallelPlot.route("/parallelPlot/index", methods=["POST"])
def parallelPlot_index():
    # 力导向图初始化加载，只需加载位置即可
    # print("/parallel/index  ", request.get_data(as_text=True))
    return parallelService.parallelPlotIndex(eval(request.get_data(as_text=True)))
