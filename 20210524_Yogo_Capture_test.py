import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import font
import time
from docutils.parsers.rst.directives import flag


class Application(tk.Frame):
    flag = 0
    def __init__(self,master, video_source=0):
        super().__init__(master)

        self.master.geometry("700x700")
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font( family="Meiryo UI", size=15, weight="normal" )
        self.font_btn_big = font.Font( family="Meiryo UI", size=20, weight="bold" )
        self.font_btn_small = font.Font( family="Meiryo UI", size=15, weight="bold" )

        self.font_lbl_bigger = font.Font( family="Meiryo UI", size=45, weight="bold" )
        self.font_lbl_big = font.Font( family="Meiryo UI", size=30, weight="bold" )
        self.font_lbl_middle = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_small = font.Font( family="Meiryo UI", size=12, weight="normal" )

        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture( video_source )
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT )

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = 15 #[mili seconds]
        self.update()


    def create_widgets(self):

        #Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text = 'Camera', font=self.font_frame)
        self.frame_cam.place(x = 10, y = 10)
        self.frame_cam.configure(width = self.width+30, height = self.height+50)
        self.frame_cam.grid_propagate(0)

        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=0,padx = 10, pady=10)

        # Frame_Button
        self.frame_btn = tk.LabelFrame( self.master, text='Control', font=self.font_frame )
        self.frame_btn.place( x=10, y=550 )
        self.frame_btn.configure( width=self.width + 30, height=120 )
        self.frame_btn.grid_propagate( 0 )
        #
        # self.frame_btn = tk.StringVar()



        #Snapshot Button

   

        self.btn_snapshot = tk.StringVar()
        #self.btn_snapshot.set("Snapshot")
        self.btn_snapshot = tk.Button( self.frame_btn, text='Snapshot', font=self.font_btn_big)
        self.btn_snapshot.configure(width = 15, height = 1, command=self.press_snapshot_button)
        self.btn_snapshot.configure(width = 15, height = 1, command=self.changeText)
        #self.btn_snapshot.configure(width = 15, height = 1, command=self.changeText_For)
        self.btn_snapshot.grid(column=0, row=0, padx=30, pady= 10)
        self.flag = 0
     



        # Close
        self.btn_close = tk.Button( self.frame_btn, text='Close', font=self.font_btn_big )
        self.btn_close.configure( width=15, height=1, command=self.press_close_button )
        self.btn_close.grid( column=1, row=0, padx=20, pady=10 )
    
    def changeText(self): 
        if self.flag == 0:
            self.flag += 1
            self.btn_snapshot = tk.Button(self.frame_btn, text='1 Shot', font=self.font_btn_big)
            self.btn_snapshot.configure(width = 15, height = 1, command=self.press_snapshot_button)
            self.btn_snapshot.configure(width = 15, height = 1, command=self.changeText)
            self.btn_snapshot.grid(column=0, row=0, padx=30, pady= 10)
        elif self.flag > 20:
            Text_Next_Format = '撮りすぎな'
            Text_Next = Text_Next_Format.format(self.flag)
            self.btn_snapshot = tk.Button(self.frame_btn, text=Text_Next, font=self.font_btn_big)
            self.btn_snapshot.configure(width = 15, height = 1, command=self.press_snapshot_button)
            self.btn_snapshot.configure(width = 15, height = 1, command=self.changeText)
            self.btn_snapshot.grid(column=0, row=0, padx=30, pady= 10)
            pass

        else:
            self.flag += 1
            Text_Next_Format = '{} Shots'
            Text_Next = Text_Next_Format.format(self.flag)
            self.btn_snapshot = tk.Button(self.frame_btn, text=Text_Next, font=self.font_btn_big)
            self.btn_snapshot.configure(width = 15, height = 1, command=self.press_snapshot_button)
            self.btn_snapshot.configure(width = 15, height = 1, command=self.changeText)
            self.btn_snapshot.grid(column=0, row=0, padx=30, pady= 10)
            pass




    def update(self):
        #Get a frame from the video source
        _, frame = self.vcap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

        #self.photo -> Canvas
        self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)

        self.master.after(self.delay, self.update)

    def press_snapshot_button(self):
        # Get a frame from the video source

        _, frame = self.vcap.read()

        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #create_widgets_redisplay(self)

        cv2.imwrite( "frame-" + time.strftime( "%Y-%d-%m-%H-%M-%S" ) + ".jpg",
                     cv2.cvtColor( frame1, cv2.COLOR_BGR2RGB ) )

    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()





def main():
    root = tk.Tk()
    app = Application(master=root)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()
