#coding:utf-8
#全文脈で最低でも計10回出現した単語のみを意味空間に用いる単語として抽出する

import csv


  #csvファイルの読み込み
filename = 'context.csv'

f = open(filename, 'rb')
context = list(csv.reader(f))
f.close()


 #最低出現回数の設定
threshold = 10


 #ワードリスト候補を格納する空リスト、対応する単語の出現回数を記録する空リストの生成
cand_wordlist = []
num_wordfreq = []
wordlist = []

 #進行度合いを表示する為の変数
num = 0


 #以下候補ワードリストを生成する処理
for row in context:

    for word in row:
        if word in cand_wordlist:
            idx = cand_wordlist.index(word)
            num_wordfreq[idx] = num_wordfreq[idx] + 1
        else:
            cand_wordlist.append(word)
            num_wordfreq.append(1)

    num = num + 1
    print num



 #閾値以上回数出現した単語の選出
for idx in range(len(cand_wordlist)):
    if num_wordfreq[idx] >= threshold:
        wordlist.append(cand_wordlist[idx])



 #csvファイルに結果の出力
f = open('wordlist_30.csv', 'ab')
csvWriter = csv.writer(f)
csvWriter.writerow(wordlist)
f.close()



 #単語総数の表示
print "num of candidate words : " + str(len(cand_wordlist))
print "num of words in final wordlist : " + str(len(wordlist))
