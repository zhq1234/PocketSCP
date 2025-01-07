from flask import Blueprint, request
from flask_cors import CORS
from pocket_service import singleAxisService

singleAxis = Blueprint("singleAxis", __name__)
CORS(singleAxis, resource=r"/*")
# CORS(subPocket, resource={r"/*": {"origins": "*"}})

@singleAxis.route("/singleAxis/index", methods=["GET", "POST"])
def singleAxis_index():
    # 子口袋数据加载
    print("/singleAxis/index", request.get_data(as_text=True))
    return singleAxisService.singleAxisIndex(eval(request.get_data(as_text=True)))