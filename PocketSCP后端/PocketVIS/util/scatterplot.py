import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# 生成示例数据
n_samples = 1000
n_features = 3
n_clusters = 20

# 使用make_blobs生成数据
data, labels = make_blobs(n_samples=n_samples, n_features=n_features, centers=n_clusters, cluster_std=0.6, random_state=42)

# 为了保证在z轴上有重叠，手动调整一些簇的z轴位置
for i in range(n_clusters):
    if i % 2 == 0:
        data[labels == i, 2] += 5  # 增加z轴上的值
    else:
        data[labels == i, 2] -= 5  # 减少z轴上的值

# 将数据分成x, y, z
x, y, z = data[:, 0], data[:, 1], data[:, 2]

# 创建三维散点图
fig = plt.figure(figsize=(18, 6))

ax = fig.add_subplot(131, projection='3d')
scatter = ax.scatter(x, y, z, c=labels, cmap='viridis')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title("3D Scatter Plot")
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
ax.add_artist(legend1)

# 使用PCA降维到二维
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data)

# 绘制PCA降维后的二维散点图
ax2 = fig.add_subplot(132)
scatter2 = ax2.scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap='viridis')
ax2.set_xlabel('PCA Component 1')
ax2.set_ylabel('PCA Component 2')
ax2.set_title("2D Scatter Plot using PCA")
legend2 = ax2.legend(*scatter2.legend_elements(), title="Clusters")
ax2.add_artist(legend2)

# 使用t-SNE降维到二维
tsne = TSNE(n_components=2, random_state=0)
data_tsne = tsne.fit_transform(data)

# 绘制t-SNE降维后的二维散点图
ax3 = fig.add_subplot(133)
scatter3 = ax3.scatter(data_tsne[:, 0], data_tsne[:, 1], c=labels, cmap='viridis')
ax3.set_xlabel('t-SNE Dimension 1')
ax3.set_ylabel('t-SNE Dimension 2')
ax3.set_title("2D Scatter Plot using t-SNE")
legend3 = ax3.legend(*scatter3.legend_elements(), title="Clusters")
ax3.add_artist(legend3)

# 显示图像
plt.tight_layout()
plt.show()
