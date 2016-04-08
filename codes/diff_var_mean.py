#coding:utf-8
#算出した類似度行列を用いて，各名詞句に対し，類似度が高い単語の類似度の差分と分散、平均で相関係数を求める
#差分：類似度1位の単語の類似度値　- 類似度n位の単語の類似度値(n:2~51)
#平均：全類似度の平均値
#分散: 類似度上位10個,15個,100個,1000個,全類似度を用いた時のそれぞれの分散値


import csv
import numpy
import sys


#名詞句のベクトル表現の算出アルゴリズムとそのパラメータの値
pass_ = str(sys.argv[1]) + str(sys.argv[2])

#2160個の複合名詞句
f = open("../data/2160_nncomp.txt", "r")
stims = [x.rstrip().split("-") for x in f]
f.close()

#コーパスに現れる単語で作れる名詞句のリスト
nncomplistpass = "../data/nncomplist.csv"
f = open(nncomplistpass, "r")
complist = csv.reader(f)
complist = list(complist)
f.close()

#2160
#gravesの収集した有意味性の平均値
f = open("../data/mean_rate.txt", "r")
rates = [x.rstrip() for x in f]
f.close()

#類似度のリスト
simspass = "../data/results/" +pass_+ "/sims_nncomp_notign.csv"
f = open(simspass, "r")
simlist = numpy.array(list(csv.reader(f))).astype("float")
f.close()

#書き込み先
outputfilepass = "../data/results/" +pass_+ "/diff_var_mean.csv"
f = open(outputfilepass, "w")
csvwriter = csv.writer(f)


num = 0

graves = []
mean = []
diffs = []
vars_1510100ALL = []


#空リストdiffsに一番高い類似度とn番目の類似度の差を追加していく、nは1から51まで
for idx in range(len(stims)):
    if stims[idx] == complist[num]:
        #平均の格納
        mean.append(numpy.average(simlist[num]))

        #降順のソート
        simlist[num] = numpy.sort(simlist[num])[-1::-1]

        #分散の格納
        tmp_var = []
        for i in [10, 50, 100, 1000, len(simlist[0])]:
            tmp_var.append(numpy.var(simlist[num][:i]))
        vars_1510100ALL.append(tmp_var)

        #差分の格納
        tmp_diff = []
        for i in range(150):
            diff = simlist[num][0] - simlist[num][i+1]
            tmp_diff.append(diff)
        diffs.append(tmp_diff)

        graves.append(float(rates[idx]))
        num = num + 1


cor_mean = []
cors_vars = []
cors_diffs = []

mean = numpy.array(mean)
diffs = numpy.array(diffs)
vars_1510100ALL = numpy.array(vars_1510100ALL)
graves = numpy.array(graves)

cor_mean.append(numpy.corrcoef(mean, graves)[0,1])


for idx in range(5):
    col = vars_1510100ALL[:,idx]
    cors_vars.append(numpy.corrcoef(col, graves)[0,1])

for idx in range(150):
    col = diffs[:,idx]
    cors_diffs.append(numpy.corrcoef(col, graves)[0,1])


csvwriter.writerow(["mean:"])
csvwriter.writerow(cor_mean)
csvwriter.writerow(["vars:"])
csvwriter.writerow(cors_vars)
csvwriter.writerow(["diffs:"])
csvwriter.writerow(cors_diffs)
f.close()
