import json

from PocketVIS.util import message
from PocketVIS.util import mongodbUtil
import ast
dbname = mongodbUtil.DBNAME
dbname_node = mongodbUtil.DBNAME_NODE
dbname_edge = mongodbUtil.DBNAME_EDGE
dbname_pocket = mongodbUtil.DBNAME_POCKET

def forcePlot_select_residue_pocket(params):
    print(params)
    if params is None:
        return message.false_message("空参")
    residue_str = params['residue']
    residue_list = [int(x) for x in residue_str.split(',')]
    conn = mongodbUtil.mongo_conn()

    # 打印调试信息
    # print(residue_list)

    selectPocket = []
    selectPocekt1=[]
    selectPocket2=[]
    selectPocket3=[]
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1,"residueID":1 }):
        # print(type(data['residueID']))
        array = ast.literal_eval(data['residueID'])

        # if ((18 in array and 16 in array and 96 in array and 26 in array and 85 in array and 17 in array and 88 in array and 89 in array and 93 in array and 95 in array and 97 in array and 98 in array)    ):
        if all(item in array for item in residue_list):
        # if (( 43 in array and 119 in array and 120 in array and 121 in array and 122 in array and 123 in array and 124 in array and 125 in array and 126 in array and 127 in array and 128 in array and 129 in array and 130 in array and 131 in array and 134 in array and 135 in array and 145 in array and 146 in array and 147 in array and 148 in array and 149 in array and 150 in array and 151 in array and 152 in array)):
       # if ((  300 and 48 in array)):
           print(data['frame_pocket'])
           number_part =data['frame_pocket'] .split('_')[0]
           number = int(number_part)
           # if(number<940 and number!=697  ):
           selectPocket.append(data['frame_pocket'])
            # selectPocekt.append(data['frame_pocket'])
        #       print('')

            # pocket.append([data['']])

        # if (( 43 in array and 119 in array and 120 in array and 121 in array and 122 in array and 123 in array and 124 in array and 125 in array and 126 in array and 127 in array and 128 in array and 129 in array and 130 in array and 131 in array and 134 in array and 135 in array and 145 in array and 146 in array and 147 in array and 148 in array and 149 in array and 150 in array and 151 in array and 152 in array)):
        #     # selectPocekt.append(data['frame_pocket'])
        #     number_part = data['frame_pocket'].split('_')[0]
        #     number = int(number_part)
        #     if ( number != 282 and number != 291 and number != 68 and number != 273):
        #      selectPocket.append(data['frame_pocket'])

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

    # print(len(selectPocket_volume))
    # print(len(selectPocket1_volume))
    # print(len(common_elements))
    # print((selectPocket_volume))
    # print((selectPocket1_volume))
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

# (8_8,57_23,16_12,17_19,15_22,21_23,38_22,35_21,26_23,9_20,55_14,46_19,1_17,5_18,34_12,3_21,28_11,36_18,44_7,25_22,33_29,51_19,40_19,19_25,55_20,34_4,47_25,39_20,7_10,2_20,40_12,59_18,15_7,11_16,30_11,54_25,4_3,50_17,53_21,31_13,41_18,14_3,33_12,13_1,19_17,31_6,5_6,22_22,
#  52_24,32_22,29_20,23_16,36_7,27_21,28_19,13_11,48_6,21_7,30_15,12_16,20_23,16_7,20_10,9_18,14_15,6_14,23_2,12_1,47_19,18_20,44_4,7_1,17_6,10_8,10_10,42_19,18_1,43_6,23_11,27_10,8_15,43_17,50_12,54_21,48_13,38_11,56_21,2_16,41_7,24_9,45_3,49_19,11_1,58_24,45_19,37_2,29_4,32_5,24_4)
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


