import pandas as pd

print('文件读取中....')
sheet1 = pd.read_csv('F:\\BaiduNetdiskDownload\\allec_2500_2d_1484.csv')
sheet1 = pd.DataFrame(sheet1)
sheet2 = pd.read_csv('F:\\keyan\\论文\\分子可视化项目\\PocketVIS\\util\\5ht1b_2500_POCKET.csv')
sheet2 = pd.DataFrame(sheet2)
print('文件读取完成')
print('开始操作...')
sheet2.insert(sheet2.shape[1],'x',0)
sheet2.insert(sheet2.shape[1],'y',0)
len1 = len(sheet1)
print(len)
len2 = len(sheet2)
print(len1)
for i in range(len2):
    framePocket = sheet2.loc[i,'frame_pocket']
    # print(framePocket,'frame_pocket=="'+framePocket+'"',sheet1.query('frame_pocket=="'+framePocket+'"')['x'])
    sheet2.loc[i,'x'] = sheet1.query('frame_pocket=="'+framePocket+'"')['x'].iloc[0]
    sheet2.loc[i, 'y'] = sheet1.query('frame_pocket=="' + framePocket + '"')['y'].iloc[0]

# for i in range(len1):
#     framePocket = sheet1.loc[i,'frame_pocket']
#     for j in range(len2):
#         if sheet2.loc[j,'frame_pocket'] == framePocket:
#             sheet2.loc[i,'volume'] = sheet2.loc[j,'volume']
#             break
print('操作结束')
# str = '1000_10'
# temp = sheet1.query('frame_pocket=="'+str+'"')['x']




# for i in range(len(sheet1)):
#     sheet1.loc[i,'x'] = int(sheet1.loc[i,'x'])
#     sheet1.loc[i, 'y'] = int(sheet1.loc[i, 'y'])

sheet2.to_csv('F:\\BaiduNetdiskDownload\\5ht1b_2500_POCKET_1.csv',index=None)