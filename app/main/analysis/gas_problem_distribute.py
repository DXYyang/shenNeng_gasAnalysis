def gas_problem_distribute(k):
    import codecs
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.cluster import KMeans
    # 文档预料 空格连接
    corpus = []
    # 读取预料 一行预料为一个文档
    for line in open('app/main/analysis/tmp/gascut.txt', 'r', encoding='utf-8').readlines():
        corpus.append(line.strip())
    vectorizer = CountVectorizer()
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    from sklearn.metrics.pairwise import cosine_similarity
    dist = 1 - cosine_similarity(vectorizer.fit_transform(corpus))#计算每个文档与其他文档的余弦相似度，1-余弦矩阵为了在二维平面中绘制余弦距离
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    # 打印特征向量文本内容
    resName = "app/main/analysis/tmp/Gas_Result.txt"
    result = codecs.open(resName, 'w', 'utf-8')
    for j in range(len(word)):
        result.write(word[j] + ' ')
    result.write('\r\n\r\n')
    for i in range(len(weight)):
        for j in range(len(word)):
            result.write(str(weight[i][j]) + ' ')
        result.write('\r\n\r\n')
    result.close()
    clf = KMeans(n_clusters=k)
    return {'dist':dist,'word':word,'clf':clf,'weight':weight}