def find_2acu_diff():
    # except298=['18_20', '5_6', '45_19', '54_21', '17_6', '32_5', '38_11', '9_18', '50_12',
    # '24_4', '29_20', '30_15', '7_10', '28_11', '21_7', '34_12', '43_17', '44_4',
    # '2_16', '31_6', '41_7', '36_7', '33_12', '12_16', '14_15', '40_12', '16_7',
    # '11_16', '20_23', '55_14', '27_10', '15_22', '23_16', '8_15', '48_13', '13_11',
    # '10_10', '19_17', '47_19', '23_2']
    except298=['2_16', '5_6', '7_10', '8_15', '9_18', '10_10', '11_16', '12_16', '13_11', '14_15', '15_22', '16_7', '17_6',
     '18_20', '19_17', '20_23', '21_7', '23_2', '23_16', '24_4', '27_10', '28_11', '29_20', '30_15', '31_6', '32_5',
     '33_12', '34_12', '36_7', '38_11', '40_12', '41_7', '43_17', '44_4', '45_19', '47_19', '48_13', '50_12', '54_21',
     '55_14']
    residue298=['1_17', '2_20', '3_21', '4_3', '5_18', '6_14', '7_1', '8_8', '9_20', '10_8', '10_28', '11_1', '12_1', '13_1',
     '14_3', '15_7', '16_12', '17_19', '18_1', '19_25', '20_10', '21_23', '22_22', '23_11', '24_9', '25_22',
     '26_23', '27_21', '28_19', '29_4', '30_11', '31_13', '32_22', '33_29', '34_4', '35_21', '36_18', '37_2', '37_14',
     '38_22', '39_20', '40_19', '41_18', '42_19', '43_6', '44_7', '45_3', '46_19', '47_25', '48_6', '49_19', '50_17',
     '51_19', '52_24', '53_21', '54_25', '55_20', '56_21', '57_23', '58_24', '59_18']
    conn = mongodbUtil.mongo_conn()
    residue_count_except298 = {}
    residue_count_298 = {}
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1,"residueID":1 }):
        # print(type(data['residueID']))
        array = ast.literal_eval(data['residueID'])

        # if ((18 in array and 16 in array and 96 in array and 26 in array and 85 in array and 17 in array and 88 in array and 89 in array and 93 in array and 95 in array and 97 in array and 98 in array)    ):
        # if (298 in array):
        #     residue_48_Pocket.append(data['frame_pocket'])
        #     print(data['residueID'])
        # 遍历 data['pocket_frame'] 并统计残基数量
        if(data['frame_pocket'] in except298):
            for residue in ast.literal_eval(data['residueID']):
                 if residue in residue_count_except298:
                     residue_count_except298[residue] += 1
                 else:
                     residue_count_except298[residue] = 1

        if (data['frame_pocket'] in residue298):
            for residue in ast.literal_eval(data['residueID']):
                if residue in  residue_count_298:
                    residue_count_298[residue] += 1
                else:
                    residue_count_298[residue] = 1

    sorted_residue_count_except298 = dict(sorted(residue_count_except298.items(), key=lambda item: item[1], reverse=True))
    print(residue_count_except298)
    sorted_residue_count_298 = dict(sorted(residue_count_298.items(), key=lambda item: item[1], reverse=True))
    print(sorted_residue_count_298)
    # 找出两个字典中都有的键
    # common_keys = set(residue_count_except298.keys()) & set(sorted_residue_count_298.keys())

    # 创建一个新的字典，存储这些键和值
    # common_dict = {key: (residue_count_except298[key], sorted_residue_count_298[key]) for key in common_keys}
    #
    # print(common_dict)

    # 找出两个字典中都有的键
    common_keys = set(residue_count_except298.keys()) & set(sorted_residue_count_298.keys())

    # 设置一个阈值，只有当两个字典中的值都大于这个阈值时，才将其包括在结果中
    threshold = 1

    # 设置一个差异阈值，只有当两个字典中的值差异小于这个阈值时，才将其包括在结果中
    difference_threshold = 100

    # 创建一个新的字典，存储这些键和值
    common_dict = {key: (residue_count_except298[key], sorted_residue_count_298[key]) for key in common_keys
                   if residue_count_except298[key] > threshold and sorted_residue_count_298[key] > threshold and abs(
            residue_count_except298[key] - sorted_residue_count_298[key]) <= difference_threshold}

    print(common_dict)


    # print(residue_48_Pocket)
# 所有

