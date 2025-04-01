from PocketVIS.util import message
from PocketVIS.util import mongodbUtil

dbname = mongodbUtil.DBNAME
dbname_pocket = mongodbUtil.DBNAME_POCKET
dbname_edge = mongodbUtil.DBNAME_EDGE
# dbname_subpocket = mongodbUtil.DBNAME_SUBPOCKET
# dbname_subpocket = mongodbUtil.DBNAME_POCKET1


def subPocketIndex(params):
    print(params)
    if params is None:
        return message.false_message("空参")
    conn = mongodbUtil.mongo_conn()
    # subpocketData = []
    collection = conn[dbname][dbname_subpocket]
    # data = collection.find({'source': {'$in': params["frame_pocket"]}, 'target': {'$in': params["frame_pocket"]}})
    data = collection.find()

    # print(data)
    # 转化为数组
    result = []
    residue=set()

    for item in data:
        # result.append([item['source'], item['target'], item['weight1']])
        result.append([item['source'], item['target'], item['weight']])
        residue.add(item['source'])
    # 返回 JSON 格式的数据
    # return result
    # for data in conn[dbname][dbname_subpocket].find({"weight2": 1.0}, {"_id": 0, "id": 0, "source": 1, "target": 1, "weight1": 1, "weight2": 1}):
    #     subpocketData.append(data)
    # print(residue)
    # residue = list(residue)
    # residue = sorted(list(residue))
    residue = sorted(list(residue), key=lambda x: int(x))
    print(residue)
    try:
        return message.success_message({'subSimilarity': result, 'residue': residue})
    except Exception as e:
        print("Error:", e)
        return message.false_message("内部错误")
    # return message.success_message({'subSimilarity': result})
    # return message.success_message({'subSimilarity': result,'residue':residue})

if __name__ == '__main__':
    print('111')
    # print(subPocketIndex({"frame_pocket":["83_6", "95_8", "52_13", "89_5", "8_8", "4_4", "92_6", "40_9", "7_12", "16_6", "94_6", "91_12", "85_8", "53_10", "24_10", "5_10", "42_8", "84_9", "47_8", "64_10", "75_9", "10_7", "86_3", "71_7", "65_10", "34_10", "26_8",
    #          "15_9", "43_9", "93_8", "37_9", "46_8", "68_10", "88_9", "17_11",  "33_13", "49_12"]}))
    print(subPocketIndex({"frame_pocket": ["1", "2", "3", "4", "5", "6", "7"]}))
