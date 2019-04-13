from .textprocess import get_txt,cut_sentence,segment
import numpy as np
posdict = get_txt("app/main/sentiment_analysis/data/sentiment_dictionary/positive_negative_dictionary/posdict.txt","alllines")
negdict = get_txt("app/main/sentiment_analysis/data/sentiment_dictionary/positive_negative_dictionary/negdict.txt","alllines")
mostdict = get_txt('app/main/sentiment_analysis/data/sentiment_dictionary/adverb_degree_dictionary/most.txt', 'alllines')
verydict = get_txt('app/main/sentiment_analysis/data/sentiment_dictionary/adverb_degree_dictionary/very.txt', 'alllines')
moredict = get_txt('app/main/sentiment_analysis/data/sentiment_dictionary/adverb_degree_dictionary/more.txt', 'alllines')
ishdict = get_txt('app/main/sentiment_analysis/data/sentiment_dictionary/adverb_degree_dictionary/ish.txt', 'alllines')
insufficientdict = get_txt('app/main/sentiment_analysis/data/sentiment_dictionary/adverb_degree_dictionary/insufficiently.txt', 'alllines')
inversedict = get_txt('app/main/sentiment_analysis/data/sentiment_dictionary/adverb_degree_dictionary/inverse.txt', 'alllines')

def match_senti(word, sentiment_value):
    if word in mostdict:
        sentiment_value*=2.0
    elif word in verydict:
        sentiment_value*=1.5
    elif word in moredict:
        sentiment_value*=1.25
    elif word in ishdict:
        sentiment_value*=0.5
    elif word in insufficientdict:
        sentiment_value*=0.25
    elif word in inversedict:
        sentiment_value*=-1
    return sentiment_value
def change_positive_num(poscount, negcount):
    pos_count=0
    neg_count=0
    if poscount < 0 and negcount >= 0:
        neg_count += negcount - poscount
        pos_count = 0
    elif negcount < 0 and poscount >= 0:
        pos_count = poscount - negcount
        neg_count = 0
    elif poscount < 0 and negcount < 0:
        neg_count = -poscount
        pos_count = -negcount
    else:
        pos_count = poscount
        neg_count = negcount
    return [pos_count, neg_count]
def sumup_sentence_sentiment_score(score_list):
    score_array = np.array(score_list)
    Pos = np.sum(score_array[:,0])
    Neg = np.sum(score_array[:,1])
    AvgPos = np.mean(score_array[:,0])
    AvgNeg = np.mean(score_array[:,1])
    StdPos = np.std(score_array[:,0])
    StdNeg = np.std(score_array[:,1])
    return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]
def single_review_sentiment_score(review):
    single_review_senti_score = []
    cuted_review =cut_sentence(review)
    for sent in cuted_review:
        seg_sent = segment(sent, 'list')
        i = 0
        s = 0
        poscount = 0
        negcount = 0
        for word in seg_sent:
            if word in posdict:
                poscount += 1
                for w in seg_sent[s:i]:
                    poscount = match_senti(w, poscount)
                s= i + 1
            elif word in negdict:
                negcount += 1
                for w in seg_sent[s:i]:
                    negcount = match_senti(w, negcount)
                s = i + 1
            elif word == "！" or word == "!":
                for w2 in seg_sent[::-1]:
                    if w2 in posdict:
                        poscount += 2
                        break
                    elif w2 in negdict:
                        negcount += 2
                        break
            i+= 1
        single_review_senti_score.append(change_positive_num(poscount, negcount))
    review_sentiment_score = sumup_sentence_sentiment_score(single_review_senti_score)
    return review_sentiment_score