# ['8_8', '57_23', '16_12', '17_19', '15_22', '21_23', '38_22', '35_21', '26_23', '9_20', '55_14', '46_19', '1_17', '5_18', '34_12', '3_21', '28_11', '36_18', '44_7', '25_22', '33_29', '51_19', '40_19', '19_25', '55_20', '34_4', '47_25', '39_20', '7_10', '2_20', '40_12', '59_18', '15_7', '11_16', '30_11', '54_25', '4_3', '50_17', '53_21', '31_13', '41_18', '14_3', '33_12', '13_1', '19_17', '31_6', '5_6', '22_22', '52_24', '32_22', '29_20', '23_16', '36_7', '27_21', '28_19', '13_11', '48_6', '21_7', '30_15', '12_16', '20_23', '16_7', '20_10', '9_18', '14_15', '6_14', '23_2', '12_1', '47_19', '18_20', '44_4', '7_1', '17_6', '10_8', '10_10', '42_19', '18_1', '43_6', '23_11', '27_10', '8_15', '43_17', '50_12', '54_21', '48_13', '38_11', '56_21', '2_16', '41_7', '24_9', '45_3', '49_19', '11_1', '58_24', '45_19', '37_2', '29_4', '32_5', '24_4']
# # 298：
# ['1_17', '2_20', '3_21', '4_3', '5_18', '6_14', '7_1', '8_8', '9_20', '10_8', '10_28', '11_1', '12_1', '13_1', '14_3', '15_7', '16_12', '17_19', '18_1', '19_25', '20_10', '21_23', '22_22', '23_11', '23_21', '24_9', '25_22', '26_23', '27_21', '28_19',  '29_4', '30_11', '31_13', '32_22', '33_29', '34_4', '35_21', '36_18', '37_2', '37_14', '38_22', '39_20', '40_19', '41_18', '42_19', '43_6', '44_7', '45_3', '46_19', '47_25', '48_6', '49_19', '50_17', '51_19', '52_24', '53_21', '54_25', '55_20', '56_21', '57_23', '58_24', '59_18']
#
# # 大
# ['18_20', '5_6', '45_19', '54_21', '17_6', '32_5', '38_11', '9_18', '50_12',
#  '24_4', '29_20', '30_15', '7_10', '28_11', '21_7', '34_12', '43_17', '44_4',
#  '2_16', '31_6', '41_7', '36_7', '33_12', '12_16', '14_15', '40_12', '16_7',
#  '11_16', '20_23', '55_14', '27_10', '15_22', '23_16', '8_15', '48_13', '13_11',
#  '10_10', '19_17', '47_19', '23_2']
def find298_300():

    residue298=['1_17', '2_20', '3_21', '4_3', '5_18', '6_14', '7_1', '8_8', '9_20', '10_8', '10_28', '11_1', '12_1', '13_1',
     '14_3', '15_7', '16_12', '17_19', '18_1', '19_25', '20_10', '21_23', '22_22', '23_11', '23_21', '24_9', '25_22',
     '26_23', '27_21', '28_19', '29_4', '30_11', '31_13', '32_22', '33_29', '34_4', '35_21', '36_18', '37_2', '37_14',
     '38_22', '39_20', '40_19', '41_18', '42_19', '43_6', '44_7', '45_3', '46_19', '47_25', '48_6', '49_19', '50_17',
     '51_19', '52_24', '53_21', '54_25', '55_20', '56_21', '57_23', '58_24', '59_18']
    conn = mongodbUtil.mongo_conn()
    residue_count_except298 = {}
    residue_count_298 = {}
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1,"residueID":1 }):
        # print(type(data['residueID']))
        # array = ast.literal_eval(data['residueID'])
        if data['frame_pocket'] == '34_4':
         # if ((18 in array and 16 in array and 96 in array and 26 in array and 85 in array and 17 in array and 88 in array and 89 in array and 93 in array and 95 in array and 97 in array and 98 in array)    ):
        # if (298 in array):
        #     residue_48_Pocket.append(data['frame_pocket'])
              print('34_4:'+data['residueID'])
        if data['frame_pocket'] == '47_25':
            print('47_25:' + data['residueID'])
        if data['frame_pocket'] == '31_13':
             print('31_13:' + data['residueID'])
        # 遍历 data['pocket_frame'] 并统计残基数量
        if (data['frame_pocket'] in residue298):
            for residue in ast.literal_eval(data['residueID']):
                if residue in  residue_count_298:
                    residue_count_298[residue] += 1
                else:
                    residue_count_298[residue] = 1
    sorted_residue_count_298 = dict(sorted(residue_count_298.items(), key=lambda item: item[1], reverse=True))
    print(sorted_residue_count_298)

