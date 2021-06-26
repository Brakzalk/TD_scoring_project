#! /usr/bin/ python
# -*- coding: utf-8 -*-

#画像を縦横統一するやつ
# あまりに縦長、横長すぎるやつを消去する機能もつける

import sys
import os
from PIL import Image
from PIL import ImageFile
import cv2
#PILが標準設定だとでかい画像を読めないらしいので回避
ImageFile.LOAD_TRUNCATED_IMAGES = True



def imglist_get(dir_path):
    '''
    指定されたディレクトリの画像一覧リストを返す
    input:
        画像ファイルを配置したディレクトリパス
    output:
        ファイル一覧のリスト
  '''
    files = os.listdir(dir_path)
    files = [x for x in files if ".jpg" in x or ".jpeg" in x or ".png" in x or ".bmp" in x]
    return files


def only_jpg_format(dir_path, files, delete_oldimg = True):
    '''
    全画像をjpgにフォーマットする(png,bmp)
    変換前の画像は削除する
    input:
        画像ファイルを配置したディレクトリパス
        画像ファイル一覧
        旧画像の削除可否
    output:
        変換した画像の一覧リスト
  '''
    return_list = []
    files_other = [x for x in files if ".png" in x or ".bmp" in x]
    for nm in files_other:
        old_name = dir_path + "/" + nm
        new_name = dir_path + "/" + nm[:-4]+".jpg"
        img = Image.open(old_name)
        #カラーマップRGBじゃないやつがまじってたときのため
        if img.mode != "RGB":
            img = img.convert("RGB")
        #JPG画像に変換、保存
        img.save(new_name,"JPEG")
        return_list.append(old_name)
        if delete_oldimg:
            print("元画像をremoveしました")
            print(old_name,"→",new_name)
            os.remove(old_name)#png画像は消去

    files_other = [x for x in files if ".jpeg" in x]
    for nm in files_other:
        old_name = dir_path + "/" + nm
        new_name = dir_path + "/" + nm[:-5]+".jpg"
        os.rename(old_name, new_name)

            
    return return_list


def imsize_resize(dir_path, files, width_max=1440, height_max=900):
    '''
    大きすぎる画像サイズを、規定に合わせて調整する
    input:
        画像ファイルを配置したディレクトリパス
        画像ファイル一覧
        最大横幅
        最大縦幅
    output:
        変換した画像の一覧リスト
  '''
    return_list = []
    for nm in files:
        img = cv2.imread(dir_path+"/"+nm)
        height = img.shape[0]
        width = img.shape[1]
        #表示できる画面サイズを超えている時のみ処理
        if height>height_max or width>width_max:
            #高さの超え具合のほうが大きい場合
            if height/height_max > width/width_max:
                height_r = height_max
                width_r  = width * height_max / height
            #横幅の超え具合のほうが大きい場合
            else:
                height_r = height * width_max / width
                width_r  = width_max
            img = cv2.resize(img , (int(width_r), int(height_r)))
            cv2.imwrite(dir_path+"/"+nm, img)
            return_list.append(nm)
    return return_list


if __name__ == '__main__':
    data_path = sys.argv[1]#dir
    files = imglist_get(data_path)
    imsize_resize(data_path, files)

