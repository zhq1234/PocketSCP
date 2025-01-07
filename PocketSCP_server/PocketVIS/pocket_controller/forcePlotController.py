from flask import Blueprint, request
from flask_cors import CORS
from pocket_service import forcePlotService

forcePlot = Blueprint("forcePlot", __name__)
CORS(forcePlot, resource=r"/*")
# CORS(forcePlot, resource={r"/*": {"origins": "*"}})

@forcePlot.route("/forcePlot/index", methods=["GET", "POST"])
def forcePlot_index():
    print('get inininin')
    # 力导向图初始化加载，只需加载位置即可
    print("/forcePlot/index  ", request.get_data(as_text=True))

    return forcePlotService.forcePlotIndex()

@forcePlot.route("/forcePlot/select_residue_pocket", methods=["GET", "POST"])
def forcePlot_select_residue_pocket():
    print('select_residue_pocekt')
    # 力导向图初始化加载，只需加载位置即可
    print("/forcePlot/select_residue_pocket", request.get_data(as_text=True))

    return forcePlotService.forcePlot_select_residue_pocket()

@forcePlot.route("/forcePlot/linkLine", methods=["GET", "POST"])
def forcePlotLinkLine():
    # 连线
    print("forcePlot/linkLine ", request.get_data(as_text=True))
    return forcePlotService.forcePlotLinkLine(eval(request.get_data(as_text=True)))


@forcePlot.route("/forcePlot/changeColor", methods=["GET", "POST"])
def forcePlotChangeColor():
    print("/forcePlot/changeColor ", request.get_data(as_text=True))
    return forcePlotService.forcePlotChangeColor(eval(request.get_data(as_text=True)))