def find_same_time():
    # down=[725_11,777_5,776_10,921_3,567_3,576_5,642_8,640_9,732_7,731_13,655_11,808_9,653_9,986_4,814_12,748_8,855_7,517_6,644_5,836_8,636_10,641_12,687_6,927_10,
    #         568_8,578_10,721_7,535_11,670_6,496_11,753_5,678_3,801_7,581_9,824_6,648_10,745_11,944_4,833_4,899_10,433_5,861_11,683_16,750_10,573_9,479_9,734_8,428_3,
    #         832_12,823_14,835_7,889_10,698_13,862_7,830_10,664_10,1000_4,429_4,794_9,682_9,768_10,926_7,662_8,756_9,455_13,465_10,859_5,828_7,880_8,710_16,680_7,809_6,
    #         712_5,645_8,844_16,359_6,713_6,582_14,686_9,660_9,654_7,733_10,656_8,974_16,746_12,929_3,744_12,657_7,652_9,831_10,739_13,988_6,658_8,992_6,574_7,829_5,536_10,
    #         811_7,985_2,688_14,377_7,549_5,990_4,994_7,993_13,864_11,430_3,651_2,903_9,475_14,483_5,837_17,454_5,501_3,857_16,827_9,451_14,834_15,530_13,658_6,486_5,707_8,
    #         418_6,679_14,492_6,437_5,489_10,772_7,936_6,521_4,632_3,838_5,716_4,497_8,674_12,826_8,825_6,879_9,765_8,672_9,522_7,759_11,669_8,693_9,494_14,738_8,980_9,965_5,
    #         420_10,988_7,909_8,816_8,575_7,355_8,401_11,931_12,532_8,962_10,464_12,775_9,798_9,562_10,506_10,930_5,378_9,692_11,639_16,308_6,375_7,761_8,996_1,491_8,696_4,695_14,525_6,866_18,714_9,351_5,488_9,395_6,999_2,460_16,998_3,997_3,396_6,
    #         392_9,305_11,715_10,125_7,463_10,587_8,668_8,663_8,963_11,958_7,9_7,956_11,72_10,296_8,297_9,924_3,237_12,701_9,525_5,708_11,966_10,376_6,979_6,967_4,328_6,431_6,943_6,984_9,412_9,598_9,313_11,977_6,342_9,369_10,71_10,379_6,380_10,528_10,325_8]
    down = [
        "725_11", "777_5", "776_10", "921_3", "567_3", "576_5", "642_8", "640_9", "732_7", "731_13", "655_11", "808_9",
        "653_9", "986_4", "814_12", "748_8", "855_7", "517_6", "644_5", "836_8", "636_10", "641_12", "687_6", "927_10",
        "568_8", "578_10", "721_7", "535_11", "670_6", "496_11", "753_5", "678_3", "801_7", "581_9", "824_6", "648_10",
        "745_11", "944_4", "833_4", "899_10", "433_5", "861_11", "683_16", "750_10", "573_9", "479_9", "734_8", "428_3",
        "832_12", "823_14", "835_7", "889_10", "698_13", "862_7", "830_10", "664_10", "1000_4", "429_4", "794_9",
        "682_9", "768_10", "926_7", "662_8", "756_9", "455_13", "465_10", "859_5", "828_7", "880_8", "710_16", "680_7",
        "809_6","712_5", "645_8", "844_16", "359_6", "713_6", "582_14", "686_9", "660_9", "654_7", "733_10", "656_8", "974_16",
        "746_12", "929_3", "744_12", "657_7", "652_9", "831_10", "739_13", "988_6", "658_8", "992_6", "574_7", "829_5",
        "536_10","811_7", "985_2", "688_14", "377_7", "549_5", "990_4", "994_7", "993_13", "864_11", "430_3", "651_2", "903_9",
        "475_14", "483_5", "837_17", "454_5", "501_3", "857_16", "827_9", "451_14", "834_15", "530_13", "658_6", "486_5", "707_8",
        "418_6", "679_14", "492_6", "437_5", "489_10", "772_7", "936_6", "521_4", "632_3", "838_5", "716_4", "497_8",
        "674_12", "826_8", "825_6", "879_9", "765_8", "672_9", "522_7", "759_11", "669_8", "693_9", "494_14", "738_8",
        "980_9", "965_5", "420_10", "988_7", "909_8", "816_8", "575_7", "355_8", "401_11", "931_12", "532_8", "962_10", "464_12", "775_9",
        "798_9", "562_10", "506_10", "930_5", "378_9", "692_11", "639_16", "308_6", "375_7", "761_8", "996_1", "491_8",
        "696_4", "695_14", "525_6", "866_18", "714_9", "351_5", "488_9", "395_6", "999_2", "460_16", "998_3", "997_3","396_6",
        "392_9", "305_11", "715_10", "125_7", "463_10", "587_8", "668_8", "663_8", "963_11", "958_7", "9_7", "956_11",
        "72_10", "296_8", "297_9", "924_3", "237_12", "701_9", "525_5", "708_11", "966_10", "376_6", "979_6", "967_4",
        "328_6", "431_6", "943_6", "984_9", "412_9", "598_9", "313_11", "977_6", "342_9", "369_10", "71_10", "379_6",
        "380_10", "528_10", "325_8"
    ]
    # up=[670_10,825_10,670_4,862_5,792_8,671_10,889_12,304_1,452_17,886_6,605_8,568_10,932_4,232_2,913_9,903_16,811_12,519_12,805_12,454_15,551_9,573_10,196_3,834_8,547_2,576_6,977_5,756_13,526_12,569_6,494_4,893_9,803_10,719_16,665_12,688_7,451_8,639_9,693_8,843_11,793_15,799_12,784_8,786_14,869_7,750_13,710_10,850_10,520_3,674_8,865_14,528_3,572_13,755_8,743_7,748_6,962_5,872_10,770_7,829_7,807_8,808_7,742_11,804_9,595_4,857_9,798_10,591_6,707_11,590_3,525_7,435_16,874_12,882_4,810_13,764_5,637_10,906_8,682_6,730_8,981_13,853_7,762_12,867_7,908_9,864_14,801_4,521_2,451_9,885_5,765_4,979_4,684_6,890_5,712_10,876_5,610_6,837_6,767_14,861_8,668_12,456_6,910_10,878_5,988_3,891_9,912_10,870_9,816_11,602_5,777_12,609_11,398_8,968_3,854_4,581_6,844_5,425_8,685_6,824_11,523_3,859_11,650_7,776_12,919_6,934_6,656_10,599_6,477_9,866_10,826_7,984_2,822_7,918_8,695_4,935_3,768_4,534_5,470_3,892_6,686_5,537_4,928_3,692_5,821_6,673_14,476_8,562_16,832_4,479_13,563_8,453_4,980_3,894_3,417_9,862_8,405_14,412_10,654_6,819_7,877_12,855_11,856_8,598_11,715_4,875_9,339_6,342_8,333_8,640_12,463_11,253_8,952_5,223_7,282_7,944_17,284_6,469_13,387_12,611_13,430_7,612_6,947_5,795_5,541_6,917_4,472_3,372_11,948_9,687_4,478_9,737_10,620_8,888_4,409_4,276_4,286_3,251_7,731_6,488_7,763_11,464_6,957_14,956_16,922_10,895_6,236_11,713_9,766_6,300_9,787_7,806_2,904_6,397_6,522_11]
    up = [
        "670_10", "825_10", "670_4", "862_5", "792_8", "671_10", "889_12", "304_1", "452_17", "886_6", "605_8",
        "568_10", "932_4", "232_2", "913_9", "903_16", "811_12", "519_12", "805_12", "454_15", "551_9", "573_10",
        "196_3", "834_8", "547_2", "576_6", "977_5", "756_13", "526_12", "569_6", "494_4", "893_9", "803_10", "719_16",
        "665_12", "688_7", "451_8", "639_9", "693_8", "843_11", "793_15", "799_12", "784_8", "786_14", "869_7",
        "750_13", "710_10", "850_10", "520_3", "674_8", "865_14", "528_3", "572_13", "755_8", "743_7", "748_6", "962_5",
        "872_10", "770_7", "829_7", "807_8", "808_7", "742_11", "804_9", "595_4", "857_9", "798_10", "591_6", "707_11",
        "590_3", "525_7", "435_16", "874_12", "882_4", "810_13", "764_5", "637_10", "906_8", "682_6", "730_8", "981_13",
        "853_7", "762_12", "867_7", "908_9", "864_14", "801_4", "521_2", "451_9", "885_5", "765_4", "979_4", "684_6",
        "890_5", "712_10", "876_5", "610_6", "837_6", "767_14", "861_8", "668_12", "456_6", "910_10", "878_5", "988_3",
        "891_9", "912_10", "870_9", "816_11", "602_5", "777_12", "609_11", "398_8", "968_3", "854_4", "581_6", "844_5",
        "425_8", "685_6", "824_11", "523_3", "859_11", "650_7", "776_12", "919_6", "934_6", "656_10", "599_6", "477_9",
        "866_10", "826_7", "984_2", "822_7", "918_8", "695_4", "935_3", "768_4", "534_5", "470_3", "892_6", "686_5",
        "537_4", "928_3", "692_5", "821_6", "673_14", "476_8", "562_16", "832_4", "479_13", "563_8", "453_4", "980_3",
        "894_3", "417_9", "862_8", "405_14", "412_10", "654_6", "819_7", "877_12", "855_11", "856_8", "598_11", "715_4",
        "875_9", "339_6", "342_8", "333_8", "640_12", "463_11", "253_8", "952_5", "223_7", "282_7", "944_17", "284_6",
        "469_13", "387_12", "611_13", "430_7", "612_6", "947_5", "795_5", "541_6", "917_4", "472_3", "372_11", "948_9",
        "687_4", "478_9", "737_10", "620_8", "888_4", "409_4", "276_4", "286_3", "251_7", "731_6", "488_7", "763_11",
        "464_6", "957_14", "956_16", "922_10", "895_6", "236_11", "713_9", "766_6", "300_9", "787_7", "806_2", "904_6",
        "397_6", "522_11"
    ]
    # 提取 down 和 up 列表中的 x 值
    down_x = {item.split('_')[0] for item in down}
    up_x = {item.split('_')[0] for item in up}

    # 找到重叠的 x 值
    overlap_x = down_x.intersection(up_x)

    print(overlap_x)
    # 找共同残基
    conn = mongodbUtil.mongo_conn()
    front = {}
    back = {}
    back2={}
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1, "residueID": 1}):
        # print(type(data['residueID']))
        # array = ast.literal_eval(data['residueID'])
        # 还有693_8
        if (data['frame_pocket'] == '692_5'):
            front=ast.literal_eval(data['residueID'])
            print(front)
        # 还有693_9
        if (data['frame_pocket'] == '692_11'):
            back=ast.literal_eval(data['residueID'])
            print(back)
        # if (data['frame_pocket'] == '777_12'):
        #     back2=ast.literal_eval(data['residueID'])
        #     print(back2)
        if (data['frame_pocket'] == '495_6'):
            print(ast.literal_eval(data['residueID']))

        # list1 = [224, 227, 131, 220, 223]
        # list2 = [130, 227, 223, 131, 248, 251, 252, 255]

        # 将列表转换为集合，然后取交集
        intersection = list(set(front) & set(back))

    print(intersection)
