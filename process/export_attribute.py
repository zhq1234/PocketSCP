# 创建一个字典来存储所有的Pocket信息
#把其中的fields5改成4了
import argparse
import  re
import sys

import pandas as pd
def export_attribute( filepath,filepath1):
    pockets = {}
    list_pockets=[]
# total作用计算生成的list_pocket有多少行
    total=0
# data用来装shuxing
    data=[]


# 遍历每个文件
    end=60
    for i in range(1, end):
    # 用filename文件读取每个口袋的属性
        filename = f'{filepath1}\\output_{i}_out\\output_{i}_info.txt'
         # 用filename1文件读取HETATM和ATOM
        filename1 = f'{filepath1}\\output_{i}_out\\output_{i}_out.pdb'



        pocket_id = 0
        with open(filename, 'r') as file:
            lines = file.readlines()
            # print(lines)
            pocket_dict = {}
            for line in lines:
                # print(line)
                if "Pocket" in line:
                    pocket_id += 1
                    total+=1
                    # 把time_pocket写入csv文件
                    time_pocket = str(i) + f'_{pocket_id}'
                    list_pockets.append(time_pocket)
                    # print(time_pocket)
                    pocket_dict = {}
                    pockets[f'{i}_{pocket_id}'] = pocket_dict

                elif ":" in line:
                    key, value = [x.strip() for x in line.split(":")]
                    pocket_dict[key] = float(value)

            # print(pockets[f'frame_pocket{i}_{1}'])
            # print(pockets[f'frame_pocket{i}_{2}'])
        #
        # 1.走到这一步得时候已经知道每个modelxxx文件下有几个口袋了 pocket_id就是
        # if(i==(end-1)):
        #     dict={'pdb_frame':list_pockets}
        #     df=pd.DataFrame(dict)
        #     df.to_csv(f'D:\\研究生一年级\\分子动力学课题\\处理数据\\list_pocket_DhA_20001.csv')


        with open(filename1, 'r') as file1:

            # pocket_info = []
            # print(pocket_id)
            lines = file1.readlines()
            for j in range(1, pocket_id + 1):
                    # print(j)
                    pocket_info = []
                    frame_info = []
                    first=1
                    second=1
                    replacement_number=0
                    for line in lines:
                        if "ATOM" in line:
                            frame_info.append(line);
                        elif "HETATM" in line:
                            replacement_number += 1
                            match = re.search(r'HETATM(\d+)', line)
                            if match:
                                if(replacement_number<10):
                                    line = re.sub(r'HETATM(\d+)', f'HETATM    {replacement_number}', line)
                                elif (replacement_number >= 100):
                                    line = re.sub(r'HETATM(\d+)', f'HETATM  {replacement_number}', line)
                                else:
                                    line = re.sub(r'HETATM(\d+)', f'HETATM   {replacement_number}', line)
                                # re.sub(r'HETATM\s*(\d+)', f'HETATM {replacement_number}', content)
                                # print(line)
                                fields = line.split()
                                # first = fields[5]
                                second = fields[5]
                                if (first != int(second)):
                                    replacement_number = 1
                                    first = int(second)
                                    # print(first)
                                    if (replacement_number < 10):
                                        line = re.sub(r'HETATM(\d+)', f'HETATM    {replacement_number}', line)
                                    elif (replacement_number >= 100):
                                        line = re.sub(r'HETATM(\d+)', f'HETATM  {replacement_number}', line)
                                    else:
                                        line = re.sub(r'HETATM(\d+)', f'HETATM   {replacement_number}', line)
                                # pocket_info.append(line)
                            else :
                                if (replacement_number < 10):
                                    line = re.sub(r'HETATM\s*(\d+)', f'HETATM    {replacement_number}', line)
                                elif (replacement_number >= 100):
                                    line = re.sub(r'HETATM\s*(\d+)', f'HETATM  {replacement_number}', line)
                                else:
                                    line = re.sub(r'HETATM\s*(\d+)', f'HETATM   {replacement_number}', line)
                                # print(line)
                                fields = line.split()
                                second=fields[5]
                                if(first!=int(second)):
                                    replacement_number=1
                                    first=int(second)
                                    if (replacement_number < 10):
                                        line = re.sub(r'HETATM\s*(\d+)', f'HETATM    {replacement_number}', line)
                                    elif (replacement_number >= 100):
                                        line = re.sub(r'HETATM\s*(\d+)', f'HETATM  {replacement_number}', line)
                                    else:
                                        line = re.sub(r'HETATM\s*(\d+)', f'HETATM   {replacement_number}', line)
                            # if(first!=int(second)):
                            #     first=int(second)
                            #     replacement_number=0
                            # print(line)
                            # print(j)
                            if(first==j):
                                # print(j)
                                pocket_info.append(line)
                    pockets[f'{i}_{j}']['pocket_info'] = pocket_info

                    pockets[f'{i}_{j}']['frame_info'] = frame_info

                    # shuxing.append(frame_info)
                    # shuxing.append(pocket_info)
            # print(pockets)
            # print(frame_info)
            for j in range(1,  pocket_id+1):
                # filename2 = f'F:\\share\\2acu\\output_{i}_out\\pockets\\pocket{j}_atm.pdb'
                filename2 = f'{filepath1}\\output_{i}_out\\pockets\\pocket{j}_atm.pdb'
                shuxing = []
                spheres=[]
                residualID=set({})
                with open(filename2, 'r') as file2:
                        for line in file2:
                            fields = line.split()
                            if fields[0] == "ATOM":
                                # print(fields[1])
                                # print(type(fields[1]))
                                spheres.append(int(fields[1]))
                                residualID.add(int(fields[5]))
                pockets[f'{i}_{j}']['spheres'] = spheres
                pockets[f'{i}_{j}']['residualID'] = residualID
                spheres=pockets[f'{i}_{j}']['spheres']
                residualID=pockets[f'{i}_{j}']['residualID']
                score=pockets[f'{i}_{j}']['Score']
                Drug=pockets[f'{i}_{j}']['Druggability Score']
                Number=pockets[f'{i}_{j}']['Number of Alpha Spheres']
                Tsasa=pockets[f'{i}_{j}']['Total SASA']
                Psasa=pockets[f'{i}_{j}']['Polar SASA']
                Asasa=pockets[f'{i}_{j}']['Apolar SASA']
                Volume=pockets[f'{i}_{j}']['Volume']
                Mlhd=pockets[f'{i}_{j}']['Mean local hydrophobic density']
                Masr=pockets[f'{i}_{j}']['Mean alpha sphere radius']
                msocacc=pockets[f'{i}_{j}']['Mean alp. sph. solvent access']
                alalsppro=pockets[f'{i}_{j}']['Apolar alpha sphere proportion']
                Hydro = pockets[f'{i}_{j}']['Hydrophobicity score']
                volumescore=pockets[f'{i}_{j}']['Volume score']
                Polarityscore=pockets[f'{i}_{j}']['Polarity score']
                chargescore=pockets[f'{i}_{j}']['Charge score']
                Propor=pockets[f'{i}_{j}']['Proportion of polar atoms']
                Asd=pockets[f'{i}_{j}']['Alpha sphere density']
                Cent=pockets[f'{i}_{j}']['Cent. of mass - Alpha Sphere max dist']
                Flexi=pockets[f'{i}_{j}']['Flexibility']
                fr_info=pockets[f'{i}_{j}']['frame_info']
                po_info=pockets[f'{i}_{j}']['pocket_info']
                # shuxing.append([f'frame_pocket{i}_{j}',i,j,score,Drug,Number,Tsasa,Psasa,Asasa,Volume,Mlhd,Masr,Massa,Aasp,Hydro,Volumescore,Polarityscore,Propor,Asd,Cent,Flexi,spheres,residualID,fr_info,po_info])
                # shuxing.append(
                #     [ i, j, score, Drug, Number, Tsasa, Psasa, Asasa, Volume, Mlhd, Masr, Massa,
                #      Aasp, Hydro, Volumescore, Polarityscore, Propor, Asd, Cent, Flexi])
                data.append([f'{i}_{j}',i,j,score,Drug,Number,Tsasa,Psasa,Asasa,Volume,Mlhd,Masr,msocacc,alalsppro,Hydro,volumescore,Polarityscore,chargescore,Propor,Asd,Cent,Flexi,spheres,residualID,fr_info,po_info])
                # data.append(shuxing)

