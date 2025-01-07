from util import message
from util import mongodbUtil

dbname = mongodbUtil.DBNAME
dbname_pocket = mongodbUtil.DBNAME_POCKET


# 进行初始化
def molStar_Init(param):
    data = ""
    # 查询初始化帧
    data += molStar_frameIndex(param)
    # 查询第一帧的口袋
    data += molStar_pocketIndex(param)
    return data


# 查询指定的口袋
def molStar_framePocket(param):
    data = ""
    print('param'+param)
    con = mongodbUtil.mongo_conn()
    for d in con[dbname][dbname_pocket].find({"frame_pocket": param}, {"_id": 0, "frameInfo": 1, "pocketInfo": 1,"x": 1,"y": 1}):
        data += d["frameInfo"]
        data += d["pocketInfo"]
    con.close()
    print(data)
    return data


# 返回帧数据
def molStar_frame(params):
    frames = params["frame_pocket"]
    con = mongodbUtil.mongo_conn()
    frame_pocket = {}  # 某帧某个口袋
    for data in con[dbname][dbname_pocket].find({"frame_pocket": {"$in": frames}}, {"_id": 0, "frame_pocket": 1, "frameInfo": 1, "pocketInfo": 1}):
        frame_pocket[data["frame_pocket"]] = {"frameInfo": data["frameInfo"], "pocketInfo": data["pocketInfo"], "frame_pocket": data["frame_pocket"]}
    con.close()
    min_num = min([int((x.split("_"))[0]) for x in frames])
    max_num = max([int((x.split("_"))[0]) for x in frames])

    # 查询请求参数
    return message.success_message({"frameData": frame_pocket, "numRange": {"max": max_num, "min": min_num}})


# 第一帧的frame数据
def molStar_frameIndex(param):
    con = mongodbUtil.mongo_conn()
    data = ""
    for d in con[dbname][dbname_pocket].find({"frame_pocket": param}, {"_id": 0, "frameInfo": 1}).limit(1):
        data = d["frameInfo"]
    con.close()
    return data


# 获取第一帧的pocket
def molStar_pocketIndex(param):
    con = mongodbUtil.mongo_conn()
    data = ""
    frameID = ""
    for d in con[dbname][dbname_pocket].find({"frame_pocket": param}, {"_id": 0, "frameID": 1}):
        frameID = d["frameID"]
    for d in con[dbname][dbname_pocket].find({"frameID": frameID}, {"pocketInfo": 1, "_id": 0}):
        data += d["pocketInfo"]
    con.close()
    # print('===============================')
    # print(data)
    return data


# 获取指定帧的口袋
def molStart_pocket(param):
    con = mongodbUtil.mongo_conn()
    data = ""
    for d in con[dbname][dbname_pocket].find({"frame_pocket": param}, {"_id": 0, "pocketInfo": 1}):
        data = d["pocketInfo"]
    con.close()
    return data
def molStar_bar(param):
    try:
        print('this is molStar_bar')
        print(param)
        clusterBar = len(param["frame_pocket"])  # 表示一共多少簇
        print('1111')
        print(clusterBar);
        param["frame_pocket"][0].pop()
        if(clusterBar>1):
            param["frame_pocket"][1].pop()
        print((param["frame_pocket"]));
        # param["frame_pocket"]是[['30_7', '31_14', '55_9', '46_14', '15_13', '52_20', '47_13', '6_2', '40_18', '55_5']]
        data = sorted(list(set([int(x.split("_")[0]) for i in param["frame_pocket"] for x in i])))  # 帧范围
        print(data)
        conn = mongodbUtil.mongo_conn()
        barData = []
        maxVolume = -1
        minVolume = 0xFFFFFFFF
        maxDis = -1
        minDis = 0xFFFFFFFF
        maxHydropscore = -0x7fffffff  # 最大疏水性
        minHydropscore = 0x7fffffff  # 最小疏水性
        frame_framePocket_dict = {}  # 帧和口袋编号映射
        for index in range(len(param["frame_pocket"])):
            for d in param["frame_pocket"][index]:
                temp = conn[dbname][dbname_pocket].find_one({"frame_pocket": d}, {
                    "_id": 0,
                    "pocketID": 0,
                    "raw": 0,
                    "processed": 0,
                    "spheres": 0,
                    "residueID": 0,
                    "flexibility": 0,
                    "x": 0,
                    "y": 0,
                    "name": 0,
                    "frameInfo": 0,
                    "pocketInfo": 0
                })
                # print('=======')
                # print(temp)
                # print(d)
                if d.split("_")[0] not in frame_framePocket_dict:
                    frame_framePocket_dict[d.split("_")[0]] = []
                frame_framePocket_dict[d.split("_")[0]].append(d)
                maxVolume = max(maxVolume, temp["volume"])
                minVolume = min(minVolume, temp["volume"])
                maxDis = max(maxDis, temp["alphaspmaxdist"])
                minDis= min(minDis, temp["alphaspmaxdist"])
                barData.append({
                    "frame_pocket": temp["frame_pocket"],
                    "volume": temp["volume"],  # 体积
                    "hydropscore": temp["hydropscore"],
                    "totalsasa": temp["totalsasa"],
                    "polarsasa": temp["polarsasa"],
                    "apolarsasa": temp["apolarsasa"],
                    "mlohyden": temp["mlohyden"],
                    "malspra": temp["malspra"],
                    "msoacc": temp["msoacc"],
                    "alalsppro": temp["alalsppro"],
                    "volumescore": temp["volumescore"],
                    "propolatoms": temp["propolatoms"],
                    "alspdensity": temp["alspdensity"],
                    "alphaspmaxdist": temp["alphaspmaxdist"], # 质心和阿尔法球的最大距离
                    "alphanum": temp["alphanum"],
                    "polarityscore": temp["polarityscore"],
                    "i": int(str(temp["frame_pocket"]).split("_")[0]) - int(data[0]),
                    "j": index})
        # print({"frameExtent": [int(data[0]), int(data[-1])], "clusterBar": clusterBar, "barData": barData, "maxVolume": maxVolume + 50, "minVolume": minVolume, "frameMap": frame_framePocket_dict})
        conn.close()
        return message.success_message({"frameExtent": [int(data[0]), int(data[-1])], "clusterBar": clusterBar, "barData": barData, "maxVolume": maxVolume + 50, "minVolume": minVolume, "maxDis": maxDis+ 50, "minDis": minDis, "frameMap": frame_framePocket_dict})
    except:
        print('error find....')
        print(temp,d)

