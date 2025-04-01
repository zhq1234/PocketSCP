import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Bio import PDB
import glob
import pandas as pd
from scipy.spatial import distance
from sklearn.cluster import KMeans
import re
import math
import os
import argparse
print("当前工作目录：",os.getcwd())

def initial_layout_fun(file_path):
    # file_path = "E:/data/100/model.14_out/pockets/*.pdb"
    center_dist = {}
    frame_id=0 
    pdb_files = glob.glob(file_path)
    # frame_id = re.findall(r'\d+', pdb_outfile)[-1]
    pocket_id = 0
    c_num = 0
    for pdb_file in pdb_files:
        pocket_id = pocket_id+1
        c_num = c_num+1
        # 创建 PDB 解析器对象
        parser = PDB.PDBParser(PERMISSIVE=True, QUIET=True)
        # 解析 PDB 文件
        structure = parser.get_structure("protein", pdb_file)

        """计算蛋白质结构的质心坐标"""
        coords_sum = np.zeros(3)
        total_atoms = 0
        for atom in structure.get_atoms():
            coords_sum += atom.coord
            total_atoms += 1
        
        frame_pocket = str(frame_id)+"_"+str(pocket_id)
        center_dist[frame_pocket]= coords_sum / total_atoms

  
    # 手动选择的初始点
    initial_points = np.array(list(center_dist.values()))  # 示例初始点

    sums=np.zeros(3)
    total_num=0
    for point in initial_points:
        total_num=total_num+1
        sums=sums+point
        # 投影中心
        p_center = sums/total_num

    # 返回初始布局（口袋的三维坐标）和质心（口袋坐标的质心）
    return p_center

def layout_3d(folder_path):
    # folder_path = "E:/data/2000/"
    pdb_outfiles = glob.glob(folder_path+"\\*_out")
    center_dist = {}
    colors_dist= {}
    frame_id=0 
    # 口袋集数量
    max=0
    c_num = 22
    # 初始布局
    for pdb_outfile in pdb_outfiles:
        pdb_files =[]
        frame_id = re.findall(r'\d+', pdb_outfile)[-1]
        pocket_path = pdb_outfile+"/pockets"
        pdb_files = glob.glob(pocket_path+"/*.pdb")
        pocket_id = 0
        for pdb_file in pdb_files:
            pocket_id = (int)(re.findall(r'\d+', pdb_file)[-1])
            # 创建 PDB 解析器对象
            parser = PDB.PDBParser(PERMISSIVE=True, QUIET=True)
            # 解析 PDB 文件
            structure = parser.get_structure("protein", pdb_file)

            """计算蛋白质结构的质心坐标"""
            coords_sum = np.zeros(3)
            total_atoms = 0
            for atom in structure.get_atoms():
                coords_sum += (atom.coord * 1)
                total_atoms += 1
       
            frame_pocket = str(frame_id)+"_"+str(pocket_id)

      
            if( pocket_id > max):
                max = pocket_id

            # 将质心坐标及其颜色存储到 center_dist 字典中
            center_dist[frame_pocket] = {
                "coords": coords_sum / total_atoms,
                # "color": color
            }
    # center_dist[frame_pocket]= coords_sum / total_atoms
    return center_dist


def layout_2d(points_3d, p_center):
    # 从 points_3d 字典中提取 3D 坐标
    points=[value['coords'] for value in points_3d.values()]
  

    # 计算投影角度
    # 已知正切值
    tangent_value = p_center[2] / math.sqrt(p_center[0]**2 + p_center[1]**2)
    # 计算余弦值
    cosine_value = 1 / math.sqrt(1 + tangent_value**2)
    # 计算正弦值
    sine_value = tangent_value * cosine_value
    # 定义一个投影矩阵
    # m_matrix = np.array([
    #     [1, 0, 0],
    #     [0, cosine_value, -sine_value],
    #     [0, sine_value, cosine_value]
    # ])
    m_matrix = np.array([
        [cosine_value, -sine_value,0],
        [sine_value, cosine_value,0],
        [0, 0, 0],
    ])


    # 将3D坐标投影到2D平面
    points_2d = {}
    for key,value in points_3d.items():
        points_2d[key] = np.dot(value['coords'], m_matrix) +  p_center


    data = []
    for node in points_2d:
        node_name = node
        x, y, z = points_2d[node]
        data.append({
            'frame_pocket': node_name,
            'x': x,
            'y': y,
        })

    # 将数据转换为 DataFrame
    df_nodes = pd.DataFrame(data)

    # 将 DataFrame 导出为 CSV 文件
    output_file = f'{args.filepath}\\2acu_2d.csv'
    df_nodes.to_csv(output_file, index=False, encoding='utf-8')
    print(f"节点信息已导出到 {output_file}")
       

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=str, default=None)
    parser.add_argument('--filepath1', type=str, default=None)
    # parser.add_argument('--bb', type=int, default=32)
    args = parser.parse_args()
    # print(sys.argv)
    p_center = initial_layout_fun(f"{args.filepath1}\\output_13_out\\pockets\\*.pdb")
    print("质心坐标：", p_center)
    points_3d = layout_3d(f"{args.filepath1}")
    layout_2d(points_3d, p_center)

# E:/vmShare/GPX4_out/frame_15_out/pockets/*.pdb


