import xlrd
import jieba
import jieba.posseg
jieba.load_userdict('app/main/sentiment_analysis/data/userdict.txt')
def get_txt(filepath,para):
    if para=='alllines':
        txt_file1=open(filepath,'r',encoding='utf8')
        txt_tmp1=txt_file1.readlines()
        txt_tmp2=''.join(txt_tmp1)
        txt_data1=txt_tmp2.split('\n')
        txt_file1.close()
        return txt_data1
    elif para=='oneline':
        txt_file2=open(filepath,'r',encoding='utf8')
        txt_tmp=txt_file2.readline()
        txt_data2=txt_tmp
        txt_file2.close()
        return txt_data2
def segment(sentence,para):
    if para=='str':
        seg_list=jieba.cut(sentence)
        seg_result=' '.join(seg_list)
        return seg_result
    elif para=='list':
        seg_list2=jieba.cut(sentence)
        seg_result2=[]
        for w in seg_list2:#generator 转list
            seg_result2.append(w)
        return seg_result2
def cut_sentence(words):
    start = 0
    i = 0
    token = 'none'
    cutted_sentence = []
    punt_list = ',.!?;~，。！？；～… '
    for word in words:
        if word not in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
        elif word in punt_list and token in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
        else:
            cutted_sentence.append(words[start:i+1])
            start = i+1
            i += 1
    if start < len(words):
        cutted_sentence.append(words[start:])
    return cutted_sentence

