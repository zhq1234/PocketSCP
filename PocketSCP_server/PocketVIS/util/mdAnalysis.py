import MDAnalysis as mda
import os


def getPDBFromFile(dirName,xtcName,pdbName):
    # 定义要保存pdb文件的文件夹路径
    output_folder = "F:\\proj\\dataset\\test\\uploadFile\\" + dirName + "\\pdb_output"

    # 如果文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取蛋白质轨迹文件
    u = mda.Universe("F:\\proj\\dataset\\test\\uploadFile\\" + dirName + "\\" + pdbName,"F:\\proj\\dataset\\test\\uploadFile\\" + dirName + "\\" + xtcName)
    # print(u.trajectory)

    # 选择蛋白质的氨基酸原子
    protein_atoms = u.select_atoms("protein") # u.select_atoms("protein or resname CLA") 选择蛋白质和残基名为CLA的原子

    # 第一次迭代，保存第一帧的蛋白质坐标
    first_frame_coordinates = protein_atoms.positions.copy()

    # 遍历每一帧并保存为pdb文件
    for ts in u.trajectory:
        # print("ts: ", ts)
        pdb_filename = os.path.join(output_folder,"frame_" + str(ts.frame+1) + ".pdb")
        with mda.Writer(pdb_filename, multiframe=False, bonds=None, n_atoms=protein_atoms.n_atoms) as pdb:
            pdb.write(protein_atoms)

    print('xtc handle finish.')
# # 循环遍历每一帧并保存为单独的 PDB 文件
# for ts in u.trajectory:
#     # 提取当前帧蛋白质的坐标
#     current_frame_coordinates = protein_atoms.positions
    
#      # 计算当前帧与第一帧的蛋白质坐标对齐的变换
#     transformation, rmsd = mda.align_atoms(current_frame_coordinates, first_frame_coordinates)
    
#     # 应用变换到当前帧的所有原子上
#     protein_atoms.rotate(transformation)

#     # # 应用变换到当前帧的所有原子上
#     # u.atoms.translate(-first_frame_coordinates.mean(axis=0))  # 将第一帧的质心移动到原点
#     # u.atoms.rotate(transformation.T)  # 应用对齐的旋转变换
    
#     # 构造输出文件名，例如：frame_00001.pdb
#     pdb_filename = os.path.join(output_folder,"frame_" + str(ts.frame+1) + ".pdb")
#     # output_filename = "frame_{:05d}.pdb".format(ts.frame)
#     # 保存当前帧的结构为 PDB 文件
#     # u.atoms.write(pdb_filename)
#     with mda.Writer(pdb_filename, multiframe=False, bonds=None, n_atoms=protein_atoms.n_atoms) as pdb:
#         pdb.write(protein_atoms)