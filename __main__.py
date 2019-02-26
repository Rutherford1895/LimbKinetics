from tkinter import *
from tkinter import filedialog
import pandas as pd
import time
import pickle

colors = ['red', 'orange', 'gold', 'lime green', 'navy', 'dodger blue', 'dark violet']
greys = ['grey34', 'grey37', 'grey41', 'grey45', 'grey49', 'grey53', 'grey57', 'grey61', 'grey65', 'grey69']


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
        self.parameters = {"upper_frame_limit": 5000,
                           "lower_frame_limit": 0,
                           "scale_factor": 3,
                           "start_frame": 300,
                           "end_frame": 430,
                           "skip_frame": 10,
                           "velocity_normalization_factor": 6.0,
                           "acceleration_normalization_factor": 180.0,
                           "offset_x": -50,
                           "offset_y": -150,
                           "sleep_time": 0,
                           "upward_start_frame": 405,
                           "upward_end_frame": 430,
                           "threshold_on": 413
                           }

        self.filename = 'data1.csv'

        # Controllers
        # Top-down layout
        self.lb1 = Label(self.fm_2, text='From frame:')
        self.lb1.pack(side=TOP, anchor='w')

        self.str1 = StringVar()
        self.str1.set(self.parameters['start_frame'])
        self.spb1 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.parameters['upper_frame_limit'],
                            increment=1,
                            textvariable=self.str1,
                            command=self.set_start_frame)
        self.spb1.pack(side=TOP)

        self.lb2 = Label(self.fm_2, text='To frame:')
        self.lb2.pack(side=TOP, anchor='w')

        self.str2 = StringVar()
        self.str2.set(self.parameters['end_frame'])
        self.spb2 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.parameters['upper_frame_limit'],
                            increment=1,
                            textvariable=self.str2,
                            command=self.set_end_frame)
        self.spb2.pack(side=TOP)

        self.lb3 = Label(self.fm_2, text='Skip ? frame:')
        self.lb3.pack(side=TOP, anchor='w')

        self.str3 = StringVar()
        self.str3.set(self.parameters['skip_frame'])
        self.spb3 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.parameters['upper_frame_limit'],
                            increment=1,
                            textvariable=self.str3,
                            command=self.set_skip_frame)
        self.spb3.pack(side=TOP)

        self.lb4 = Label(self.fm_2, text='Offset X:')
        self.lb4.pack(side=TOP, anchor='w')

        self.str4 = StringVar()
        self.str4.set(self.parameters['offset_x'])
        self.spb4 = Spinbox(self.fm_2,
                            from_=(wid-200)*(-1),
                            to=(wid-200),
                            increment=1,
                            textvariable=self.str4,
                            command=self.set_offset_x)
        self.spb4.pack(side=TOP)

        self.lb5 = Label(self.fm_2, text='Offset Y:')
        self.lb5.pack(side=TOP, anchor='w')

        self.str5 = StringVar()
        self.str5.set(self.parameters['offset_y'])
        self.spb5 = Spinbox(self.fm_2,
                            from_=hei*(-1),
                            to=hei,
                            increment=1,
                            textvariable=self.str5,
                            command=self.set_offset_y)
        self.spb5.pack(side=TOP)

        self.lb6 = Label(self.fm_2, text='Sleep time:')
        self.lb6.pack(side=TOP, anchor='w')

        self.str6 = StringVar()
        self.str6.set(self.parameters['sleep_time'])
        self.spb6 = Spinbox(self.fm_2,
                            from_=0,
                            to=1,
                            increment=0.01,
                            textvariable=self.str6,
                            command=self.set_sleep_time)
        self.spb6.pack(side=TOP)

        self.lb7 = Label(self.fm_2, text='Upward starting by:')
        self.lb7.pack(side=TOP, anchor='w')

        self.str7 = StringVar()
        self.str7.set(self.parameters['upward_start_frame'])
        self.spb7 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.parameters['upper_frame_limit'],
                            increment=1,
                            textvariable=self.str7,
                            command=self.set_upward_start_frame)
        self.spb7.pack(side=TOP)

        self.lb8 = Label(self.fm_2, text='Upward ending by:')
        self.lb8.pack(side=TOP, anchor='w')

        self.str8 = StringVar()
        self.str8.set(self.parameters['upward_end_frame'])
        self.spb8 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.parameters['upper_frame_limit'],
                            increment=1,
                            textvariable=self.str8,
                            command=self.set_upward_end_frame)
        self.spb8.pack(side=TOP)

        self.lb9 = Label(self.fm_2, text='Threshold on:')
        self.lb9.pack(side=TOP, anchor='w')

        self.str9 = StringVar()
        self.str9.set(self.parameters['threshold_on'])
        self.spb9 = Spinbox(self.fm_2,
                            from_=1,
                            to=self.parameters['upper_frame_limit'],
                            increment=1,
                            textvariable=self.str9,
                            command=self.set_threshold_on)
        self.spb9.pack(side=TOP)

        self.chkvar1 = IntVar()
        self.chkvar1.set(1)
        self.chkbtn1 = Checkbutton(self.fm_2, text="Draw sticks", variable=self.chkvar1,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn1.pack(side=TOP, anchor='w')

        self.chkvar2 = IntVar()
        self.chkvar2.set(0)
        self.chkbtn2 = Checkbutton(self.fm_2, text="Draw in colors", variable=self.chkvar2,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn2.pack(side=TOP, anchor='w')

        self.chkvar3 = IntVar()
        self.chkvar3.set(1)
        self.chkbtn3 = Checkbutton(self.fm_2, text="Draw Acceleration", variable=self.chkvar3,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn3.pack(side=TOP, anchor='w')

        self.chkvar5 = IntVar()
        self.chkvar5.set(1)
        self.chkbtn5 = Checkbutton(self.fm_2, text="Draw Velocity", variable=self.chkvar5,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn5.pack(side=TOP, anchor='w')

        self.chkvar4 = IntVar()
        self.chkvar4.set(1)
        self.chkbtn4 = Checkbutton(self.fm_2, text="Draw toe end", variable=self.chkvar4,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn4.pack(side=TOP, anchor='w')

        self.chkvar6 = IntVar()
        self.chkvar6.set(0)
        self.chkbtn6 = Checkbutton(self.fm_2, text="Draw from beginning", variable=self.chkvar6,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn6.pack(side=TOP, anchor='w')

        self.chkvar7 = IntVar()
        self.chkvar7.set(0)
        self.chkbtn7 = Checkbutton(self.fm_2, text="Draw to ending", variable=self.chkvar7,
                                   onvalue=1, offvalue=0,
                                   # height=5, width=20
                                   )
        self.chkbtn7.pack(side=TOP, anchor='w')

        self.fm_3 = Frame(self.fm_2)
        self.fm_3.pack(side=TOP)

        self.btn3 = Button(self.fm_3, text='Save params', width=50, command=self.save_parameters)
        self.btn3.pack(side=TOP)
        '''
        # Loading parameters can be automated.
        self.btn4 = Button(self.fm_3, text='Load params', width=50, command=self.load_parameters)
        self.btn4.pack(side=TOP)
        '''

        # Bottom-up layout
        self.btn5 = Button(self.fm_2, text='Resume', width=100, command=self.resume)
        self.btn5.pack(side=BOTTOM)

        self.btn4 = Button(self.fm_2, text='Pause', width=100, command=self.pause)
        self.btn4.pack(side=BOTTOM)

        self.btn1 = Button(self.fm_2, text='Start over', width=100, command=self.start_over)
        self.btn1.pack(side=BOTTOM)

        self.lb_frame_upper_int = IntVar()
        self.lb_frame_upper_int.set(self.parameters['upper_frame_limit'])
        self.lb_frame_upper_str = StringVar()
        self.lb_frame_upper_str.set("Frame to: " + str(self.lb_frame_upper_int.get()))
        self.lb_frame_upper = Label(self.fm_2, textvariable=self.lb_frame_upper_str)
        self.lb_frame_upper.pack(side=BOTTOM)

        self.lb_frame_lower_int = IntVar()
        self.lb_frame_lower_int.set(self.parameters['lower_frame_limit'])
        self.lb_frame_lower_str = StringVar()
        self.lb_frame_lower_str.set("Frame from: " + str(self.lb_frame_lower_int.get()))
        self.lb_frame_lower = Label(self.fm_2, textvariable=self.lb_frame_lower_str)
        self.lb_frame_lower.pack(side=BOTTOM)

        self.lb_frame_counter_int = IntVar()
        self.lb_frame_counter_int.set(0)
        self.lb_frame_counter_str = StringVar()
        self.lb_frame_counter_str.set("Frame "+str(self.lb_frame_counter_int.get()))
        self.lb_frame_counter = Label(self.fm_2, textvariable=self.lb_frame_counter_str)
        self.lb_frame_counter.pack(side=BOTTOM)

        self.btn2 = Button(self.fm_2, text='Load file', width=100, command=self.load_file)
        self.btn2.pack(side=BOTTOM)

        self.lb_file_name = Label(self.fm_2, text=self.filename,
                                  #height=50,
                                  justify='center', wraplength=180)
        self.lb_file_name.pack(side=BOTTOM)

        self.canvas = Canvas(self.fm_1, bg='white')
        self.canvas.config(width=wid-200, height=hei)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        self.pack(fill=BOTH, expand=1)

        # read file
        self.time_frames = list()
        self.csv_data = None
        self.read_in()

        # pause and resume
        self.drawing_counter = 0  # Counting time frames to determine the color in color mode
        self.paused = 0
        self.paused_at_frame = 0

    def read_in(self):
        self.time_frames = list()
        try:
            f = open(self.filename+'.frames', "rb")
            self.time_frames = pickle.load(f)
            f.close()
            print("Time frame data loaded.")
        except IOError:
            print("Time frame data file is not found. Generating...")
            self.csv_data = None
            self.read_csv_data(self.filename)

            # generate time frames
            # self.time_frames = list()
            self.generate_time_frames()
            f = open(self.filename+'.frames', "wb")
            pickle.dump(self.time_frames, f)
            f.close()
            print("Time frame data saved.")
        self.parameters['upper_frame_limit'] = int(self.time_frames[-1].info['Frame'])
        self.parameters['lower_frame_limit'] = int(self.time_frames[0].info['Frame'])
        self.lb_frame_upper_int.set(self.parameters['upper_frame_limit'])
        self.lb_frame_upper_str.set("Frames to: "+str(self.parameters['upper_frame_limit']))
        self.lb_frame_lower_int.set(self.parameters['lower_frame_limit'])
        self.lb_frame_lower_str.set("Frames from: " + str(self.parameters['lower_frame_limit']))

        # self.load_parameters()  # load other parameters

    def draw_a_time_frame(self, i):
        print("Drawing frame {}...".format(i))
        t = self.time_frames[i]  # temporary variable, the current time frame.

        # Draw the 'threshold on' time point
        if i == self.parameters['threshold_on']:
            current_point = dict()
            current_point['Y5'] = self.flip_x(self.transform(t.info['Y5']))
            current_point['Z5'] = self.flip_y(self.transform(t.info['Z5']))
            current_point['Y5v'] = t.info['Y5\'']
            current_point['Z5v'] = t.info['Z5\'']
            current_point['Y5a'] = t.info['Y5\'\'']
            current_point['Z5a'] = t.info['Z5\'\'']
            current_point['yz_combined_velocity'] = t.info['yz_combined_velocity']
            current_point['yz_combined_acceleration'] = t.info['yz_combined_acceleration']
            print('Draw V/A for this ''threshold on'' frame')
            self.draw_velocity_acceleration(current_point)

    def draw_all_time_frames(self):
        print("Start drawing time frames")
        self.critical_point = dict()  # the first point going upward
        self.last_point = [0, 0]  # Store the last point for drawing trajectory
        # for i in range(len(self.time_frames)):
        for i in range(self.parameters['lower_frame_limit'], self.parameters['upper_frame_limit']):
            print("Drawing frame {}...".format(i))
            if self.paused == 1:  # exit when paused
                return

            t = self.time_frames[i - self.parameters['lower_frame_limit']]  # temporary variable, the current time frame

            # Draw the threshold on time point

            if i == self.parameters['threshold_on']:
                current_point = dict()
                current_point['Y5'] = self.flip_x(self.transform(t.info['Y5']))
                current_point['Z5'] = self.flip_y(self.transform(t.info['Z5']))
                current_point['Y5v'] = t.info['Y5\'']
                current_point['Z5v'] = t.info['Z5\'']
                current_point['Y5a'] = t.info['Y5\'\'']
                current_point['Z5a'] = t.info['Z5\'\'']
                current_point['yz_combined_velocity'] = t.info['yz_combined_velocity']
                current_point['yz_combined_acceleration'] = t.info['yz_combined_acceleration']
                print('Draw V/A for this ''threshold on'' frame')
                self.draw_velocity_acceleration(current_point)

            # Draw the sticks
            # 200 Hz -> lower frequency, but frequency gets higher in the upward part.

            # in a frame range, raise the frequency
            if self.parameters['upward_end_frame'] > self.lb_frame_counter_int.get() > self.parameters['upward_start_frame']:
                real_time_skip_frame = max(self.parameters['skip_frame']/10, 1)  # increase frequency by lowering skip_frame
            else:
                real_time_skip_frame = self.parameters['skip_frame']

            if self.chkvar6.get() == 1:
                starting = int(self.parameters['lower_frame_limit'])
            else:
                starting = int(self.parameters['start_frame'])

            if self.chkvar7.get() == 1:
                ending = int(self.parameters['upper_frame_limit'])
            else:
                ending = int(self.parameters['end_frame'])

            if i % real_time_skip_frame == 0 and starting <= i <= ending:
                if self.chkvar1.get() == 1:  # Check if to draw the sticks
                    self.draw_stick(
                        [t.info['Y1'], t.info['Z1'], t.info['Y2'], t.info['Z2'],
                         t.info['Y3'], t.info['Z3'], t.info['Y4'], t.info['Z4'],
                         t.info['Y5'], t.info['Z5']],
                        # color=colors[drawing_counter % 7] if self.chkvar2.get() == 1 else greys[drawing_counter % 10]
                        color=colors[self.drawing_counter % 7] if self.chkvar2.get() == 1 else 'grey40'
                    )

                print("Time frame " + str(t.number) + " drawn.")

                # Update frame counter, both int and str
                self.lb_frame_counter_int.set(str(t.info['Frame']))
                self.lb_frame_counter_str.set("Frame "+str(t.info['Frame']))

                self.drawing_counter += 1  # Counting time frames
                self.paused_at_frame = i  # Store current frame number

                time.sleep(self.parameters['sleep_time'])

            # Draw the toe end, or the trace
            if starting <= i <= ending and self.chkvar4.get() == 1:  # Apply to every time frame
                if self.last_point != [0, 0]:  # When it's not the first frame
                    self.draw_trajectory(t)
                self.last_point[0] = self.flip_x(self.transform(t.info['Y5']))
                self.last_point[1] = self.flip_y(self.transform(t.info['Z5']))
        # Draw the last part to close the trajectory
        if self.chkvar4.get() == 1:
            self.draw_trajectory(t)

        print(self.critical_point)

    def set_start_frame(self):
        self.parameters['start_frame'] = int(self.spb1.get())

    def set_end_frame(self):
        self.parameters['end_frame'] = int(self.spb2.get())

    def set_skip_frame(self):
        self.parameters['skip_frame'] = int(self.spb3.get())

    def set_offset_x(self):
        self.parameters['offset_x'] = int(self.spb4.get())

    def set_offset_y(self):
        self.parameters['offset_y'] = int(self.spb5.get())

    def set_sleep_time(self):
        self.parameters['sleep_time'] = float(self.spb6.get())

    def set_upward_start_frame(self):
        self.parameters['upward_start_frame'] = int(self.spb7.get())

    def set_upward_end_frame(self):
        self.parameters['upward_end_frame'] = int(self.spb8.get())

    def set_threshold_on(self):
        self.parameters['threshold_on'] = int(self.spb9.get())

    def start_over(self):
        self.paused = 0  # clear the paused flag

        # manually update parameters
        self.set_start_frame()
        self.set_end_frame()
        self.set_skip_frame()
        self.set_offset_x()
        self.set_offset_y()
        self.set_sleep_time()
        self.set_upward_start_frame()
        self.set_upward_end_frame()
        self.set_threshold_on()

        self.canvas.delete('all')
        self.canvas.update()

        self.draw_all_time_frames()

    def pause(self):
        self.paused = 1

    def resume(self):
        self.paused = 0  # clear the paused flag

        self.parameters['start_frame'] = self.paused_at_frame
        self.set_end_frame()
        self.set_skip_frame()
        self.set_offset_x()
        self.set_offset_y()
        self.set_sleep_time()
        self.set_upward_start_frame()
        self.set_upward_end_frame()
        self.set_threshold_on()

        self.draw_all_time_frames()

    def save_parameters(self):
        f1 = open(self.filename + '.params', "wb")
        pickle.dump(self.parameters, f1)
        f1.close()
        print("Parameters for",self.filename, "saved.")

    def load_parameters(self):
        try:
            f1 = open(self.filename+'.params', "rb")
            self.parameters = pickle.load(f1)
            f1.close()
            print("Parameters for",self.filename, "loaded.")
        except IOError:
            print("Cannot find saved parameters for", self.filename, ".")

        # TODO refresh panel after reading parameters in.

    def load_file(self):
        new_filename = filedialog.askopenfilename()
        if self.filename != new_filename:
            self.filename = new_filename
            if self.filename != '':
                self.lb_file_name.config(text="File: "+self.filename)
                self.read_in()

    def draw_velocity_acceleration(self, p):
        # Draw velocity arrow
        if self.chkvar3.get() == 1:
            self.canvas.create_line(p['Y5']+self.parameters['offset_x'], p['Z5']+self.parameters['offset_y'],
                                    p['Y5']-p['Y5v']/self.parameters['velocity_normalization_factor']+self.parameters['offset_x'],
                                    p['Z5']-p['Z5v']/self.parameters['velocity_normalization_factor']+self.parameters['offset_y'],
                                    arrow=LAST, fill='black')

        # Draw acceleration arrow
        if self.chkvar5.get() == 1:
            self.canvas.create_line(p['Y5']+self.parameters['offset_x'], p['Z5']+self.parameters['offset_y'],
                                    p['Y5']-p['Y5a']/self.parameters['acceleration_normalization_factor']+self.parameters['offset_x'],
                                    p['Z5']-p['Z5a']/self.parameters['acceleration_normalization_factor']+self.parameters['offset_y'],
                                    arrow=LAST, fill='red')

        self.canvas.update()

    def draw_trajectory(self, t):
        # if self.last_point[1] < 596:  # self.flip_y(self.transform(t.info['Z5'])): # moving upward, set color to blue
        # in a frame range, set color to blue
        '''
        if self.parameters['upward_end_frame'] > self.lb_frame_counter_int.get() > self.parameters['upward_start_frame']:
            c = colors[5]
            if self.critical_point == {}:  # record this point as the first point upward
                # cannot let self.critical_point = info, because '=' has a different meaning when used between dicts
                self.critical_point['Y5'] = self.flip_x(self.transform(t.info['Y5']))
                self.critical_point['Z5'] = self.flip_y(self.transform(t.info['Z5']))
                self.critical_point['Y5v'] = t.info['Y5\'']
                self.critical_point['Z5v'] = t.info['Z5\'']
                self.critical_point['Y5a'] = t.info['Y5\'\'']
                self.critical_point['Z5a'] = t.info['Z5\'\'']
                self.critical_point['yz_combined_velocity'] = t.info['yz_combined_velocity']
                self.critical_point['yz_combined_acceleration'] = t.info['yz_combined_acceleration']

                if self.chkvar3.get() == 1:  # Check if to draw the arrows  # TODO check if this is needed to keep
                    self.draw_velocity_acceleration(self.critical_point)
        '''
        if self.parameters['upward_end_frame'] > self.lb_frame_counter_int.get() > self.parameters['upward_start_frame']:
            c = colors[5]
            '''
            if self.critical_point == {}:  # record this point as the first point upward
                # cannot let self.critical_point = info, because '=' has a different meaning when used between dicts
                self.critical_point['Y5'] = self.flip_x(self.transform(t.info['Y5']))
                self.critical_point['Z5'] = self.flip_y(self.transform(t.info['Z5']))
                self.critical_point['Y5v'] = t.info['Y5\'']
                self.critical_point['Z5v'] = t.info['Z5\'']
                self.critical_point['Y5a'] = t.info['Y5\'\'']
                self.critical_point['Z5a'] = t.info['Z5\'\'']
                self.critical_point['yz_combined_velocity'] = t.info['yz_combined_velocity']
                self.critical_point['yz_combined_acceleration'] = t.info['yz_combined_acceleration']

            #if self.chkvar3.get() == 1 and self.lb_frame_counter_int.get() == self.parameters['threshold_on']:  # Check if to draw the arrows  # TODO check if this is needed to keep
                print("AAAAAAA")
                self.draw_velocity_acceleration(self.critical_point)
            '''
        else:  # not moving upward, set color to grey
            c = 'grey40'
        self.canvas.create_line(self.last_point[0]+self.parameters['offset_x'],
                                self.last_point[1]+self.parameters['offset_y'],
                                self.flip_x(self.transform(t.info['Y5']))+self.parameters['offset_x'],
                                self.flip_y(self.transform(t.info['Z5']))+self.parameters['offset_y'], fill=c, width=2)
        self.canvas.update()

    def draw_stick(self, pts, color):
        pts_scaled = list()
        for p in pts:
            pts_scaled.append(self.transform(p))  # enlarge by 5 times then offset backward
        # Draw the sticks
        self.canvas.create_line(self.flip_x(pts_scaled[0])+self.parameters['offset_x'],
                                self.flip_y(pts_scaled[1])+self.parameters['offset_y'],
                                self.flip_x(pts_scaled[2])+self.parameters['offset_x'],
                                self.flip_y(pts_scaled[3])+self.parameters['offset_y'],
                                self.flip_x(pts_scaled[4])+self.parameters['offset_x'],
                                self.flip_y(pts_scaled[5])+self.parameters['offset_y'],
                                self.flip_x(pts_scaled[6])+self.parameters['offset_x'],
                                self.flip_y(pts_scaled[7])+self.parameters['offset_y'],
                                self.flip_x(pts_scaled[8])+self.parameters['offset_x'],
                                self.flip_y(pts_scaled[9])+self.parameters['offset_y'],
                                fill=color,
                                width=2)
        # Draw the joints
        self.draw_dot(self.flip_x(pts_scaled[0]), self.flip_y(pts_scaled[1]))
        self.draw_dot(self.flip_x(pts_scaled[2]), self.flip_y(pts_scaled[3]))
        self.draw_dot(self.flip_x(pts_scaled[4]), self.flip_y(pts_scaled[5]))
        self.draw_dot(self.flip_x(pts_scaled[6]), self.flip_y(pts_scaled[7]))
        # self.draw_dot(hei-pts_scaled[8], wid-pts_scaled[9]) # Don't draw this last black dot. It will be in blue/grey.
        self.canvas.update()

    def draw_dot(self, x, y, color='black'):
        self.canvas.create_line(x+self.parameters['offset_x'], y+self.parameters['offset_y'], x+self.parameters['offset_x'], y+1+self.parameters['offset_y'], fill=color)

    def transform(self, a):
        new_a = a * self.parameters['scale_factor'] + 0
        return new_a

    def flip_x(self, b):
        new_b = (wid-200) - b
        return new_b

    def flip_y(self, c):
        new_c = hei - c
        return new_c

    def read_csv_data(self, fn):
        self.csv_data = pd.read_csv(fn)
        print("Successfully read in "+fn+",")

    def generate_time_frames(self):
        """
        csv_data -> time frames
        """
        print("Generating time frames...")
        column_titles = list()
        for line_list in self.csv_data:
            column_titles.append(line_list)

        # self.upper_frame_limit = self.csv_data.shape[0]
        self.parameters['upper_frame_limit'] = self.csv_data.shape[0]

        for i in range(self.upper_frame_limit):
            information = dict()
            for title in column_titles:
                information[title] = self.csv_data[title].tolist()[i]
            self.time_frames.append(TimeFrame(i, information))


class TimeFrame:

    """
    A frame of frozen kinetics, depicting a certain time point
    """

    def __init__(self, n, i):
        self.number = n
        self.info = i
        print("Added time frame number "+str(n))


if __name__ == '__main__':
    root = Tk()
    wid = 1000
    hei = 900
    root.wm_title("Kinetics")
    root.geometry(str(wid) + "x" + str(hei) + "+200+50")
    app = Kinetics(root)
    root.mainloop()

# ①帧数的起止，以实际帧数为准，比如有的CSV文件起始帧数并不是1，有可能是2000+。 (DONE)
# ②抬起相的starting 和ending都有个开关，因为有时候我需要大致浏览一下总体的步态情况，然后再选择感兴趣的抬起相进行起止。 (DONE)
# ③a和v是否可以分开画呢 (DONE)，
# ④咱们的运行过程中是否可以加入一个暂停pause键  (DONE)
# TODO 同时再加上刚刚你说的那个功能，多加几个关键帧。
# Todo 时间轴，打点
# 背景改成白色
# TODO Pause暂停后可以继续
# TODO 速度和加速度箭头长度调整
# TODO 解决data0213的load问题
