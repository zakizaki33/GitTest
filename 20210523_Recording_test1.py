import cv2
import numpy as np
import os
import datetime
import time
#===================
FPS = 200
Recording_time_unit = 10





second_Base = time.time()

dt_now = datetime.datetime.now()
st_dt_now = str(dt_now)
st_dt_now = st_dt_now.replace(':', '-')
st_dt_now = str(st_dt_now)
print(st_dt_now)
new_path = st_dt_now[0:19]#フォルダ名
new_path_base = st_dt_now[0:19]#フォルダ名

if not os.path.exists(new_path):#ディレクトリがなかったら
    os.mkdir(new_path)#作成したいフォルダ名を作成





##########################################################################################


try: 
    while True:
        dt_now = datetime.datetime.now()
        st_dt_now = str(dt_now)
        st_dt_now = st_dt_now.replace(':', '-')
        st_dt_now = str(st_dt_now)
        new_path = st_dt_now[0:19]

        F_N = str(new_path_base) + '\\' + st_dt_now + str('.m4v')
        print('F_N')
        print(F_N)


        cap = cv2.VideoCapture(0)

        #保存
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        fps = FPS
        size = (640, 480)

        writer2 = cv2.VideoWriter(F_N, fmt, fps, size)
        second = time.time()
        while True:
            _, frame = cap.read()
            frame = cv2.resize(frame, size)
            
            #保存
            writer2.write(frame)
            cv2.imshow('frame', frame)      

            second2 = time.time()
            Sec_Def = second2 - second

            if Sec_Def > Recording_time_unit:
                print(Sec_Def)
                writer2.release()
                cap.release()
                cv2.destroyAllWindows()
                break
            else:
                pass
            if cv2.waitKey(1) == 13:
                break
except KeyboardInterrupt:   # exceptに例外処理を書く
    print('stop!')