def find_DHA_same_residue():
  # except298是up

    except298 = [
        "670_10", "825_10", "670_4", "862_5", "792_8", "671_10", "889_12", "304_1", "452_17", "886_6", "605_8",
        "568_10", "932_4", "232_2", "913_9", "903_16", "811_12", "519_12", "805_12", "454_15", "551_9", "573_10",
        "196_3", "834_8", "547_2", "576_6", "977_5", "756_13", "526_12", "569_6", "494_4", "893_9", "803_10", "719_16",
        "665_12", "688_7", "451_8", "639_9", "693_8", "843_11", "793_15", "799_12", "784_8", "786_14", "869_7",
        "750_13", "710_10", "850_10", "520_3", "674_8", "865_14", "528_3", "572_13", "755_8", "743_7", "748_6", "962_5",
        "872_10", "770_7", "829_7", "807_8", "808_7", "742_11", "804_9", "595_4", "857_9", "798_10", "591_6", "707_11",
        "590_3", "525_7", "435_16", "874_12", "882_4", "810_13", "764_5", "637_10", "906_8", "682_6", "730_8", "981_13",
        "853_7", "762_12", "867_7", "908_9", "864_14", "801_4", "521_2", "451_9", "885_5", "765_4", "979_4", "684_6",
        "890_5", "712_10", "876_5", "610_6", "837_6", "767_14", "861_8", "668_12", "456_6", "910_10", "878_5", "988_3",
        "891_9", "912_10", "870_9", "816_11", "602_5", "777_12", "609_11", "398_8", "968_3", "854_4", "581_6", "844_5",
        "425_8", "685_6", "824_11", "523_3", "859_11", "650_7", "776_12", "919_6", "934_6", "656_10", "599_6", "477_9",
        "866_10", "826_7", "984_2", "822_7", "918_8", "695_4", "935_3", "768_4", "534_5", "470_3", "892_6", "686_5",
        "537_4", "928_3", "692_5", "821_6", "673_14", "476_8", "562_16", "832_4", "479_13", "563_8", "453_4", "980_3",
        "894_3", "417_9", "862_8", "405_14", "412_10", "654_6", "819_7", "877_12", "855_11", "856_8", "598_11", "715_4",
        "875_9", "339_6", "342_8", "333_8", "640_12", "463_11", "253_8", "952_5", "223_7", "282_7", "944_17", "284_6",
        "469_13", "387_12", "611_13", "430_7", "612_6", "947_5", "795_5", "541_6", "917_4", "472_3", "372_11", "948_9",
        "687_4", "478_9", "737_10", "620_8", "888_4", "409_4", "276_4", "286_3", "251_7", "731_6", "488_7", "763_11",
        "464_6", "957_14", "956_16", "922_10", "895_6", "236_11", "713_9", "766_6", "300_9", "787_7", "806_2", "904_6",
        "397_6", "522_11"
    ]
    # residue298是down
    residue298 = [
        "725_11", "777_5", "776_10", "921_3", "567_3", "576_5", "642_8", "640_9", "732_7", "731_13", "655_11", "808_9",
        "653_9", "986_4", "814_12", "748_8", "855_7", "517_6", "644_5", "836_8", "636_10", "641_12", "687_6", "927_10",
        "568_8", "578_10", "721_7", "535_11", "670_6", "496_11", "753_5", "678_3", "801_7", "581_9", "824_6", "648_10",
        "745_11", "944_4", "833_4", "899_10", "433_5", "861_11", "683_16", "750_10", "573_9", "479_9", "734_8", "428_3",
        "832_12", "823_14", "835_7", "889_10", "698_13", "862_7", "830_10", "664_10", "1000_4", "429_4", "794_9",
        "682_9", "768_10", "926_7", "662_8", "756_9", "455_13", "465_10", "859_5", "828_7", "880_8", "710_16", "680_7",
        "809_6", "712_5", "645_8", "844_16", "359_6", "713_6", "582_14", "686_9", "660_9", "654_7", "733_10", "656_8",
        "974_16",
        "746_12", "929_3", "744_12", "657_7", "652_9", "831_10", "739_13", "988_6", "658_8", "992_6", "574_7", "829_5",
        "536_10", "811_7", "985_2", "688_14", "377_7", "549_5", "990_4", "994_7", "993_13", "864_11", "430_3", "651_2",
        "903_9",
        "475_14", "483_5", "837_17", "454_5", "501_3", "857_16", "827_9", "451_14", "834_15", "530_13", "658_6",
        "486_5", "707_8",
        "418_6", "679_14", "492_6", "437_5", "489_10", "772_7", "936_6", "521_4", "632_3", "838_5", "716_4", "497_8",
        "674_12", "826_8", "825_6", "879_9", "765_8", "672_9", "522_7", "759_11", "669_8", "693_9", "494_14", "738_8",
        "980_9", "965_5", "420_10", "988_7", "909_8", "816_8", "575_7", "355_8", "401_11", "931_12", "532_8", "962_10",
        "464_12", "775_9",
        "798_9", "562_10", "506_10", "930_5", "378_9", "692_11", "639_16", "308_6", "375_7", "761_8", "996_1", "491_8",
        "696_4", "695_14", "525_6", "866_18", "714_9", "351_5", "488_9", "395_6", "999_2", "460_16", "998_3", "997_3",
        "396_6",
        "392_9", "305_11", "715_10", "125_7", "463_10", "587_8", "668_8", "663_8", "963_11", "958_7", "9_7", "956_11",
        "72_10", "296_8", "297_9", "924_3", "237_12", "701_9", "525_5", "708_11", "966_10", "376_6", "979_6", "967_4",
        "328_6", "431_6", "943_6", "984_9", "412_9", "598_9", "313_11", "977_6", "342_9", "369_10", "71_10", "379_6",
        "380_10", "528_10", "325_8"
    ]
    conn = mongodbUtil.mongo_conn()
    residue_count_except298 = {}
    residue_count_298 = {}
    for data in conn[dbname][dbname_pocket].find({}, {"_id": 0, "frame_pocket": 1,"residueID":1 }):
        # print(type(data['residueID']))
        array = ast.literal_eval(data['residueID'])

        # if ((18 in array and 16 in array and 96 in array and 26 in array and 85 in array and 17 in array and 88 in array and 89 in array and 93 in array and 95 in array and 97 in array and 98 in array)    ):
        # if (298 in array):
        #     residue_48_Pocket.append(data['frame_pocket'])
        #     print(data['residueID'])
        # 遍历 data['pocket_frame'] 并统计残基数量
        if(data['frame_pocket'] in except298):
            for residue in ast.literal_eval(data['residueID']):
                 if residue in residue_count_except298:
                     residue_count_except298[residue] += 1
                 else:
                     residue_count_except298[residue] = 1

        if (data['frame_pocket'] in residue298):
            for residue in ast.literal_eval(data['residueID']):
                if residue in  residue_count_298:
                    residue_count_298[residue] += 1
                else:
                    residue_count_298[residue] = 1

    sorted_residue_count_except298 = dict(sorted(residue_count_except298.items(), key=lambda item: item[1], reverse=True))
    print(residue_count_except298)
    sorted_residue_count_298 = dict(sorted(residue_count_298.items(), key=lambda item: item[1], reverse=True))
    print(sorted_residue_count_298)
    # 找出两个字典中都有的键
    # common_keys = set(residue_count_except298.keys()) & set(sorted_residue_count_298.keys())

    # 创建一个新的字典，存储这些键和值
    # common_dict = {key: (residue_count_except298[key], sorted_residue_count_298[key]) for key in common_keys}
    #
    # print(common_dict)

    # 找出两个字典中都有的键
    common_keys = set(residue_count_except298.keys()) & set(sorted_residue_count_298.keys())

    # 设置一个阈值，只有当两个字典中的值都大于这个阈值时，才将其包括在结果中
    threshold = 1

    # 设置一个差异阈值，只有当两个字典中的值差异小于这个阈值时，才将其包括在结果中
    difference_threshold = 400

    # 创建一个新的字典，存储这些键和值
    common_dict = {key: (residue_count_except298[key], sorted_residue_count_298[key]) for key in common_keys
                   if residue_count_except298[key] > threshold and sorted_residue_count_298[key] > threshold and abs(
            residue_count_except298[key] - sorted_residue_count_298[key]) <= difference_threshold}

    print(common_dict)


    # print(residue_48_Pocket)
