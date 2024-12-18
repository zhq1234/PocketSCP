from util import message
from util import mongodbUtil
import ast
dbname = mongodbUtil.DBNAME
dbname_node = mongodbUtil.DBNAME_NODE
dbname_edge = mongodbUtil.DBNAME_EDGE
dbname_pocket = mongodbUtil.DBNAME_POCKET

def forcePlot_select_residue_pocket():
    conn = mongodbUtil.mongo_conn()
    selectPocket = []
    selectPocekt1=[]
    selectPocket2=[]
    selectPocket3=[]
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1,"residueID":1 }):
        # print(type(data['residueID']))
        array = ast.literal_eval(data['residueID'])

        # if ((18 in array and 16 in array and 96 in array and 26 in array and 85 in array and 17 in array and 88 in array and 89 in array and 93 in array and 95 in array and 97 in array and 98 in array)    ):
        if ((  300 and 48 in array)):
            selectPocket.append(data['frame_pocket'])
        #       print('')

            # pocket.append([data['']])

        if ((43 in array and 119 in array and 120 in array and 121 in array and 122 in array and 123 in array and 124 in array and 125 in array and 126 in array and 127 in array and 128 in array and 129 in array and 130 in array and 131 in array and 134 in array and 135 in array and 145 in array and 146 in array and 147 in array and 148 in array and 149 in array and 150 in array and 151 in array and 152 in array)):
            selectPocekt1.append(data['frame_pocket'])
        #      selectPocket.append(data['frame_pocket'])
    #     if(data['residueID']==48):
    #         selectPocket.append(data)
    # for index in selectPocket:
    #     print(index)
    print(selectPocket)
    print(selectPocekt1)
    for index in selectPocket:
        selectPocket2.append(index.split("_")[0])

    for index1 in selectPocekt1 :
        selectPocket3.append(index1.split("_")[0])

    print(selectPocket2)
    print(selectPocket3)
    common_elements = (list(set(selectPocket2) & set(selectPocket3)))
    common_elements = sorted(map(int, common_elements))
    selectPocket_volume=[]
    selectPocket1_volume=[]
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1, "residueID": 1,"volume": 1,}):
        # print(data['frame_pocket'])
        flag=0
        if(int(data['frame_pocket'].split("_")[0]) in common_elements and data['frame_pocket'] in selectPocket):
            selectPocket_volume.append(int(data['volume']))
            flag=1
        if (int(data['frame_pocket'].split("_")[0]) in common_elements and data['frame_pocket'] in selectPocekt1):
            selectPocket1_volume.append(int(data['volume']))
            # print(data['frame_pocket'])
        if((data['frame_pocket'] in selectPocket and data['frame_pocket'] in selectPocekt1)):
            print('11111111111111111'+data['frame_pocket'])

    print(len(selectPocket_volume))
    print(len(selectPocket1_volume))
    print(len(common_elements))
    print((selectPocket_volume))
    print((selectPocket1_volume))
    return message.success_message(
        {"select_pocket": selectPocket})
# 生成力导向图，默认
def forcePlotIndex():
    conn = mongodbUtil.mongo_conn()
    forceData = []
    max_x, max_y = 0, 0
    min_v = 9999
    max_v = 0
    min_alphanum,max_alphanum = 9999,0
    min_totalsasa,max_totalsasa = 9999,0
    min_polarsasa,max_polarsasa = 9999,0
    min_apolarsasa,max_apolarsasa = 9999,0
    min_mlohyden,max_mlohyden = 9999,0
    min_malspra,max_malspra = 9999,0
    min_msoacc,max_msoacc = 9999,0
    min_alalsppro,max_alalsppro = 9999,0
    min_propolatoms,max_propolatoms = 9999,0
    min_alspdensity,max_alspdensity = 9999,0
    min_alphaspmaxdist,max_alphaspmaxdist = 9999,0
    min_polarityscore,max_polarityscore = 9999,0
    min_frame,max_frame = 99999,0
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1, "x": 1, "y": 1, "color": 1,"volume": 1, "tag": 1,"alphanum": 1,"totalsasa": 1,"polarsasa": 1,"apolarsasa": 1,"mlohyden": 1,"malspra": 1,"msoacc": 1,"alalsppro": 1,"propolatoms": 1,"alspdensity": 1,"alphaspmaxdist": 1,"polarityscore": 1,"frameID":1 }):
        max_x = max(abs(data["x"]), max_x)
        max_y = max(abs(data["y"]), max_y)
        min_v = min(data['volume'],min_v)
        max_v = max(data['volume'],max_v)

        min_alphanum = min(data['alphanum'], min_alphanum)
        max_alphanum = max(data['alphanum'], max_alphanum)

        min_totalsasa = min(data['totalsasa'], min_totalsasa)
        max_totalsasa = max(data['totalsasa'], max_totalsasa)

        min_polarsasa = min(data['polarsasa'], min_polarsasa)
        max_polarsasa = max(data['polarsasa'], max_polarsasa)

        min_apolarsasa = min(data['apolarsasa'], min_apolarsasa)
        max_apolarsasa = max(data['apolarsasa'], max_apolarsasa)

        min_mlohyden = min(data['mlohyden'], min_mlohyden)
        max_mlohyden = max(data['mlohyden'], max_mlohyden)

        min_malspra = min(data['malspra'], min_malspra)
        max_malspra = max(data['malspra'], max_malspra)

        min_msoacc = min(data['msoacc'], min_msoacc)
        max_msoacc = max(data['msoacc'], max_msoacc)

        min_alalsppro = min(data['alalsppro'], min_alalsppro)
        max_alalsppro = max(data['alalsppro'], max_alalsppro)

        min_propolatoms = min(data['propolatoms'], min_propolatoms)
        max_propolatoms = max(data['propolatoms'], max_propolatoms)

        min_alspdensity = min(data['alspdensity'], min_alspdensity)
        max_alspdensity = max(data['alspdensity'], max_alspdensity)

        min_alphaspmaxdist = min(data['alphaspmaxdist'], min_alphaspmaxdist)
        max_alphaspmaxdist = max(data['alphaspmaxdist'], max_alphaspmaxdist)

        min_polarityscore = min(data['polarityscore'],min_polarityscore)
        max_polarityscore = max(data['polarityscore'],max_polarityscore)


        min_frame = min(data['frameID'],min_frame)
        max_frame = max(data['frameID'], max_frame)

        forceData.append(data)
    return message.success_message({"forceData": forceData, "maxX": max_x + int(max_x / 10), "maxY": max_y + int(max_y / 10), "minV": min_v,"maxV":max_v,"min_alphanum":min_alphanum,"max_alphanum":max_alphanum,"min_totalsasa":min_totalsasa,"max_totalsasa":max_totalsasa,"min_polarsasa":min_polarsasa,"max_polarsasa":max_polarsasa,"min_apolarsasa":min_apolarsasa,"max_apolarsasa":max_apolarsasa,"min_mlohyden":min_mlohyden,"max_mlohyden":max_mlohyden,"min_malspra":min_malspra,"max_malspra":max_malspra,"min_msoacc":min_msoacc,"max_msoacc":max_msoacc,"min_alalsppro":min_alalsppro,"max_alalsppro":max_alalsppro,"min_propolatoms":min_propolatoms,"max_propolatoms":max_propolatoms,"min_alspdensity":min_alspdensity,"max_alspdensity":max_alspdensity,"min_alphaspmaxdist":min_alphaspmaxdist,"max_alphaspmaxdist":max_alphaspmaxdist,"min_polarityscore":min_polarityscore,"max_polarityscore":max_polarityscore,"min_frame":min_frame,"max_frame":max_frame})
