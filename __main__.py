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

        # Viewer and Controllers part
        self.fm_1 = LabelFrame(self.master, text='Viewer', width=wid-200)
        self.fm_1.propagate(False)
        self.fm_1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.canvas = Canvas(self.fm_1, bg='white')
        self.canvas.config(width=wid - 200, height=hei-250)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        # Simulation Controller: Slider

        self.fm_3 = LabelFrame(self.fm_1, width=wid-200)
        self.fm_3.propagate(False)
        self.fm_3.pack(side=BOTTOM, fill=BOTH, expand=YES)
        '''
        self.slider = Scale(self.fm_3, from_=1, to=1000, orient="horizontal")
        self.slider.bind("<buttonRelease-1",
                         func=None
                         )
        self.slider.pack(side=TOP, fill=X)
        '''

        # Simulation Controller: Button
        self.fm_4 = Frame(self.fm_3, width=wid-200)
        self.fm_4.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.btn1 = Button(self.fm_4, text='Start over', command=self.start_over)
        self.btn1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.btn4 = Button(self.fm_4, text='Pause', command=self.pause)
        self.btn4.pack(side=LEFT, fill=BOTH, expand=YES)

        self.btn5 = Button(self.fm_4, text='Resume', command=self.resume)
        self.btn5.pack(side=LEFT, fill=BOTH, expand=YES)

        # Settings part 1
        self.fm_2 = LabelFrame(self.master, text='Settings', width=200)
        self.fm_2.propagate(False)
        self.fm_2.pack(side=LEFT, fill=BOTH, expand=YES)

        # parameters
        self.parameters = {"upper_frame_limit": 5000,
                           "lower_frame_limit": 0,
                           "total_frames": 5000,
                           "scale_factor": 3,
                           "start_frame": 300,
                           "end_frame": 440,
                           "skip_frame": 10,
                           "velocity_normalization_factor": 1.0,
                           "acceleration_normalization_factor": 60.0,
                           "offset_x": -50,
                           "offset_y": -150,
                           "sleep_time": 0,
                           "upward_period_1a": 405,
                           "upward_period_1b": 430,
                           "upward_period_2a": 405,
                           "upward_period_2b": 430,
                           "upward_period_3a": 405,
                           "upward_period_3b": 430,
                           "upward_period_4a": 405,
                           "upward_period_4b": 430,
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

        # self.lb9 = Label(self.fm_2, text='Threshold on:')
        # self.lb9.pack(side=TOP, anchor='w')
        # 
        # self.str9 = StringVar()
        # self.str9.set(self.parameters['threshold_on'])
        # self.spb9 = Spinbox(self.fm_2,
        #                     from_=1,
        #                     to=self.parameters['upper_frame_limit'],
        #                     increment=1,
        #                     textvariable=self.str9,
        #                     command=self.set_threshold_on)
        # self.spb9.pack(side=TOP) # 

        self.lb10 = Label(self.fm_2, text='Velocity (black) divided by:')
        self.lb10.pack(side=TOP, anchor='w')

        self.str10 = StringVar()
        self.str10.set(self.parameters['velocity_normalization_factor'])
        self.spb10 = Spinbox(self.fm_2,
                             from_=0.1,
                             to=100,
                             increment=0.1,
                             textvariable=self.str10,
                             command=self.set_v_arrow_factor)
        self.spb10.pack(side=TOP)

        self.lb11 = Label(self.fm_2, text='Acceleration (red) divided by:')
        self.lb11.pack(side=TOP, anchor='w')

        self.str11 = StringVar()
        self.str11.set(self.parameters['acceleration_normalization_factor'])
        self.spb11 = Spinbox(self.fm_2,
                             from_=0.1,
                             to=100,
                             increment=0.1,
                             textvariable=self.str11,
                             command=self.set_a_arrow_factor)
        self.spb11.pack(side=TOP)

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

        self.btn3 = Button(self.fm_2, text='Save parameters', width=50, command=self.save_parameters)
        self.btn3.pack(side=TOP)

        # Bottom-up layout, setting upward periods
        self.fm_6 = Frame(self.fm_3, width=wid - 200)
        self.fm_6.pack(side=BOTTOM, fill=BOTH, expand=YES)
        # up1a
        self.lb_up1a = Label(self.fm_6, text='Up1A:')
        self.lb_up1a.pack(side=LEFT, anchor='w')

        self.str_up1a = StringVar()
        self.str_up1a.set(self.parameters['upward_period_1a'])
        self.spb_up1a = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up1a,
                                command=self.set_upward_1a)
        self.spb_up1a.pack(side=LEFT, expand=YES)
        # up1b
        self.lb_up1b = Label(self.fm_6, text='Up1B:')
        self.lb_up1b.pack(side=LEFT, anchor='w')

        self.str_up1b = StringVar()
        self.str_up1b.set(self.parameters['upward_period_1b'])
        self.spb_up1b = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up1b,
                                command=self.set_upward_1b)
        self.spb_up1b.pack(side=LEFT, expand=YES)
        # up2a
        self.lb_up2a = Label(self.fm_6, text='Up2A:')
        self.lb_up2a.pack(side=LEFT, anchor='w')

        self.str_up2a = StringVar()
        self.str_up2a.set(self.parameters['upward_period_2a'])
        self.spb_up2a = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up2a,
                                command=self.set_upward_2a)
        self.spb_up2a.pack(side=LEFT, expand=YES)
        # up2b
        self.lb_up2b = Label(self.fm_6, text='Up2B:')
        self.lb_up2b.pack(side=LEFT, anchor='w')

        self.str_up2b= StringVar()
        self.str_up2b.set(self.parameters['upward_period_2b'])
        self.spb_up2b = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up2b,
                                command=self.set_upward_2b)
        self.spb_up2b.pack(side=LEFT, expand=YES)
        # up3a
        self.lb_up3a = Label(self.fm_6, text='Up3A:')
        self.lb_up3a.pack(side=LEFT, anchor='w')

        self.str_up3a = StringVar()
        self.str_up3a.set(self.parameters['upward_period_3a'])
        self.spb_up3a = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up3a,
                                command=self.set_upward_3a)
        self.spb_up3a.pack(side=LEFT, expand=YES)
        # up1b
        self.lb_up3b = Label(self.fm_6, text='Up3B:')
        self.lb_up3b.pack(side=LEFT, anchor='w')

        self.str_up3b = StringVar()
        self.str_up3b.set(self.parameters['upward_period_3b'])
        self.spb_up3b = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up3b,
                                command=self.set_upward_3b)
        self.spb_up3b.pack(side=LEFT, expand=YES)
        # up2a
        self.lb_up4a = Label(self.fm_6, text='Up4A:')
        self.lb_up4a.pack(side=LEFT, anchor='w')

        self.str_up4a = StringVar()
        self.str_up4a.set(self.parameters['upward_period_4a'])
        self.spb_up4a = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up4a,
                                command=self.set_upward_4a)
        self.spb_up4a.pack(side=LEFT, expand=YES)
        # up2b
        self.lb_up4b = Label(self.fm_6, text='Up4B:')
        self.lb_up4b.pack(side=LEFT, anchor='w')

        self.str_up4b = StringVar()
        self.str_up4b.set(self.parameters['upward_period_4b'])
        self.spb_up4b = Spinbox(self.fm_6,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up4b,
                                command=self.set_upward_4b)
        self.spb_up4b.pack(side=LEFT, expand=YES)


        # Bottom-up layout, displaying frame range
        self.fm_5 = Frame(self.fm_3, width=wid - 200)
        self.fm_5.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.lb_frame_upper_int = IntVar()
        self.lb_frame_upper_int.set(self.parameters['upper_frame_limit'])
        self.lb_frame_upper_str = StringVar()
        self.lb_frame_upper_str.set("Frame to: " + str(self.lb_frame_upper_int.get()))
        self.lb_frame_upper = Label(self.fm_5, textvariable=self.lb_frame_upper_str)
        self.lb_frame_upper.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.lb_frame_lower_int = IntVar()
        self.lb_frame_lower_int.set(self.parameters['lower_frame_limit'])
        self.lb_frame_lower_str = StringVar()
        self.lb_frame_lower_str.set("Frame from: " + str(self.lb_frame_lower_int.get()))
        self.lb_frame_lower = Label(self.fm_5, textvariable=self.lb_frame_lower_str)
        self.lb_frame_lower.pack(side=RIGHT, fill=BOTH, expand=YES)

        '''
        self.lb_frame_counter_int = IntVar()
        self.lb_frame_counter_int.set(0)
        self.lb_frame_counter_str = StringVar()
        self.lb_frame_counter_str.set("Frame "+str(self.lb_frame_counter_int.get()))
        self.lb_frame_counter = Label(self.fm_2, textvariable=self.lb_frame_counter_str)
        self.lb_frame_counter.pack(side=BOTTOM, fill=BOTH, expand=YES)
        '''

        self.btn2 = Button(self.fm_2, text='Load file', width=100, command=self.load_file)
        self.btn2.pack(side=BOTTOM)

        self.lb_file_name = Label(self.fm_2, text=self.filename,
                                  #height=50,
                                  justify='center', wraplength=180)
        self.lb_file_name.pack(side=BOTTOM)

        self.pack(fill=BOTH, expand=1)

        # read file
        self.time_frames = list()
        self.csv_data = None
        self.read_in()

        # pause and resume
        self.frame_counter = 0
        self.drawing_counter = 0  # Counting time frames to determine the color in color mode
        self.paused = 0
        self.paused_at_frame = 0

        # canvas item ids
        self.canvas_ids = dict()

        # upward frames
        self.upward_frames = list()
        self.threshold_on = list()

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
            self.generate_time_frames()
            self.transformation()  # transform and offset before saving
            f = open(self.filename+'.frames', "wb")
            pickle.dump(self.time_frames, f)
            f.close()
            print("Time frame data saved.")

        self.parameters['upper_frame_limit'] = int(self.time_frames[-1].info['Frame'])
        self.parameters['lower_frame_limit'] = int(self.time_frames[0].info['Frame'])
        self.ensure_start_end_range()

        self.lb_frame_upper_int.set(self.parameters['upper_frame_limit'])
        self.lb_frame_upper_str.set("Frames to: "+str(self.parameters['upper_frame_limit']))
        self.lb_frame_lower_int.set(self.parameters['lower_frame_limit'])
        self.lb_frame_lower_str.set("Frames from: " + str(self.parameters['lower_frame_limit']))

        # Add the slider
        try:
            self.slider.destroy()
        except:
            pass
        self.slider = Scale(self.fm_3,
                            # from_=self.parameters['start_frame'],
                            from_=self.parameters['lower_frame_limit'],
                            to=self.parameters['upper_frame_limit'],  # Temporarily like this
                            orient="horizontal")
        self.slider.bind("<ButtonRelease-1>",
                         func=self.start_from_a_certain_frame
                         )
        self.slider.pack(side=BOTTOM, fill=X, expand=YES)
        print("Parameters:\n", self.parameters)
        # self.load_parameters()  # load other parameters

    def ensure_start_end_range(self):
        # Ensure simulation range within upper and lower boundary
        if self.parameters['end_frame'] > self.parameters['upper_frame_limit'] or self.parameters['end_frame'] < self.parameters['lower_frame_limit']:
            self.parameters['end_frame'] = self.parameters['upper_frame_limit']
            self.str2.set(self.parameters['end_frame'])

        if self.parameters['start_frame'] < self.parameters['lower_frame_limit'] or self.parameters['start_frame'] > self.parameters['upper_frame_limit']:
            self.parameters['start_frame'] = self.parameters['lower_frame_limit']
            self.str1.set(self.parameters['start_frame'])

    def draw_time_frames(self, starting, ending):
        print("Start drawing time frames...")
        print("Starting from {}, ending by {}".format(starting, ending))

        self.last_point = [0, 0]  # Store the last point for drawing toe_end

        if self.chkvar6.get() == 1:  # If drawing from beginning
            starting = int(self.parameters['lower_frame_limit'])

        if self.chkvar7.get() == 1:  # If drawing to the end
            ending = int(self.parameters['upper_frame_limit'])

        # for i in range(len(self.time_frames)):
        # for i in range(self.parameters['lower_frame_limit'], self.parameters['upper_frame_limit']):
        for i in range(starting, ending+1):  # ending is not included in range, so +1 is needed
            # Use a list to collect ids on Canvas of this frame
            ids = list()

            # print("Drawing frame {}...".format(i))
            if self.paused == 1:  # exit when paused
                return

            t = self.time_frames[i - self.parameters['lower_frame_limit']]  # temporary variable, the current time frame
            # Draw the threshold on time point

            #if i == self.parameters['threshold_on']:
            if i in self.threshold_on:  # There are multiple frames for threshold on
                print('Draw V/A for this ''threshold on'' frame')
                ids += self.draw_velocity_acceleration(t.info)

            # Draw the sticks
            # 200 Hz -> lower frequency, but frequency gets higher in the upward part.

            # in a frame range, raise the frequency
            #if self.parameters['upward_period_1a'] < self.frame_counter < self.parameters['upward_period_1b']:
            if self.frame_counter in self.upward_frames:
                real_time_skip_frame = max(self.parameters['skip_frame']/10, 1)  # increase frequency by lowering skip_frame
            else:
                real_time_skip_frame = self.parameters['skip_frame']

            if i % real_time_skip_frame == 0 and starting <= i <= ending:
                if self.chkvar1.get() == 1:  # Check if to draw the sticks
                    ids += self.draw_stick(
                        [t.info['Y1'], t.info['Z1'], t.info['Y2'], t.info['Z2'],
                         t.info['Y3'], t.info['Z3'], t.info['Y4'], t.info['Z4'],
                         t.info['Y5'], t.info['Z5']],
                        # color=colors[drawing_counter % 7] if self.chkvar2.get() == 1 else greys[drawing_counter % 10]
                        color=colors[self.drawing_counter % 7] if self.chkvar2.get() == 1 else 'grey40'
                        )

                    time.sleep(self.parameters['sleep_time'])

            # Draw the toe end
            if starting <= i <= ending and self.chkvar4.get() == 1:  # Apply to every time frame
                if self.last_point != [0, 0]:  # When it's not the first frame
                    ids += self.draw_toe_end(t)
                    # if_draw_toe_end = 1
                self.last_point[0] = t.info['Y5']
                self.last_point[1] = t.info['Z5']

            # Update frame counter, both int and str
            # self.lb_frame_counter_int.set(str(t.info['Frame']))
            # self.lb_frame_counter_str.set("Frame "+str(t.info['Frame']))
            self.frame_counter = t.info['Frame']

            # add ids from this frame to the dictionary
            self.canvas_ids[self.frame_counter] = ids

            # Set slide bar position
            self.slider.set(t.info['Frame'])

            self.drawing_counter += 1  # Counting time frames
            self.paused_at_frame = i  # Update paused frame in case there will be a pause

        # Draw the last part to close the toe end loop
        if self.chkvar4.get() == 1:
            self.canvas_ids[self.frame_counter] += self.draw_toe_end(t)

    def start_from_a_certain_frame(self, position):
        # print("position", position)  # we don't use this mouse position
        self.pause()

        if self.slider.get() < self.paused_at_frame:  # the slider bar was dragged backward
            print(self.slider.get(), self.paused_at_frame)
            for i in range(self.paused_at_frame, self.slider.get(), -1):  # loop backward
                if i in self.canvas_ids.keys():
                    for j in self.canvas_ids[i]:
                        self.canvas.delete(j)  # delete all items on canvas that after this new starting point
                        self.canvas.update()
        self.canvas.update()
        self.paused_at_frame = self.slider.get()

    def set_start_frame(self):
        self.parameters['start_frame'] = int(self.spb1.get())
        # Reset the slider

        self.slider.destroy()
        self.slider = Scale(self.fm_3,
                            # from_=self.parameters['start_frame'],
                            from_=self.parameters['lower_frame_limit'],
                            to=self.parameters['upper_frame_limit'],  # Temporarily like this
                            orient="horizontal")
        self.slider.bind("<ButtonRelease-1>",
                         func=self.start_from_a_certain_frame
                         )
        self.slider.pack(side=BOTTOM, fill=X, expand=YES)

    def set_end_frame(self):
        self.parameters['end_frame'] = int(self.spb2.get())
        # Reset the slider
        self.slider.destroy()
        self.slider = Scale(self.fm_3,
                            # from_=self.parameters['start_frame'],
                            from_=self.parameters['lower_frame_limit'],
                            to=self.parameters['upper_frame_limit'],  # Temporarily like this
                            orient="horizontal")
        self.slider.bind("<ButtonRelease-1>",
                         func=self.start_from_a_certain_frame
                         )
        self.slider.pack(side=BOTTOM, fill=X, expand=YES)

    def set_skip_frame(self):
        self.parameters['skip_frame'] = int(self.spb3.get())

    def set_offset_x(self):
        self.parameters['offset_x'] = int(self.spb4.get())

    def set_offset_y(self):
        self.parameters['offset_y'] = int(self.spb5.get())

    def set_sleep_time(self):
        self.parameters['sleep_time'] = float(self.spb6.get())

    def set_upward_1a(self):
        self.parameters['upward_period_1a'] = int(self.spb_up1a.get())

    def set_upward_1b(self):
        self.parameters['upward_period_1b'] = int(self.spb_up1b.get())

    def set_upward_2a(self):
        self.parameters['upward_period_2a'] = int(self.spb_up2a.get())

    def set_upward_2b(self):
        self.parameters['upward_period_2b'] = int(self.spb_up2b.get())

    def set_upward_3a(self):
        self.parameters['upward_period_3a'] = int(self.spb_up3a.get())

    def set_upward_3b(self):
        self.parameters['upward_period_3b'] = int(self.spb_up3b.get())

    def set_upward_4a(self):
        self.parameters['upward_period_4a'] = int(self.spb_up4a.get())

    def set_upward_4b(self):
        self.parameters['upward_period_4b'] = int(self.spb_up4b.get())

    def set_v_arrow_factor(self):
        self.parameters['velocity_normalization_factor'] = float(self.spb10.get())

    def set_a_arrow_factor(self):
        self.parameters['acceleration_normalization_factor'] = float(self.spb11.get())

    def set_upward_periods(self):
        self.threshold_on.clear()
        self.upward_frames.clear()
        self.set_upward_1a()
        self.set_upward_1b()
        self.upward_frames += list(range(self.parameters['upward_period_1a'], self.parameters['upward_period_1b']))
        self.set_upward_2a()
        self.set_upward_2b()
        self.upward_frames += list(range(self.parameters['upward_period_2a'], self.parameters['upward_period_2b']))
        self.set_upward_3a()
        self.set_upward_3b()
        self.upward_frames += list(range(self.parameters['upward_period_3a'], self.parameters['upward_period_3b']))
        self.set_upward_4a()
        self.set_upward_4b()
        self.upward_frames += list(range(self.parameters['upward_period_4a'], self.parameters['upward_period_4b']))
        self.threshold_on.append(self.parameters['upward_period_1a'])
        self.threshold_on.append(self.parameters['upward_period_2a'])
        self.threshold_on.append(self.parameters['upward_period_3a'])
        self.threshold_on.append(self.parameters['upward_period_4a'])

    def start_over(self):
        self.paused = 0  # clear the paused flag

        # manually update parameters
        self.set_start_frame()
        self.set_end_frame()
        self.set_skip_frame()
        self.set_offset_x()
        self.set_offset_y()
        self.set_sleep_time()
        self.set_upward_periods()
        self.set_v_arrow_factor()
        self.set_v_arrow_factor()

        self.canvas.delete('all')
        self.canvas.update()

        self.draw_time_frames(self.parameters['start_frame'], self.parameters['end_frame'])

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
        self.set_upward_periods()
        self.set_v_arrow_factor()
        self.set_a_arrow_factor()

        self.draw_time_frames(self.parameters['start_frame'], self.parameters['end_frame'])

    def save_parameters(self):
        f1 = open(self.filename + '.params', "wb")
        pickle.dump(self.parameters, f1)
        f1.close()
        print("Parameters for", self.filename, "saved.")

    def update_ui_parameters(self):
        self.str1.set(self.parameters['start_frame'])
        self.str2.set(self.parameters['end_frame'])
        self.str3.set(self.parameters['skip_frame'])
        self.str4.set(self.parameters['offset_x'])
        self.str5.set(self.parameters['offset_y'])
        self.str6.set(self.parameters['sleep_time'])
        self.set_upward_periods()
        self.str10.set(self.parameters['velocity_normalization_factor'])
        self.str11.set(self.parameters['acceleration_normalization_factor'])

    def load_parameters(self):
        try:
            f1 = open(self.filename+'.params', "rb")
            self.parameters = pickle.load(f1)
            f1.close()
            print(self.parameters)
            self.update_ui_parameters()  # update parameters in UI
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
                # Test
                self.load_parameters()

    def draw_velocity_acceleration(self, p):
        # create a list to collect item ids
        ids = list()

        # Draw velocity arrow
        if self.chkvar3.get() == 1:
            ids.append(self.canvas.create_line(p['Y5']+self.parameters['offset_x'], p['Z5']+self.parameters['offset_y'],
                                    p['Y5']-p['Y5v']/self.parameters['velocity_normalization_factor']+self.parameters['offset_x'],
                                    p['Z5']-p['Z5v']/self.parameters['velocity_normalization_factor']+self.parameters['offset_y'],
                                    arrow=LAST, fill='black'))

        # Draw acceleration arrow
        if self.chkvar5.get() == 1:
            ids.append(self.canvas.create_line(p['Y5']+self.parameters['offset_x'], p['Z5']+self.parameters['offset_y'],
                                    p['Y5']-p['Y5a']/self.parameters['acceleration_normalization_factor']+self.parameters['offset_x'],
                                    p['Z5']-p['Z5a']/self.parameters['acceleration_normalization_factor']+self.parameters['offset_y'],
                                    arrow=LAST, fill='red'))

        self.canvas.update()
        return ids

    def draw_toe_end(self, t):
        # create a list to collect item ids
        ids = list()

        # if self.last_point[1] < 596:  # self.flip_y(self.transform(t.info['Z5'])): # moving upward, set color to blue
        # in a frame range, set color to blue

        # if self.parameters['upward_period_1b'] > self.frame_counter > self.parameters['upward_period_1a']:
        if self.frame_counter in self.upward_frames:
            c = colors[5]

        else:  # not moving upward, set color to grey
            c = 'grey40'
        ids.append(self.canvas.create_line(self.last_point[0]+self.parameters['offset_x'],
                                self.last_point[1]+self.parameters['offset_y'],
                                t.info['Y5']+self.parameters['offset_x'],
                                t.info['Z5']+self.parameters['offset_y'], fill=c, width=2))
        self.canvas.update()
        return ids

    def draw_stick(self, pts, color):
        # create a list to collect item ids
        ids = list()

        # Draw the sticks
        ids.append(self.canvas.create_line(pts[0]+self.parameters['offset_x'],
                                pts[1]+self.parameters['offset_y'],
                                pts[2]+self.parameters['offset_x'],
                                pts[3]+self.parameters['offset_y'],
                                pts[4]+self.parameters['offset_x'],
                                pts[5]+self.parameters['offset_y'],
                                pts[6]+self.parameters['offset_x'],
                                pts[7]+self.parameters['offset_y'],
                                pts[8]+self.parameters['offset_x'],
                                pts[9]+self.parameters['offset_y'],
                                fill=color,
                                width=2))
        # Draw the joints
        ids += (self.draw_dot(pts[0], pts[1]))
        ids += (self.draw_dot(pts[2], pts[3]))
        ids += (self.draw_dot(pts[4], pts[5]))
        ids += (self.draw_dot(pts[6], pts[7]))
        self.canvas.update()
        return ids

    def draw_dot(self, x, y, color='black'):
        # create a list to collect item ids
        ids = list()
        ids.append(self.canvas.create_line(x+self.parameters['offset_x'], y+self.parameters['offset_y'], x+self.parameters['offset_x'], y+1+self.parameters['offset_y'], fill=color))
        return ids

    def transform(self, a):
        new_a = a * self.parameters['scale_factor'] + 0
        return new_a
