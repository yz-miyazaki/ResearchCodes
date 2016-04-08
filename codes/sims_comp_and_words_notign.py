#coding:utf-8
#各複合名詞句に対し意味空間上の全ての単語との類似度を計算
#その際名詞句の構成に用いられている単語との類似度の部分を無視せず(notign)に0で埋める
#出力は行ベクトルの要素がある名詞句がそれぞれの単語に対する類似度であるような行列になる
#計算量膨大注意！


#並列化の為のモジュールとCPU数を図るためのモジュールのインポート
from multiprocessing import Pool, cpu_count
import numpy
import csv
import sys


pass_ = str(sys.argv[1]) + str(sys.argv[2])


#プロセス数をCPU数で決定
num_proc = cpu_count()


#2つのベクトルの受け取りcos類似度を返す関数
def culcsim(wordvec, nncompvec):
    if len(wordvec) != len(nncompvec):
        print ("vectors length are different. there are something wrong in semantic space.")

    v1 = numpy.array(wordvec)
    v2 = numpy.array(nncompvec)

    norm_v1 = numpy.linalg.norm(v1)
    norm_v2 = numpy.linalg.norm(v2)

    dot_v1v2 = numpy.dot(v1, v2)

    if norm_v1 == 0 or norm_v2 == 0:
        return 0

    cosine_simirality = dot_v1v2 / (norm_v1 * norm_v2)

    return cosine_simirality



#ループで全部の類似度の計算を行う関数、同時に合成に用いた単語との類似度計算をif文で弾く
#用いる変数は両方共グローバル変数なので引数がいらない？
def func_roop(idx):
    idx_ign1 = wordlist.index(nncomplist[idx][0])
    idx_ign2 = wordlist.index(nncomplist[idx][1])
    idxb = 0
    simlist = []

    for word in semspc:
        if idxb == idx_ign1:
            simlist.append(0.0)
            idxb = idxb + 1
        elif idxb == idx_ign2:
            simlist.append(0.0)
            idxb = idxb + 1
        else:
            sim = culcsim(word, comp_semspc[idx])
            simlist.append(sim)
            idxb = idxb + 1

    return simlist



#意味空間の読み込み(グローバル変数)
f = open("../data/semspc_svd.csv", "rb")
tmp_semspc = list(csv.reader(f))
semspc = []
for vec in tmp_semspc:
    semspc.append([float(x) for x in vec])
f.close()


#名詞句の意味空間の読み込み（グローバル変数）
nncomp_filepass = "../data/results/" + pass_+ "/nncomp_semspc.csv"
f = open(nncomp_filepass, "rb")
tmp_semspc = list(csv.reader(f))
comp_semspc = []
for vec in tmp_semspc:
    comp_semspc.append([float(x) for x in vec])
f.close()


#意味空間に用いられている単語一覧の取得（グローバル変数）
f = open("../data/wordlist_30.csv", "rb")
wordlist = csv.reader(f)
wordlist = list(wordlist)[0]
f.close()


#用いる複合名詞句の一覧(グローバル変数)
nncomplist_filepass = "../data/nncomplist.csv"
f = open(nncomplist_filepass, "rb")
nncomplist = csv.reader(f)
nncomplist = list(nncomplist)
f.close()


#名詞句の各単語との類似度の出力先
#「名詞句の数　＊　単語の数の行列」となる
output_filepass = "../data/results/" + pass_ + "/sims_nncomp_notign.csv"
f = open(output_filepass, "w")
csvwriter = csv.writer(f)


#メイン関数部分
if __name__ == "__main__":
    num_roop = len(comp_semspc)
    p = Pool()
    simlist_matrix = p.map(func_roop, range(num_roop))

    csvwriter.writerows(simlist_matrix)
    f.close()
