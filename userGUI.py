from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cv2
import showVideoOnGui
import tkinter
import PIL
import threading
import time
from threading import Thread, Lock

class UserGUI(Frame):

    def __init__(self, parent, controller, main):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.main = main
        self.stop = False
        self.canvas = Canvas(parent, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(578.0, 9.0, 578.0, 590.0, fill="#3D7892", outline="")
        self.canvas.create_rectangle(26.0, 105.0, 551.0, 560.0, fill="#FFFFFF", outline="#000000")
        self.canvas.create_text(620.0, 242.0, anchor="nw", text="translated words :", fill="#000000",
                                font=("Roboto", 18 * -1))
        self.canvas.create_text(702.0, 40.0, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
        #### textarea   later : textarea.insert(tk.END, *variable*)
        self.textarea = Text(parent, height=18, width=40)
        self.textarea.place(x=615, y=270)

        # Drop down
        self.clicked = StringVar()
        self.options = []
        self.numOfCams = self.camerasConnected()
        if self.numOfCams == 0:
            self.messagebox.showerror("Error", "Please connect camera!")
            self.clicked.set("no camera")
        else:
            for i in range(self.numOfCams):
                self.options.append(i + 1)
            # clicked.set(options[0])
        self.chooseCamera = ttk.OptionMenu(parent, self.clicked, self.options[0], *self.options)
        self.chooseCamera.place(x=680, y=150, width=100, height=30)
        # create start/stop Btn - and texts
        self.startBtn_image = PhotoImage(file='assets/start_btn.png')
        self.stopBtn_image = PhotoImage(file='assets/stop_btn.png')
        self.goBack_image = PhotoImage(file='assets/goBack.png')
        self.startBtn = Button(parent, image=self.startBtn_image, borderwidth=0, highlightthickness=0,
                               command=lambda: [threading.Thread(target=self.show_video).start(),
                                                self.startvideo()], relief="flat")
        self.stopBtn = Button(parent, image=self.stopBtn_image, borderwidth=0, highlightthickness=0,
                              command=lambda: self.stopvideo(),
                              relief="flat")
        self.goBackBtn = Button(parent, image=self.goBack_image, borderwidth=0, highlightthickness=0,
                                command=lambda: controller.show_frame(self.main), relief="flat")
        self.startBtn.place(x=814, y=150, width=77, height=30)
        self.stopBtn.place(x=902, y=150, width=77, height=30)
        self.goBackBtn.place(x=26, y=32, width=25, height=25)

    def startvideo(self):
        self.stop = False

    def stopvideo(self):
        self.stop = True

    def clearCapture(self, capture):
        capture.release()
        cv2.destroyAllWindows()

    def camerasConnected(self):
        n = 0
        for i in range(3):
            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.clearCapture(cap)
                n += 1
            except:
                self.clearCapture(cap)
                break
        return n

    def show_video(self):
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()  # Read frame from webcam
        canvas = tkinter.Canvas(self.parent, width=640, height=480)
        canvas.place(x=10, y=80)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        if not self.stop:
            self.parent.after(10, self.show_video())


        # x = threading.Thread(target=update, args=(userGui,))
        # update(userGui)
        # x.start()
        # userGui.resizable(False, False)
        # userGui.mainloop()
