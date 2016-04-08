#coding:utf-8
#dilationアルゴリズムを用いて2つの名詞から複合名詞句のベクトル表現を算出するプログラム


import csv
import sys


pass_ = str(sys.argv[1]) + str(sys.argv[2])


#HeadVector,ModifirerVector,lambdaを受け取って、dilationアルゴリズムを用い算出した複合名詞句のベクトル表現を返す関数
def dilation(h, m, l):
    xi = 0
    yi = 0
    mh = 0
    mm = 0
    p = []

#意味空間の作成に間違いがあった時のエラーメッセージ
    if len(h) != len(m):
        print ("vectors length are different. there are something wrong in semantic space.")

    #内積m‥h、m‥mの計算
    for idx in range(len(h)) :
        mh = mh + float(m[idx]) * float(h[idx])
        mm = mm + float(m[idx]) * float(m[idx])

    #名詞句ベクトルの各要素の計算
    for idx in range(len(h)) :
        tmp = (l-1) * mh * float(m[idx]) + mm *float(h[idx])
        p.append(tmp)
    return p


#dilationアルゴリズムの挙動を決定するlambdaパラメータの設定
lmd = int(sys.argv[2]) / 10.0


#gravesらが調査に用いた複合名詞句リストを読み込み、
#2つの単語のリストへ分割 ([[word1, word2], [word3, word4], ...])
f = open("../data/2160_nncomp.txt", "r")
tmp = f.read()
nncomplist = []
tmp = tmp.rstrip().split("\r\n")
for comp in tmp:
    nncomplist.append(comp.split("-"))
f.close()


#意味空間に用いられている単語リストの読み込み
f = open("../data/wordlist_30.csv", "rb")
wordlist =  f.read().rstrip().split(",")
f.close()


#意味空間の読み込み
f = open("../data/semspc_svd.csv", "rb")
semspc = list(csv.reader(f))

#出力先パスの指定，複合句の意味空間の保存，Gravesの評定データを用いる事が出来る複合句の保存
semspc_output_filepass = "../data/results/" + pass_ + "/nncomp_semspc.csv"
complist_output_filepass = "../data/results/" + pass_ + "/nncomplist.csv"

f_nncomp_semspc = open(semspc_output_filepass, "w")
csvw_nnsemspc = csv.writer(f_nncomp_semspc)

f_nncomplist = open(complist_output_filepass, "w")
csvw_complist = csv.writer(f_nncomplist)


#dilationアルゴリズムを用いた実際の計算
for nncomp in nncomplist :
    #もし単語リスト中に存在しない名詞を用いた複合名詞句であれば計算を飛ばす
    if (nncomp[0] not in wordlist) or (nncomp[1] not in wordlist):
        continue

    print nncomp

    idxa = wordlist.index(nncomp[0])
    idxb = wordlist.index(nncomp[1])

    nncomp_vec = dilation(semspc[idxa], semspc[idxb], lmd)
    csvw_nnsemspc.writerow(nncomp_vec)
    nncomp_vec = []

    csvw_complist.writerow(nncomp)


f_nncomp_semspc.close()
f_nncomplist.close()