# 所有

# ['8_8', '57_23', '16_12', '17_19', '15_22', '21_23', '38_22', '35_21', '26_23', '9_20', '55_14', '46_19', '1_17', '5_18', '34_12', '3_21', '28_11', '36_18', '44_7', '25_22', '33_29', '51_19', '40_19', '19_25', '55_20', '34_4', '47_25', '39_20', '7_10', '2_20', '40_12', '59_18', '15_7', '11_16', '30_11', '54_25', '4_3', '50_17', '53_21', '31_13', '41_18', '14_3', '33_12', '13_1', '19_17', '31_6', '5_6', '22_22', '52_24', '32_22', '29_20', '23_16', '36_7', '27_21', '28_19', '13_11', '48_6', '21_7', '30_15', '12_16', '20_23', '16_7', '20_10', '9_18', '14_15', '6_14', '23_2', '12_1', '47_19', '18_20', '44_4', '7_1', '17_6', '10_8', '10_10', '42_19', '18_1', '43_6', '23_11', '27_10', '8_15', '43_17', '50_12', '54_21', '48_13', '38_11', '56_21', '2_16', '41_7', '24_9', '45_3', '49_19', '11_1', '58_24', '45_19', '37_2', '29_4', '32_5', '24_4']
# # 298：
# ['1_17', '2_20', '3_21', '4_3', '5_18', '6_14', '7_1', '8_8', '9_20', '10_8', '10_28', '11_1', '12_1', '13_1', '14_3', '15_7', '16_12', '17_19', '18_1', '19_25', '20_10', '21_23', '22_22', '23_11', '23_21', '24_9', '25_22', '26_23', '27_21', '28_19',  '29_4', '30_11', '31_13', '32_22', '33_29', '34_4', '35_21', '36_18', '37_2', '37_14', '38_22', '39_20', '40_19', '41_18', '42_19', '43_6', '44_7', '45_3', '46_19', '47_25', '48_6', '49_19', '50_17', '51_19', '52_24', '53_21', '54_25', '55_20', '56_21', '57_23', '58_24', '59_18']
#
# # 大
# ['18_20', '5_6', '45_19', '54_21', '17_6', '32_5', '38_11', '9_18', '50_12',
#  '24_4', '29_20', '30_15', '7_10', '28_11', '21_7', '34_12', '43_17', '44_4',
#  '2_16', '31_6', '41_7', '36_7', '33_12', '12_16', '14_15', '40_12', '16_7',
#  '11_16', '20_23', '55_14', '27_10', '15_22', '23_16', '8_15', '48_13', '13_11',
#  '10_10', '19_17', '47_19', '23_2']
if __name__ == '__main__':
    print(HexToRGB("#b91313"))
    # forcePlotIndex()
    # forcePlot_select_residue_pocket(0)
    # find_2acu_diff()
    # find298_300()
    # find_same_time()
    find_DHA_same_residue()