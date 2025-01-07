import rmsd
import os
filenames = os.listdir(r'F:\proj\dataset\生物分子数据集\DHA\2000_pdb\2000')
lens = len(filenames)
prePath = 'F:\\proj\\dataset\\生物分子数据集\\DHA\\2000_pdb\\2000\\'
bestItem = None
minRMSD = 9999
sumRMSD = 0
x = []
y = []
z = []
for i in range(lens):
    sumRMSD = 0
    for j in range(lens):
        sumRMSD += float(os.popen('calculate_rmsd '+ prePath + filenames[i] + ' ' + prePath + filenames[j]).read())
    if minRMSD > sumRMSD:
        minRMSD = sumRMSD
        bestItem = i
print(minRMSD,filenames[bestItem])
