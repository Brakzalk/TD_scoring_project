# -*- coding: utf-8 -*-
import sys


def read_annotation(read_fname="../commons/annotation_setting.txt"):
    '''
    アノテーション定義ファイルを読み込む
    input:
        アノテーション定義テキストファイルのディレクトリ
    output:
        辞書
  '''
    annotation_dic = {}
    g = open(read_fname, 'r')
    for g_line in g:
        g_line = g_line.replace(" ", "")
        if g_line=="" or "#" in g_line or not ":" in g_line:
            continue
        g_word = g_line.split(":")
        annotation_dic[g_word[0]] = g_word[1].replace("\n", "")
    g.close()
    print(annotation_dic)
    return annotation_dic

              


if __name__ == '__main__':
    dic = read_annotation()
    print(str(dic))
