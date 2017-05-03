#thanks to Jan Bodnar for providing the code i built the GUI off of
#link to the website: http://zetcode.com/gui/tkinter/

#also thanks to alexwieder for providing some examples on opening and saving files
#that website is: https://tkinter.unpythonic.net/wiki/tkFileDialog
#tkinter: tkFileDialog (last edited 2015-09-17 17:40:10 by alexwieder)

from Tkinter import *

import Tkconstants, tkFileDialog
import tkColorChooser

import svgutils.transform as st
import sys
import svgutils.compose as sc
from lxml import etree
import lxml.etree as et
import lxml.builder
import math #for sqrt
import re #for finding all instances of a substring in a string

#defaults
global_stroke_width = '1px'
line_tolerance = 100
end_point_tolerance = 100
global_stroke_color = '#000000'

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("SVG Editor")
        self.pack(fill=BOTH, expand=1)

        self.btn = Button(self, text = 'Open SVG File',
            command=self.askopenfilename, width=15)
        #self.btn.place(x=30, y=220)
        self.btn.pack(anchor=W, padx=5, expand=False)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Stroke Width (include units):", width=25)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        self.entry1 = Entry(frame1)
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Line Tolerance (in px):", width=25)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        self.entry2 = Entry(frame2)
        self.entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        lbl3 = Label(frame3, text="End Point Tolerance (in px):", width=25)
        lbl3.pack(side=LEFT, padx=5, pady=5)

        self.entry3 = Entry(frame3)
        self.entry3.pack(fill=X, padx=5, expand=True)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbl4 = Label(frame4, text="Stroke Color (in #XxXxXx format):", width=25)
        lbl4.pack(side=LEFT, padx=5, pady=5)

        self.entry4 = Entry(frame4)
        self.entry4.pack(fill=X, padx=5, expand=True)

        self.btn = Button(self, text="Test Stroke Color",
            command=self.color_button_press, width=15)
        #self.btn.place(x=30, y=140)
        self.btn.pack(anchor=W, padx=5, expand=False)

        frame5 = Frame(self)
        frame5.pack(anchor=W)

        lbl5 = Label(frame5, text="Stroke Color:", width=18)
        lbl5.pack(anchor=W, padx=5, pady=5)

        self.frame = Frame(self, border=1,
            relief=SUNKEN, width=200, height=25)
        #self.frame.place(x=160, y=140)
        self.frame.place(x=175,y=188)

        self.btn = Button(self, text="Submit Inputs",
            command=self.submit, width=15)
        #self.btn.place(x=30, y=180)
        self.btn.pack(anchor=W, padx=5, expand=False)

        frame6 = Frame(self)
        frame6.pack(fill=X)

        lbl6 = Label(frame6, text="Name of Edited SVG:", width=25)
        lbl6.pack(side=LEFT, padx=5, pady=5)

        self.entry6 = Entry(frame6)
        self.entry6.pack(fill=X, padx=5, expand=True)

        #self.btn = Button(self, text = 'Save SVG',
        #    command=self.asksaveasfilename, width=15)
        #self.btn.place(x=30, y=260)
        #self.btn.pack(anchor=W, padx=5, expand=False)

        self.btn = Button(self, text = 'Run SVGedit',
            command=self.run_svgedit, width=30)
        #self.btn.place(x=30, y=260)
        self.btn.pack(anchor=W, padx=5, expand=False)

        self.btn = Button(self, text="Default Values",
            command=self.autopopulate_default_values, width=12)
        self.btn.place(x=30, y=180)
        self.btn.pack(anchor=E, padx=5, expand=False)

        self.btn = Button(self, text="?",
            command=self.help, width=2)
        self.btn.place(x=30, y=180)
        self.btn.pack(anchor=E, padx=5, expand=False)


        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.svg'
        options['filetypes'] = [('all files', '.*'), ('svg files', '.svg')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'edited_svg.svg'
        #options['parent'] = root
        options['title'] = 'This is a title'

        # This is only available on the Macintosh, and only when Navigation Services are installed.
        #options['message'] = 'message'

        # if you use the multiple file version of the module functions this option is set automatically.
        #options['multiple'] = 1

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        #options['parent'] = root
        options['title'] = 'This is a title'

    def askopenfilename(self):

        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        global filename
        filename = tkFileDialog.askopenfilename(**self.file_opt)

        frame0 = Frame(self)
        frame0.pack(fill=X)

        lbl0 = Label(frame0, text=filename, width=25)
        lbl0.pack(side=TOP, padx=5, pady=5)

        # open file on your own
        if filename:
          return open(filename, 'r')

    def asksaveasfilename(self):

        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        global edited_filename
        edited_filename = tkFileDialog.asksaveasfilename(**self.file_opt)

        # open file on your own
        if edited_filename:
          return open(edited_filename, 'w')

    def get_edited_filename(self):
        global edited_filename
        edited_filename = self.entry6.get()

    def submit(self):
        global global_stroke_width
        global line_tolerance
        global end_point_tolerance
        global global_stroke_color
        global_stroke_width = self.entry1.get()
        line_tolerance = self.entry2.get()
        end_point_tolerance = self.entry3.get()
        global_stroke_color = self.entry4.get()

    def color_button_press(self):
        global_stroke_color = self.entry4.get()
        self.frame.config(bg=global_stroke_color)

    def autopopulate_default_values(self):
        self.entry1.insert(END, '0.01mm')
        self.entry2.insert(END, '100')
        self.entry3.insert(END, '50')
        self.entry4.insert(END, '#FF0000')
        self.entry6.insert(END, 'edited svg')
        self.color_button_press()
        self.submit()

    def help(self):
        root = Tk()
        root.geometry("500x370+600+150")
        app = Help(root)
        root.mainloop()

    def run_svgedit(self):
        self.get_edited_filename()
        svgedit_setup()
        main_svgedit()

class Help(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Help and Recomendations")
        self.pack(fill=BOTH, expand=1)

        self.btn = Button(self, text = 'Pick the SVG file you want to edit',
            state=DISABLED, width=25)
        #self.btn.place(x=30, y=220)
        self.btn.pack(anchor=W, padx=5, expand=False)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Stroke Width (include units):", width=25, fg='grey')
        lbl1.pack(side=LEFT, padx=5, pady=5)

        self.entry1 = Entry(frame1)
        self.entry1.insert(END, '0.01mm')
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Line Tolerance (in px):", width=25, fg='grey')
        lbl2.pack(side=LEFT, padx=5, pady=5)

        self.entry2 = Entry(frame2)
        self.entry2.insert(END, '100')
        self.entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        lbl3 = Label(frame3, text="End Point Tolerance (in px):", width=25, fg='grey')
        lbl3.pack(side=LEFT, padx=5, pady=5)

        self.entry3 = Entry(frame3)
        self.entry3.insert(END, '50')
        self.entry3.pack(fill=X, padx=5, expand=True)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbl4 = Label(frame4, text="Stroke Color (in #XxXxXx format):", width=25, fg='grey')
        lbl4.pack(side=LEFT, padx=5, pady=5)

        self.entry4 = Entry(frame4)
        self.entry4.insert(END, '#FF0000')
        self.entry4.pack(fill=X, padx=5, expand=True)

        self.btn = Button(self, text="See what color the paths will become",
            state=DISABLED, width=30)
        #self.btn.place(x=30, y=140)
        self.btn.pack(anchor=W, padx=5, expand=False)

        frame5 = Frame(self)
        frame5.pack(anchor=W)

        lbl5 = Label(frame5, text="Stroke Color:", width=18, fg='grey')
        lbl5.pack(anchor=W, padx=5, pady=5)

        self.frame = Frame(self, border=1,
            relief=SUNKEN, width=200, height=25)
        #self.frame.place(x=160, y=140)
        self.frame.place(x=175,y=188)

        self.btn = Button(self, text="Save the inputs, these will affect the edited svg",
            state=DISABLED, width=34)
        #self.btn.place(x=30, y=180)
        self.btn.pack(anchor=W, padx=5, expand=False)

        frame6 = Frame(self)
        frame6.pack(fill=X)

        lbl6 = Label(frame6, text="Name of new SVG (extension unnecessary):", width=31, fg='grey')
        lbl6.pack(side=LEFT, padx=5, pady=5)

        self.entry6 = Entry(frame6)
        self.entry6.pack(fill=X, padx=5, expand=True)

        self.btn = Button(self, text = 'Create a new SVG with edited values',
            state=DISABLED, width=30)
        #self.btn.place(x=30, y=260)
        self.btn.pack(anchor=W, padx=5, expand=False)

        self.btn = Button(self, text="Opens this window",
            state=DISABLED, width=15)
        self.btn.place(x=30, y=180)
        self.btn.pack(anchor=E, padx=5, expand=False)

        frame0 = Frame(self)
        frame0.pack(fill=X)

        lbl0 = Label(frame0, text='Directory and name of svg that will be edited', width=35, fg='grey')
        lbl0.pack(side=TOP, padx=5, pady=5)

        #self.btn = Button(self, text="Quit",
        #    command=quit, width=20)
        #self.btn.place(x=30, y=180)
        #self.btn.pack(anchor=S, padx=5, expand=False)


def svgedit_setup():
    global tree
    tree = etree.parse(filename, etree.XMLParser())
    global drawing_as_string
    drawing_as_string = etree.tostring(tree.getroot())

#find instances of a char in a string
#returns an array with values corresonding to locations of char
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

#returns string of drawing with all stroke width changed to desired width
def change_stroke_width(newwidth):
    stroke_width_arr = [m.start() for m in re.finditer('stroke-width:', drawing_as_string)] # array of index instances of substing in sting
    new_drawing_as_string = drawing_as_string

    iterations = 0
    new_arr = [new_drawing_as_string.find('stroke-width:')]

    for i in stroke_width_arr:
        local_stroke_width = new_drawing_as_string[new_arr[iterations]:new_drawing_as_string.find(';', new_arr[iterations])] #gives the string describing stroke-width

        new_drawing_as_string = new_drawing_as_string[0:new_arr[iterations]] + 'stroke-width:' + newwidth + new_drawing_as_string[new_arr[iterations] + len(local_stroke_width):len(new_drawing_as_string)]

        new_arr.append(new_drawing_as_string.find('stroke-width:', new_arr[iterations] + 1))
        iterations += 1

    return new_drawing_as_string

#returns a string of the drawing with newvalue replacing the old value of 'name_of_value'
#name_of_value must be exact and include the ':'
def change_value_of(newvalue, name_of_value):
    arr = [m.start() for m in re.finditer(name_of_value, drawing_as_string)] # array of index instances of substing in sting
    new_drawing_as_string = drawing_as_string

    iterations = 0
    new_arr = [new_drawing_as_string.find(name_of_value)]

    for i in arr:
        local_value = new_drawing_as_string[new_arr[iterations]:new_drawing_as_string.find(';', new_arr[iterations])] #gives the string describing vvalue

        new_drawing_as_string = new_drawing_as_string[0:new_arr[iterations]] + name_of_value + newvalue + new_drawing_as_string[new_arr[iterations] + len(local_value):len(new_drawing_as_string)]

        new_arr.append(new_drawing_as_string.find(name_of_value, new_arr[iterations] + 1))
        iterations += 1

    return new_drawing_as_string

#takes in a string of a path
#returns the end points of that path in x,y
def get_end_points(element):
    if "c" in element.get("d"): #stops function if dealing with a piecewise path
        return "Piecewise"

    if element.get("d").startswith("m"):
        commas = find(element.get("d"), ',')
        spaces = find(element.get("d"), ' ')

        #i stands for inital, f stands for final
        xis = element.get("d")[spaces[0]     : commas[0]] #variable + 's' = a string of that variable
        yis = element.get("d")[commas[0] + 1 : spaces[1]] #-1 is to remove comma from output
        change_in_xis = element.get("d")[spaces[1] : commas[1]]
        change_in_yis = element.get("d")[commas[1] + 1: ]          #-1 is to remove comma from output, end point is end of string

        xi = float(xis) #change strings into floats
        yi = float(yis)
        change_in_xi = float(change_in_xis)
        change_in_yi = float(change_in_yis)

        xf = xi + change_in_xi #create x,y coords based of x1 and y1 and their change variable
        yf = yi + change_in_yi

        list = [[xi,yi],[xf,yf]]
        return list #retruns the two x,y coords that coorespond to the start and end of the straight path

#returns color of lines in hex
def get_stroke_color(element):
    return element.get("style")[element.get("style").find("stroke") + len("stroke:#") : element.get("style").find("stroke") + len("stroke:#") + 6] #substring from 'style' marker, from 'stroke:#' to the end of the hex number(6 digits)

def get_stroke_width(element):
    return element.get("style")[element.get("style").find("stroke-width:") + len("stroke-width:") : element.get("style").find(";stroke-linecap:")]

#removes a line of the two lines are close enough
def check_similar_lines(line1,line2):
    new_drawing_as_string = drawing_as_string
    if line1[1] == line2[1]: #checks for same color

        xi1 = line1[0][0][0]
        yi1 = line1[0][0][1]
        xf1 = line1[0][1][0]
        yf1 = line1[0][1][1]

        xi2 = line2[0][0][0]
        yi2 = line2[0][0][1]
        xf2 = line2[0][1][0]
        yf2 = line2[0][1][1]

        if line_tolerance > math.sqrt(math.pow(xi1-xi2,2) + math.pow(yi1-yi2,2)) and line_tolerance > math.sqrt(math.pow(xf1-xf2,2) + math.pow(yf1-yf2,2)): #checks if the lines share similar start and end conditions
            new_drawing_as_string = remove_line(line1) #removes one line if they are close enough

        if line_tolerance > math.sqrt(math.pow(xi1-xf2,2) + math.pow(yi1-yf2,2)) and line_tolerance > math.sqrt(math.pow(xf1-xi2,2) + math.pow(yf1-yi2,2)): #same as previous if statment, but allows for lines going in the oppistie directions
            new_drawing_as_string = remove_line(line1)#removes one line if they are close enough

    return new_drawing_as_string

#takes two lines, compares color, then compares how close the endpoints are
#draws a line between the points if true
def check_points(line1, line2):
    if line1[1] == line2[1]: #checks for same color

        xi1 = line1[0][0][0]
        yi1 = line1[0][0][1]
        xf1 = line1[0][1][0]
        yf1 = line1[0][1][1]

        xi2 = line2[0][0][0]
        yi2 = line2[0][0][1]
        xf2 = line2[0][1][0]
        yf2 = line2[0][1][1]

        if end_point_tolerance > math.sqrt(math.pow(xi1-xi2,2) + math.pow(yi1-yi2,2)):
            new_line1 = sc.Line([[xi1,yi1],[xi2,yi2]], global_stroke_width, global_stroke_color) #second input is width in
            new_drawing_as_string = draw_line(new_line1)
        if end_point_tolerance > math.sqrt(math.pow(xi1-xf2,2) + math.pow(yi1-yf2,2)):
            new_line2 = sc.Line([[xi1,yi1],[xf2,yf2]], global_stroke_width, global_stroke_color)
            new_drawing_as_string = draw_line(new_line2)
        if end_point_tolerance > math.sqrt(math.pow(xf1-xi2,2) + math.pow(yf1-yi2,2)):
            new_line3 = sc.Line([[xf1,yf1],[xi2,yi2]], global_stroke_width, global_stroke_color)
            new_drawing_as_string = draw_line(new_line3)
        if end_point_tolerance > math.sqrt(math.pow(xf1-xf2,2) + math.pow(yf1-yf2,2)):
            new_line4 = sc.Line([[xf1,yf1],[xf2,yf2]], global_stroke_width, global_stroke_color)
            new_drawing_as_string = draw_line(new_line4)

    return new_drawing_as_string

#returns element tree with line element added in
#line is a svg element
def draw_line(line):
    first_of_new_str = drawing_as_string[0:drawing_as_string.find('>', drawing_as_string.rfind('<path')) + 1]
    end_of_new_str = drawing_as_string[drawing_as_string.find('>', drawing_as_string.rfind('<path')) + 1 : len(drawing_as_string)]

    new_drawing_as_string = first_of_new_str + '\n' + line.tostr() + end_of_new_str

    return new_drawing_as_string

#line is an array
def remove_line(line):
    new_drawing_as_string = drawing_as_string

    line_xi = line[0][0][0]
    line_yi = line[0][0][1]
    line_xf = line[0][1][0]
    line_yf = line[0][1][1]

    line_x = line_xi
    line_y = line_yi
    line_change_x = line_xf-line_xi
    line_change_y = line_yf-line_yi

    #line_end_points = str(xi) + ',' + str(yi) + ' ' + str(change_in_x) + ',' + str(change_in_y)
    line_color = line[1]
    #line_stoke_width =

    stroke_width_arr =  [m.start() for m in re.finditer('<path', drawing_as_string)]

    for i in stroke_width_arr:
        local_path = drawing_as_string[i:drawing_as_string.find('/>', i)] #gives the string describing the specific path

        local_color = local_path[local_path.find('stroke:') : local_path.find('stroke:') + len('stroke:') + 7] #gives string desribing path color, 7 is the length of a hexcode (#123456)
        #local_stroke_width = local_path[local_path.find('stroke-width:'):local_path.find(';',local_path.find('stroke-width:'))] #gives the string describing stroke-width
        local_end_points_str = local_path[local_path.find('d="') + len('d="m '):local_path.find('" ',local_path.find('d="'))]

        if 'c' in local_end_points_str:
            continue

        comma1 = local_end_points_str.find(',')
        comma2 = local_end_points_str.rfind(',')
        space = local_end_points_str.find(' ')

        local_end_points = [[local_end_points_str[0:comma1], local_end_points_str[comma1+1:space]], [local_end_points_str[space+1:comma2], local_end_points_str[comma2+1:len(local_end_points_str)]] ]

        local_x = local_end_points[0][0]
        local_y= local_end_points[0][1]
        local_change_x = local_end_points[1][0]
        local_change_y = local_end_points[1][1]

        if line_x == local_x and line_y == local_x and line_change_x == local_change_x and line_change_y == local_change_y:
            new_drawing_as_string = drawing_as_string[0 : drawing_as_string.find(local_path)] + drawing_as_string[drawing_as_string.find('/>', drawing_as_string.find(local_path)) : end]

    return new_drawing_as_string

#main method that runs the code
def main_svgedit():
    global drawing_as_string

    drawing_as_string = change_stroke_width(global_stroke_width)

    #goes through svg file and looks only at the elements that are labeled 'path'
    #numoflines is equal to the number of staight paths
    num_of_lines = 0
    for element in tree.iter():
        if element.tag.split("}")[1] == "path":
            if "c" not in element.get("d"):
                num_of_lines += 1

    #list of endpoints of straight lines and color
    #pathlist is in the format  { [ [ (xi,yi), (xf,yf) ], [color] ] , [ [ (xi,yi), (xf,yf) ], [color] ]}
    path_list = [None] * num_of_lines
    k = 0
    for element in tree.iter():
        if element.tag.split("}")[1] == "path":
            if "c" not in element.get("d"):
                path_list[k] = [get_end_points(element) , get_stroke_color(element)]
                k += 1

    for i in range(0,k):
        for j in range(0,k):
            if i == j: continue
            drawing_as_string = check_similar_lines(path_list[i],path_list[j])

    for i in range(0,k):
        for j in range(0,k):
            if i == j: continue
            drawing_as_string = check_points(path_list[i],path_list[j])

    drawing_as_string = change_value_of(global_stroke_color, 'stroke:')

    rootsvg = etree.fromstring(drawing_as_string)
    doc = etree.ElementTree(rootsvg)
    #global edited_filename
    doc.write(edited_filename + '.svg')

def main():
    global root
    root = Tk()
    root.geometry("430x370+150+150")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