# print(data)
    data_col = [
         'frame_pocket',
        'frameID',
        'pocketID',
        'score',
        'drugscore',
        'alphanum',
        'totalsasa',
        'polarsasa',
        'apolarsasa',
        'volume',
        'mlohyden',
        'malspra',
        'msoacc',
        'alalsppro',
        'hydropscore',
        'volumescore',
        'polarityscore',
        'chargescore',
        'propolatoms',
        'alspdensity',
        'alphaspmaxdist',
        'flexibility',
        'spheres',
        'residueID',
        'frameInfo',
        'pocketInfo'
    ]

    # pd.DataFrame(data,columns=data_col).to_csv(f'D:\\研究生二年级\\分子动力学课题\\Github-PocketSCP\\2acu_60_TEST_POCKET.csv',index=False)
    pd.DataFrame(data, columns=data_col).to_csv(f'{filepath}\\2acu_attribute.csv', index=False)



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--filepath', type=str, default = None)
  parser.add_argument('--filepath1', type=str, default=None)
  # parser.add_argument('--bb', type=int, default=32)
  args = parser.parse_args()
  # print(sys.argv)
  export_attribute(args.filepath,args.filepath1)
  # export_attribute('D:\\研究生二年级\\分子动力学课题\\Github-PocketSCP')
