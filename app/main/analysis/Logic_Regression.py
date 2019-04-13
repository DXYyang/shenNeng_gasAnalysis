def Logic_Regression_plot(frame):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(15,15))
    fig.set(alpha=0.2)  # 设定图表颜色alpha参数
    plt.subplot2grid((3, 2), (0, 0))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    frame['sales_well'].value_counts().plot(kind='bar')
    plt.title(u"销售好坏（1为好）")
    plt.ylabel(u"数量")
    plt.subplot2grid((3, 2), (0, 1))
    plt.scatter(frame['sales_well'], frame['month_avg_income'])
    plt.ylabel(u"居民月收入")
    plt.grid(b=True, which='major', axis='y')
    plt.title(u"按月收入看销售好坏 (1为好)")
    plt.subplot2grid((3, 2), (1, 0))
    plt.scatter(frame['sales_well'], frame['district_GDP'])
    plt.ylabel(u"地区GDP")
    plt.grid(b=True, which='major', axis='y')
    plt.title(u"按地区GDP看销售好坏 (1为好)")
    plt.subplot2grid((3, 2), (1, 1))
    plt.scatter(frame['sales_well'], frame['liquid_price'])
    plt.ylabel(u"液化气价格")
    plt.grid(b=True, which='major', axis='y')
    plt.title(u"按液化气价格看销售好坏 (1为好)")
    plt.subplot2grid((3, 2), (2, 0), colspan=2)
    frame['population'].plot(kind='kde')
    plt.xlabel(u"人口数量")
    plt.ylabel(u"密度")
    plt.title(u"人口密度函数")
    plt.legend()
    return plt
def train_data(frame):
    from sklearn import linear_model
    train_df = frame.filter(regex='gas_sales|sales_well|district_.*|population|month_.*|gas_price|liquid_price')
    train_np = train_df.as_matrix()
    y = train_np[:, 0]
    X = train_np[:, 1:]
    clf = linear_model.LogisticRegression(C=1.0, penalty='l1')#C 正则化程度，越小越高,penalty l1正则化 防止过拟合
    clf.fit(X, y)
    return clf