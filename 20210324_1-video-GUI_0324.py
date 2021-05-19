import tkinter as tk
# from tkinter import ttk
import cv2
import PIL.Image
import PIL.ImageTk
from tkinter import font
# import time
import shutil
import os
import datetime
import threading
# import sys
from multiprocessing import Process
#  追記　 ここから
#  global flag
#  flag=0
#  追記　 ここまで
#  testtestest


class Application(tk.Frame):

    flag = 0
    t1 = threading

    def __init__(self, master, video_source=0):
        super().__init__(master)

        self.master.geometry("700x700")
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font(
            family="Meiryo UI", size=15, weight="normal")
        self.font_btn_big = font.Font(
            family="Meiryo UI", size=20, weight="bold")
        self.font_btn_small = font.Font(
            family="Meiryo UI", size=15, weight="bold")

        self.font_lbl_bigger = font.Font(family="Meiryo UI", size=45, weight="bold")
        self.font_lbl_big = font.Font(family="Meiryo UI", size=30, weight="bold")
        self.font_lbl_middle = font.Font(family="Meiryo UI", size=15, weight="bold")
        self.font_lbl_small = font.Font(family="Meiryo UI", size=12, weight="normal")

        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture(video_source)
        self.width = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = int(self.vcap.get(cv2.CAP_PROP_FPS))

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = 15  # [mili seconds]
        self.update()

    def create_widgets(self):

        # Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text='Camera', font=self.font_frame)
        self.frame_cam.place(x=10, y=10)
        self.frame_cam.configure(width=self.width + 30, height=self.height + 50)
        self.frame_cam.grid_propagate(0)

        # Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)

        # Frame_Button
        self.frame_btn = tk.LabelFrame(self.master, text='Control', font=self.font_frame)
        self.frame_btn.place(x=10, y=550)
        self.frame_btn.configure(width=self.width + 30, height=120)
        self.frame_btn.grid_propagate(0)

        # Snapshot Button
        # https://www.shido.info/py/tkinter2.html
        # btnを”録画スタート だよ”という表示で作る
        self.btn_snapshot = tk.Button(self.frame_btn, text='録画スタート だよ', font=self.font_btn_big)
        # ボタンが押された時に、press_snapshot_button を発動する
        self.btn_snapshot.configure(width=20, height=1, command=self.press_snapshot_button)
        self.btn_snapshot.grid(column=0, row=0, padx=20, pady=10)

        # 追記ZAKI　2021-05-17　ここから　
        # label
        text1 = "録画停止中"
        text2 = "録画実行中"
        words1 = tk.Label(text=text1, font=("", 12))
        words1.pack()
        # words1.place(x=500, y=500)
        # 追記　ここまで　

        # Close
        self.btn_close = tk.Button(self.frame_btn, text='Close', font=self.font_btn_big)
        self.btn_close.configure(width=15, height=1, command=self.press_close_button)
        self.btn_close.grid(column=1, row=0, padx=20, pady=10)

    def update(self):
        # Get a frame from the video source
        _, frame = self.vcap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

        # self.photo -> Canvas
        self.canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.master.after(self.delay, self.update)

    def press_snapshot_button(self):
        # 録画スタート
        # スレッドではなくて、プロセスを使うらしい？
        # https://qiita.com/ttiger55/items/5e1d5a3405d2b3ef8f40

        # threading.Thread(target=self.video_recode).start()
        Process(target=self.video_recode).start()
        # Process(target=test111).start()
        # ppp= Process(target=test111)
        # ppp.start()

        # flag の値に応じて、ボタンに表記される文言を変える
        # https://www.delftstack.com/ja/howto/python-tkinter/how-to-change-the-tkinter-button-text/

        if (self.flag == 0):
            # self.t1.start()
            self.btn_snapshot.configure(text="STOP だよ")
            self.flag = 1
        else:
            # sys.exit()
            self.btn_snapshot.configure(text="録画START だよ")
            self.flag = 0

    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()

    def video_recode(self):
        # ビデオ入力取得（applicationクラスでなんとかならないか。。。）
        w = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = int(self.vcap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）

        dt_now = datetime.datetime.now()

        # 古い動画の削除
        yesterday = dt_now - datetime.timedelta(days=1)
        try:
            shutil.rmtree(yesterday.strftime('%Y%m%d'))
        except OSError as err:
            print("OS error: {0}".format(err))
            # print("NONONO")

        # フォルダの作成
        folder_name = dt_now.strftime('%Y%m%d')
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        video_name = folder_name + "/" + dt_now.strftime('%Y%m%d%H%M%S') + ".mp4"
        print(video_name)

        # 動画ファイルの保存

        video = cv2.VideoWriter(video_name, fourcc, fps, (int(w), int(h)))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）

        # 動画の保存処理
        count = 0
        while True:
            _, frame = self.vcap.read()
            video.write(frame)                                     # 動画を1フレームずつ保存する

            count = count + 1
            if count == (fps * 15):
                break


def test111():
    print("HELLO PYTHON")


def main():

    root = tk.Tk()

    # http://utisam.hateblo.jp/entry/2013/01/12/212958
    root.state('zoomed')  # when windows
    # root.attributes("-zoomed","1") # when Linux & Mac

    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
