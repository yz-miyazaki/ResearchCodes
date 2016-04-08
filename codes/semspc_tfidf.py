#-*- coding: utf-8 -*-

#redsvdに用いる事が可能なスパース行列のフォーマットで単語・文脈行列を保存する


import csv
import math


#文脈中単語が何回出現したかを計算する関数
def count(word, context):
    num = 0
    for c in context:
        if word == c:
            num +=1
    return num



#単語リストの読み込み:wordlist (要素数15000くらい)
#wordlist = ["hello", "world", .......]
f = open('../data/wordlist_30.csv', 'r')
reader = csv.reader(f)
wordlist = reader.next()
f.close()
print len(wordlist)


#文脈行列の読み込み:Ctxtreader:
#リストのリスト形式、入れ子になったリストが一文の単語を保存している
#Ctextreader= [ ["first", "sentence"],
#                       :
#             , ["last", "sentense"] ]
fCtxt = open('../data/context_30.csv', 'r')
Ctxt = list(csv.reader(fCtxt))
fCtxt.close()


#row_semantic_spaceを書き込むファイルのopen
semspc = open('../data/sem_spc_tfidf', 'w')


idx_row = 0


#idfで使う合計文脈数
num_doc = 100000


#出現回数を数え,tf-idf方を施してsemspcに1行毎に書き込んでいく処理
for word in wordlist:
    idx_col = 0
    tmp_row_freq = []
    tmp_row_idx = []
    semspc_row = ""
    num_df = 0


    for col in Ctxt:
        wordfreq = count(word, col)
        if wordfreq != 0:
            tmp_row_idx.append(idx_col) #ある単語が出現した文脈のインデックスを保存
            tmp_row_freq.append(wordfreq) #文脈における単語の出現回数
            num_df = num_df + 1 #Document frequencyの数を１加算
        idx_col += 1


    idf = math.log(num_doc / num_df)


    for idx in range(len(tmp_row_idx)):
        tf = float(tmp_row_freq[idx]) / len(Ctxt[tmp_row_idx[idx]])
        tf_idf = tf * idf
        elem = str(tmp_row_idx[idx]) + ":" + str(tf_idf) + " "
        semspc_row = semspc_row + elem


    semspc_row = semspc_row + "\n"
    semspc.write(semspc_row)


    idx_row = idx_row + 1
    print idx_row


semspc.close()
