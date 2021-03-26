from tkinter import *
from tkinter import filedialog,messagebox
# import tkinter.font
import os
import ctypes
from PIL import ImageTk,Image
from PIL import ImageOps, ImageDraw
import imghdr
from collections import*


################ DRAW ################

def drawOnImage(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=True
    drawWindow=Toplevel(canvas.data.mainWindow)
    drawWindow.title="Draw"
    drawFrame=Frame(drawWindow)
    redButton=Button(drawFrame, bg="red", width=2, \
                     command=lambda: colourChosen(drawWindow,canvas, "red"))
    redButton.grid(row=0,column=0)
    blueButton=Button(drawFrame, bg="blue", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "blue"))
    blueButton.grid(row=0,column=1)
    greenButton=Button(drawFrame, bg="green",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "green"))
    greenButton.grid(row=0,column=2)
    magentaButton=Button(drawFrame, bg="magenta", width=2,\
                         command=lambda: colourChosen(drawWindow,canvas, "magenta"))
    magentaButton.grid(row=1,column=0)
    cyanButton=Button(drawFrame, bg="cyan", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "cyan"))
    cyanButton.grid(row=1,column=1)
    yellowButton=Button(drawFrame, bg="yellow",width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "yellow"))
    yellowButton.grid(row=1,column=2)
    orangeButton=Button(drawFrame, bg="orange", width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "orange"))
    orangeButton.grid(row=2,column=0)
    purpleButton=Button(drawFrame, bg="purple",width=2, \
                        command=lambda: colourChosen(drawWindow,canvas, "purple"))
    purpleButton.grid(row=2,column=1)
    brownButton=Button(drawFrame, bg="brown",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "brown"))
    brownButton.grid(row=2,column=2)
    blackButton=Button(drawFrame, bg="black",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "black"))
    blackButton.grid(row=3,column=0)
    whiteButton=Button(drawFrame, bg="white",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "white"))
    whiteButton.grid(row=3,column=1)
    grayButton=Button(drawFrame, bg="gray",width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "gray"))
    grayButton.grid(row=3,column=2)
    drawFrame.pack(side=BOTTOM)


def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image!=None:
        canvas.data.drawColour=colour
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()


def drawDraw(event, canvas):
    if canvas.data.drawOn==True:
        x=int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
        y=int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x-3, y-3, x+ 3, y+3), fill=canvas.data.drawColour,\
                     outline=None)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)


######################## FEATURES ###########################

def closeHistWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.histWindowClose=True

def histogram(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    histWindow=Toplevel(canvas.data.mainWindow)
    histWindow.title("Histogram")
    canvas.data.histCanvasWidth=350
    canvas.data.histCanvasHeight=475
    histCanvas = Canvas(histWindow, width=canvas.data.histCanvasWidth, \
                        height=canvas.data.histCanvasHeight)
    histCanvas.pack()
    # provide sliders to the user to manipulate red, green and blue amounts in the image
    redSlider=Scale(histWindow, from_=-100, to=100, \
                    orient=HORIZONTAL, label="R")
    redSlider.pack()
    blueSlider=Scale(histWindow, from_=-100, to=100,\
                     orient=HORIZONTAL, label="B")
    blueSlider.pack()
    greenSlider=Scale(histWindow, from_=-100, to=100,\
                      orient=HORIZONTAL, label="G")
    greenSlider.pack()
    OkHistFrame=Frame(histWindow)
    OkHistButton=Button(OkHistFrame, text="OK", \
                        command=lambda: closeHistWindow(canvas))
    OkHistButton.grid(row=0,column=0)
    OkHistFrame.pack(side=BOTTOM)
    initialRGB=(0,0,0)
    changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, initialRGB)


def changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, previousRGB):
    if canvas.data.histWindowClose==True:
        histWindow.destroy()
        canvas.data.histWindowClose=False
    else:
        # the slider value indicates the % by which the red/green/blue
        # value of the pixels of the image need to incresed (for +ve values)
        # or decreased (for -ve values)
        if canvas.data.image!=None and histWindow.winfo_exists() :
            R, G, B= canvas.data.image.split()
            sliderValR=redSlider.get()
            (previousR, previousG, previousB)= previousRGB
            scaleR=(sliderValR-previousR)/100.0
            R=R.point(lambda i: i+ int(round(i*scaleR)))
            sliderValG=greenSlider.get()
            scaleG=(sliderValG-previousG)/100.0
            G=G.point(lambda i: i+ int(round(i*scaleG)))
            sliderValB=blueSlider.get()
            scaleB=(sliderValB-previousB)/100.0
            B=B.point(lambda i: i+ int(round(i*scaleB)))
            canvas.data.image = Image.merge(canvas.data.image.mode, (R, G, B))

            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            displayHistogram(canvas, histWindow, histCanvas)
            previousRGB=(sliderValR, sliderValG, sliderValB)
            canvas.after(200, lambda: changeColours(canvas, redSlider,\
                blueSlider, greenSlider,  histWindow, histCanvas, previousRGB))

def displayHistogram(canvas,histWindow, histCanvas):
    histCanvasWidth=canvas.data.histCanvasWidth
    histCanvasHeight=canvas.data.histCanvasHeight
    margin=50
    if canvas.data.image!=None:
        histCanvas.delete(ALL)
        im=canvas.data.image
        #x-axis
        histCanvas.create_line(margin-1, histCanvasHeight-margin+1,\
                               margin-1+ 258, histCanvasHeight-margin+1)
        xmarkerStart=margin-1
        for i in range(0,257,64):
            xmarker="%d" % (i)
            histCanvas.create_text(xmarkerStart+i,\
                                   histCanvasHeight-margin+7, text=xmarker)
        #y-axis
        histCanvas.create_line(margin-1, \
                               histCanvasHeight-margin+1, margin-1, margin)
        ymarkerStart= histCanvasHeight-margin+1
        for i in range(0, histCanvasHeight-2*margin+1, 50):
            ymarker="%d" % (i)
            histCanvas.create_text(margin-1-10,\
                                   ymarkerStart-i, text=ymarker)

        R, G, B=im.histogram()[:256], im.histogram()[256:512], \
                 im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo=R[i]
            histCanvas.create_oval(i+margin, \
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin, \
                                   fill="red", outline="red")
        for i in range(len(G)):
            pixelNo=G[i]
            histCanvas.create_oval(i+margin, \
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin, \
                                   fill="green", outline="green")
        for i in range(len(B)):
            pixelNo=B[i]
            histCanvas.create_oval(i+margin,\
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin,\
                                   fill="blue", outline="blue")

def colourPop(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=True
    canvas.data.drawOn=False
    messagebox.showinfo(title="Colour Pop", message="Click on a part of the image which you want in colour" , parent=canvas.data.mainWindow)
    if canvas.data.cropPopToHappen==False:
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: getPixel(event, canvas))


def getPixel(event, canvas):
    # have to check if Colour Pop button is pressed or not, otherwise, the root
    # events which point to different functions based on what button has been
    # pressed will get mixed up
    try: # to avoid confusion between the diffrent events
        # asscoaited with crop and colourPop
        if canvas.data.colourPopToHappen==True and \
           canvas.data.cropPopToHappen==False and canvas.data.image!=None :
            data=[]
            # catch the location of the pixel selected by the user
            # multiply it by the scale to get pixel's olaction of the
            #actual image
            canvas.data.pixelx=\
            int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
            canvas.data.pixely=\
            int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
            pixelr, pixelg, pixelb= \
            canvas.data.image.getpixel((canvas.data.pixelx, canvas.data.pixely))
            # the amount of deviation allowed from selected pixel's value
            tolerance=60
            for y in range(canvas.data.image.size[1]):
                for x in range(canvas.data.image.size[0]):
                    r, g, b= canvas.data.image.getpixel((x, y))
                    avg= int(round((r + g + b)/3.0))
                    # if the deviation of each pixel value > tolerance,
                    # make them gray else keep them coloured
                    if (abs(r-pixelr)>tolerance or
                        abs(g-pixelg)>tolerance or
                        abs(b-pixelb)>tolerance ):
                        R, G, B= avg, avg, avg
                    else:
                        R, G, B=r,g,b
                    data.append((R, G, B))
            canvas.data.image.putdata(data)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
    except:
        pass
    canvas.data.colourPopToHappen=False


