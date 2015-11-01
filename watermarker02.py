
#will be a program used to paste a watermark on a photo jpg. 
#using the Python Imaging Library (PIL)
# and the function PASTE
# http://effbot.org/imagingbook/image.htm

#Coming additions:
#Analyse resolution: recommending resolution increase on the wm image if to low compared to the photo itself
#make messages work!


#////////// VERSION NOTES//////////////////
# Version 0.2 Now allows black watermarks and png files selection for watermark file
# Version 0.1. First test release compiled for testing and feedback. Might still have problems with black watermarks. 



#//////IMPORTS////
from Tkinter import * #will build a GUI on Tk
import os
from tkFileDialog import askopenfilename, askopenfilenames, askdirectory #for browse for file functionality
from win32com.shell import shell, shellcon # from this we will get the desktop path suing SHGetFolderPath later on
from PIL import Image, ImageEnhance #actually from PILLOW, but called as PIL..... 


#/////Global functions/////
#none, as avoided


#////CLASSES/////
class Scale_and_Place_GUI(Frame): #making this its own class as it will involve several Tkinter objects and functions as it is made more complex in the future. Keeping GUI_App simple
    def __init__(self, parent):
        Frame.__init__(self, parent) #this is not standard, but I think the pack function is defined in the init of Frame, so I need to call it
        self.myParent = parent
        self.wm_position = StringVar(self.myParent)
        self.wm_position.set("bottom right") #variable which will be set using the position choice menu, has default bottom right
        self.do_scale = IntVar()
		
		#a toolbar with GUI objects from Tk
        self.gui_section1 = LabelFrame(self.myParent, text="Watermark Scale and Position", padx=5, pady=5)
        self.position_choice = OptionMenu(self.gui_section1,self.wm_position,"top left", "top right", "bottom left", "bottom right", "center") #an optin menu from which we can fetch the position of the watermark (selectable by the user)
        self.scale_checkbox = Checkbutton(self.gui_section1, text="use scale factor for watermark file", variable=self.do_scale) #checkbutton requires a Tkinter variable wrapper objekt
        self.scale_bar = Scale(self.gui_section1, from_=1, to=10, orient = HORIZONTAL)
        self.scale_bar.set(4) #setting the scaler denominator to 4 as default
		
		#labels above them
        self.scale_explanation = Label(self.gui_section1, text="Choose scale, bottom\n of photo / bottom of wm =")
        self.position_explanation = Label(self.gui_section1, text="Choose position\n of watermark")		
		
		#placing GUI objects
        #self.gui_section1.grid(row=0, column=0)
        self.scale_explanation.grid(row=0, column=2)
        self.position_explanation.grid(row=0, column=3)
        self.scale_checkbox.grid(row=1, column=1, sticky=(S, W))
        self.scale_bar.grid(row=1,column=2, sticky=(N))
        self.position_choice.grid(row=1, column=3)
        #self.position_choice.pack(side=RIGHT, padx=2, pady=2)
          
    #methods of the class    
        
    def get_scale(self):
        if self.do_scale.get() == 1:
            return self.scale_bar.get() #using get procedure on the variable as this variable is a Tkinter variable wrapper object
        else:
            return 1
		
    
    
    def get_position(self):
        return self.wm_position.get() #using get procedure on the variable as this variable is a Tkinter variable wrapper object
      
class Save_Options_GUI(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.myParent = parent
        #self.result_file_suffix = "_wm" #string used to name files that have been watermarked. default will be _wm
        self.store_location = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, None, 0) #a store location (folder) default is desktop
		
        #GUI elements
        self.gui_section1 = LabelFrame(self.myParent,text="Save Options",padx=5, pady=5) #LabelFrame is like a fram, but it gives a text and framing line grafically
        self.store_browse_button = Button(self.gui_section1, text ="select save folder", width = 16, command = self.store_browse_callback)
        self.store_location_label = Text(self.gui_section1, bg = "lightgrey", width = 25, height = 1, padx =5, pady=5) #text widget which will show path to storage folder
        self.file_suffix_input = Entry(self.gui_section1, width = 10)
        self.file_suffix_input.insert(0, "_wm")
		
		#labels
        self.suffix_explanation = Label(self.gui_section1, text="choose a suffix to add to\n the watermarked photo name:")
		
		#PLacing in the grid
		#self.gui_section1.grid() #not necessary, done in the main GUI_App widget
        self.store_browse_button.grid(row=1,column=2)
        self.store_location_label.grid(row=1, column=1)
        self.suffix_explanation.grid(row=0,column=1, sticky=(N,E))
        self.file_suffix_input.grid(row=0, column=2, sticky=(S,W))
        self.gui_section1.grid_rowconfigure(1, pad=15) #adding some space around the widgets in the row. done by calling its parent (which the rows are in)
        self.gui_section1.grid_rowconfigure(2, pad=15)
		
    def store_browse_callback(self):
        self.store_location = askdirectory(initialdir=self.store_location, title="choose where to store watermarked files")
        self.store_location_label.delete(1.0, END) #emptying the text widget
        self.store_location_label.config(width = len(self.store_location)+1)
        self.store_location_label.insert(INSERT, self.store_location) 

    def get_store_location(self):
		return self.store_location
	
    def get_file_suffix(self):
        self.result_file_suffix = self.file_suffix_input.get()	
        return self.result_file_suffix

	  
