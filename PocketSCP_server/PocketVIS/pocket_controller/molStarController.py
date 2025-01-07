from flask import Blueprint, request
from flask_cors import CORS
from pocket_service import molStarService


molStar = Blueprint("molStar", __name__)
CORS(molStar, resource=r"/*")



@molStar.route("/molStar/caculatecolor", methods=["GET"])
def molStart_changecolor():
    print("/molStar/caculatecolor", request.args.get("frame_pocket"))
    return molStarService.changecolor(request.args.get("frame_pocket"))
#
@molStar.route("/molStar/molStarInit", methods=["GET", "POST"])
def molStar_init():
    print("/molStar/molStarInit")
    print('00000', type(molStarService.molStar_Init(request.args.get("frame_pocket"))))
    return molStarService.molStar_Init(request.args.get("frame_pocket"))


# frame 数据
@molStar.route("/molStar/frame", methods=["GET", "POST"])
def molStar_frame():
    # 获取get请求参数
    print("/molStar/frame", request.get_data(as_text=True))
    return molStarService.molStar_frame(eval(request.get_data(as_text=True)))  # 返回默认参数


# 加载第一帧数据
@molStar.route("/molStar/framePocket", methods=["GET", "POST"])
def molStart_framePocket():
    print("/molStar/frameIndex", request.args.get("frame_pocket"))
    param = "0"
    if request.args.get("frame_pocket") is not None:
        param = request.args.get("frame_pocket")

    return molStarService.molStar_framePocket(param)


# 柱状图计算
@molStar.route("/molStar/frame_bar", methods=["GET", "POST"])
def molStart_bar():
    # print("/molStar/frame_bar", request.get_data(as_text=True))
    temp = molStarService.molStar_bar(eval(request.get_data(as_text=True)));
    temp['data']['barData'] = sorted(temp['data']['barData'],key=lambda d:d['i'])
    print(temp['data']['barData'])
    return temp


# 滑动块选择数据
@molStar.route("/molStar/slider", methods=["GET"])
def molStart_Slider():
    print("/molStar/slider", request.args.get("frame_pocket"))
    return molStarService.molStart_Slider(request.args.get("frame_pocket"))



# 加载第一帧的pocket
@molStar.route("/molStar/pocketIndex", methods=["GET", "POST"])
def molStart_pocketIndex():
    print("/molStar/pocketIndex", )
    if request.args.get("frame_pocket") is None:
        return molStarService.molStart_pocketIndex()
    else:
        return molStarService.molStart_pocket(request.args.get("frame_pocket"))