def crop(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
    # have to check if crop button is pressed or not, otherwise,
    # the root events which point to
    # different functions based on what button has been pressed
    # will get mixed up
    canvas.data.cropPopToHappen=True
    messagebox.showinfo(title="Crop", \
                          message="Draw cropping rectangle and press Enter" ,\
                          parent=canvas.data.mainWindow)
    if canvas.data.image!=None:
        canvas.data.mainWindow.bind("<ButtonPress-1>", \
                                    lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", \
                                    lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    # detects the start of the crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.startCropX=event.x
        canvas.data.startCropY=event.y

def drawCrop(event,canvas):
    # keeps extending the crop rectange as the user extends
    # his desired crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.tempCropX=event.x
        canvas.data.tempCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                 canvas.data.tempCropX, \
            canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

def endCrop(event, canvas):
    # set canvas.data.endCrop=True so that button pressed movements
    # are not caught anymore but set it to False when "Enter"
    # is pressed so that crop can be performed another time too
    if canvas.data.cropPopToHappen==True:
        canvas.data.endCrop=True
        canvas.data.endCropX=event.x
        canvas.data.endCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                 canvas.data.endCropX, \
            canvas.data.endCropY, fill="gray", stipple="gray12", width=0 )
        canvas.data.mainWindow.bind("<Return>", \
                                lambda event: performCrop(event, canvas))

def performCrop(event,canvas):
    canvas.data.image=\
    canvas.data.image.crop(\
    (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
    int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
    canvas.data.endCrop=False
    canvas.data.cropPopToHappen=False
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)



def rotateFinished(canvas, rotateWindow, rotateSlider, previousAngle):
    if canvas.data.rotateWindowClose==True:
        rotateWindow.destroy()
        canvas.data.rotateWindowClose=False
    else:
        if canvas.data.image!=None and rotateWindow.winfo_exists():
            canvas.data.angleSelected=rotateSlider.get()
            if canvas.data.angleSelected!= None and \
               canvas.data.angleSelected!= previousAngle:
                canvas.data.image=\
                canvas.data.image.rotate(float(canvas.data.angleSelected))
                canvas.data.imageForTk=makeImageForTk(canvas)
                drawImage(canvas)
        canvas.after(200, lambda:rotateFinished(canvas,\
                    rotateWindow, rotateSlider, canvas.data.angleSelected) )


def closeRotateWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.rotateWindowClose=True

def rotate(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    rotateWindow=Toplevel(canvas.data.mainWindow)
    rotateWindow.title("Rotate")
    rotateSlider=Scale(rotateWindow, from_=0, to=360, orient=HORIZONTAL)
    rotateSlider.pack()
    OkRotateFrame=Frame(rotateWindow)
    OkRotateButton=Button(OkRotateFrame, text="OK",\
                          command=lambda: closeRotateWindow(canvas))
    OkRotateButton.grid(row=0,column=0)
    OkRotateFrame.pack(side=BOTTOM)
    rotateFinished(canvas, rotateWindow, rotateSlider, 0)

def closeBrightnessWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose=True

def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False

    else:
        # increasing pixel values according to slider value increases
        #brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal-previousVal)/100.0
            canvas.data.image=canvas.data.image.point(\
                lambda i: i+ int(round(i*scale)))
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200, \
            lambda: changeBrightness(canvas, brightnessWindow, \
                                     brightnessSlider, sliderVal))


def brightness(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    brightnessWindow=Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessSlider=Scale(brightnessWindow, from_=-100, to=100,\
                           orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=Frame(brightnessWindow)
    OkBrightnessButton=Button(OkBrightnessFrame, text="OK", \
                              command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
    brightnessSlider.set(0)

def reset(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    ### change back to original image
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def mirror(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.mirror(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def flip(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.flip(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)


def transpose(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # I treated the image as a continuous list of pixel values row-wise
    # and simply excnaged the rows and the coloums
    # in oder to make it rotate clockewise, I reversed all the rows
    if canvas.data.image!=None:
        imageData=list(canvas.data.image.getdata())
        newData=[]
        newimg=Image.new(canvas.data.image.mode,\
                (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in range(canvas.data.image.size[0]):
            addrow=[]
            for j in range(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData+=addrow
        newimg.putdata(newData)
        canvas.data.image=newimg.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

############### FILTERS ######################

def covertGray(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    #### The existing method to convert to a grayscale image converts the ####
    ####         image mode, so I used my own function to convert         ####
    # value of each channel of a pixel is set to the average of the original
    # values of the channels
    if canvas.data.image!=None:
        data=[]
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                avg= int(round((r + g + b)/3.0))
                R, G, B= avg, avg, avg
                data.append((R, G, B))
        canvas.data.image.putdata(data)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def sepia(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # this method first converts the image to B&W and then adds the
    # same amount of red and green to every pixel
    if canvas.data.image!=None:
        sepiaData=[]
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                avg= int(round((r + g + b)/3.0))
                R, G, B= avg+100, avg+50, avg
                sepiaData.append((R, G, B))
        canvas.data.image.putdata(sepiaData)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def invert(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.invert(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def solarize(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    solarizeWindow=Toplevel(canvas.data.mainWindow)
    solarizeWindow.title("Solarize")
    solarizeSlider=Scale(solarizeWindow, from_=0, to=255, orient=HORIZONTAL)
    solarizeSlider.pack()
    OkSolarizeFrame=Frame(solarizeWindow)
    OkSolarizeButton=Button(OkSolarizeFrame, text="OK",\
                            command=lambda: closeSolarizeWindow(canvas))
    OkSolarizeButton.grid(row=0,column=0)
    OkSolarizeFrame.pack(side=BOTTOM)
    ### beacsue intial silderVal=0
    performSolarize(canvas, solarizeWindow, solarizeSlider, 255)


def performSolarize(canvas, solarizeWindow, solarizeSlider, previousThreshold):
    if canvas.data.solarizeWindowClose==True:
        solarizeWindow.destroy()
        canvas.data.solarizeWindowClose=False

    else:
        # the  slider denotes the % of solarization thta the user wants,
        # so the threshold (above which pixels are inverted) is inversely
        # related to the slider value
        if solarizeWindow.winfo_exists():
            sliderVal=solarizeSlider.get()
            threshold=255-sliderVal
            if canvas.data.image!=None and threshold!=previousThreshold:
                canvas.data.image=ImageOps.solarize(canvas.data.image,\
                                                    threshold=threshold)
                canvas.data.imageForTk=makeImageForTk(canvas)
                drawImage(canvas)
            canvas.after(200, lambda: performSolarize(canvas, \
                                solarizeWindow, solarizeSlider, threshold))

def closeSolarizeWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.solarizeWindowClose=True

def posterize(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # we basically reduce the range of colurs from 256 to 5 bits
    # and so, assign a single new value to each colour value
    # in each succesive range
    posterData=[]
    if canvas.data.image!=None:
        for col in range(canvas.data.imageSize[1]):
            for row in range(canvas.data.imageSize[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                if r in range(32):
                    R=0
                elif r in range(32, 96):
                    R=64
                elif r in range(96, 160):
                    R=128
                elif r in range(160, 224):
                    R=192
                elif r in range(224,256):
                    R=255
                if g in range(32):
                    G=0
                elif g in range(32, 96):
                    G=64
                elif g in range(96, 160):
                    G=128
                elif g in range(160, 224):
                    G=192
                elif g in range(224,256):
                    G=255
                if b in range(32):
                    B=0
                elif b in range(32, 96):
                    B=64
                elif b in range(96, 160):
                    B=128
                elif b in range(160, 224):
                    B=192
                elif b in range(224,256):
                    B=255
                posterData.append((R, G, B))
        canvas.data.image.putdata(posterData)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)



################ EDIT MENU FUNCTIONS ############################

def keyPressed(canvas, event):
    if event.keysym=="z":
        undo(canvas)
    elif event.keysym=="y":
        redo(canvas)


# we use deques so as to make Undo and Redo more efficient and avoid
# memory space isuues
# after each change, we append the new version of the image to
# the Undo queue
def undo(canvas):
    if len(canvas.data.undoQueue)>0:
        # the last element of the Undo Deque is the
        # current version of the image
        lastImage=canvas.data.undoQueue.pop()
        # we would want the current version if wehit redo after undo
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue)>0:
        # the previous version of the image
        canvas.data.image=canvas.data.undoQueue[-1]
    save(canvas)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

def redo(canvas):
    if len(canvas.data.redoQueue)>0:
        canvas.data.image=canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue)>0:
        # we remove this version from the Redo Deque beacuase it
        # has become our current image
        lastImage=canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

############# MENU COMMANDS ################

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image!=None:
        filename=filedialog.asksaveasfilename(defaultextension=".jpg")
        im=canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image!=None:
        im=canvas.data.image
        im.save(canvas.data.imageLocation)

def newImage(canvas):
    imageName=filedialog.askopenfilename()
    filetype=""
    #make sure it's an image file
    try: filetype=imghdr.what(imageName)
    except:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff','jpg']:
        canvas.data.imageLocation=imageName
        im = Image.open(imageName)
        canvas.data.image=im
        canvas.data.originalImage=im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize=im.size #Original Image dimensions
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
    else:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)

                    ########BLUR AN IMAGE#########
# def BlurImg(root, canvas):
#     cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('mask',(500,500))
#     filename= 'flower.jpg'
#     cwd = os.getcwd()
#     name_file=os.path.splitext(filename)[0]
#
#     path_save_temp=os.path.join(cwd,'Data')
#     path_save_folder=os.path.join(path_save_temp,f'{name_file}_blur_data')
#     if not os.path.exists(path_save_folder):
#         os.makedirs(path_save_folder)
#
#     img=cv2.imread(filename)
#     img = cv2.GaussianBlur(img,(5,5),0)
#     img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#
#     file_save_blur= os.path.join(path_save_folder,'blur.png')
#     im_blur = cv2.GaussianBlur(img,(81,81),0)
#     cv2.imwrite(file_save_blur,im_blur)
#
#     xs,ys,w,h = cv2.selectROI('mask',img)
#     crop_img=crop_img_true=crop_img_contour=img[ys:ys+h, xs:xs+w]
#
#     if not crop_img_true.shape[0]> 1:
#         crop_img_true=img
#
#     x,y,z,a,b,c=(tr.tracker(crop_img_true))
#     crop_img_true=cv2.cvtColor(crop_img_true,cv2.COLOR_BGR2HSV)
#
#     file_save_mask_inrange= os.path.join(path_save_folder,'mask inRange.png')
#     mask_inRange=cv2.inRange(crop_img_true,(x,y,z),(a,b,c))
#     cv2.imwrite(file_save_mask_inrange,mask_inRange)
#
#     _, threshold = cv2.threshold(mask_inRange, 250, 255, cv2.THRESH_BINARY)
#     Gauss_threshold =cv2.adaptiveThreshold(threshold,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,101,10)
#
#     blank_space_black= np.zeros((crop_img_true.shape[0],crop_img_true.shape[1]),np.uint8)
#     blank_space_black[:]=(0)
#
#     _,contours,_ = cv2.findContours(Gauss_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#
#
#     maxi=cv2.contourArea(contours[0])
#     c=[]
#
#     for cnt in contours:
#         if cv2.contourArea(cnt)>=maxi:
#             maxi=cv2.contourArea(cnt)
#             ##        print(cv2.contourArea(cnt))
#             c= cnt
#
# file_save_contour= os.path.join(path_save_folder,'Contour.png')
# cv2.drawContours(crop_img_contour, c, -1, (0, 255, 0), 5)
# cv2.imwrite(file_save_contour,crop_img_contour)
#
#
# file_save_poly= os.path.join(path_save_folder,'mask fill poly.png')
# mask_poly=cv2.fillConvexPoly(blank_space_black,c,(255,255,255))
# cv2.imwrite(file_save_poly,mask_poly)
#
# crop_img_true=cv2.cvtColor(crop_img_true,cv2.COLOR_HSV2BGR)
#
# file_save_mask_bitwise= os.path.join(path_save_folder,'mask bitwise and.png')
# mask_bitwise_and = cv2.bitwise_and(crop_img_true,crop_img_true,mask=mask_poly)
# cv2.imwrite(file_save_mask_bitwise,mask_bitwise_and)
#
# im2= Image.open(file_save_mask_bitwise)
# im2=im2.convert('RGBA')
#
# datas=im2.getdata()
# newdata=[]
#
# for data in datas:
#     if data[0]== 0 and data[1]== 0 and data[2]== 0:
#         newdata.append((255,255,255,0))
#     else:
#         newdata.append(data)
#
# file_save_transparent= os.path.join(path_save_folder,'transparent.png')
# im2.putdata(newdata)
# im2.save(file_save_transparent)
#
# im_blur= Image.open(file_save_blur)
#
# file_save_final= os.path.join(path_save_folder,'final.png')
# im_blur.paste(im2,(xs,ys),im2)
# im_blur.save(file_save_final)
#
# im_final= Image.open(file_save_final)
# im_final.show('Final Result')
# cv2.waitKey(0)
# cv2.destroyAllWindows()

######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
        imageWidth=canvas.data.image.size[0]
        imageHeight=canvas.data.image.size[1]
        #To make biggest version of the image fit inside the canvas
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,\
                int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)

def drawImage(canvas):
    if canvas.data.image!=None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))


############# DESKTOP BK ##############

## Please comment this function out if you use this on any OS apart from Windows

def desktopBk(canvas):
    if canvas.data.image!=None:
        new=canvas.data.image.copy()
        # Windows desktop photos are supposed to be bitmap images
        newLocation=os.path.dirname(\
            canvas.data.imageLocation)+"/desktopPhoto.bmp"
        new.save(newLocation)
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, str(newLocation), 0)


############ INITIALIZE ##############

def init(root, canvas):

    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image=None
    canvas.data.angleSelected=None
    canvas.data.rotateWindowClose=False
    canvas.data.brightnessWindowClose=False
    canvas.data.brightnessLevel=None
    canvas.data.histWindowClose=False
    canvas.data.solarizeWindowClose=False
    canvas.data.posterizeWindowClose=False
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.endCrop=False
    canvas.data.drawOn=True

    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()

def buttonsInit(root, canvas):
    backgroundColour="Green"
    buttonWidth=14
    buttonHeight=2
    toolKitFrame=Frame(root)
    # helv36 = tkinter.font(family='Helvetica', size=36, weight='bold')
    cropButton=Button(toolKitFrame, text="Crop",\
                      background=backgroundColour ,\
                      width=buttonWidth, height=buttonHeight, \
                      command=lambda:crop(canvas))
    cropButton.grid(row=0,column=1)
    rotateButton=Button(toolKitFrame, text="Rotate",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda:rotate(canvas))
    rotateButton.grid(row=0,column=2)
    brightnessButton=Button(toolKitFrame, text="Brightness",\
                            background=backgroundColour ,\
                            width=buttonWidth, height=buttonHeight,\
                            command=lambda:brightness(canvas))
    brightnessButton.grid(row=0,column=3)
    histogramButton=Button(toolKitFrame, text="Histogram",\
                           background=backgroundColour ,\
                           width=buttonWidth,height=buttonHeight, \
                           command=lambda:histogram(canvas))
    histogramButton.grid(row=0,column=4)
    colourPopButton=Button(toolKitFrame, text="Colour Pop",\
                           background=backgroundColour, \
                           width=buttonWidth,height=buttonHeight, \
                           command=lambda:colourPop(canvas))
    colourPopButton.grid(row=0,column=5)
    mirrorButton=Button(toolKitFrame, text="Mirror",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda:mirror(canvas))
    mirrorButton.grid(row=0,column=6)
    flipButton=Button(toolKitFrame, text="Flip",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      command=lambda:flip(canvas))
    flipButton.grid(row=0,column=7)
    transposeButton=Button(toolKitFrame, text="Transpose",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda:transpose(canvas))
    transposeButton.grid(row=0,column=8)
    drawButton=Button(toolKitFrame, text="Draw",\
                      background=backgroundColour ,width=buttonWidth,\
                      height=buttonHeight,command=lambda:drawOnImage(canvas))
    drawButton.grid(row=0,column=9)
    resetButton=Button(toolKitFrame, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       height=buttonHeight, command=lambda:reset(canvas))
    resetButton.grid(row=0,column=10)
    #Please comment this button out if you use this on any OS apart from Windows
    desktopButton=Button(toolKitFrame, text="Make Desktop Bk",\
                          background=backgroundColour,height=buttonHeight,\
                          width=buttonWidth,command=lambda:desktopBk(canvas))
    desktopButton.grid(row=0,column=11)
    toolKitFrame.pack(side=TOP)

def menuInit(root, canvas):
    menu=Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=lambda:newImage(canvas))
    filemenu.add_command(label="New from Clipboard", command=lambda:newImage(canvas))
    filemenu.add_separator()
    filemenu.add_command(label="Save", command=lambda:save(canvas))
    filemenu.add_command(label="Save As", command=lambda:saveAs(canvas))
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    ## Edit pull-down Menu
    editmenu = Menu(menu, tearoff=0)
    editmenu.add_command(label="Undo   Ctrl+Z", command=lambda:undo(canvas))
    editmenu.add_command(label="Redo   Ctrl+Y", command=lambda:redo(canvas))
    menu.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menu)
    #For selection menu
    filemenu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Select', menu=filemenu1)
    ## Filter pull-down Menu
    filtermenu = Menu(menu, tearoff=0)
    filtermenu.add_command(label="Black and White", \
                           command=lambda:covertGray(canvas))
    filtermenu.add_command(label="Sepia",\
                           command=lambda:sepia(canvas))
    filtermenu.add_command(label="Invert", \
                           command=lambda:invert(canvas))
    filtermenu.add_command(label="Solarize", \
                           command=lambda:solarize(canvas))
    filtermenu.add_command(label="Posterize", \
                           command=lambda:posterize(canvas))
    menu.add_cascade(label="Filter", menu=filtermenu)
    root.config(menu=menu)
    # For Effects Menu
    filemenu2 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Effects', menu=filemenu2)
    # filemenu2.add_command(label="Blur", command=lambda:BlurImg(canvas))
    # For Tools Menu
    filemenu3 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Tools', menu=filemenu3)
    # For Retouch
    filemenu4 = Menu(menu, tearoff=0)
    menu.add_cascade(label='Retouch', menu=filemenu4)



def run():
    # create the root and the canvas
    root = Tk()
    root.title("IEditor")
    root.iconbitmap(r'C:\Users\Shubh\Pictures\gui.ico')
    canvasWidth=1024
    canvasHeight=640
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="#4B4B4B")
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=root
    init(root, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))

    root.mainloop()


run()
