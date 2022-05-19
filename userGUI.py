from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cv2
from showVideoOnGui import StartVideo
from UserToVideo import AdapterUserGui
import tkinter
import PIL
import threading
from threading import Thread, Lock


class UserGUI(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.stop = False
        self.canvas = Canvas(parent, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.video_canvas = tkinter.Canvas(self.parent, width=640, height=480)
        self.video_canvas.place(x=10, y=80)
        self.adapt = AdapterUserGui(self.stop, self.video_canvas)
        self.canvas.create_rectangle(670.0, 9.0, 670.0, 590.0, fill="#3D7892", outline="")
        self.canvas.create_rectangle(8.0, 78.0, 654.0, 564.0, fill="#FFFFFF", outline="#000000")
        self.canvas.create_text(680.0, 242.0, anchor="nw", text="translated words :", fill="#000000",
                                font=("Roboto", 18 * -1))
        self.canvas.create_text(750.0, 40.0, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
        #### textarea   later : textarea.insert(tk.END, *variable*)
        self.textarea = Text(parent, height=18, width=40)
        self.textarea.place(x=680, y=270)


        # Drop down
        self.clicked = StringVar()
        self.options = []
        self.numOfCams = 0
        self.check_cameras()
        # clicked.set(options[0])
        self.chooseCamera = ttk.OptionMenu(parent, self.clicked, self.options[0], *self.options)
        self.chooseCamera.place(x=680, y=150, width=100, height=30)
        # create start/stop Btn - and texts
        self.startBtn_image = PhotoImage(file='assets/start_btn.png')
        self.stopBtn_image = PhotoImage(file='assets/stop_btn.png')
        self.goBack_image = PhotoImage(file='assets/goBack.png')
        self.startBtn = Button(parent, image=self.startBtn_image, borderwidth=0, highlightthickness=0,
                               command=lambda: [self.startvideo()], relief="flat")
        self.stopBtn = Button(parent, image=self.stopBtn_image, borderwidth=0, highlightthickness=0,
                              command=lambda: self.stopvideo(),
                              relief="flat")
        self.goBackBtn = Button(parent, image=self.goBack_image, borderwidth=0, highlightthickness=0,
                                command=lambda: 1+1 , relief="flat") #controller.show_frame()
        self.startBtn.place(x=814, y=150, width=77, height=30)
        self.stopBtn.place(x=902, y=150, width=77, height=30)
        self.goBackBtn.place(x=26, y=32, width=25, height=25)

    def check_cameras(self):
        self.numOfCams = self.camerasConnected()  # can do status bar progress
        if self.numOfCams == 0:
            # messagebox.showerror("Error", "Please connect camera!")
            self.clicked.set("no camera")
            self.options.append("no camera")
        else:
            for i in range(self.numOfCams):
                self.options.append(i + 1)

    def startvideo(self):
        self.adapt.set_stop = False
        #self.check_cameras()
        if self.numOfCams == 0:
            messagebox.showerror("Error", "Please connect camera!")
        else:
            self.capture = cv2.VideoCapture(int(self.clicked.get()) - 1)
            self.adapt.set_capture(self.capture)
            camera = StartVideo(self.adapt, self)
            threading.Thread(target=camera.showVideo()).start()
            #threading.Thread(target=camera.showVideo()).start()
            self.startBtn.config(state="disabled")

    def stopvideo(self):
        self.adapt.set_stop = True
        self.startBtn.config(state="normal")

    def clearCapture(self, capture):
        capture.release()
        cv2.destroyAllWindows()

    def camerasConnected(self):
        n = 0
        for i in range(3):
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                if cap:
                    ret, frame = cap.read()
                    if ret:
                        #cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.clearCapture(cap)
                        n += 1
            except:
                self.clearCapture(cap)
                break
        return n

    def show_video(self):
        while not self.stop:
            ret, frame = self.capture.read()  # Read frame from webcam
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.video_canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
                #self.after(15, self.show_video())  # this is with if
                self.update()  # this is with while
        else:
            self.capture.release()
            #cv2.destroyAllWindows()
