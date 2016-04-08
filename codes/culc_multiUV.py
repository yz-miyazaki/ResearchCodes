#coding:utf-8
#redsvdで出力された3つの行列のうち.Uの行列と.Sの行列の積で意味空間を生成
#出力ファイル名はsemscp_svd.csv

import csv


f = open("../data/semspc.U", "rb")
tmp_semspc = f.read().rstrip().split("\n")
semspc = []
for vec in tmp_semspc:
    vec = vec.rstrip().split(" ")
    semspc.append([float(x) for x in vec])
f.close()


f = open("../data/semspc.S", "rb")
singular = f.read().rstrip().split("\n")
singular = [float(x) for x in singular]
f.close()


f = open("../data/semscp_svd.csv", "w")
writer = csv.writer(f)

for idx_col in range(len(singular)):
    for idx_row in range(len(semspc)):
        semspc[idx_row][idx_col] = semspc[idx_row][idx_col] * singular[idx_col]


writer.writerows(semspc)
