# -*- coding: utf-8 -*-
import sys
sys.path.append("../commons/")
import annotation_dic as andc
import os
import cv2
import datetime



def main(data_dir, write_dir, dic):
    '''
    画像を読み込んで、イメージを書き出す
    input:
        読み込み画像ディレクトリ
        書き出し画像ディレクトリ
        アノテーション情報のdictionaly
  '''
    #ディレクトリ読み込み & jpg画像のみ読み込み
    files = os.listdir(data_dir)
    files = [x for x in files if ".jpg" in x or ".jpeg" in x]
    for file in files:
        img_file_pah = data_dir + "/" + file
        txt_file_path   = data_dir + "/" + file.split(".")[0]+".txt"

        
        image = cv2.imread(img_file_pah, cv2.IMREAD_COLOR)
        imsize_y = image.shape[0]#tate
        imsize_x = image.shape[1]#yoko
        # 両方ある場合のみ
        if os.path.exists(txt_file_path) and os.path.exists(img_file_pah):
            g = open(txt_file_path, 'r')
            for g_line in g:
                g_word = g_line.split(" ")
                folder = write_dir + "/" + str(g_word[0])+"_"+dic[g_word[0]]
                if not os.path.exists(folder):
                    os.mkdir(folder)
                x = float(g_word[1])
                y = float(g_word[2])
                w = float(g_word[3])
                h = float(g_word[4][:-2])
                x = int((x-w/2.0)*imsize_x)
                y = int((y-h/2.0)*imsize_y)
                w = int(w*1.0*imsize_x)
                h = int(h*1.0*imsize_y)
                x_end = x + w
                y_end = y + h
                dt_now = datetime.datetime.now()
                date = dt_now.strftime('%Y_%m_%d_%H_%M_%S')
                output_img_path = folder + "/" + date + "_" + file
                cv2.imwrite(output_img_path, image[y:y_end,x:x_end])
                
                


if __name__ == '__main__':
    data_dir = sys.argv[1]#dir
    output_dir = sys.argv[2]#dir
    dic = andc.read_annotation()
    main(data_dir, output_dir, dic)
