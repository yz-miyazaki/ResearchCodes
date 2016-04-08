#coding: UTF-8
#xmlファイル(BNC)から１０万の文脈を単語のリストとしてcsvファイルに出力するプログラム
#ここでは30以上の単語を持つ段落を文脈とする

import os
import re
import csv
from BeautifulSoup import BeautifulStoneSoup


#コーパスのパスを指定
#現在は存在しません
corpus_loc = "　"


noun = re.compile('hw="(\w*)" pos="SUBST"')
verb = re.compile('hw="(\w*)" pos="VERB"')


#Textsの中のディレクトリ一覧の取得
DirTexts = os.listdir(corpus_loc)


#抽出する文脈の数のインデックス、初期値0、最大値10万
idx = 0
idx_max = 100000


#出力先csvファイルのオープン
fcsv = open('context_30.csv', 'w')
csvWriter = csv.writer(fcsv)


#Texts中のA,B,C.....を回すループ
for dirs in DirTexts:
    dirpass = corpus_loc + dirs + "/"
    files = os.listdir(dirpass)

    #A,B.....の中のA0,A1,.......を回すループ
    for subdir1 in files:
        subdir2 = dirpass + subdir1 + "/"
        xml_files = os.listdir(subdir2)

        for xmls in xml_files:
            xml_filepass = subdir2 + xmls

            f = open(xml_filepass)
            xml_doc = f.read()
            f. close()

            soup = BeautifulStoneSoup(xml_doc)

            pTag = soup.find("p")
            while pTag != None:
                paragraph = str(pTag)
                wordlist = noun.findall(paragraph)
                wordlist = [word for word in wordlist + verb.findall(paragraph) if word != "be"]

                if len(wordlist) > 30:
                    csvWriter.writerow(wordlist)
                    print "len if wordlist is : " + str(len(wordlist))
                    print idx
                    idx +=1

                pTag = pTag.findNext('p')

                if idx == idx_max : break
            if idx == idx_max : break
        if idx == idx_max : break
    if idx == idx_max : break

fcsv.close()
