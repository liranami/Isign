from tkinter import *
from PIL import Image, ImageTk
import userGUI

def main(win=None):
    if win:
        win.destroy()
    window = Tk()
    window.geometry("1024x600")
    window.title("Isign")
    icon = PhotoImage(file='assets/Logo.png')
    window.iconphoto(True, icon)
    window.configure(bg="#FFFFFF")
    canvas = Canvas(window, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    # create blue rectangle and on top of it our Isign LOGO
    canvas.create_rectangle(0.0, 0.0, 500.0, 600.0, fill="#78BFDD", outline="")
    logo_img = Image.open('assets/Logo.png')
    logo_resize = logo_img.resize((450, 450), Image.ANTIALIAS)
    logo_img = ImageTk.PhotoImage(logo_resize)
    logo = canvas.create_image(240.0, 300.0, image=logo_img)
    # end
    # create start/stop Btn - and texts
    userBtn_image = PhotoImage(file='assets/user.png')
    developerBtn_image = PhotoImage(file='assets/developer.png')
    userBtn = Button(image=userBtn_image, borderwidth=0, highlightthickness=0,
                     command=lambda: userGUI.changeToUserWin(window), relief="flat")
    developerBtn = Button(image=developerBtn_image, borderwidth=0, highlightthickness=0,
                          command=lambda: print('developer btn click'), relief="flat")
    userBtn.place(x=660, y=390, width=208, height=60)
    developerBtn.place(x=660, y=250, width=208, height=60)
    canvas.create_text(721, 191, anchor="nw", text="You are", fill="#000000", font=("Roboto", 24 * -1))
    canvas.create_text(746, 340, anchor="nw", text="Or", fill="#000000", font=("Roboto", 24 * -1))
    canvas.create_text(698, 56, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
    # end
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    main()
