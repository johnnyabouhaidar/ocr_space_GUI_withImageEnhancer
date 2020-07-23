from tkinter import filedialog
from tkinter import *
from PIL import ImageTk , Image,ImageEnhance
import json
import requests
import os
import cv2
import numpy as np

mainWindow = Tk()
mainWindow.title('OCR.SPACE')
mainWindow.geometry('800x800')
def get_image_path():
    #####
    def ocrapicall():
        spinn = spnbox.get()
        txt=Text(mainWindow,height=20,width=80)
        txt.grid(row=4,column=2)

        img =Image.open(fnamevar)
        img=img.convert(mode='L')
        x,y=img.size
        img2=img.resize((x*1,y*1))
        #####....#####pillow_to_opencv_transition
        enhancer=ImageEnhance.Brightness(img2)
        enhanced_im = enhancer.enhance(float(spinn))
        newpath='newenhanced'+os.path.basename(fnamevar)
        enhanced_im.save(newpath,dpi=(300,300))
        enhanced_im2 = cv2.imread(newpath)
        #################
        kernel=np.ones((1,1),np.uint8)
        enhanced_im2 = cv2.dilate(enhanced_im2,kernel,iterations=1)
        enhanced_im2 = cv2.erode(enhanced_im2,kernel,iterations=1)
        newpath2='newnonoiseenhanced'+os.path.basename(fnamevar)
        cv2.imwrite(newpath2,enhanced_im2)
        #enhanced_im2.save(newpath2,dpi=(300,300))
        #enhanced_im.show()
        

        def ocr_space_file(filename, overlay=False, api_key='4c71bb1f0f88957', language='eng',table=False,pdf=False,scale=True,engine=1):
                payload = {'isOverlayRequired': overlay,
                        'apikey': api_key,
                        'language': language,
                        'isTable':table,
                        'isCreateSearchablePdf':pdf,
                        'scale':scale,
                        'OCREngine':engine
                       }
                with open(filename, 'rb') as f:
                    r = requests.post('https://api.ocr.space/parse/image',
                                  files={filename: f},
                                  data=payload,
                                  )
                return r.content.decode()

        test_file = ocr_space_file(filename=newpath2, language=lang.get(),table=True,engine = v.get())
        data=json.loads(test_file)
        with open('personal.json', 'w') as json_file:
                json.dump(data, json_file)

        for i in range(100):
                try:
                        line = data['ParsedResults'][0]['TextOverlay']['Lines'][i]['LineText']
                        if line[0]=='0':
                            line = line.replace('0','O',1)
                        txt.insert(END,line)
                        txt.insert(END,'\n')
                        
                except:
                        txt.insert(END,"----------------------------------")
                        txt.insert(END,"\n")
                        break
  
    
    mainWindow.filename = filedialog.askopenfilename(title = "Select image", filetypes =[("Image Files Only","*.jpg *.png *.jpeg")])
    fnamevar = mainWindow.filename
    img = ImageTk.PhotoImage(Image.open(fnamevar))
    imglbl=Label(mainWindow,image=img,height=700,width=700)
    imglbl.image=img
    imglbl.grid(row=4,column=0)
    brightlbl = Label(mainWindow, text="Adjust brightness").grid(row=0,column=2, sticky =W)
    spnbox = Spinbox(mainWindow, from_=0.0, to =2, format = '%.2f' , increment = 0.1)
    spnbox.grid(row=0,column = 1)
    v=IntVar()
    b = Radiobutton(mainWindow,text="Engine 1",variable = v,value = 1).grid(row = 2,column = 1,sticky = W)
    b = Radiobutton(mainWindow,text="Engine 2",variable = v,value = 2).grid(row = 3,column = 1,sticky = W)
    lang = StringVar()
    langentry = Entry(mainWindow,width =22,textvariable = lang).grid(row=1,column =1)
    langlbl = Label(mainWindow, text = "Enter language(ara or eng)").grid(row=1,column = 2,sticky =W)
    cnvrtbtn=Button(mainWindow,text='Convert to Text',command = ocrapicall).grid(row=4,column=1)

##############################
btn1=Button(mainWindow,text='Browse',command = get_image_path).grid(row=0,column=0)
mainWindow.mainloop()
