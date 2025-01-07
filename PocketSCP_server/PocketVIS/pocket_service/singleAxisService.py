from util import message
from util import mongodbUtil

dbname = mongodbUtil.DBNAME
dbname_pocket = mongodbUtil.DBNAME_POCKET
dbname_edge = mongodbUtil.DBNAME_EDGE
frames = mongodbUtil.FRAMES
def singleAxisIndex(params):
    if params is None:
        return message.false_message("空参")
    conn = mongodbUtil.mongo_conn()
    # subpocketData = []
    collection = conn[dbname][dbname_pocket]
    max_volume = 0  # 体积
    min_volume = 0x7fffffff
    max_hydropscore = -0x7fffffff  # 最大疏水性
    min_hydropscore = 0x7fffffff  # 最小疏水性
    max_totalsasa = -0x7fffffff
    min_totalsasa = 0x7fffffff
    max_polarsasa = -0x7fffffff
    min_polarsasa = 0x7fffffff
    max_apolarsasa = -0x7fffffff
    min_apolarsasa = 0x7fffffff
    max_mlohyden = 50
    min_mlohyden = 0
    max_malspra = -0x7fffffff
    min_malspra = 0x7fffffff
    max_msoacc = -0x7fffffff
    min_msoacc = 0x7fffffff
    max_alalsppro = -0x7fffffff
    min_alalsppro = 0x7fffffff
    max_volumescore = -0x7fffffff
    min_volumescore = 0x7fffffff
    max_propolatoms = -0x7fffffff
    min_propolatoms = 0x7fffffff
    max_alspdensity = -0x7fffffff
    min_alspdensity = 0x7fffffff
    max_alphaspmaxdist = 20
    min_alphaspmaxdist = 0
    max_alphanum = 0
    max_polarityScore = 10  # 极性得分
    min_polarityScore = 0

    data = collection.find({'frame_pocket': {'$in': params['frame_pocket']}},{
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

    # 转化为数组
    result = {}
    volume_arr = []
    polarsasa_arr = []
    apolarsasa_arr = []
    mlohyden_arr = []
    alspdensity_arr = []
    alphaspmaxdist_arr = []
    # 结果返回的格式为 {vol:[[0, 5],[1, 1],[2, 0]], dist:[[0, 5],[1, 1],[2, 0]]}
    # 格式为{属性名:[值]}
    for d in data:
        # 最大体积
        max_volume = max(d["volume"], max_volume)
        min_volume = min(d["volume"], min_volume)
        max_totalsasa = max(d["totalsasa"], max_totalsasa)
        min_totalsasa = min(d["totalsasa"], min_totalsasa)
        max_polarsasa = max(d["polarsasa"], max_polarsasa)
        min_polarsasa = min(d["polarsasa"], min_polarsasa)
        max_apolarsasa = max(d["apolarsasa"], max_apolarsasa)
        min_apolarsasa = min(d["apolarsasa"], min_apolarsasa)
        max_mlohyden = max(d["mlohyden"], max_mlohyden)
        min_mlohyden = min(d["mlohyden"], min_mlohyden)
        max_alspdensity = max(d["alspdensity"], max_alspdensity)
        min_alspdensity = min(d["alspdensity"], min_alspdensity)
        max_alphaspmaxdist = max(d["alphaspmaxdist"], max_alphaspmaxdist)
        min_alphaspmaxdist = min(d["alphaspmaxdist"], min_alphaspmaxdist)

        max_malspra = max(d["malspra"], max_malspra)
        min_malspra = min(d["malspra"], min_malspra)
        max_msoacc = max(d["msoacc"], max_msoacc)
        min_msoacc = min(d["msoacc"], min_msoacc)
        max_alalsppro = max(d["alalsppro"], max_alalsppro)
        min_alalsppro = min(d["alalsppro"], min_alalsppro)
        max_volumescore = max(d["volumescore"], max_volumescore)
        min_volumescore = min(d["volumescore"], min_volumescore)
        max_propolatoms = max(d["propolatoms"], max_propolatoms)
        min_propolatoms = min(d["propolatoms"], min_propolatoms)

        max_alphanum = max(d["alphanum"], max_alphanum)
        # max_polarityScore = max(d["polarityscore"], max_polarityScore)
        # min_polarityScore = min((d["polarityscore"], min_polarityScore))


        volume_arr.append([d['frameID'],d['frame_pocket'], d['volume'],d['volume']/ max_volume])
        polarsasa_arr.append([d['frameID'],d['frame_pocket'], d['polarsasa'],d['polarsasa']/ max_polarsasa])

        apolarsasa_arr.append([d['frameID'],d['frame_pocket'], d['apolarsasa'],d['apolarsasa']/ max_apolarsasa])
        mlohyden_arr.append([d['frameID'],d['frame_pocket'], d['mlohyden'],d['mlohyden']/ max_mlohyden])
        alspdensity_arr.append([d['frameID'],d['frame_pocket'], d['alspdensity'],d['alspdensity']/ max_alspdensity])
        alphaspmaxdist_arr.append([d['frameID'],d['frame_pocket'], d['alphaspmaxdist'],d['alphaspmaxdist']/ max_alphaspmaxdist])

        result["Volume"] = volume_arr
        result["Polar SASA"] = polarsasa_arr
        result["Apolar SASA"] = apolarsasa_arr
        result["Mean local hydrophobic density"] = mlohyden_arr
        result["Alpha sphere density"] = alspdensity_arr
        result["Cent. of mass - Alpha Sphere max dist"] = alphaspmaxdist_arr
        result['frame_num'] = frames
    print(result)#zwz大傻逼,lxf大帅比

    return message.success_message({'singleAxisData': result})

if __name__ == '__main__':
    print('111')
    print(singleAxisIndex({"frame_pocket":["83_6", "95_8", "52_13", "89_5", "8_8", "4_4", "92_6", "40_9", "7_12", "16_6", "94_6", "91_12", "85_8", "53_10", "24_10", "5_10", "42_8", "84_9", "47_8", "64_10", "75_9", "10_7", "86_3", "71_7", "65_10", "34_10", "26_8",
             "15_9", "43_9", "93_8", "37_9", "46_8", "68_10", "88_9", "17_11",
             "33_13", "49_12"]}))