from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import time
import pickle

colors = ['red', 'orange', 'gold', 'lime green', 'navy', 'dodger blue', 'dark violet']
greys = ['grey34', 'grey37', 'grey41', 'grey45', 'grey49', 'grey53', 'grey57', 'grey61', 'grey65', 'grey69']


class Kinetics(Frame):

    def __init__(self, master):
        super().__init__(master)

        # Viewer, controllers and settings 1
        self.fm_viewer_settings_1 = LabelFrame(self.master, text='Viewer', width=wid - 200)
        self.fm_viewer_settings_1.propagate(False)
        self.fm_viewer_settings_1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.canvas = Canvas(self.fm_viewer_settings_1, bg='white')
        self.canvas.config(width=wid - 200, height=hei-550)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        # Simulation Controller: Slider. The slider is defined elsewhere

        self.fm_settings_1 = Frame(self.fm_viewer_settings_1, width=wid - 200)
        self.fm_settings_1.propagate(False)
        self.fm_settings_1.pack(side=BOTTOM, fill=BOTH, expand=YES)

        # Simulation Controller: Button
        self.fm_controlling_buttons = Frame(self.fm_settings_1, width=wid - 200)
        self.fm_controlling_buttons.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.btn_start_over = Button(self.fm_controlling_buttons, text='Start over', command=self.start_over)
        self.btn_start_over.pack(side=LEFT, fill=BOTH, expand=YES)

        self.btn_pause = Button(self.fm_controlling_buttons, text='Pause', command=self.pause)
        self.btn_pause.pack(side=LEFT, fill=BOTH, expand=YES)

        self.btn_resume = Button(self.fm_controlling_buttons, text='Resume', command=self.resume)
        self.btn_resume.pack(side=LEFT, fill=BOTH, expand=YES)

        # Settings part 2
        self.fm_settings_2 = LabelFrame(self.master, text='Settings', width=200)
        self.fm_settings_2.propagate(False)
        self.fm_settings_2.pack(side=LEFT, fill=BOTH, expand=YES)

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
                           "lifted_period_1a": 414,
                           "lifted_period_1b": 430,
                           "lifted_period_2a": 0,
                           "lifted_period_2b": 0,
                           "lifted_period_3a": 0,
                           "lifted_period_3b": 0,
                           "lifted_period_4a": 0,
                           "lifted_period_4b": 0,
                           "lifted_period_5a": 0,
                           "lifted_period_5b": 0,
                           "lifted_period_6a": 0,
                           "lifted_period_6b": 0,
                           "lifted_period_7a": 0,
                           "lifted_period_7b": 0,
                           "lifted_period_8a": 0,
                           "lifted_period_8b": 0,
                           "lifted_period_9a": 0,
                           "lifted_period_9b": 0,
                           "lifted_period_10a": 0,
                           "lifted_period_10b": 0,
                           "colored_period_1a": 0,
                           "colored_period_1b": 0,
                           "colored_period_2a": 0,
                           "colored_period_2b": 0,
                           "colored_period_3a": 0,
                           "colored_period_3b": 0,
                           "colored_period_4a": 0,
                           "colored_period_4b": 0,
                           "colored_period_5a": 0,
                           "colored_period_5b": 0,
                           "colored_period_1_color": 'grey40',
                           "colored_period_2_color": 'grey40',
                           "colored_period_3_color": 'grey40',
                           "colored_period_4_color": 'grey40',
                           "colored_period_5_color": 'grey40'
                           }

        self.filename = 'data1.csv'

        # Controllers
        # Top-down layout
        self.lb_from_frame = Label(self.fm_settings_2, text='From frame:')
        self.lb_from_frame.pack(side=TOP, anchor='w')

        self.str_from_frame = StringVar()
        self.str_from_frame.set(self.parameters['start_frame'])
        self.spb_from_frame = Spinbox(self.fm_settings_2,
                                      from_=1,
                                      to=self.parameters['upper_frame_limit'],
                                      increment=1,
                                      textvariable=self.str_from_frame,
                                      command=self.set_start_frame)
        self.spb_from_frame.pack(side=TOP)

        self.lb_to_frame = Label(self.fm_settings_2, text='To frame:')
        self.lb_to_frame.pack(side=TOP, anchor='w')

        self.str_to_frame = StringVar()
        self.str_to_frame.set(self.parameters['end_frame'])
        self.spb_to_frame = Spinbox(self.fm_settings_2,
                                    from_=1,
                                    to=self.parameters['upper_frame_limit'],
                                    increment=1,
                                    textvariable=self.str_to_frame,
                                    command=self.set_end_frame)
        self.spb_to_frame.pack(side=TOP)

        self.lb_skip_frame = Label(self.fm_settings_2, text='Skip ? frame:')
        self.lb_skip_frame.pack(side=TOP, anchor='w')

        self.str_skip_frame = StringVar()
        self.str_skip_frame.set(self.parameters['skip_frame'])
        self.spb_skip_frame = Spinbox(self.fm_settings_2,
                                      from_=1,
                                      to=self.parameters['upper_frame_limit'],
                                      increment=1,
                                      textvariable=self.str_skip_frame,
                                      command=self.set_skip_frame)
        self.spb_skip_frame.pack(side=TOP)

        self.lb_offset_x = Label(self.fm_settings_2, text='Offset X:')
        self.lb_offset_x.pack(side=TOP, anchor='w')

        self.str_offset_x = StringVar()
        self.str_offset_x.set(self.parameters['offset_x'])
        self.spb_offset_x = Spinbox(self.fm_settings_2,
                                    from_=(wid-200)*(-1),
                                    to=(wid-200),
                                    increment=1,
                                    textvariable=self.str_offset_x,
                                    command=self.set_offset_x)
        self.spb_offset_x.pack(side=TOP)

        self.lb_offset_y = Label(self.fm_settings_2, text='Offset Y:')
        self.lb_offset_y.pack(side=TOP, anchor='w')

        self.str_offset_y = StringVar()
        self.str_offset_y.set(self.parameters['offset_y'])
        self.spb_offset_y = Spinbox(self.fm_settings_2,
                                    from_=hei*(-1),
                                    to=hei,
                                    increment=1,
                                    textvariable=self.str_offset_y,
                                    command=self.set_offset_y)
        self.spb_offset_y.pack(side=TOP)

        self.lb_sleep_time = Label(self.fm_settings_2, text='Sleep time:')
        self.lb_sleep_time.pack(side=TOP, anchor='w')

        self.str_sleep_time = StringVar()
        self.str_sleep_time.set(self.parameters['sleep_time'])
        self.spb_sleep_time = Spinbox(self.fm_settings_2,
                                      from_=0,
                                      to=1,
                                      increment=0.01,
                                      textvariable=self.str_sleep_time,
                                      command=self.set_sleep_time)
        self.spb_sleep_time.pack(side=TOP)

        self.lb_velocity_denominator = Label(self.fm_settings_2, text='Velocity (black) divided by:')
        self.lb_velocity_denominator.pack(side=TOP, anchor='w')

        self.str_velocity_denominator = StringVar()
        self.str_velocity_denominator.set(self.parameters['velocity_normalization_factor'])
        self.spb_velocity_denominator = Spinbox(self.fm_settings_2,
                                                from_=0.1,
                                                to=100,
                                                increment=0.1,
                                                textvariable=self.str_velocity_denominator,
                                                command=self.set_v_arrow_factor)
        self.spb_velocity_denominator.pack(side=TOP)

        self.lb_acceleration_denominator = Label(self.fm_settings_2, text='Acceleration (red) divided by:')
        self.lb_acceleration_denominator.pack(side=TOP, anchor='w')

        self.str_acceleration_denominator = StringVar()
        self.str_acceleration_denominator.set(self.parameters['acceleration_normalization_factor'])
        self.spb_acceleration_denominator = Spinbox(self.fm_settings_2,
                                                    from_=0.1,
                                                    to=1000,
                                                    increment=0.1,
                                                    textvariable=self.str_acceleration_denominator,
                                                    command=self.set_a_arrow_factor)
        self.spb_acceleration_denominator.pack(side=TOP)

        self.lb_sacle_factor = Label(self.fm_settings_2, text='Scale factor:')
        self.lb_sacle_factor.pack(side=TOP, anchor='w')

        self.str_scale_factor = StringVar()
        self.str_scale_factor.set(self.parameters['scale_factor'])
        self.spb_scale_factor = Spinbox(self.fm_settings_2,
                                        from_=0.1,
                                        to=10,
                                        increment=0.1,
                                        textvariable=self.str_scale_factor,
                                        command=self.set_scale_factor)
        self.spb_scale_factor.pack(side=TOP)

        self.chkvar_draw_sticks = IntVar()
        self.chkvar_draw_sticks.set(1)
        self.chkbtn_draw_sticks = Checkbutton(self.fm_settings_2, text="Draw sticks", variable=self.chkvar_draw_sticks,
                                              onvalue=1, offvalue=0,
                                              # height=5, width=20
                                              )
        self.chkbtn_draw_sticks.pack(side=TOP, anchor='w')

        self.chkvar_draw_in_colors = IntVar()
        self.chkvar_draw_in_colors.set(0)
        self.chkbtn_draw_in_colors = Checkbutton(self.fm_settings_2, text="Draw in colors", variable=self.chkvar_draw_in_colors,
                                                 onvalue=1, offvalue=0,
                                                 # height=5, width=20
                                                 )
        self.chkbtn_draw_in_colors.pack(side=TOP, anchor='w')

        self.chkvar_draw_acceleration = IntVar()
        self.chkvar_draw_acceleration.set(1)
        self.chkbtn_draw_acceleration = Checkbutton(self.fm_settings_2, text="Draw Acceleration", variable=self.chkvar_draw_acceleration,
                                                    onvalue=1, offvalue=0,
                                                    # height=5, width=20
                                                    )
        self.chkbtn_draw_acceleration.pack(side=TOP, anchor='w')

        self.chkvar_draw_velocity = IntVar()
        self.chkvar_draw_velocity.set(1)
        self.chkbtn_draw_velocity = Checkbutton(self.fm_settings_2, text="Draw Velocity", variable=self.chkvar_draw_velocity,
                                                onvalue=1, offvalue=0,
                                                # height=5, width=20
                                                )
        self.chkbtn_draw_velocity.pack(side=TOP, anchor='w')

        self.chkvar_draw_toe_end = IntVar()
        self.chkvar_draw_toe_end.set(1)
        self.chkbtn_draw_toe_end = Checkbutton(self.fm_settings_2, text="Draw toe end", variable=self.chkvar_draw_toe_end,
                                               onvalue=1, offvalue=0,
                                               # height=5, width=20
                                               )
        self.chkbtn_draw_toe_end.pack(side=TOP, anchor='w')

        self.chkvar_draw_from_beginning = IntVar()
        self.chkvar_draw_from_beginning.set(0)
        self.chkbtn_draw_from_beginning = Checkbutton(self.fm_settings_2, text="Draw from beginning", variable=self.chkvar_draw_from_beginning,
                                                      onvalue=1, offvalue=0,
                                                      # height=5, width=20
                                                      )
        self.chkbtn_draw_from_beginning.pack(side=TOP, anchor='w')

        self.chkvar_draw_to_end = IntVar()
        self.chkvar_draw_to_end.set(0)
        self.chkbtn_draw_to_end = Checkbutton(self.fm_settings_2, text="Draw to ending", variable=self.chkvar_draw_to_end,
                                              onvalue=1, offvalue=0,
                                              # height=5, width=20
                                              )
        self.chkbtn_draw_to_end.pack(side=TOP, anchor='w')

        self.chkvar_horizontal_flip = IntVar()
        self.chkvar_horizontal_flip.set(1)
        self.chkbtn_horizontal_flip = Checkbutton(self.fm_settings_2, text="Horizontal Flip", variable=self.chkvar_horizontal_flip,
                                                  onvalue=1, offvalue=0,
                                                  # height=5, width=20
                                                  )
        self.chkbtn_horizontal_flip.pack(side=TOP, anchor='w')

        self.btn_save_parameters = Button(self.fm_settings_2, text='Save parameters', width=50, command=self.save_parameters)
        self.btn_save_parameters.pack(side=TOP)

        self.btn_load = Button(self.fm_settings_2, text='Load file', width=100, command=self.load_file)
        self.btn_load.pack(side=BOTTOM)

        self.lb_file_name = Label(self.fm_settings_2, text=self.filename,
                                  # height=50,
                                  justify='center', wraplength=180)
        self.lb_file_name.pack(side=BOTTOM)

        ###################
        # Settings bottom #
        ###################

        # Lifted periods
        self.fm_lifted_periods = LabelFrame(self.fm_settings_1, text='Lifted periods')
        self.fm_lifted_periods.pack(side=TOP, fill=BOTH, expand=YES)

        # Bottom-up layout, setting lifted periods
        self.fm_up_1_5 = Frame(self.fm_lifted_periods, width=wid - 200)
        self.fm_up_1_5.pack(side=TOP, fill=BOTH, expand=YES)
        # up1a
        self.lb_up1a = Label(self.fm_up_1_5, text='Up1A:')
        self.lb_up1a.pack(side=LEFT, anchor='w')

        self.str_up1a = StringVar()
        self.str_up1a.set(self.parameters['lifted_period_1a'])
        self.spb_up1a = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up1a,
                                command=self.set_lifted_1a)
        self.spb_up1a.pack(side=LEFT, expand=YES)
        # up1b
        self.lb_up1b = Label(self.fm_up_1_5, text='Up1B:')
        self.lb_up1b.pack(side=LEFT, anchor='w')

        self.str_up1b = StringVar()
        self.str_up1b.set(self.parameters['lifted_period_1b'])
        self.spb_up1b = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up1b,
                                command=self.set_lifted_1b)
        self.spb_up1b.pack(side=LEFT, expand=YES)
        # up2a
        self.lb_up2a = Label(self.fm_up_1_5, text='Up2A:')
        self.lb_up2a.pack(side=LEFT, anchor='w')

        self.str_up2a = StringVar()
        self.str_up2a.set(self.parameters['lifted_period_2a'])
        self.spb_up2a = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up2a,
                                command=self.set_lifted_2a)
        self.spb_up2a.pack(side=LEFT, expand=YES)
        # up2b
        self.lb_up2b = Label(self.fm_up_1_5, text='Up2B:')
        self.lb_up2b.pack(side=LEFT, anchor='w')

        self.str_up2b = StringVar()
        self.str_up2b.set(self.parameters['lifted_period_2b'])
        self.spb_up2b = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up2b,
                                command=self.set_lifted_2b)
        self.spb_up2b.pack(side=LEFT, expand=YES)
        # up3a
        self.lb_up3a = Label(self.fm_up_1_5, text='Up3A:')
        self.lb_up3a.pack(side=LEFT, anchor='w')

        self.str_up3a = StringVar()
        self.str_up3a.set(self.parameters['lifted_period_3a'])
        self.spb_up3a = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up3a,
                                command=self.set_lifted_3a)
        self.spb_up3a.pack(side=LEFT, expand=YES)
        # up3b
        self.lb_up3b = Label(self.fm_up_1_5, text='Up3B:')
        self.lb_up3b.pack(side=LEFT, anchor='w')

        self.str_up3b = StringVar()
        self.str_up3b.set(self.parameters['lifted_period_3b'])
        self.spb_up3b = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up3b,
                                command=self.set_lifted_3b)
        self.spb_up3b.pack(side=LEFT, expand=YES)
        # up4a
        self.lb_up4a = Label(self.fm_up_1_5, text='Up4A:')
        self.lb_up4a.pack(side=LEFT, anchor='w')

        self.str_up4a = StringVar()
        self.str_up4a.set(self.parameters['lifted_period_4a'])
        self.spb_up4a = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up4a,
                                command=self.set_lifted_4a)
        self.spb_up4a.pack(side=LEFT, expand=YES)
        # up4b
        self.lb_up4b = Label(self.fm_up_1_5, text='Up4B:')
        self.lb_up4b.pack(side=LEFT, anchor='w')

        self.str_up4b = StringVar()
        self.str_up4b.set(self.parameters['lifted_period_4b'])
        self.spb_up4b = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up4b,
                                command=self.set_lifted_4b)
        self.spb_up4b.pack(side=LEFT, expand=YES)
        # up5a
        self.lb_up5a = Label(self.fm_up_1_5, text='Up5A:')
        self.lb_up5a.pack(side=LEFT, anchor='w')

        self.str_up5a = StringVar()
        self.str_up5a.set(self.parameters['lifted_period_4a'])
        self.spb_up5a = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up5a,
                                command=self.set_lifted_5a)
        self.spb_up5a.pack(side=LEFT, expand=YES)
        # up5b
        self.lb_up5b = Label(self.fm_up_1_5, text='Up5B:')
        self.lb_up5b.pack(side=LEFT, anchor='w')

        self.str_up5b = StringVar()
        self.str_up5b.set(self.parameters['lifted_period_4b'])
        self.spb_up5b = Spinbox(self.fm_up_1_5,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up5b,
                                command=self.set_lifted_5b)
        self.spb_up5b.pack(side=LEFT, expand=YES)

        self.fm_up_6_10 = Frame(self.fm_lifted_periods, width=wid - 200)
        self.fm_up_6_10.pack(side=TOP, fill=BOTH, expand=YES)
        # up6a
        self.lb_up6a = Label(self.fm_up_6_10, text='Up6A:')
        self.lb_up6a.pack(side=LEFT, anchor='w')

        self.str_up6a = StringVar()
        self.str_up6a.set(self.parameters['lifted_period_6a'])
        self.spb_up6a = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up6a,
                                command=self.set_lifted_6a)
        self.spb_up6a.pack(side=LEFT, expand=YES)
        # up6b
        self.lb_up6b = Label(self.fm_up_6_10, text='Up6B:')
        self.lb_up6b.pack(side=LEFT, anchor='w')

        self.str_up6b = StringVar()
        self.str_up6b.set(self.parameters['lifted_period_6b'])
        self.spb_up6b = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up6b,
                                command=self.set_lifted_6b)
        self.spb_up6b.pack(side=LEFT, expand=YES)
        # up7a
        self.lb_up7a = Label(self.fm_up_6_10, text='Up7A:')
        self.lb_up7a.pack(side=LEFT, anchor='w')

        self.str_up7a = StringVar()
        self.str_up7a.set(self.parameters['lifted_period_7a'])
        self.spb_up7a = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up7a,
                                command=self.set_lifted_7a)
        self.spb_up7a.pack(side=LEFT, expand=YES)
        # up7b
        self.lb_up7b = Label(self.fm_up_6_10, text='Up7B:')
        self.lb_up7b.pack(side=LEFT, anchor='w')

        self.str_up7b= StringVar()
        self.str_up7b.set(self.parameters['lifted_period_7b'])
        self.spb_up7b = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up7b,
                                command=self.set_lifted_7b)
        self.spb_up7b.pack(side=LEFT, expand=YES)
        # up8a
        self.lb_up8a = Label(self.fm_up_6_10, text='Up8A:')
        self.lb_up8a.pack(side=LEFT, anchor='w')

        self.str_up8a = StringVar()
        self.str_up8a.set(self.parameters['lifted_period_8a'])
        self.spb_up8a = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up8a,
                                command=self.set_lifted_8a)
        self.spb_up8a.pack(side=LEFT, expand=YES)
        # up8b
        self.lb_up8b = Label(self.fm_up_6_10, text='Up8B:')
        self.lb_up8b.pack(side=LEFT, anchor='w')

        self.str_up8b = StringVar()
        self.str_up8b.set(self.parameters['lifted_period_8b'])
        self.spb_up8b = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up8b,
                                command=self.set_lifted_8b)
        self.spb_up8b.pack(side=LEFT, expand=YES)
        # up9a
        self.lb_up9a = Label(self.fm_up_6_10, text='Up9A:')
        self.lb_up9a.pack(side=LEFT, anchor='w')

        self.str_up9a = StringVar()
        self.str_up9a.set(self.parameters['lifted_period_9a'])
        self.spb_up9a = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up9a,
                                command=self.set_lifted_9a)
        self.spb_up9a.pack(side=LEFT, expand=YES)
        # up9b
        self.lb_up9b = Label(self.fm_up_6_10, text='Up9B:')
        self.lb_up9b.pack(side=LEFT, anchor='w')

        self.str_up9b = StringVar()
        self.str_up9b.set(self.parameters['lifted_period_9b'])
        self.spb_up9b = Spinbox(self.fm_up_6_10,
                                width=5,
                                from_=1,
                                to=self.parameters['upper_frame_limit'],
                                increment=1,
                                textvariable=self.str_up9b,
                                command=self.set_lifted_9b)
        self.spb_up9b.pack(side=LEFT, expand=YES)
        # up10a
        self.lb_up10a = Label(self.fm_up_6_10, text='Up10A:')
        self.lb_up10a.pack(side=LEFT, anchor='w')

        self.str_up10a = StringVar()
        self.str_up10a.set(self.parameters['lifted_period_10a'])
        self.spb_up10a = Spinbox(self.fm_up_6_10,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_up10a,
                                 command=self.set_lifted_10a)
        self.spb_up10a.pack(side=LEFT, expand=YES)
        # up10b
        self.lb_up10b = Label(self.fm_up_6_10, text='Up10B:')
        self.lb_up10b.pack(side=LEFT, anchor='w')

        self.str_up10b = StringVar()
        self.str_up10b.set(self.parameters['lifted_period_10b'])
        self.spb_up10b = Spinbox(self.fm_up_6_10,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_up10b,
                                 command=self.set_lifted_10b)
        self.spb_up10b.pack(side=LEFT, expand=YES)

        # colored periods
        self.fm_colored_periods = LabelFrame(self.fm_settings_1, text='Colored periods', width=wid - 200)
        self.fm_colored_periods.pack(side=TOP, fill=BOTH, expand=YES)

        # col1a
        self.lb_col1a = Label(self.fm_colored_periods, text='Col1A:')
        self.lb_col1a.pack(side=LEFT, anchor='w')

        self.str_col1a = StringVar()
        self.str_col1a.set(self.parameters['colored_period_1a'])
        self.spb_col1a = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col1a,
                                 command=self.set_col_1a)
        self.spb_col1a.pack(side=LEFT, expand=YES)

        # col1b
        self.lb_col1b = Label(self.fm_colored_periods, text='Col1B:')
        self.lb_col1b.pack(side=LEFT, anchor='w')

        self.str_col1b = StringVar()
        self.str_col1b.set(self.parameters['colored_period_1b'])
        self.spb_col1b = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col1b,
                                 command=self.set_col_1b)
        self.spb_col1b.pack(side=LEFT, expand=YES)

        # col2a
        self.lb_col2a = Label(self.fm_colored_periods, text='Col2A:')
        self.lb_col2a.pack(side=LEFT, anchor='w')

        self.str_col2a = StringVar()
        self.str_col2a.set(self.parameters['colored_period_2a'])
        self.spb_col2a = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col2a,
                                 command=self.set_col_2a)
        self.spb_col2a.pack(side=LEFT, expand=YES)

        # col2b
        self.lb_col2b = Label(self.fm_colored_periods, text='Col2B:')
        self.lb_col2b.pack(side=LEFT, anchor='w')

        self.str_col2b = StringVar()
        self.str_col2b.set(self.parameters['colored_period_2b'])
        self.spb_col2b = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col2b,
                                 command=self.set_col_2b)
        self.spb_col2b.pack(side=LEFT, expand=YES)

        # col3a
        self.lb_col3a = Label(self.fm_colored_periods, text='Col3A:')
        self.lb_col3a.pack(side=LEFT, anchor='w')

        self.str_col3a = StringVar()
        self.str_col3a.set(self.parameters['colored_period_3a'])
        self.spb_col3a = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col3a,
                                 command=self.set_col_3a)
        self.spb_col3a.pack(side=LEFT, expand=YES)

        # col3b
        self.lb_col3b = Label(self.fm_colored_periods, text='Col3B:')
        self.lb_col3b.pack(side=LEFT, anchor='w')

        self.str_col3b = StringVar()
        self.str_col3b.set(self.parameters['colored_period_3b'])
        self.spb_col3b = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col3b,
                                 command=self.set_col_3b)
        self.spb_col3b.pack(side=LEFT, expand=YES)

        # col4a
        self.lb_col4a = Label(self.fm_colored_periods, text='Col4A:')
        self.lb_col4a.pack(side=LEFT, anchor='w')

        self.str_col4a = StringVar()
        self.str_col4a.set(self.parameters['colored_period_4a'])
        self.spb_col4a = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col4a,
                                 command=self.set_col_4a)
        self.spb_col4a.pack(side=LEFT, expand=YES)

        # col4b
        self.lb_col4b = Label(self.fm_colored_periods, text='Col4B:')
        self.lb_col4b.pack(side=LEFT, anchor='w')

        self.str_col4b = StringVar()
        self.str_col4b.set(self.parameters['colored_period_4b'])
        self.spb_col4b = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col4b,
                                 command=self.set_col_4b)
        self.spb_col4b.pack(side=LEFT, expand=YES)

        # col5a
        self.lb_col5a = Label(self.fm_colored_periods, text='Col5A:')
        self.lb_col5a.pack(side=LEFT, anchor='w')

        self.str_col5a = StringVar()
        self.str_col5a.set(self.parameters['colored_period_5a'])
        self.spb_col5a = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col5a,
                                 command=self.set_col_5a)
        self.spb_col5a.pack(side=LEFT, expand=YES)

        # col5b
        self.lb_col5b = Label(self.fm_colored_periods, text='Col5B:')
        self.lb_col5b.pack(side=LEFT, anchor='w')

        self.str_col5b = StringVar()
        self.str_col5b.set(self.parameters['colored_period_5b'])
        self.spb_col5b = Spinbox(self.fm_colored_periods,
                                 width=5,
                                 from_=1,
                                 to=self.parameters['upper_frame_limit'],
                                 increment=1,
                                 textvariable=self.str_col5b,
                                 command=self.set_col_5b)
        self.spb_col5b.pack(side=LEFT, expand=YES)

        # color selection
        self.fm_color_selection = LabelFrame(self.fm_settings_1, text='Color selection', width=wid - 200)
        self.fm_color_selection.pack(side=TOP, fill=BOTH, expand=YES)

        self.cbox_color1 = ttk.Combobox(self.fm_color_selection, values=colors)
        self.cbox_color1.pack(side=LEFT, expand=YES)
        self.cbox_color1.bind("<<ComboboxSelected>>", self.set_period1_color)

        self.cbox_color2 = ttk.Combobox(self.fm_color_selection, values=colors)
        self.cbox_color2.pack(side=LEFT, expand=YES)
        self.cbox_color2.bind("<<ComboboxSelected>>", self.set_period2_color)

        self.cbox_color3 = ttk.Combobox(self.fm_color_selection, values=colors)
        self.cbox_color3.pack(side=LEFT, expand=YES)
        self.cbox_color3.bind("<<ComboboxSelected>>", self.set_period3_color)

        self.cbox_color4 = ttk.Combobox(self.fm_color_selection, values=colors)
        self.cbox_color4.pack(side=LEFT, expand=YES)
        self.cbox_color4.bind("<<ComboboxSelected>>", self.set_period4_color)

        self.cbox_color5 = ttk.Combobox(self.fm_color_selection, values=colors)
        self.cbox_color5.pack(side=LEFT, expand=YES)
        self.cbox_color5.bind("<<ComboboxSelected>>", self.set_period5_color)


        # displaying frame range
        self.fm_display_frame_range = Frame(self.fm_settings_1, width=wid - 200)
        self.fm_display_frame_range.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.lb_frame_upper_int = IntVar()
        self.lb_frame_upper_int.set(self.parameters['upper_frame_limit'])
        self.lb_frame_upper_str = StringVar()
        self.lb_frame_upper_str.set("Frame to: " + str(self.lb_frame_upper_int.get()))
        self.lb_frame_upper = Label(self.fm_display_frame_range, textvariable=self.lb_frame_upper_str)
        self.lb_frame_upper.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.lb_frame_lower_int = IntVar()
        self.lb_frame_lower_int.set(self.parameters['lower_frame_limit'])
        self.lb_frame_lower_str = StringVar()
        self.lb_frame_lower_str.set("Frame from: " + str(self.lb_frame_lower_int.get()))
        self.lb_frame_lower = Label(self.fm_display_frame_range, textvariable=self.lb_frame_lower_str)
        self.lb_frame_lower.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.pack(fill=BOTH, expand=1)

        # read file
        self.time_frames = list()
        self.csv_data = None
        self.read_in()

        # pause and resume
        self.frame_counter = 0
        self.drawing_counter = 0  # Counting time frames to determine the color in color mode
        self.paused = False
        self.paused_at_frame = 0

        # canvas item ids
        self.canvas_ids = dict()

        # lifted frames
        self.lifted_frames = list()
        self.threshold_on = list()

        # colored frames
        self.colored_period_1 = list()
        self.colored_period_2 = list()
        self.colored_period_3 = list()
        self.colored_period_4 = list()
        self.colored_period_5 = list()

    def read_in_from_saved(self):
        f = open(self.filename + '.frames', "rb")
        self.time_frames = pickle.load(f)
        f.close()
        print("Time frame data loaded from saved file.")

    def read_in_from_new(self):
        print("Time frame data file is not found. Generating...")
        self.csv_data = None
        self.read_csv_data(self.filename)

        # generate time frames
        self.generate_time_frames()

    def read_in(self):
        try:
            self.read_in_from_saved()
        except IOError:
            self.read_in_from_new()

        self.parameters['upper_frame_limit'] = int(self.time_frames[-1].info['Frame'])
        self.parameters['lower_frame_limit'] = int(self.time_frames[0].info['Frame'])
        self.ensure_start_end_range()

        self.lb_frame_upper_int.set(self.parameters['upper_frame_limit'])
        self.lb_frame_upper_str.set("Frames to: " + str(self.parameters['upper_frame_limit']))
        self.lb_frame_lower_int.set(self.parameters['lower_frame_limit'])
        self.lb_frame_lower_str.set("Frames from: " + str(self.parameters['lower_frame_limit']))

        # Add the slider
        try:
            self.slider.destroy()
        except:
            pass
        self.slider = Scale(self.fm_settings_1,
                            # from_=self.parameters['start_frame'],
                            from_=self.parameters['lower_frame_limit'],
                            to=self.parameters['upper_frame_limit'],  # Temporarily like this
                            orient="horizontal")
        self.slider.bind("<ButtonRelease-1>",
                         func=self.start_from_a_certain_frame
                         )
        self.slider.pack(side=BOTTOM, fill=X, expand=YES)
        print("Parameters:\n", self.parameters)

    def ensure_start_end_range(self):
        # Ensure simulation range within upper and lower boundary
        if self.parameters['end_frame'] > self.parameters['upper_frame_limit'] or self.parameters['end_frame'] < self.parameters['lower_frame_limit']:
            self.parameters['end_frame'] = self.parameters['upper_frame_limit']
            self.str_to_frame.set(self.parameters['end_frame'])

        if self.parameters['start_frame'] < self.parameters['lower_frame_limit'] or self.parameters['start_frame'] > self.parameters['upper_frame_limit']:
            self.parameters['start_frame'] = self.parameters['lower_frame_limit']
            self.str_from_frame.set(self.parameters['start_frame'])

    def draw_time_frames(self, starting, ending):
        print("Start drawing time frames...")
        print("Starting from {}, ending by {}".format(starting, ending))

        self.last_point = [0, 0]  # Store the last point for drawing toe_end

        if self.chkvar_draw_from_beginning.get() == 1:  # If drawing from beginning
            starting = int(self.parameters['lower_frame_limit'])

        if self.chkvar_draw_to_end.get() == 1:  # If drawing to the end
            ending = int(self.parameters['upper_frame_limit'])

        for i in range(starting, ending+1):  # ending is not included in range, so +1 is needed
            # Use a list to collect ids on Canvas of this frame
            ids = list()

            # print("Drawing frame {}...".format(i))
            if self.paused:  # exit when paused
                return

            t = self.time_frames[i - self.parameters['lower_frame_limit']]  # temporary variable, the current time frame

            # Decide the color

            def find_color_by_period():
                if self.parameters['colored_period_1a'] < i < self.parameters['colored_period_1b']:
                    return self.parameters['colored_period_1_color']
                elif self.parameters['colored_period_2a'] < i < self.parameters['colored_period_2b']:
                    return self.parameters['colored_period_2_color']
                elif self.parameters['colored_period_3a'] < i < self.parameters['colored_period_3b']:
                    return self.parameters['colored_period_3_color']
                elif self.parameters['colored_period_4a'] < i < self.parameters['colored_period_4b']:
                    return self.parameters['colored_period_4_color']
                elif self.parameters['colored_period_5a'] < i < self.parameters['colored_period_5b']:
                    return self.parameters['colored_period_5_color']
                else:
                    return 'grey40'

            if self.chkvar_draw_in_colors.get() == 1:
                color = colors[self.drawing_counter % 7]
            else:
                color = find_color_by_period()

            # Draw the threshold on time point
            if i in self.threshold_on:  # There are multiple frames for threshold on
                print('Draw V/A for this ''threshold on'' frame')
                ids += self.draw_velocity_acceleration(t.info)

            # Draw the sticks
            # 200 Hz -> lower frequency, but frequency gets higher in the lifted part.

            # in a frame range, raise the frequency
            if self.frame_counter in self.lifted_frames:
                real_time_skip_frame = max(self.parameters['skip_frame']/10, 1)  # increase frequency by lowering skip_frame
            else:
                real_time_skip_frame = self.parameters['skip_frame']

            if i % real_time_skip_frame == 0 and starting <= i <= ending:  # draw stick
                if self.chkvar_draw_sticks.get() == 1:  # check if to draw the sticks
                    ids += self.draw_stick(
                        [t.info['Y1'], t.info['Z1'], t.info['Y2'], t.info['Z2'],
                         t.info['Y3'], t.info['Z3'], t.info['Y4'], t.info['Z4'],
                         t.info['Y5'], t.info['Z5']],
                        # color=colors[drawing_counter % 7] if self.chkvar_draw_in_colors.get() == 1 else greys[drawing_counter % 10]
                        color=color)
                    time.sleep(self.parameters['sleep_time'])

            # Draw the toe end
            if starting <= i <= ending and self.chkvar_draw_toe_end.get() == 1:  # Apply to every time frame
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
        if self.chkvar_draw_toe_end.get() == 1:
            self.canvas_ids[self.frame_counter] += self.draw_toe_end(t)

    def start_from_a_certain_frame(self):
        self.pause()

        if self.slider.get() < self.paused_at_frame:  # the slider bar was dragged backward
            print(self.slider.get(), self.paused_at_frame)
            for i in range(self.paused_at_frame, self.slider.get(), -1):  # loop backward
                if i in self.canvas_ids.keys():
                    for j in self.canvas_ids[i]:
                        self.canvas.delete(j)  # delete all items on canvas that after this new starting point
                        self.canvas.update()
        if self.paused_at_frame < self.slider.get():  # the slider bar was dragged forward
            print(self.paused_at_frame, self.slider.get())
            self.paused = False
            self.draw_time_frames(self.paused_at_frame, self.slider.get())  # draw the added frames
            self.paused = True

        self.canvas.update()
        self.paused_at_frame = self.slider.get()

    def set_start_frame(self):
        self.parameters['start_frame'] = int(self.spb_from_frame.get())

        # Reset the slider
        self.slider.destroy()
        self.slider = Scale(self.fm_settings_1,
                            # from_=self.parameters['start_frame'],
                            from_=self.parameters['lower_frame_limit'],
                            to=self.parameters['upper_frame_limit'],  # Temporarily like this
                            orient="horizontal")
        self.slider.bind("<ButtonRelease-1>",
                         func=self.start_from_a_certain_frame
                         )
        self.slider.pack(side=BOTTOM, fill=X, expand=YES)

    def set_end_frame(self):
        self.parameters['end_frame'] = int(self.spb_to_frame.get())

        # Reset the slider
        self.slider.destroy()
        self.slider = Scale(self.fm_settings_1,
                            # from_=self.parameters['start_frame'],
                            from_=self.parameters['lower_frame_limit'],
                            to=self.parameters['upper_frame_limit'],  # Temporarily like this
                            orient="horizontal")
        self.slider.bind("<ButtonRelease-1>",
                         func=self.start_from_a_certain_frame
                         )
        self.slider.pack(side=BOTTOM, fill=X, expand=YES)

    def set_skip_frame(self):
        self.parameters['skip_frame'] = int(self.spb_skip_frame.get())

    def set_offset_x(self):
        self.parameters['offset_x'] = int(self.spb_offset_x.get())

    def set_offset_y(self):
        self.parameters['offset_y'] = int(self.spb_offset_y.get())

    def set_sleep_time(self):
        self.parameters['sleep_time'] = float(self.spb_sleep_time.get())

    def set_lifted_1a(self):
        self.parameters['lifted_period_1a'] = int(self.spb_up1a.get())

    def set_lifted_1b(self):
        self.parameters['lifted_period_1b'] = int(self.spb_up1b.get())

    def set_lifted_2a(self):
        self.parameters['lifted_period_2a'] = int(self.spb_up2a.get())

    def set_lifted_2b(self):
        self.parameters['lifted_period_2b'] = int(self.spb_up2b.get())

    def set_lifted_3a(self):
        self.parameters['lifted_period_3a'] = int(self.spb_up3a.get())

    def set_lifted_3b(self):
        self.parameters['lifted_period_3b'] = int(self.spb_up3b.get())

    def set_lifted_4a(self):
        self.parameters['lifted_period_4a'] = int(self.spb_up4a.get())

    def set_lifted_4b(self):
        self.parameters['lifted_period_4b'] = int(self.spb_up4b.get())

    def set_lifted_5a(self):
        self.parameters['lifted_period_5a'] = int(self.spb_up5a.get())

    def set_lifted_5b(self):
        self.parameters['lifted_period_5b'] = int(self.spb_up5b.get())

    def set_lifted_6a(self):
        self.parameters['lifted_period_6a'] = int(self.spb_up6a.get())

    def set_lifted_6b(self):
        self.parameters['lifted_period_6b'] = int(self.spb_up6b.get())

    def set_lifted_7a(self):
        self.parameters['lifted_period_7a'] = int(self.spb_up7a.get())

    def set_lifted_7b(self):
        self.parameters['lifted_period_7b'] = int(self.spb_up7b.get())

    def set_lifted_8a(self):
        self.parameters['lifted_period_8a'] = int(self.spb_up8a.get())

    def set_lifted_8b(self):
        self.parameters['lifted_period_8b'] = int(self.spb_up8b.get())

    def set_lifted_9a(self):
        self.parameters['lifted_period_9a'] = int(self.spb_up9a.get())

    def set_lifted_9b(self):
        self.parameters['lifted_period_9b'] = int(self.spb_up9b.get())

    def set_lifted_10a(self):
        self.parameters['lifted_period_10a'] = int(self.spb_up10a.get())

    def set_lifted_10b(self):
        self.parameters['lifted_period_10b'] = int(self.spb_up10b.get())

    def set_col_1a(self):
        self.parameters['colored_period_1a'] = int(self.spb_col1a.get())

    def set_col_1b(self):
        self.parameters['colored_period_1b'] = int(self.spb_col1b.get())

    def set_col_2a(self):
        self.parameters['colored_period_2a'] = int(self.spb_col2a.get())

    def set_col_2b(self):
        self.parameters['colored_period_2b'] = int(self.spb_col2b.get())

    def set_col_3a(self):
        self.parameters['colored_period_3a'] = int(self.spb_col3a.get())

    def set_col_3b(self):
        self.parameters['colored_period_3b'] = int(self.spb_col3b.get())

    def set_col_4a(self):
        self.parameters['colored_period_4a'] = int(self.spb_col4a.get())

    def set_col_4b(self):
        self.parameters['colored_period_4b'] = int(self.spb_col4b.get())

    def set_col_5a(self):
        self.parameters['colored_period_5a'] = int(self.spb_col5a.get())

    def set_col_5b(self):
        self.parameters['colored_period_5b'] = int(self.spb_col5b.get())

    def set_period1_color(self, *evt):
        self.parameters['colored_period_1_color'] = self.cbox_color1.get()

    def set_period2_color(self, *evt):
        self.parameters['colored_period_2_color'] = self.cbox_color2.get()

    def set_period3_color(self, *evt):
        self.parameters['colored_period_3_color'] = self.cbox_color3.get()

    def set_period4_color(self, *evt):
        self.parameters['colored_period_4_color'] = self.cbox_color4.get()

    def set_period5_color(self, *evt):
        self.parameters['colored_period_5_color'] = self.cbox_color5.get()

    def set_v_arrow_factor(self):
        self.parameters['velocity_normalization_factor'] = float(self.spb_velocity_denominator.get())

    def set_a_arrow_factor(self):
        self.parameters['acceleration_normalization_factor'] = float(self.spb_acceleration_denominator.get())

    def set_scale_factor(self):
        self.parameters['scale_factor'] = float(self.spb_scale_factor.get())

    def set_lifted_periods(self):
        self.threshold_on.clear()
        self.lifted_frames.clear()

        self.set_lifted_1a()
        self.set_lifted_1b()
        self.lifted_frames += list(range(self.parameters['lifted_period_1a'], self.parameters['lifted_period_1b']+1))

        self.set_lifted_2a()
        self.set_lifted_2b()
        self.lifted_frames += list(range(self.parameters['lifted_period_2a'], self.parameters['lifted_period_2b']+1))

        self.set_lifted_3a()
        self.set_lifted_3b()
        self.lifted_frames += list(range(self.parameters['lifted_period_3a'], self.parameters['lifted_period_3b']+1))

        self.set_lifted_4a()
        self.set_lifted_4b()
        self.lifted_frames += list(range(self.parameters['lifted_period_4a'], self.parameters['lifted_period_4b']+1))

        self.set_lifted_5a()
        self.set_lifted_5b()
        self.lifted_frames += list(range(self.parameters['lifted_period_5a'], self.parameters['lifted_period_5b']+1))

        self.set_lifted_6a()
        self.set_lifted_6b()
        self.lifted_frames += list(range(self.parameters['lifted_period_6a'], self.parameters['lifted_period_6b']+1))

        self.set_lifted_7a()
        self.set_lifted_7b()
        self.lifted_frames += list(range(self.parameters['lifted_period_7a'], self.parameters['lifted_period_7b']+1))

        self.set_lifted_8a()
        self.set_lifted_8b()
        self.lifted_frames += list(range(self.parameters['lifted_period_8a'], self.parameters['lifted_period_8b']+1))

        self.set_lifted_9a()
        self.set_lifted_9b()
        self.lifted_frames += list(range(self.parameters['lifted_period_9a'], self.parameters['lifted_period_9b']+1))

        self.set_lifted_10a()
        self.set_lifted_10b()
        self.lifted_frames += list(range(self.parameters['lifted_period_10a'], self.parameters['lifted_period_10b']+1))

        self.threshold_on.append(self.parameters['lifted_period_1a'])
        self.threshold_on.append(self.parameters['lifted_period_2a'])
        self.threshold_on.append(self.parameters['lifted_period_3a'])
        self.threshold_on.append(self.parameters['lifted_period_4a'])
        self.threshold_on.append(self.parameters['lifted_period_5a'])
        self.threshold_on.append(self.parameters['lifted_period_6a'])
        self.threshold_on.append(self.parameters['lifted_period_7a'])
        self.threshold_on.append(self.parameters['lifted_period_8a'])
        self.threshold_on.append(self.parameters['lifted_period_9a'])
        self.threshold_on.append(self.parameters['lifted_period_10a'])

    def set_colored_periods(self):
        self.set_col_1a()
        self.set_col_1b()
        self.set_col_2a()
        self.set_col_2b()
        self.set_col_3a()
        self.set_col_3b()
        self.set_col_4a()
        self.set_col_4b()
        self.set_col_5a()
        self.set_col_5b()

    def start_over(self):
        self.paused = False  # clear the paused flag

        # manually update parameters

        self.set_start_frame()
        self.set_end_frame()
        self.set_skip_frame()
        self.set_offset_x()
        self.set_offset_y()
        self.set_sleep_time()
        self.set_lifted_periods()
        self.set_colored_periods()
        self.set_v_arrow_factor()
        self.set_a_arrow_factor()
        self.set_scale_factor()

        self.canvas.delete('all')
        self.canvas.update()

        self.draw_time_frames(self.parameters['start_frame'], self.parameters['end_frame'])

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False  # clear the paused flag

        self.parameters['start_frame'] = self.paused_at_frame
        self.set_end_frame()
        self.set_skip_frame()
        self.set_offset_x()
        self.set_offset_y()
        self.set_sleep_time()
        self.set_lifted_periods()
        self.set_v_arrow_factor()
        self.set_a_arrow_factor()
        self.set_scale_factor()

        self.draw_time_frames(self.parameters['start_frame'], self.parameters['end_frame'])

    def save_parameters(self):
        f1 = open(self.filename + '.params', "wb")
        pickle.dump(self.parameters, f1)
        f1.close()
        print("Parameters for", self.filename, "saved.")

    def update_ui_parameters(self):
        self.str_from_frame.set(self.parameters['start_frame'])
        self.str_to_frame.set(self.parameters['end_frame'])
        self.str_skip_frame.set(self.parameters['skip_frame'])
        self.str_offset_x.set(self.parameters['offset_x'])
        self.str_offset_y.set(self.parameters['offset_y'])
        self.str_sleep_time.set(self.parameters['sleep_time'])
        self.set_lifted_periods()
        self.str_velocity_denominator.set(self.parameters['velocity_normalization_factor'])
        self.str_acceleration_denominator.set(self.parameters['acceleration_normalization_factor'])

    def load_parameters(self):
        try:
            f1 = open(self.filename+'.params', "rb")
            self.parameters = pickle.load(f1)
            f1.close()
            print(self.parameters)
            self.update_ui_parameters()  # update parameters in UI
            print("Parameters for", self.filename, "loaded.")
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
        if self.chkvar_draw_acceleration.get() == 1:
            if self.chkvar_horizontal_flip.get() == 1: # Horizontal flip
                ids.append(self.canvas.create_line(p['Y5']+self.parameters['offset_x'],
                                                   p['Z5']+self.parameters['offset_y'],
                                                   p['Y5']-p['Y5v']/self.parameters['velocity_normalization_factor']+self.parameters['offset_x'],
                                                   p['Z5']-p['Z5v']/self.parameters['velocity_normalization_factor']+self.parameters['offset_y'],
                                                   arrow=LAST, fill='black'))
            else:
                ids.append(self.canvas.create_line(
                    self.flip_x(p['Y5'] + self.parameters['offset_x']),
                    p['Z5'] + self.parameters['offset_y'],
                    self.flip_x(p['Y5'] - p['Y5v'] / self.parameters['velocity_normalization_factor'] + self.parameters['offset_x']),
                    p['Z5'] - p['Z5v'] / self.parameters['velocity_normalization_factor'] + self.parameters['offset_y'],
                    arrow=LAST, fill='black'))

        # Draw acceleration arrow
        if self.chkvar_draw_velocity.get() == 1:
            if self.chkvar_horizontal_flip.get() == 1:
                ids.append(self.canvas.create_line(
                    p['Y5']+self.parameters['offset_x'],
                    p['Z5']+self.parameters['offset_y'],
                    p['Y5']-p['Y5a']/self.parameters['acceleration_normalization_factor']+self.parameters['offset_x'],
                    p['Z5']-p['Z5a']/self.parameters['acceleration_normalization_factor']+self.parameters['offset_y'],
                    arrow=LAST, fill='red'))
            else:
                ids.append(self.canvas.create_line(
                    self.flip_x(p['Y5'] + self.parameters['offset_x']),
                    p['Z5'] + self.parameters['offset_y'],
                    self.flip_x(p['Y5'] - p['Y5a'] / self.parameters['acceleration_normalization_factor'] + self.parameters['offset_x']),
                    p['Z5'] - p['Z5a'] / self.parameters['acceleration_normalization_factor'] + self.parameters['offset_y'],
                    arrow=LAST, fill='red'))


        self.canvas.update()
        return ids

    def draw_toe_end(self, t):
        # create a list to collect item ids
        ids = list()

        # if self.last_point[1] < 596:  # self.flip_y(self.transform(t.info['Z5'])): # moving lifted, set color to blue
        # in a frame range, set color to blue

        # if self.parameters['lifted_period_1b'] > self.frame_counter > self.parameters['lifted_period_1a']:
        if self.frame_counter in self.lifted_frames:
            c = colors[5]

        else:  # not moving lifted, set color to grey
            c = 'grey40'
        if self.chkvar_horizontal_flip.get() == 1:  # Horizontal flip
            ids.append(self.canvas.create_line(
                self.last_point[0]+self.parameters['offset_x'],
                self.last_point[1]+self.parameters['offset_y'],
                t.info['Y5']+self.parameters['offset_x'],
                t.info['Z5']+self.parameters['offset_y'], fill=c, width=2))
        else:
            ids.append(self.canvas.create_line(
                self.flip_x(self.last_point[0] + self.parameters['offset_x']),
                self.last_point[1] + self.parameters['offset_y'],
                self.flip_x(t.info['Y5'] + self.parameters['offset_x']),
                t.info['Z5'] + self.parameters['offset_y'], fill=c, width=2))
        self.canvas.update()
        return ids

    def draw_stick(self, pts, color):
        # create a list to collect item ids
        ids = list()
        if self.chkvar_horizontal_flip.get() == 1:
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

        else:
            # Draw the sticks
            ids.append(self.canvas.create_line(self.flip_x(pts[0] + self.parameters['offset_x']),
                                               pts[1] + self.parameters['offset_y'],
                                               self.flip_x(pts[2] + self.parameters['offset_x']),
                                               pts[3] + self.parameters['offset_y'],
                                               self.flip_x(pts[4] + self.parameters['offset_x']),
                                               pts[5] + self.parameters['offset_y'],
                                               self.flip_x(pts[6] + self.parameters['offset_x']),
                                               pts[7] + self.parameters['offset_y'],
                                               self.flip_x(pts[8] + self.parameters['offset_x']),
                                               pts[9] + self.parameters['offset_y'],
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
        if self.chkvar_horizontal_flip.get() == 1:
            ids.append(self.canvas.create_line(
                x+self.parameters['offset_x'],
                y+self.parameters['offset_y'],
                x+self.parameters['offset_x'],
                y+1+self.parameters['offset_y'],
                fill=color))
        else:
            ids.append(self.canvas.create_line(
                self.flip_x(x + self.parameters['offset_x']),
                y + self.parameters['offset_y'],
                self.flip_x(x + self.parameters['offset_x']),
                y + 1 + self.parameters['offset_y'],
                fill=color))
        return ids

    def transform(self, a):
        new_a = a * self.parameters['scale_factor'] + 0
        return new_a

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
        print("Transformation of time_frames done.")

    def read_csv_data(self, fn):
        self.csv_data = pd.read_csv(fn)
        print("Successfully read in "+fn+",")

    def generate_time_frames(self):
        """
        csv_data -> time frames
        """

        # Clear exsiting time frames
        self.time_frames.clear()

        print("Generating time frames from loaded csv data...")
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

        self.transformation()  # transform and offset before saving
        f = open(self.filename + '.frames', "wb")
        pickle.dump(self.time_frames, f)
        f.close()
        print("Time frame data saved. Length: {}".format(str(len(self.time_frames))))


class TimeFrame:
    """
    A frame of one depicted frozen kinetics on a certain time point
    """

    def __init__(self, i, information):
        self.number = i
        self.info = information
        print("Added time frame number "+str(i))


if __name__ == '__main__':
    root = Tk()
    wid = 1400
    hei = 900
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
# TODO 左走右走：反向开关
# TODO 图像居中：自动化
