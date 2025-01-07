import math

from util import message
from util import mongodbUtil

dbname = mongodbUtil.DBNAME  # 数据库名
dbname_pocket = mongodbUtil.DBNAME_POCKET  # pocket表明


# 查询平行坐标图数据
def parallelPlotIndex(params: dict):
    """
        根据 frame_pocket 编号进行查询数据
    :param params: 帧_空腔 编号
    :return: 根据 帧_空腔编号查询返回属性信息
    """
    if params is None or params["frame_pocket"] is None:
        return message.false_message("参数为空！")
    conn = mongodbUtil.mongo_conn()
    frame_pocket = []
    """
        frame_pocket: 编号, 
        frameID: 所在帧, 
        volume:体积,  [0,n]
        score: pocket得分, [-1, 1]
        drugscore: 药物性得分, [0,1]
        hydropscore: 疏水性分数, [-n,n]
        alphanum: alpha球体数量,[0,n]
        polarityscore: 极性得分[0,n]
    """
    max_volume = 0  # 体积
    max_hydropscore = -0x7fffffff  # 最大疏水性
    min_hydropscore = 0x7fffffff  # 最小疏水性
    max_totalsasa = -0x7fffffff
    min_totalsasa = 0x7fffffff
    max_polarsasa = -0x7fffffff
    min_polarsasa = 0x7fffffff
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
    min_frame = 0x7fffffff

    # 返回的数据列名称
    column_name = [
        "frameID",  # 帧编号
        "volume",  # 体积
        "score",  # 得分
        "drugscore",  # 药物得分
        "hydropscore",  #
        # "totalsasa",  #
        # "polarsasa",  #
        "mlohyden",  #
        "malspra",  #
        # "msoacc",  #
        "alalsppro",  #
        "volumescore",  #
        "propolatoms",  #
        "alspdensity",  #
        "alphaspmaxdist",  #
        "alphanum",  #
        "polarityscore"  #
    ]
    max_frame = 0
    count = 0
    map_index = {}
    # 过滤列 不显示的列
    for d in conn[dbname][dbname_pocket].find({
        "frame_pocket": {
            "$in": params["frame_pocket"]  # 查询条件范围
        }
    }, {
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
    }):
        # 最大体积
        max_volume = max(d["volume"], max_volume)
        max_hydropscore = max(d["hydropscore"], max_hydropscore)
        min_hydropscore = min(d["hydropscore"], min_hydropscore)
        max_totalsasa = max(d["totalsasa"], max_totalsasa)
        min_totalsasa = min(d["totalsasa"], min_totalsasa)
        max_polarsasa = max(d["polarsasa"], max_polarsasa)
        min_polarsasa = min(d["polarsasa"], min_polarsasa)
        # max_mlohyden = max(d["mlohyden"], max_mlohyden)
        # min_mlohyden = min(d["mlohyden"], min_mlohyden)
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

        max_alspdensity = max(d["alspdensity"], max_alspdensity)
        min_alspdensity = min(d["alspdensity"], min_alspdensity)
        # max_alphaspmaxdist = max(d["alphaspmaxdist"], max_alphaspmaxdist)
        # min_alphaspmaxdist = min(d["alphaspmaxdist"], min_alphaspmaxdist)

        max_alphanum = max(d["alphanum"], max_alphanum)
        # max_polarityScore = max(d["polarityscore"], max_polarityScore)
        # min_polarityScore = min((d["polarityscore"], min_polarityScore))
        max_frame = max(max_frame, int(d["frameID"]))
        min_frame = min(min_frame, int(d["frameID"]))
        frame_pocket.append(d)
        map_index[d["frame_pocket"]] = count
        count += 1
    range_data = {
        "frameID": {"min": min_frame, "max": max_frame},
        "score": {"min": -0.2, "max": 1},
        "drugscore": {"min": 0, "max": 1},
        "volume": {"min": 0, "max": max_volume},
        "hydropscore": {"min": min_hydropscore, "max": max_hydropscore},
        "alphanum": {"min": 0, "max": max_alphanum},
        "totalsasa": {"min": min_totalsasa, "max": max_totalsasa},
        "polarsasa": {"min": min_polarsasa, "max": max_polarsasa},
        "mlohyden": {"min": min_mlohyden, "max": max_mlohyden},
        "malspra": {"min": math.floor(min_malspra), "max": math.ceil(max_malspra)},
        "msoacc": {"min": min_msoacc, "max": max_msoacc},
        "alalsppro": {"min": min_alalsppro, "max": max_alalsppro},
        "volumescore": {"min": min_volumescore, "max": max_volumescore},
        "propolatoms": {"min": min_propolatoms, "max": max_propolatoms},
        "alspdensity": {"min": min_alspdensity, "max": max_alspdensity},
        "alphaspmaxdist": {"min": min_alphaspmaxdist, "max": max_alphaspmaxdist},
        "polarityscore": {"min": min_polarityScore, "max": max_polarityScore}
    }  # 表示各个列的数据范围

    return message.success_message(
        {
            "frame_pocket_data": frame_pocket,
            "rangeData": range_data,
            "columnName": column_name,
            "mapIndex": map_index  # 下标映射
        }
    )


if __name__ == '__main__':
    response_data = parallelPlotIndex(
        {
            "frame_pocket":
                [
                    "20_1", "78_1", "32_3", "63_3", "94_2", "24_8", "68_1", "85_1", "6_2", "89_2", "55_1", "22_11", "90_7", "34_6", "84_7", "77_6", "49_2", "15_1", "86_1", "13_9", "21_4", "37_6", "12_4", "19_5", "54_5", "95_5", "97_6", "57_6", "71_5", "61_6", "72_3", "55_6", "53_7", "33_5", "9_5",
                    "90_5", "87_6", "39_8", "41_4", "98_8", "24_5", "69_2", "8_5", "90_8", "66_10", "29_7", "43_7", "71_3", "37_7", "91_4", "28_5", "61_4", "88_5", "63_4", "99_7", "59_1", "32_5", "98_4", "40_2", "41_5", "15_3", "73_4", "81_3", "46_4", "68_6", "39_5", "52_4", "99_3", "38_7", "74_5",
                    "75_3", "25_5", "84_8", "100_2", "69_7",
                ]
        }
    )

    print(response_data)