def molStart_Slider(param):
    frame, frame_pocket = param.split(",")
    framePocketData = ""
    conn = mongodbUtil.mongo_conn()
    framePocketData = conn[dbname][dbname_pocket].find_one({"frameID": int(frame)}, {"_id": 0, "frameInfo": 1})["frameInfo"]
    for d in conn[dbname][dbname_pocket].find({"frame_pocket": {"$in": str(frame_pocket).split("-")}}, {"_id": 0, "pocketInfo": 1}):
        framePocketData += d["pocketInfo"]
    # print(framePocketData)
    return framePocketData

def changecolor(param):
    frame, frame_pocket = param.split(",")
    framePocketData = ""
    residue_number=[]
    conn = mongodbUtil.mongo_conn()
    print(frame)
    print(frame_pocket)
    # 改过下面这行
    # framePocketData = conn[dbname][dbname_pocket].find_one({"frameID": int(frame), "pocketID": 1}, {"_id": 0, "frameInfo": 1})["frameInfo"]
    # print(framePocketData)
    # framePocketData = conn[dbname][dbname_pocket].find_one({"frameID": frame, "pocketID": "1"}, {"_id": 0, "frameInfo": 1})["frameInfo"]
    for d in conn[dbname][dbname_pocket].find({"frame_pocket": {"$in": str(frame_pocket).split("-")}}, {"_id": 0, "pocketInfo": 1}):
        text=d["pocketInfo"].split()
        print(text)
        # framePocketData += text[5]+' '
        residue_number.append(text[5])
    print(residue_number)
    # print(framePocketData)
    return residue_number



if __name__ == '__main__':
    molStar_frame = [
        ["20_1", "78_1", "32_3", "63_3", "94_2", "24_8", "85_1", "6_2", "89_2", "55_1", "22_11", "90_7", "34_6", "84_7", "77_6", "49_2", "15_1", ],
        ["86_1", "13_9", "21_4", "37_6", "12_4", "19_5", "54_5", "95_5", "97_6", "57_6", "71_5", "61_6", "72_3", "55_6", "53_7", "33_5", "9_5", "90_5", ],
        ["87_6", "39_8", "41_4", "98_8", "24_5", "69_2", "8_5", "90_8", "66_10", "29_7", "43_7", "71_3", "37_7", "91_4", "28_5", "61_4", "88_5", "63_4", "99_7", "59_1", "32_5", "98_4", "40_2", "41_5", "15_3", "73_4", "81_3", "46_4", "68_6",
         "39_5", "52_4", "99_3", "38_7", "74_5", "75_3", "25_5",
         "84_8", "100_2", "69_7", ]
    ]
    molStar_framePocket('1_1')
    # print(molStar_bar({"frame_pocket": molStar_frame}))
    # print(molStart_Slider("54,54_12-54_13-54_1-87_6-39_8-41_4-98_8-24_5-69_2-8_5-90_8-66_10-29_7-43_7-71_3-37_7-91_4-28_5-61_4-88_5-63_4-99_7-59_1-32_5-98_4-40_2-41_5-15_3-73_4-81_3-46_4-68_6-39_5-52_4-99_3-38_7-74_5-75_3-25_5"))
