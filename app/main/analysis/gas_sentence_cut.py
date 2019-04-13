def read_file_cut():
    import codecs
    import os
    import jieba.analyse
    respath = "app/main/analysis/tmp"
    fileName = "app/main/analysis/data/Original_Gasquestion.txt"
    resName = respath +"/gascut.txt"
    source = open(fileName, 'r', encoding='utf-8')
    if os.path.exists(resName):
        os.remove(resName)
    result = codecs.open(resName, 'w', 'utf-8')
    line = source.readline()
    line = line.rstrip('\n')
    while line != "":
        line = line.encode('utf-8').decode('utf-8')
        seglist = jieba.cut(line, cut_all=False)  # 精确模式
        output = ' '.join(list(seglist))  # 空格拼接
        result.write(output + '\r\n')#\r\n 回车换行
        line = source.readline()
        line = line.rstrip('\n')
    else:
        source.close()
        result.close()