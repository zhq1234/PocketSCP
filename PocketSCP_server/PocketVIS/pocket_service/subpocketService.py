from util import message
from util import mongodbUtil

dbname = mongodbUtil.DBNAME
dbname_pocket = mongodbUtil.DBNAME_POCKET
dbname_edge = mongodbUtil.DBNAME_EDGE
dbname_subpocket = mongodbUtil.DBNAME_SUBPOCKET

def subPocketIndex(params):
    print(params)
    if params is None:
        return message.false_message("空参")
    conn = mongodbUtil.mongo_conn()
    # subpocketData = []
    collection = conn[dbname][dbname_subpocket]
    data = collection.find({'source': {'$in': params["frame_pocket"]}, 'target': {'$in': params["frame_pocket"]}})

    # 转化为数组
    result = []
    for item in data:
        result.append([item['source'], item['target'], item['weight1']])
    # 返回 JSON 格式的数据
    # return result
    # for data in conn[dbname][dbname_subpocket].find({"weight2": 1.0}, {"_id": 0, "id": 0, "source": 1, "target": 1, "weight1": 1, "weight2": 1}):
    #     subpocketData.append(data)
    return message.success_message({'subSimilarity': result})

if __name__ == '__main__':
    print('111')
    print(subPocketIndex({"frame_pocket":["83_6", "95_8", "52_13", "89_5", "8_8", "4_4", "92_6", "40_9", "7_12", "16_6", "94_6", "91_12", "85_8", "53_10", "24_10", "5_10", "42_8", "84_9", "47_8", "64_10", "75_9", "10_7", "86_3", "71_7", "65_10", "34_10", "26_8",
             "15_9", "43_9", "93_8", "37_9", "46_8", "68_10", "88_9", "17_11",
             "33_13", "49_12"]}))