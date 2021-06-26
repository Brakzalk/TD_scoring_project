# -*- coding: utf-8 -*-
import numpy as np
import sys
import os
import cv2

class PointList():
    '''
    格頂点の位置を記録するクラス
    npoints:格納可能な頂点数
    plist:タプル　頂点番号,xyの2軸情報[x,y]
    pos:現在格納中の頂点数
  '''
    def __init__(self, npoints):
        self.npoints = npoints
        self.ptlist = np.empty((npoints, 2), dtype=int)
        self.pos = 0
    #plistにxy座標を追加
    def add(self, x, y):
        if self.pos < self.npoints:
            self.ptlist[self.pos, :] = [x, y]
            self.pos += 1
            return True
        return False


def onMouse(event, x, y, flag, params):
    '''
  マウスが配置された時のイベントを定義
  '''
    wname, img, ptlist, g, tag,moji = params
    # マウスが移動した時、マウス位置を線でわかりやすくする
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが移動したときにx線とy線を更新する
        img_now_mouse = np.copy(img)
        h, w = img_now_mouse.shape[0], img_now_mouse.shape[1]
        cv2.line(img_now_mouse, (x, 0), (x, h - 1), (255, 0, 0))
        cv2.line(img_now_mouse, (0, y), (w - 1, y), (255, 0, 0))
        cv2.imshow("path:"+wname, img_now_mouse)
    # クリックされた時、アノテーションファイルに追記する
    if event == cv2.EVENT_LBUTTONDOWN:
        #plistに追加できたとき
        if ptlist.add(x, y):
            print('[%d] ( %d, %d )' % (ptlist.pos - 1, x, y))
            cv2.circle(img, (x, y), 3, (0, 0, 255), 3)
            cv2.imshow("path:"+wname, img)
        #plistに追加できなかったとき（2個以上）
        else:
            print('All points have selected.  Press any-key.')

        #合計数と最大値が一致したとき
        if(ptlist.pos == ptlist.npoints):
            cv2.rectangle(img, (ptlist.ptlist[0][0], ptlist.ptlist[0][1]), (ptlist.ptlist[1][0], ptlist.ptlist[1][1]), (0, 0, 255), 5)
            imsize_x = img.shape[1]*1.0
            imsize_y = img.shape[0]*1.0
            x = ptlist.ptlist[0][0]*1.0/imsize_x
            y = ptlist.ptlist[0][1]*1.0/imsize_y
            w = (ptlist.ptlist[1][0]*1.0-ptlist.ptlist[0][0]*1.0)/imsize_x
            h = (ptlist.ptlist[1][1]*1.0-ptlist.ptlist[0][1]*1.0)/imsize_y
            if 0.0 < x and x < 1.0 and 0.0 < y and y < 1.0 and 0.0 < w and w < 1.0 and 0.0 < h and h < 1.0 and str(tag)!='-1':
                g.write(str(tag))#tag
                g.write(' ')#tag
                g.write("{:.6f}".format(x+w/2.0))#x
                g.write(' ')
                g.write("{:.6f}".format(y+h/2.0))#y
                g.write(' ')
                g.write("{:.6f}".format(w))#w
                g.write(' ')
                g.write("{:.6f}".format(h))#h
                g.write("\n")
            else:
                print("ERROR value.")
            ptlist.npoints = 0
        



     
def anotation_input(now_data_file, txt_file_path, dic, moji, tag):
    '''
    指定された画像のアノテーションテキストを作成する
    input:
        画像データファイルディレクトリ
        アノテーションデータファイルtxtディレクトリ
        アノテーション情報一覧dictionaly
        表示文字列
        タグ
    output:
        描画後のcv2のimg
        入力されたキー
  '''
    window_name = "path:"+txt_file_path
    k = None
    try:
        # 読み込み画像を初期化
        img = cv2.imread(now_data_file)
        # すでに存在するアノテーションを描画
        img = anotation_drow(img, txt_file_path, dic)

        g = open(txt_file_path,'a')#追記モード
        cv2.namedWindow(window_name)
        ptlist = PointList(2)
        #名前欄表示
        cv2.rectangle(img, (0, 0), (120, 15), (255,255,255), -1)
        cv2.putText(img, moji,(5,10),cv2.FONT_HERSHEY_PLAIN,1.0,(0,0,0))
        # 描画
        cv2.setMouseCallback(window_name, onMouse, [txt_file_path, img, ptlist,g,tag,moji])
        cv2.imshow(window_name, img)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()
        g.close()
    except Exception as e:
        print("Error:anotation_input")
        print(e)
    finally:
        return k



#BGR順
annotation_cloor_dic = {'0':(255, 0, 0),#青
                                    '1':(255, 255, 255),#白
                                    '2':(152, 145, 234),#薄ピンク
                                    '3':(196, 228, 252),#肌色
                                    '4':(51  , 255, 204),#薄緑
                                    '5':(102, 153, 255),#オレンジ
                                    '6':(0    , 255, 102),#緑
                                    '7':(0    , 0    , 255),#赤
                                    '8':(51  , 153, 204),#茶
                                    '9':(0    , 0    , 0    ) #黒(使用しない予定)
                                    }
def anotation_drow(img, txt_file_path, dic):
  '''
  アノテーションされたファイルを探して、既存矩形を描画
  input:
      cv2のimg
      アノテーションデータファイルtxtディレクトリ
      アノテーション情報dictionaly
  output:
      描画後のcv2のimg
'''
  try:
      g = open(txt_file_path,'r')#読み込み
      imsize_x = img.shape[1]*1.0
      imsize_y = img.shape[0]*1.0
      for g_line in g:
          g_word = g_line.split(" ")
          tag = g_word[0]
          # アノテーション情報と一致する矩形を描画
          if tag in dic.keys():
              x = float(g_word[1])
              y = float(g_word[2])
              w = float(g_word[3])
              h = float(g_word[4].replace("\n",""))
              x = int((x-w/2.0)*imsize_x)
              y = int((y-h/2.0)*imsize_y)
              w = int(w*1.0*imsize_x)
              h = int(h*1.0*imsize_y)
              color = annotation_cloor_dic[tag]
              # 矩形描画
              cv2.rectangle(img, (x, y), (x+w, y+h), color, 5)
              # テキスト表記領域描画
              cv2.rectangle(img, (x+5, y+5), (x+120, y+15), (255,255,255), -1)
              cv2.putText(img, dic[tag], (x+5,y+15), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0))
      g.close()
  except Exception as e:
      print("Error:anotation_drow")
      print(e)
  finally:
      return img
      

if __name__ == '__main__':
    None