class GUI_App(object):
    def __init__(self, parent): #the parent will be my Tk root widget, which is not visual but contains all the visual elements.
        self.myParent = parent
        parent.config(background="grey")
        #self.photo_files =["C:/Users/seriman/Desktop/Testbild.jpg"]; #setting file path strings here for quick test runs
        #self.watermark_file = "C:/Users/seriman/Desktop/wm.png"
        
        self.message_text_string = "messages will be displayed here" #string variable used to set messages in the message window
        #..................structure elements of the GUI.....................
        #creating a toolbar with buttons
        
		#self.gui_window = Frame(self.myParent) #a frame widget in which I will place other button widgets etc. the frame is placed in the main widget defined above (top) called root
        #self.gui_window2 = Frame(self.myParent) # a second frame which will help place buttons and text widgets
        #self.gui_window3 = Frame(self.myParent) # a third
        #self.gui_window4 = Frame(self.myParent) # and a fourth one for the create button
		
        self.create_button = Button(self.myParent, text="Create", width=18, command= self.create_wm_photo) #still not an existing callback
        self.create_button.grid(row=6,column=1, columnspan=3, sticky=(W+E)) #W+E stretches it from side to side of the columns it said to occupy
        self.photo_browse_button = Button(self.myParent, text ="browse for photo file", width = 21, command = self.photo_browse_callback)
        self.photo_browse_button.grid(row=1,column=2, sticky=(W))
        self.wm_browse_button = Button(self.myParent, text ="browse for watermark file", width = 21, command = self.wm_browse_callback)
        self.wm_browse_button.grid(row=2, column=2, sticky=(W))
        self.exitbutton = Button(self.myParent, text="exit", width=6, command=self.exit_app)
        self.exitbutton.grid(row=0, column=3, sticky=(S, E))
        self.place_and_scaler = Scale_and_Place_GUI(self.myParent)
        
        self.place_and_scaler.gui_section1.grid(row=4, column=1, columnspan=3) #notice how I need to place this Frame in the subclass in the grid of this main GUI_App class
        self.messages = Message(self.myParent, text=self.message_text_string, width=800)
        self.messages.grid(row=7, column=1, columnspan=3)
        self.messages.config(relief=SUNKEN)
        self.myParent.grid_rowconfigure(7, pad=20) #some padding around the message box row
        self.expl_text1 = Label(self.myParent, text="Choose file(s) to watermark and watermark file")
        self.expl_text1.config(bg ="grey")
        self.expl_text1.grid(row=0,column=1,columnspan=2, sticky=(S, W))
        self.photo_file_label = Text(self.myParent, bg = "lightgrey", width = 25, height = 1, padx =5, pady=5) #text widget which will show the filename of the selected photo file for plotting
        self.photo_file_label.grid(row=1, column=1)
        self.wm_file_label = Text(self.myParent, bg = "lightgrey", width = 25, height = 1, padx =5, pady=5) #text widget which will show the filename of the selected watermark file
        self.wm_file_label.grid(row=2, column=1)
        self.store_location = Save_Options_GUI(self.myParent)
        self.store_location.gui_section1.grid(row=5,column=1, columnspan=3, sticky=(W+E)) #notice how we call a frame in the Save_Options object
        #self.placement_pane = Canvas(self.myParent, bg = "white", width = self.canvas_width, height = self.canvas_height) #area which will be used to display how the wm will be placed
        
        self.myParent.rowconfigure(0, pad=20)
        self.myParent.rowconfigure(4, pad=20)
        #............PACKING (i.e placing) all the elements in the GUI......... the order in which this is done is important for the placement, hence not the same as order of definitions of buttons etc above
        #pack method not used here for configuring the placing and spacing
        
        #self.create_button.pack() #the pack method is a geometry manager.. has options to place things, shift them to the left and so on
		
	#.............METHODS of the GUI_App class.......................
		
    def photo_browse_callback(self):
	#we want to change the value of photo_files, which is the list of strings that create will use when fetching the files will always use. 
        self.photo_files = askopenfilenames(filetypes = [("jpg-files", "*.jpg"),("gif-files", "*gif")], initialdir="C:\TEMP") #askopenfilemanes retrns a tuple/list of unicode strings. when printed out it gives u'string'
        #self.photo_files = files_string.split(str="", num=string.count(str))
        #print self.photo_files
        #print self.photo_files[0]
        #print self.photo_files[1]
        self.photo_file_label.delete(1.0, END) #emptying the text widget
        self.photo_file_label.config(width = len(self.photo_files[0])+1)
        self.photo_file_label.insert(INSERT, self.photo_files[0]) 
	
    def wm_browse_callback(self):
        self.watermark_file  = askopenfilename(filetypes = [("jpg-files", "*.jpg"),("gif-files", "*gif"),("png-files", "*png")], initialdir="C:\TEMP") #using askoopenfilename to get name ( search path string) of the file to plot 
        self.wm_file_label.delete(1.0, END) #emptying the text widget
        self.wm_file_label.config(width = len(self.watermark_file)+1)
        self.wm_file_label.insert(INSERT, self.watermark_file) 	
	
    def exit_app(self):
        self.myParent.destroy()
		
    def unblack(self, image): #method used to make black pixels in an image white. //turned out maybe not needed, not used in version 0.1//
        
        def makewhite(value):
            if value < 10:
                value = 200
            return value
        #im = image.convert(mode = "RGBA")# might have to do this, but it is not likely as it is converted before passed to the unblack method from create_wm_photo
        pixels = image.load() #loading pixel data
        w, h = image.size #getting the image size
        #print range(0, h+1)
        for j in xrange(0, h): #for each row
            for i in xrange(1, w): #for each pixel in each row
                #print pixels[i, j]
                    r, g, b, a = pixels[i, j] #seems not to be getting rgba channels here, but just one integer
                    if a != 0:
                        r2 = makewhite(r)
                        g2 = makewhite(g)
                        b2 = makewhite(b)
                        pixels[i, j] =(r2,g2,b2)
		# im = image.split()
        # R, G, B = 0, 1, 2
		
        # def makewhite(value):
            # if value < 10:
                # value = 200
            # return value
		
        # im[R] = im[R].point(makewhite)
        # im[G] = im[G].point(makewhite)
        # im[B] = im[B].point(makewhite)
		
        # image = im.merge(im.mode,im)
        return image		
	
	
	
    def create_wm_photo(self):
        """This method will take the photo image and paste the wm image on it. It will then save a new file in your wanted directory with the chosen extension/suffix of the filename"""
        #here introduce a for loop to go over all photo files selected in the list
        #position = self.wm_position.get()
        for i in self.photo_files: #cold maybe be done with list comprehension instead. more compact?
            photo = Image.open(i)
            wm = Image.open(self.watermark_file)
            wm = wm.convert(mode = "RGBA") #making sure it has all four channels

            # we have two image objects. Now we will have to analyze them a little, and adjust the watermark (wm) so that it gets an appropriate size
            scalefactor = self.place_and_scaler.get_scale()#calling the place and scale GUI to get the scale chosen
            position = self.place_and_scaler.get_position()#calling the place and scale GUI to get the position chosen
            name = os.path.basename(i)#taking away the search path from the filename (used below to store it)
            #print scalefactor
            #print position			
            #measures of the pictures photo file is AxB, and the watermark measures axb
            A = photo.size[0]
            #print A
            B = photo.size[1]
            #print B
            a = wm.size[0]
            #print a
            b = wm.size[1]
            #print b
            #resizing the watermark
            a_new = A/scalefactor
            #print a_new
            b_new = long(b*float(a_new)/float(a)) #resize takes an integer, but in order to get a_new/a > 0 it has to be a float during that calculation
            #print b_new
            wm = wm.resize((a_new,b_new)) #resize command returns a resized copy, I.e the assignement
            
            #wm_mask= wm
            #wm_mask = self.unblack(wm) #creating an alfa channel mask, with no black!
            wm_mask = wm
			#wm_mask.convert(mode="RGBA")
            #wm_mask.show()
			#TODO! Make sure to have smarter analysis done on the picture before going over every pixel of it..... if there is nothing black then it is not necessary
     		#making a white (at least where it is black fill opacity) alfa channel (transparency in rgnb (png) mask for the pasting
			#without the mask transparancy will not be kept in the wm image, and without it beeing white, black watermarks will not work
            #now placing the wm in the chosen position
            if position == "top left":
                photo.paste(wm,(0,0),wm_mask)
            elif position == "top right":
                photo.paste(wm,(A-a_new,0),wm_mask)
            elif position == "bottom left":
                photo.paste(wm,(0,B-b_new),wm_mask)
            elif position == "bottom right":
                photo.paste(wm,(A-a_new,B-b_new),wm_mask) #the last wm argument serves as an alpha channel mask, on the pnga format
            else:
                photo.paste(wm,(A/2,B/2),mask=wm_mask)
            #print i[:-4]+self.store_location.get_file_suffix()
            photo.save(self.store_location.get_store_location()+"\\"+name[:-4]+self.store_location.get_file_suffix()+name[-4:], quality=95) #notice that it is i which is the string with the filename (we do this for i in the tuple self.photo_files)
            self.message_text_string = "Done. nn files created on your desktop"
            self.messages.config(text=self.message_text_string)



#running mainloop
if __name__ == '__main__': #hiding my main logic behind a test for whether the code is being run or imported. other wise recursion gives me two Tk windows
    root = Tk() #will be my master widget
    watermarker_graphics = GUI_App(root)
    #The Tk class is instantiated without arguments. This creates a toplevel widget 
    #of Tk which usually is the main window of an application. Each instance has its own associated Tcl interpreter.
    root.mainloop() #Mainloop for my program, waiting for an "event"
