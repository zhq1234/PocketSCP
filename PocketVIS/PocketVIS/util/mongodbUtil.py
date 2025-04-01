from pymongo import MongoClient

# 暂定数据库名称为
DBNAME = "DHA"
# DBNAME = "DhA_5000"
# DBNAME = "GPX4_100"
# DBNAME = "2acu"
# DBNAME = "GPX4_NEW"
# DBNAME = "3a"
FRAMES = 1000
# 暂定pocket数据表名为
DBNAME_POCKET = DBNAME + "_1000_POCKET"
# DBNAME_POCKET = "2acu_TEST_POCKET_new"
# DBNAME_POCKET = "P38_merge_new"
# DBNAME_POCKET = "GPX4_1000_vacant_merge"
# DBNAME_POCKET = "TEST_POCKET1"
# DBNAME_POCKET = "gpx4_file1"
# DBNAME_POCKET = "GPX4_1000_vacant_merge_new_revise"
# DBNAME_POCKET = "DHA_1000_POCKET"
# DBNAME_POCKET = "GPX4_100_POCKET"
# DBNAME_POCKET = "GPX4_1000_POCKET"
# DBNAME_POCKET = "GPX4_1000_vacant_merge_new"
# DBNAME_POCKET = "2acu_merge"
DBNAME_POCKET1 = "mdnew_subpocket"
# 蛋白质分子结构数据表名为
DBNAME_ATOM = DBNAME + "_ATOM"
# 蛋白质帧
DBNAME_FRAME = DBNAME + "_FRAME"
# 残基信息
DBNAME_RESIDUE = DBNAME + "_RESIDUE"
# 力导向图边关系
DBNAME_EDGE = DBNAME + "_EDGE"
# 力导向图节点
DBNAME_NODE = DBNAME + "_1000_NODE"
# 判斷子口袋的相似度
DBNAME_SUBPOCKET = DBNAME + "_SUBPOCKET"

def mongo_conn() -> MongoClient:
    return MongoClient('127.0.0.1', 27017)
# 10.53.21.212  0.0

