from flask import Blueprint, request
from flask_cors import CORS
from pocket_service import subpocketService

subPocket = Blueprint("subPocket", __name__)
CORS(subPocket, resource=r"/*")
# CORS(subPocket, resource={r"/*": {"origins": "*"}})

@subPocket.route("/subPocket/index", methods=["GET", "POST"])
def subPocket_index():
    # 子口袋数据加载
    print("/subPocket/index", request.get_data(as_text=True))
    return subpocketService.subPocketIndex(eval(request.get_data(as_text=True)))


