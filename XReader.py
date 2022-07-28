import tkinter as tk
from tkinter import *
from PIL import ImageGrab,ImageTk
import ctypes
import numpy
from gtts import gTTS
import tempfile
from playsound import playsound
ctypes.windll.shcore.SetProcessDpiAwareness(2) # windows 10
import pytesseract
from pytesseract import image_to_string
from pynput import keyboard
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
from deep_translator import GoogleTranslator
import threading
from pynput import keyboard


def DrawWindow():
    class ToolWin(tk.Toplevel):
        def __init__(self):
            tk.Toplevel.__init__(self)
            self._offsetx = 0
            self._offsety = 0
            self.wm_attributes('-topmost', 1)
            self.penSelect = tk.BooleanVar()
            self.overrideredirect(1)
            self.geometry('100x100')
            self.penModeId = None
            self.startPointId = None
            self.startPointIdX = 0
            self.startPointIdY = 0
            self.endPointId = None
            self.endPointIdX = 0
            self.endPointIdY = 0
            self.bind('<ButtonPress-1>', self.clickTool)
            self.bind('<B1-Motion>', self.moveTool)  # bind move event
            self.penSelect.set(True)
            self.penDraw()
            self.isJapanese = IntVar()
            draw = tk.Checkbutton(self, text="Pen", command=self.penDraw, variable=self.penSelect)

            draw.pack()

            cancel = tk.Button(self, text="Quit", command=root.destroy)
            cancel.pack()


            self.checklist =  tk.Checkbutton(self, text="jpn",variable = self.isJapanese,onvalue=1, offvalue=0)
            self.checklist.pack()

        def moveTool(self, event):
            self.geometry(
                "100x100+{}+{}".format(self.winfo_pointerx() - self._offsetx, self.winfo_pointery() - self._offsety))

        def clickTool(self, event):
            self._offsetx = event.x
            self._offsety = event.y

        def penDraw(self):
            if self.penSelect.get():
                self.penModeId = root.bind("<B1-Motion>", self.Draw)
                self.startPointId = root.bind("<ButtonPress-1>", self.setStarPoint)
                self.endPointId = root.bind("<ButtonRelease-1>", self.setEndPoint)
            else:
                root.unbind('<B1-Motion>', self.penModeId)
                root.unbind("<ButtonPress-1>", self.startPointId)
                root.unbind("<ButtonRelease-1>", self.endPointId)

        def setStarPoint(self, event):
            self.startPointIdX = event.x
            self.startPointIdY = event.y
            try:
                engine.endLoop()
            except:
                pass

        def threadFunction(self):

            miniImg = grabeImage.crop([self.startPointIdX, self.startPointIdY, self.endPointIdX, self.endPointIdY])
            q
            try:
                output = image_to_string(miniImg)
            except:
                output = " "
            print(self.isJapanese.get())
            if self.isJapanese.get() == 1:
                output = image_to_string(miniImg,'jpn')
                print("jap")
            output = str(output)
            output = output.replace('\n',' ')
            print(output)
            if output.replace(" ","") =="" or output.replace(" ","") =="0":
                output = "Loading failed, please mark form left top coner to right down coner"

            try:

                output=GoogleTranslator(source='auto', target='pl').translate(output)

            except:
                output = "Translacja nieudana"
            print('Output: ', output)
            speech = gTTS(text=output,lang='pl',slow=False)
            tempdir = tempfile.TemporaryDirectory()
            speech.save(tempdir.name + '\dxxx.mp3')
            playsound(tempdir.name + '\dxxx.mp3', block=True)
            tempdir.cleanup()


        def setEndPoint(self, event):
            self.endPointIdX = event.x
            self.endPointIdY = event.y
            fullCanvas.delete("all")
            fullCanvas.create_image(0, 0, anchor="nw", image=background)

            fullCanvas.create_rectangle(self.startPointIdX, self.startPointIdY, self.endPointIdX, self.endPointIdY,
                                        outline="red")

            anotherThread = threading.Thread(target=self.threadFunction)
            anotherThread.start()


        def Draw(self, event):  # r = 3
            fullCanvas.delete("all")
            fullCanvas.create_image(0, 0, anchor="nw", image=background)

            fullCanvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="black")
            fullCanvas.create_rectangle(self.startPointIdX, self.startPointIdY, event.x, event.y,
                                        outline="red")

    def showTool():  # the small tool window
        toolWin = ToolWin()
        toolWin.mainloop()


    root = tk.Tk()
    root.state('zoomed')
    root.overrideredirect(1)

    fullCanvas = tk.Canvas(root)
    grabeImage = ImageGrab.grab(all_screens=True)
    background = ImageTk.PhotoImage(grabeImage) # show the background,make it "draw on the screen".
    fullCanvas.create_image(0,0,anchor="nw",image=background)

    fullCanvas.pack(expand="YES",fill="both")

    root.after(100,showTool)

    root.mainloop()



def on_release(key):

    if format(key)== "'q'":
        DrawWindow()



    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(

        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(

    on_release=on_release)
listener.start()
