import math

from util import message as ru
from util import mongodbUtil
from util.alphabetUtils import random_alphabets

dbname = mongodbUtil.DBNAME  # 数据库名
dbname_pocket = mongodbUtil.DBNAME_POCKET  # pocket表明


# 生成矩阵
def generaMatrix(k):
    m = []
    for i in range(k):
        n = []
        for j in range(k):
            n.append({"len": 0, "frame_pocket": ""})
        m.append(n)
    return m

# sphere_pocket {帧_口袋:内壁原子}
# 内壁原子集合和所在帧_口袋之间映射
def spheres_pocket_process(params):
    d = dict()
    for k in params.keys():
        for v in params[k]:
            if str(v) not in d.keys():
                d[str(v)] = set()
            d[str(v)].add(k)
    return d


# 通过内壁原子返回所在口袋编号

def process_spheres(sphere_pocket, s):
    """
    :param sphere_pocket: 内壁原子与口袋的映射
    :param s:   内壁原子
    :return:    口袋序列
    """
    pocket_set = set()
    for s1 in s:
        # 取 并集
        pocket_set = pocket_set | sphere_pocket[str(s1)]

    return ",".join([str(x) for x in list(pocket_set)])


# 通过内壁原子进行计算
# 生成N*N的记录矩阵；
# 查询数据库，获取每一组数据中的内壁原子以及它们的频次；
# 将查询结果按照给定的簇进行分组，生成包含节点名称、内壁原子编号、频次等信息的clusters列表；
# 计算每个簇所占比例以及外围圆弧的弧度；
# 计算每个簇之间的内部弧线以及它们的弧度；
# 根据计算结果生成弦图所需的数据结构。

