"""
Purpose: A user friendly GUI to display 2d images of a 3d scan.

Created by Dan Hudetz on 7/18/19
"""

import tkinter as t
import h5py as hdf
import numpy as np
import time
from PIL import Image, ImageTk
from scipy.ndimage import sobel

def showDrawing(event):
    threshold=thresholdScale.get()
    startTime=time.time()
    imageArray=np.array(dataSet[imageScale.get(),:,:])
    dimension=imageArray[0].size
    imageArray=(imageArray-imageArray.min())/(imageArray.max()-imageArray.min())*threshold/255
    maskArray=np.array(file.get(list(file.items())[0][0])[imageScale.get(),...])
    maskArray=sobel(maskArray)
    maskArray = np.sqrt(maskArray**2)
    minmaxLabel.configure(text="Min = "+str(imageArray.min())+" Max = "+str(imageArray.max()))
    maskArray=(maskArray-maskArray.min())/(maskArray.max()-maskArray.min())
    if not applyMask.get():
        finalArray=np.rint(imageArray*255)
    else:
        imageArray=np.rint(imageArray*255)
        rgbArray = np.zeros((dimension,dimension,3), 'uint8')     
        rgbArray[..., 0] = imageArray+maskArray*(255-thresholdScale.get())
        rgbArray[..., 1] = imageArray
        rgbArray[..., 2] = imageArray
        finalArray=rgbArray
    img=Image.fromarray(finalArray)
    img=img.resize((800,800))
    img=ImageTk.PhotoImage(master=window, image=img)

    window.dontDeleteMePlease=img
    canvas.create_image(pixelWidth, pixelHeight, image=img)
    print(time.time()-startTime)

fileLocation="\\\\wales.es.anl.gov\\DataArchive\\Software\\SegView\\sample_data\dataset_01.hdf5"
groupNumber=1

###############################################################################
window = t.Tk()
window.geometry("900x1000")
window.title("SegView")
###############################################################################
screen0=t.Frame(window)
screen0.pack()

pixelWidth=400
pixelHeight=400

print('Loading data...')
file=hdf.File(fileLocation, 'r')
dataSet=file.get(list(file.items())[1][0])
print('Finished loading.')

imageScale=t.Scale(screen0, from_=0, to=dataSet.len()-1, resolution=1, orient=t.HORIZONTAL, length=500)
imageScale.grid(row=2, column=0)
imageScale.bind("<ButtonRelease-1>", showDrawing)
imageScale.bind("<Motion>", showDrawing)
#imageScale.set(7649)

thresholdScale=t.Scale(screen0, from_=0, to=255, resolution=1, orient=t.HORIZONTAL, length=500)
thresholdScale.grid(row=3, column=0)
thresholdScale.bind("<ButtonRelease-1>", showDrawing)
thresholdScale.bind("<Motion>", showDrawing)

applyMask=t.IntVar()
check=t.Checkbutton(screen0, text="apply mask", var=applyMask)
check.grid(row=4, column=0)

minmaxLabel=t.Label(screen0, text="Min = Max =", font="Courier 14")
minmaxLabel.grid(row=1, column=0)

canvas=t.Canvas(screen0, width=pixelWidth*2, height=pixelHeight*2)
canvas.grid(row=0, column=0)

window.mainloop()
file.close()

