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
import pandas as pd


def csvAppend(filepath):
    csv1 = pd.read_csv(f"{filepath}\\2acu_attribute.csv",header=0)
    # csv1 = pd.read_csv('F:/BaiduNetdiskDownload/export2000_shuxing.csv')
    sheet1 = pd.DataFrame(csv1)
    sheet2 = pd.read_csv(f"{filepath}\\2acu_2d.csv",header=0)
    sheet2 = pd.DataFrame(sheet2)
    sheet1.insert(sheet2.shape[1], 'x', 0)
    sheet1.insert(sheet2.shape[1], 'y', 0)
    # sheet2 = pd.DataFrame(csv2)
    len1 = len(sheet1)
    # str1 = sheet1.loc[1,'frameInfo'].replace('[','')
    # str1 = sheet1.loc[1,'frameInfo'].replace(']','')
    # str1 = sheet1.loc[1,'frameInfo'].replace('\\n,','\n')
    for i in range(len1):
        sheet1.loc[i, 'spheres'] = sheet1.loc[i, 'spheres'].replace('\'', '')
        sheet1.loc[i, 'residueID'] = sheet1.loc[i, 'residueID'].replace('\'', '')
        sheet1.loc[i, 'residueID'] = sheet1.loc[i, 'residueID'].replace('{', '[')
        sheet1.loc[i, 'residueID'] = sheet1.loc[i, 'residueID'].replace('}', ']')
        sheet1.loc[i,'frame_pocket'] = sheet1.loc[i,'frame_pocket'].replace('frame_pocket','')
        sheet1.loc[i, 'frameInfo'] = sheet1.loc[i, 'frameInfo'].replace('[', '')
        sheet1.loc[i, 'frameInfo'] = sheet1.loc[i, 'frameInfo'].replace(']', '')
        sheet1.loc[i, 'frameInfo'] = sheet1.loc[i, 'frameInfo'].replace('\\n', '\n')
        sheet1.loc[i, 'frameInfo'] = sheet1.loc[i, 'frameInfo'].replace(', ', '')
        sheet1.loc[i, 'frameInfo'] = sheet1.loc[i, 'frameInfo'].replace('\'', '')
        sheet1.loc[i, 'pocketInfo'] = sheet1.loc[i, 'pocketInfo'].replace('[', '')
        sheet1.loc[i, 'pocketInfo'] = sheet1.loc[i, 'pocketInfo'].replace(']', '')
        sheet1.loc[i, 'pocketInfo'] = sheet1.loc[i, 'pocketInfo'].replace('\'', '')
        sheet1.loc[i, 'pocketInfo'] = sheet1.loc[i, 'pocketInfo'].replace('\\n', '\n')
        sheet1.loc[i, 'pocketInfo'] = sheet1.loc[i, 'pocketInfo'].replace(', ', '')

        framePocket = sheet1.loc[i, 'frame_pocket']
        # print(framePocket,'frame_pocket=="'+framePocket+'"',sheet1.query('frame_pocket=="'+framePocket+'"')['x'])
        sheet1.loc[i, 'x'] = sheet2.query('frame_pocket=="' + framePocket + '"')['x'].iloc[0]
        sheet1.loc[i, 'y'] = sheet2.query('frame_pocket=="' + framePocket + '"')['y'].iloc[0]
    sheet1.to_csv(f"{filepath}\\2acu_merge.csv",index=None)
    # sheet1.to_csv('GPX4_2000_POCKET.csv',index=None)
# csvAppend(1,1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=str, default=None)
    # parser.add_argument('--filepath1', type=str, default=None)
    # parser.add_argument('--bb', type=int, default=32)
    args = parser.parse_args()
    # csvAppend(args.filepath)
    csvAppend(f'D:\\研究生二年级\\分子动力学课题\\Github-PocketSCP')

    # print(sys.argv)
    # p_center = initial_layout_fun(f"{args.filepath1}\\output_1_out\\pockets\\*.pdb")
    # print("质心坐标：", p_center)
    # points_3d = layout_3d(f"{args.filepath1}")
    # layout_2d(points_3d, p_center)