def chordPlotIndex(param):
    # print('口袋集',param)
    """
        弦图信息查询
    :param param:  {padAngle:0.1, frame_pocket:[[]]}  # padAngle:间隔角度(弧度)，frame_pocket:传入不同的簇
    :return:
    """
    if param is None:
        return ru.false_message("空参")
    pad_angle = param["padAngle"]  # 间隔角度

    # 生成N*N的矩阵
    matrix = generaMatrix(len(param["frame_pocket"]))  # 生成记录矩阵
    max_num = 0  # 记录返回最大值
    con = mongodbUtil.mongo_conn()
    clusters = []  # 每一簇的数据
    count = 0
    atom_count = 0  # 每组数据中内壁原子数量
    # 每个口袋中的内壁原子
    sphere_pocket = {}
    for frame in param["frame_pocket"]:
        frame_set = set()  #
        frame_dict = {}
        for data in con[dbname][dbname_pocket].find({
            "frame_pocket": {
                "$in": frame
            }}, {
            "_id": 0,
            "spheres": 1,
            "colorLabel": 1,
            "frame_pocket": 1
        }):  # 查询出的几组数据
            #  sphere_pocket {帧_口袋:内壁原子数组}
            sphere_pocket[data["frame_pocket"]] = data["spheres"]
            # 遍历 内壁原子数组  d是每个原子序列号
            for d in data["spheres"]:
                if d not in frame_set:
                    frame_dict[str(d)] = 0
                    # 帧_口袋 的 原子集合
                    frame_set.add(d)
                # 某个原子出现次数
                frame_dict[str(d)] += 1
                if max_num < frame_dict[str(d)]:
                    max_num = frame_dict[str(d)]
        # 某个口袋的原子总数
        atom_count += len(list(frame_set))
        # node:节点名称，frame_set:该节点原子编号，frame_dict:该节点原子出现频次，atomNum:该节点原子数量
        clusters.append({
            "node": random_alphabets(count),  # node编号
            "frame_set": list(frame_set),  # 有哪些内壁原子
            "frame_pocket": ",".join(frame),  # 该簇中选中的pocket
            "frame_dict": frame_dict,  # 内壁原子频次
            "atomNum": len(list(frame_set))
        })  # 几组数据
        count += 1
    # 内壁原子与口袋的映射，即 内壁原子: {所在口袋} #同一个内壁原子可能存在于不同编号的口袋中
    sphere_pocket = spheres_pocket_process(sphere_pocket)
    '''
        out arcs 
        每个环的长度
    '''
    # print(atom_count)
    temp_out_arcs = []  # 外围圆弧弧度
    start_angle = 0
    for i in range(len(clusters)):  # 每部分占比
        temp = math.pi * 2 * clusters[i]["atomNum"] / atom_count
        temp_out_arcs.append({
            "startAngle": start_angle,
            "endAngle": start_angle + temp - pad_angle,
            "index": i,
            "v": clusters[i]["atomNum"]
        })
        start_angle += temp

    '''
        end arcs 
    '''
    # print(out_arcs_temp)
    '''
        inner arc percentage
    '''
    out_arcs = []  # 外环弧线
    for i in range(len(clusters)):
        s = set()  # 当前节点所有交集原子
        row_count = 0  # 每行数据总和
        for j in range(len(clusters)):
            if i == j:
                continue
            #     求两簇空腔数据的交集
            s_temp = set(clusters[i]["frame_set"]) & set(clusters[j]["frame_set"])
            # s 与 s_temp 取并集
            s = s.union(s_temp)
            #
            matrix[i][j] = {"len": len(list(s_temp)), "frame_pocket": process_spheres(sphere_pocket, s)}
            row_count += matrix[i][j]["len"]
        clusters[i]["unionAtomNum"] = len(list(s))  # 表示所有有交集的原子
        temp_start_angle = temp_out_arcs[i]["startAngle"]  # 每个行的开始弧度
        temp_angle = temp_out_arcs[i]["endAngle"] - temp_out_arcs[i]["startAngle"]
        # 计算每行弧的值
        for j in range(len(clusters)):
            # print('clusters[i]["unionAtomNum"] : + ', clusters[i]["unionAtomNum"], '  clusters[i]["atomNum"] : ', clusters[i]["atomNum"],
            #       "  matrix[i][j] : ", matrix[i][j], " row_count : ", row_count, " temp_angle : ", temp_angle)
            if row_count != 0:
                matrix[i][j] = {
                    "startAngle": temp_start_angle,
                    "endAngle": temp_start_angle + clusters[i]["unionAtomNum"] / clusters[i]["atomNum"] * matrix[i][j]["len"] / row_count * temp_angle,
                    "index": i,
                    "subindex": j,
                    "frame_pocket": matrix[i][j]["frame_pocket"],
                    "v": matrix[i][j]["len"]
                }
            else:
                # 如果与其他簇没有交集，则该段均为灰色
                matrix[i][j] = {
                    "startAngle": temp_start_angle,
                    "endAngle": temp_start_angle,
                    "index": i,
                    "subindex": j,
                    "frame_pocket": matrix[i][j]["frame_pocket"],
                    "v": matrix[i][j]["len"]
                }
            temp_start_angle = matrix[i][j]["endAngle"]
        out_arcs.append({
            "startAngle": temp_out_arcs[i]["startAngle"],
            "endAngle": matrix[i][j]["endAngle"],
            "v": clusters[i]["unionAtomNum"],
            "frame_pocket": clusters[i]["frame_pocket"],
            "index": i,
            "colorIndex": i,
            "class": "arc_" + str(i)
        })  # " 进行赋值颜色 "
        out_arcs.append({
            "startAngle": matrix[i][j]["endAngle"],
            "endAngle": temp_out_arcs[i]["endAngle"],
            "v": clusters[i]["atomNum"] - clusters[i]["unionAtomNum"],
            "frame_pocket": clusters[i]["frame_pocket"],
            "colorIndex": i,
            "color": "gray"
        })
    '''
        end
    '''
    # print("outArc : ", out_arcs)
    '''
        start ribbon
        中间的带状图
    '''
    ribbons = []
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            ribbons.append({
                "source": matrix[i][j],
                "target": matrix[j][i],
                # "frame_pocket": matrix[j][i]["frame_pocket"],
                "class": "arc_" + str(i) + " arc_" + str(j),  # ribbon 中设置class
            })
    '''
        end ribbon
    '''
    # print(ribbons)
    # print("ribbons : ", ribbons)
    '''
        start bar 每个弧上的柱状图
        表示出现某个频次的数量
    '''
    arc_bar = []
    frequency = 0  # 表示
    for i in range(len(clusters)):
        arc_line = {}
        for key in clusters[i]["frame_dict"].keys():
            # print(key)
            if str(clusters[i]["frame_dict"][key]) not in arc_line.keys():
                arc_line[str(clusters[i]["frame_dict"][key])] = 0
            arc_line[str(clusters[i]["frame_dict"][key])] += 1
        temp_keys = list(arc_line.keys())
        temp_keys.sort()  # 排序后的列表
        pad = (temp_out_arcs[i]["endAngle"] - temp_out_arcs[i]["startAngle"]) / len(temp_keys)  # 间距
        start_angle = temp_out_arcs[i]["startAngle"]
        for temp_key in temp_keys:
            arc_bar.append({
                "startAngle": start_angle,
                "endAngle": start_angle + pad,
                "v": arc_line[temp_key],
                "flag": temp_key,
                "class": str(i) + "_" + str(j) + " arc_" + str(i)  # 外部柱状图class
            })
            frequency = max(arc_line[temp_key], frequency)
            start_angle += pad
            # print(arc_line[temp_key])
        # print(temp_keys)
        # temp_out_arcs[i]
    # print(frequency, arc_lines)
    # print("arc_bar ", arc_bar)
    # 对位置进行计算
    # print(frequency)
    # print("ribbons ", ribbons)
    '''
        end bar 每个弧上的柱状图
    '''


    con.close()
    return ru.success_message({
        "arcs": out_arcs,  # 外弧线
        "ribbons": ribbons,  # 内部关系连线
        "clusters": clusters,  # 所有节点数据
        "arc_bar": arc_bar,  # # 外部柱状图
        "max_frequency": frequency,  # 出现最大频次
        "max_num": max_num
    })


