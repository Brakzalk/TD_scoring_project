# -*- coding: utf-8 -*-
import sys
sys.path.append(".")
import add_annotation as adan
import img_format as imf
sys.path.append("../commons/")
import annotation_dic as andc
import enum
import os

# キーコード
# https://tosh914.hatenadiary.org/entry/20121120/1353415648
class Keys(enum.IntEnum):
    ESC = 27
    ZERO = 48
    ONE = 49
    NINE = 57
    HYPHEN = 45 # - ハイフン
    NICO = 94 #^ キャレット
    


def main(data_dir, dic, already_file_read_skip=False):
    '''
    指定されたフォルダの内容を読み込み、アノテーションツールを起動する
    input:
        画像ファイルの存在するディレクトリ
        アノテーション情報のdictionaly
        アノテーションファイルがある画像も読み込むか設定
  '''
    #ディレクトリ読み込み
    files = os.listdir(data_dir)
    for file in files:
        if ".jpg" in file:
            now_data_file = data_dir + "/" + file
            txt_file_path = now_data_file[:-4] + ".txt"
            print(now_data_file)
            print(txt_file_path)
            
            # テキストファイルが存在するか確認
            if not os.path.exists(txt_file_path):
                #飛ばしモードの場合はスキップ
                if already_file_read_skip:
                    continue
                #処理モードの場合はファイル作成
                else:
                    print("Create Image:",txt_file_path)
                    g = open(txt_file_path, 'w')
                    g.write("")
                    g.close()
                    
            #初期化
            moji = "Please InputKey"
            tag = -1
            #終了が押されるまでアノテーションを継続
            while True:
                # キー待ちを行い、アノテーションした場所にタグを付与する
                k = adan.anotation_input(now_data_file, txt_file_path, dic, moji, tag)
                # escキーで次の画像に
                if k == Keys.ESC:
                    break
                # 入力されたキーがアノテーション情報に対応するか(1~9)
                elif k >=Keys.ONE and k <=Keys.NINE:
                    tag = k-Keys.ONE.value #タグの数値から1引いた値にする
                    if str(tag) in dic.keys():
                        moji = dic[str(tag)]
                        print(tag,moji)
                    else:
                        moji = "NotFound:tag_key"
                # ゼロの場合はアノテーション情報全リセット
                elif k==Keys.ZERO:
                    tag = -1
                    moji = "ALL DELETE!!!!!"
                    g = open(txt_file_path, 'w')
                    g.write("")
                    g.close()
                elif k==Keys.HYPHEN:
                    exit()
                elif k==Keys.NICO:
                    print("remove:",now_data_file)
                    os.remove(txt_file_path )
#                    os.remove(now_data_file)
                    break
                else:
                    #オプションを表示
                    tag = -1
                    moji = str(dic)
                    


if __name__ == '__main__':
    data_dir = sys.argv[1]#dir
    files = imf.imglist_get(data_dir)
    imf.imsize_resize(data_dir, files)
    dic = andc.read_annotation()
    main(data_dir, dic ,False)