。
    def flip_x(self, b):
        new_b = (wid-200) - b
        return new_b

    def flip_y(self, c):
        new_c = hei - c
        return new_c

    def transformation(self):
        for time_frame in self.time_frames:
            for item_y in ['Y1', 'Y2', 'Y3', 'Y4', 'Y5']:
                time_frame.info[item_y] = self.flip_x(self.transform(time_frame.info[item_y]))
            for item_z in ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']:
                time_frame.info[item_z] = self.flip_y(self.transform(time_frame.info[item_z]))
            for item_v in ['Y5\'', 'Z5\'']:
                time_frame.info[item_v[:-1]+'v'] = time_frame.info[item_v]
            for item_a in ['Y5\'\'', 'Z5\'\'']:
                time_frame.info[item_a[:-2]+'a'] = time_frame.info[item_a]

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
        self.parameters['total_frames'] = self.csv_data.shape[0]
        for i in range(self.parameters['total_frames']):
            information = dict()
            for title in column_titles:
                information[title] = self.csv_data[title].tolist()[i]
            self.time_frames.append(TimeFrame(i, information))


class TimeFrame:

    """
    A frame of frozen kinetics, depicting a certain time point
    """

    def __init__(self, i, information):
        self.number = i
        self.info = information
        print("Added time frame number "+str(i))


if __name__ == '__main__':
    root = Tk()
    wid = 1000
    hei = 800
    root.wm_title("Kinetics")
    root.geometry(str(wid) + "x" + str(hei) + "+200+50")
    app = Kinetics(root)
    root.mainloop()


# ①帧数的起止，以实际帧数为准，比如有的CSV文件起始帧数并不是1，有可能是2000+。
# ②抬起相的starting 和ending都有个开关，因为有时候我需要大致浏览一下总体的步态情况，然后再选择感兴趣的抬起相进行起止。
# ③a和v是否可以分开画呢
# ④咱们的运行过程中是否可以加入一个暂停pause键
# 同时再加上刚刚你说的那个功能，多加几个关键帧。
# 时间轴，打点
# 背景改成白色
# Pause暂停后可以继续
# 速度和加速度箭头长度调整
# 解决data0213的load问题