# 为什么加上十分之一的maxX maxY

# 将参数 param 解析为字典类型，根据字典中的 similar 和 frame_pocket 的值查询 MongoDB 数据库，以获取符合条件的数据。
#nibushangbanm
# 对于查询结果，代码首先将 frame_pocket 中的每个点添加到一个集合 s 中，然后遍历每个点 pocket，并找到其到其他点的所有边。
# 对于每条边，如果其权重大于等于 similar，则将该边的源节点和目标节点存储到列表 line 中，并将目标节点的度数和源节点的度数加一。
#
# 最后，函数返回一个包含连接线数据和每个节点的度数的字典，通过 message.success_message() 函数封装成一个成功的响应消息返回给客户端。
def forcePlotLinkLine(param):
    print("forceLinkLine ", param)
    # 查询指定的点，根据重叠度，返回指定的线
    conn = mongodbUtil.mongo_conn()
    weightMin = float(param["similarMin"])
    weightMax = float(param["similarMax"])
    pockets = str(param["frame_pocket"]).strip().split(",")
    print(weightMin, weightMax, pockets)
    line = []
    s = set()
    degree = dict()  # 计算各个点的度
    # rangeDegree = {max: -1, min: 0}
    for pocket in pockets:
        s.add(pocket)
        # degree[pocket] = 0 出度初始化
        if pocket not in degree:
            degree[pocket] = 0
        for edge in conn[dbname][dbname_edge].find({"source": pocket, "weight": {'$gte': weightMin, '$lte': weightMax}}, {"target": 1}):
            # frame_pocket 的目标节点不在 s集合中 就在line数组中添加一个[source,target]
            if edge["target"] not in s:
                line.append([pocket, edge["target"]])
            # frame_pocket 的目标节点不在 degree 字典中 就令degree[target]=0 入度初始化
            if edge["target"] not in degree:
                degree[edge["target"]] = 0
            degree[edge["target"]] += 1  # degree入度+1
            degree[pocket] += 1  # 出度+1
    # print(degree) 没用到degree
    # line 是 包含 [source,target] 的二维数组
    return message.success_message({"link": line, "degree": degree})


def forcePlotChangeColor(param):
    conn = mongodbUtil.mongo_conn()
    # print(param)
    for pocket in str(param["frame_pocket"]).strip().split(","):
        # conn[dbname][dbname_pocket].update({"frame_pocket": pocket}, {"$set": {"color": param["color"]}})
        conn[dbname][dbname_pocket].update({"frame_pocket": pocket}, {"$set": {"color": param["color"]}})

        # conn[dbname][dbname_pocket].update_many({"frame_pocket": {"$in": str(param["frame_pocket"]).strip().split(",")}}, {"$set": {"color": param["color"]}})
    return message.success_message({})


def HexToRGB(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    rgb = "rgb(" + str(r) + ',' + str(g) + ',' + str(b) + ")"
    return rgb


if __name__ == '__main__':
    print(HexToRGB("#b91313"))
    # forcePlotIndex()
    forcePlot_select_residue_pocket()
