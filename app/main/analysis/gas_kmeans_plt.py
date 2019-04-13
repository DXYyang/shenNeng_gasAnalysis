def gas_kmeans_pit(dist,list,clusters):
    import matplotlib.pyplot as plt
    from sklearn.manifold import MDS
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    MDS()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # 将1-余弦距离矩阵降维转化为二维数组
    xs, ys = pos[:, 0], pos[:, 1]#所有点在二维图上的坐标
    clusters_name={}
    for index,data in enumerate(list):
        clusters_name[index]=','.join(data[:3])
    import pandas as pd
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters))
    groups = df.groupby('label')
    # 设置绘图
    fig, ax = plt.subplots(figsize=(17, 9))  # 设置大小
    ax.margins(0.05)  # 可选项，只添加 5% 的填充（padding）来自动缩放（auto scaling）。
    # 对聚类进行迭代并分布在绘图上
    # 我用到了 cluster_name 和 cluster_color 字典的“name”项，这样会返回相应的 color 和 label
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
                label=clusters_name[name],
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params(
            axis='x',  # 使用 x 坐标轴
            which='both',  # 同时使用主刻度标签（major ticks）和次刻度标签（minor ticks）
            bottom='off',  # 取消底部边缘（bottom edge）标签
            top='off',  # 取消顶部边缘（top edge）标签
            labelbottom='off')
        ax.tick_params(
            axis='y',  # 使用 y 坐标轴
            which='both',  # 同时使用主刻度标签（major ticks）和次刻度标签（minor ticks）
            left='off',  # 取消底部边缘（bottom edge）标签
            top='off',  # 取消顶部边缘（top edge）标签
            labelleft='off')
    ax.legend(numpoints=1)  # 图例（legend）中每项只显示一个点
    return plt
