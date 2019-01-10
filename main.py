from tkinter import *
from tkinter import filedialog
import pandas as pd
import time
import pickle

colors = ['red','orange','gold','lime green','navy','dodger blue','dark violet']
greys = ['grey34','grey37','grey41','grey45','grey49','grey53','grey57','grey61','grey65','grey69']



class Kinetics(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.fm_1 = LabelFrame(self.master, text='Viewer', width=wid-200)
        self.fm_1.propagate(False)
        self.fm_1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.fm_2 = LabelFrame(self.master, text='Settings', width=200)
        self.fm_2.propagate(False)
        self.fm_2.pack(side=LEFT, fill=BOTH, expand=YES)

        # parameters
        self.upper_frame_limit = 1000  # will be overwritten either by reading in new frames or loading previous data
        self.scale_factor = 3  # enlarge by x times
        self.start_frame = 300
        self.end_frame = 450
        self.skip_frame = 5
        self.velocity_normalization_factor = 6.0
        self.acceleration_normalization_factor = 180.0
        self.offset_x = -200
        self.offset_y = -50
        self.sleep_time = 0

        self.filename='data1.csv'

        # Controllers
        self.lb1 = Label(self.fm_2, text='From frame:')
        self.lb1.pack(side=TOP, anchor='w')

        self.str1 = StringVar()
        self.str1.set(self.start_frame)
        self.spb1 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.upper_frame_limit,
                            increment=1,
                            textvariable=self.str1,
                            command=self.set_start_frame)
        self.spb1.pack(side=TOP)

        self.lb2 = Label(self.fm_2, text='To frame:')
        self.lb2.pack(side=TOP, anchor='w')

        self.str2 = StringVar()
        self.str2.set(self.end_frame)
        self.spb2 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.upper_frame_limit,
                            increment=1,
                            textvariable=self.str2,
                            command=self.set_end_frame)
        self.spb2.pack(side=TOP)

        self.lb3 = Label(self.fm_2, text='Skip ? frame:')
        self.lb3.pack(side=TOP, anchor='w')

        self.str3 = StringVar()
        self.str3.set(self.skip_frame)
        self.spb3 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.upper_frame_limit,
                            increment=1,
                            textvariable=self.str3,
                            command=self.set_skip_frame)
        self.spb3.pack(side=TOP)

        self.lb4 = Label(self.fm_2, text='Offset X:')
        self.lb4.pack(side=TOP, anchor='w')

        self.str4 = StringVar()
        self.str4.set(self.offset_x)
        self.spb4 = Spinbox(self.fm_2,
                            # from_=0,
                            # to=800,
                            increment=1,
                            textvariable=self.str4,
                            command=self.set_offset_x)
        self.spb4.pack(side=TOP)

        self.lb5 = Label(self.fm_2, text='Offset Y:')
        self.lb5.pack(side=TOP, anchor='w')

        self.str5 = StringVar()
        self.str5.set(self.offset_y)
        self.spb5 = Spinbox(self.fm_2,
                            # from_=0,
                            # to=600,
                            increment=1,
                            textvariable=self.str5,
                            command=self.set_offset_y)
        self.spb5.pack(side=TOP)

        self.lb6 = Label(self.fm_2, text='Sleep time:')
        self.lb6.pack(side=TOP, anchor='w')

        self.str6 = StringVar()
        self.str6.set(self.sleep_time)
        self.spb6 = Spinbox(self.fm_2,
                            from_=0,
                            # to=600,
                            increment=0.01,
                            textvariable=self.str6,
                            command=self.set_sleep_time)
        self.spb6.pack(side=TOP)

        self.chkvar1 = IntVar()
        self.chkvar1.set(1)
        self.chkvar2 = IntVar()
        self.chkvar2.set(0)
        self.chkbtn1 = Checkbutton(self.fm_2, text="Draw sticks", variable=self.chkvar1,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn2 = Checkbutton(self.fm_2, text="Draw in colors", variable=self.chkvar2,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn1.pack(side=TOP, anchor='w')
        self.chkbtn2.pack(side=TOP, anchor='w')

        self.btn1 = Button(self.fm_2, text='Start over', width=100, command=self.start_over)
        self.btn1.pack(side=BOTTOM)

        self.lb_frame_counter_str = StringVar()
        self.lb_frame_counter_str.set("Frame "+str(0))
        self.lb_frame = Label(self.fm_2, textvariable=self.lb_frame_counter_str)
        self.lb_frame.pack(side=BOTTOM)

        self.lb_frame_total_str = StringVar()
        self.lb_frame_total_str.set("Total frames: " + str(self.upper_frame_limit))
        self.lb_frame = Label(self.fm_2, textvariable=self.lb_frame_total_str)
        self.lb_frame.pack(side=BOTTOM)

        self.btn2 = Button(self.fm_2, text='Load file', width=100, command=self.load_file)
        self.btn2.pack(side=BOTTOM)
        self.lb_file_name = Label(self.fm_2, text=self.filename, height=150, justify='center', wraplength=180)
        self.lb_file_name.pack(side=BOTTOM)

        self.canvas = Canvas(self.fm_1)
        self.canvas.config(width=wid-200, height=hei)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)
        self.pack(fill=BOTH, expand=1)

        # read file

        self.read_in()

    def read_in(self):
        self.time_frames = []
        try:
            f = open(self.filename+'.frames', "rb")
            self.time_frames = pickle.load(f)
            self.upper_frame_limit = len(self.time_frames)
            f.close()
            self.lb_frame_total_str.set("Total frames: "+str(self.upper_frame_limit))
            print("Time frame data loaded.")
        except IOError:
            print("Time frame data file is not found. Generating...")
            #self.filename = 'data1.csv'
            self.data = None
            self.read_csv_data(self.filename)

            # generate time frames
            # self.time_frames=[]
            self.generate_time_frames()
            f = open(self.filename+'.frames', "wb")
            pickle.dump(self.time_frames, f)
            self.upper_frame_limit = len(self.time_frames)
            f.close()
            self.lb_frame_total_str.set("Total frames: "+str(self.upper_frame_limit))
            print("Time frame data saved.")

        # automatically draw time frames and trajectory
        # self.draw_all_time_frames()

    def draw_all_time_frames(self):
        print("Start drawing time frames")
        self.critical_point = {} # the first point going upward
        drawing_counter = 0 # Counting time frames to determine the color in color mode
        self.last_point = [0,0] # Store the last point for drawing trajectory
        for i in range(len(self.time_frames)):
            t = self.time_frames[i] # temporary variable, the current time frame

            # Draw the sticks
            if i % int(self.skip_frame) == 0 and int(self.start_frame) <= i <= int(self.end_frame): # 200 Hz -> lower frequency
                if self.chkvar1.get() == 1:  # Check if to draw the sticks
                    self.draw_stick(
                        [t.info['Y1'], t.info['Z1'], t.info['Y2'], t.info['Z2'],
                         t.info['Y3'], t.info['Z3'], t.info['Y4'], t.info['Z4'],
                         t.info['Y5'], t.info['Z5']],
                        color= colors[drawing_counter%7] if self.chkvar2.get() == 1 else greys[drawing_counter%10]
                    )

                # Draw velocity and acceleration for every point
                current_point = {}
                current_point['Y5'] = self.flip_x(self.transform(t.info['Y5']))
                current_point['Z5'] = self.flip_y(self.transform(t.info['Z5']))
                current_point['Y5v'] = t.info['Y5\'']
                current_point['Z5v'] = t.info['Z5\'']
                current_point['Y5a'] = t.info['Y5\'\'']
                current_point['Z5a'] = t.info['Z5\'\'']
                current_point['yz_combined_velocity'] = t.info['yz_combined_velocity']
                current_point['yz_combined_acceleration'] = t.info['yz_combined_acceleration']
                self.draw_velocity_acceleration(current_point)

                print("Time frame " + str(t.number) + " drawn.")
                self.lb_frame_counter_str.set("Frame "+str(t.number))

                drawing_counter += 1  # Counting time frames

                time.sleep(self.sleep_time)

            # Draw the trajectory
            if int(self.start_frame) <= i <= int(self.end_frame): # Apply to every time frame
                if self.last_point != [0,0]: # When it's not the first frame
                    self.draw_trajectory(t)
                self.last_point[0] = self.flip_x(self.transform(t.info['Y5']))
                self.last_point[1] = self.flip_y(self.transform(t.info['Z5']))
        # Draw the last part to close the trajectory
        self.draw_trajectory(t)

        print(self.critical_point)

    def set_start_frame(self):
        self.start_frame = int(self.spb1.get())

    def set_end_frame(self):
        self.end_frame = int(self.spb2.get())

    def set_skip_frame(self):
        self.skip_frame = int(self.spb3.get())

    def set_offset_x(self):
        self.offset_x = int(self.spb4.get())

    def set_offset_y(self):
        self.offset_y = int(self.spb5.get())

    def set_sleep_time(self):
        self.sleep_time = float(self.spb6.get())

    def start_over(self):
        # manually update parameters
        self.set_start_frame()
        self.set_end_frame()
        self.set_skip_frame()
        self.set_offset_x()
        self.set_offset_y()
        self.set_sleep_time()

        self.canvas.delete('all')
        self.canvas.update()

        #self.time_frames = []
        #self.generate_time_frames()
        self.draw_all_time_frames()

    def load_file(self):
        new_filename = filedialog.askopenfilename()
        if self.filename != new_filename:
            self.filename = new_filename
            if self.filename != '':
                self.lb_file_name.config(text="File: "+self.filename)
                self.read_in()


    def draw_velocity_acceleration(self,p):
        # Draw velocity arrow
        #scale_factor_v = p['yz_combined_velocity']/velocity_normalization_factor
        # print(scale_factor_v)
        self.canvas.create_line(p['Y5']+self.offset_x,p['Z5']+self.offset_y, p['Y5']-p['Y5v']/self.velocity_normalization_factor+self.offset_x, p['Z5']-p['Z5v']/self.velocity_normalization_factor+self.offset_y, arrow=LAST, fill='black')

        # Draw acceleration arrow
        #scale_factor_a = p['yz_combined_velocity']/acceleration_normalization_factor
        #print(scale_factor_a)
        self.canvas.create_line(p['Y5']+self.offset_x,p['Z5']+self.offset_y, p['Y5']-p['Y5a']/self.acceleration_normalization_factor+self.offset_x, p['Z5']-p['Z5a']/self.acceleration_normalization_factor+self.offset_y, arrow=LAST, fill='red')

        self.canvas.update()

    def draw_trajectory(self,t):
        if self.last_point[1] < 397:  # self.flip_y(self.transform(t.info['Z5'])): # moving upward, set color
            c = colors[5]
            if self.critical_point == {}: # record this point as the first point upward
                # cannot let self.critical_point = info, because = has a different meaning when used between dicts
                self.critical_point['Y5'] = self.flip_x(self.transform(t.info['Y5']))
                self.critical_point['Z5'] = self.flip_y(self.transform(t.info['Z5']))
                self.critical_point['Y5v'] = t.info['Y5\'']
                self.critical_point['Z5v'] = t.info['Z5\'']
                self.critical_point['Y5a'] = t.info['Y5\'\'']
                self.critical_point['Z5a'] = t.info['Z5\'\'']
                self.critical_point['yz_combined_velocity'] = t.info['yz_combined_velocity']
                self.critical_point['yz_combined_acceleration'] = t.info['yz_combined_acceleration']
                self.draw_velocity_acceleration(self.critical_point)
        else:  # not moving upward, set color
            c = 'grey40'
        self.canvas.create_line(self.last_point[0]+self.offset_x, self.last_point[1]+self.offset_y, self.flip_x(self.transform(t.info['Y5']))+self.offset_x,
                                self.flip_y(self.transform(t.info['Z5']))+self.offset_y, fill=c, width=2)
        self.canvas.update()

    def draw_stick(self,pts,color):
        pts_scaled=[]
        for p in pts:
            pts_scaled.append(self.transform(p)) # enlarge by 5 times then offset backward
        # Draw the sticks
        self.canvas.create_line(self.flip_x(pts_scaled[0])+self.offset_x, self.flip_y(pts_scaled[1])+self.offset_y, self.flip_x(pts_scaled[2])+self.offset_x,
                                self.flip_y(pts_scaled[3])+self.offset_y, self.flip_x(pts_scaled[4])+self.offset_x, self.flip_y(pts_scaled[5])+self.offset_y,
                                self.flip_x(pts_scaled[6])+self.offset_x, self.flip_y(pts_scaled[7])+self.offset_y, self.flip_x(pts_scaled[8])+self.offset_x,
                                self.flip_y(pts_scaled[9])+self.offset_y, fill=color, width=2)
        # Draw the joints
        self.draw_dot(self.flip_x(pts_scaled[0]), self.flip_y(pts_scaled[1]))
        self.draw_dot(self.flip_x(pts_scaled[2]), self.flip_y(pts_scaled[3]))
        self.draw_dot(self.flip_x(pts_scaled[4]), self.flip_y(pts_scaled[5]))
        self.draw_dot(self.flip_x(pts_scaled[6]), self.flip_y(pts_scaled[7]))
        # self.draw_dot(800-pts_scaled[8], 600-pts_scaled[9]) # Don't draw this last black dot. It will be in blue/grey.
        self.canvas.update()

    def draw_dot(self,x,y,color='black'):
        self.canvas.create_line(x+self.offset_x,y+self.offset_y,x+self.offset_x,y+1+self.offset_y,fill=color)

    def transform(self,a):
        new_a = a * self.scale_factor + 0
        return new_a

    def flip_x(self,b):
        new_b = wid - b
        return new_b

    def flip_y(self,c):
        new_c = hei - c
        return new_c

    def read_csv_data(self,fn):
        self.data = pd.read_csv(fn)
        print("Successfully read in "+fn+",")

    def generate_time_frames(self):
        print("Generating time frames...")
        column_titles =[]
        for line_list in self.data:
            column_titles.append(line_list)

        #for i in range(self.data.shape[0]):
        self.upper_frame_limit = self.data.shape[0]

        for i in range(self.upper_frame_limit):
            information = {}
            for title in column_titles:
                information[title]=self.data[title].tolist()[i]
            self.time_frames.append(TimeFrame(i,information))


class TimeFrame:

    """A frame of kinetics, depicting a certain time point"""

    def __init__(self,n,i):
        self.number = n
        self.info = i
        print("Added time frame number "+str(n))


if __name__ == '__main__':
    root = Tk()
    wid = 1000
    hei = 800
    root.wm_title("Kinetics")
    root.geometry(str(wid) + "x" + str(hei) + "+1000+100")
    app = Kinetics(root)
    root.mainloop()