if __name__ == '__main__':
    print('chord')
    # 表示四簇数据
    # print(chordPlotIndex({
    #     "padAngle": 0.02,
    #     "frame_pocket": [
    #         ["76_4", "49_4", "47_5", "65_4", "2_5", "63_2", "15_8", "86_7", "7_9", "72_5", "22_5", "79_5", "11_4", "12_6", "82_5", "85_6", "28_6", "39_6", "18_6", "66_5", ],
    #         ["83_6", "95_8", "52_13", "89_5", "8_8", "4_4", "92_6", "40_9", "7_12", "16_6", "94_6", "91_12", "85_8", "53_10", "24_10", "5_10", "42_8", "84_9", "47_8", "64_10", "75_9", "10_7", "86_3", "71_7", "65_10", "34_10", "26_8",
    #          "15_9", "43_9", "93_8", "37_9", "46_8", "68_10", "88_9", "17_11",
    #          "33_13", "49_12", ],
    #         ["87_2", "93_4", "47_7", "54_9", "72_4", "65_6", "57_5", "6_5", "3_5", "98_8", "24_5", "69_2", "8_5", "90_8", "66_10", "29_7", "43_7", "71_3", "37_7", "91_4", "28_5", "61_4", "88_5", "4_5", "26_4", "59_4", "30_7", ],
    #         ["41_4", "29_5", "74_7", "94_3", "83_4", "65_5", "44_4", "31_10", "35_5", "82_6", "75_6", "1_8", "36_5", "23_4", "58_4", "88_7", "92_3", "4_7", "7_8", "56_7", "63_7", "25_11", "68_4", "70_4", "80_3", "27_4", "51_4", "22_4",
    #          "84_5", "47_4", "11_5", "32_6", ],
    #         ["49_8", "74_9", "93_10", "76_9", "45_8", "41_9", "89_6", "51_9", "87_9", "34_8", ],
    #         ["73_6", "45_4", "99_6", "94_4", "32_8", "62_4", "84_2", "12_5", "63_5", "18_9", "44_10", "86_4", "22_8", "25_9", "21_9", "7_5", "52_5", "31_5", "27_5", "41_10", "10_8", "2_10", "78_5", "17_10", "70_6", "49_7", "38_11", "14_4",
    #          "40_3", "58_7", "97_8", "15_5", "68_5", "16_3", "1_3",
    #          "23_5", "13_4", "5_5", ],
    #         ["22_3", "21_2", "24_3", "39_7", "3_6", "19_12", "49_15", "99_2", "25_3", "66_14", "78_11", "12_12", "60_12", "23_10", "14_11", "30_12", "9_11", "34_14", "98_12", "88_11", "84_13", "74_12", "65_14", "89_13", "87_13", "53_12",
    #          "50_11", "72_12", "77_15", "48_13", "62_11", "97_10", "29_12",
    #          "45_13", "46_10", "92_15", "44_8", "54_12", ]
    #     ]
    # }))
    # print(math.pi)    # 3.141592653589793
