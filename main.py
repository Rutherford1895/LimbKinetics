from tkinter import *
import pandas as pd
import time

colors = ['red','orange','gold','lime green','navy','dodger blue','dark violet']
greys = ['grey34','grey37','grey41','grey45','grey49','grey53','grey57','grey61','grey65','grey69']
scale_factor = 3 # enlarge by x times
start_frame = 300
end_frame = 450
every_n_frame = 1
velocity_normalization_factor = 6.0
acceleration_normalization_factor = 180.0


class Kinetics(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.canvas = Canvas(self)
        self.canvas.config(width=wid, height=hei)
        self.canvas.pack()
        self.pack(fill=BOTH, expand=1)

        # read file
        self.filename = 'data1.csv'
        self.data = None
        self.read_data(self.filename)

        # generate time frames
        self.time_frames=[]
        self.generate_time_frames()

        # draw time frames and trajectory
        print("Start drawing time frames")
        self.critical_point = {} # the first point going upward
        drawing_counter = 0 # Counting time frames to determine the color in color mode
        self.last_point = [0,0] # Store the last point for drawing trajectory
        for i in range(len(self.time_frames)):
            t = self.time_frames[i] # temporary variable, the current time frame

            # Draw the limb
            if i % every_n_frame == 0 and start_frame <= i <= end_frame: # 200 Hz -> lower frequency
                '''
                # In grey
                self.draw_time_frame(
                    [t.info['Y1'] , t.info['Z1'], t.info['Y2'] , t.info['Z2'],
                    t.info['Y3'] , t.info['Z3'], t.info['Y4'] , t.info['Z4'],
                    t.info['Y5'] , t.info['Z5']], greys[drawing_counter%10])
                # In colors
                '''
                '''
                self.draw_time_frame(
                    [t.info['Y1'], t.info['Z1'], t.info['Y2'], t.info['Z2'],
                     t.info['Y3'], t.info['Z3'], t.info['Y4'], t.info['Z4'],
                     t.info['Y5'], t.info['Z5']], colors[drawing_counter%7])
                '''
                print("Time frame "+str(t.number)+" drawn.")
                drawing_counter += 1 # Counting time frames

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

                #time.sleep(0.1)

            # Draw the trajectory
            if start_frame <= i <= end_frame: # Apply to every time frame
                if self.last_point != [0,0]: # When it's not the first frame
                    self.draw_trajectory(t)
                self.last_point[0] = self.flip_x(self.transform(t.info['Y5']))
                self.last_point[1] = self.flip_y(self.transform(t.info['Z5']))
        # Draw the last part to close the trajectory
        self.draw_trajectory(t)

        print(self.critical_point)

    def draw_velocity_acceleration(self,p):
        # Draw velocity arrow
        #scale_factor_v = p['yz_combined_velocity']/velocity_normalization_factor
        # print(scale_factor_v)
        self.canvas.create_line(p['Y5'],p['Z5'],p['Y5']-p['Y5v']/velocity_normalization_factor,p['Z5']-p['Z5v']/velocity_normalization_factor,arrow=LAST,fill='black')

        # Draw acceleration arrow
        #scale_factor_a = p['yz_combined_velocity']/acceleration_normalization_factor
        #print(scale_factor_a)
        self.canvas.create_line(p['Y5'],p['Z5'],p['Y5']-p['Y5a']/acceleration_normalization_factor,p['Z5']-p['Z5a']/acceleration_normalization_factor,arrow=LAST,fill='red')

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
        self.canvas.create_line(self.last_point[0], self.last_point[1], self.flip_x(self.transform(t.info['Y5'])),
                                self.flip_y(self.transform(t.info['Z5'])), fill=c, width=2)
        self.canvas.update()

    def draw_time_frame(self,pts,color):
        pts_scaled=[]
        for p in pts:
            pts_scaled.append(self.transform(p)) # enlarge by 5 times then offset backward
        # Draw the sticks
        self.canvas.create_line(self.flip_x(pts_scaled[0]), self.flip_y(pts_scaled[1]), self.flip_x(pts_scaled[2]),
                                self.flip_y(pts_scaled[3]), self.flip_x(pts_scaled[4]), self.flip_y(pts_scaled[5]),
                                self.flip_x(pts_scaled[6]), self.flip_y(pts_scaled[7]), self.flip_x(pts_scaled[8]),
                                self.flip_y(pts_scaled[9]), fill=color, width=2)
        # Draw the joints
        self.draw_dot(self.flip_x(pts_scaled[0]), self.flip_y(pts_scaled[1]))
        self.draw_dot(self.flip_x(pts_scaled[2]), self.flip_y(pts_scaled[3]))
        self.draw_dot(self.flip_x(pts_scaled[4]), self.flip_y(pts_scaled[5]))
        self.draw_dot(self.flip_x(pts_scaled[6]), self.flip_y(pts_scaled[7]))
        # self.draw_dot(800-pts_scaled[8], 600-pts_scaled[9]) # Don't draw this last black dot. It will be in blue/grey.
        self.canvas.update()

    def draw_dot(self,x,y,color='black'):
        self.canvas.create_line(x,y,x,y+1,fill=color)

    def transform(self,a):
        new_a = a * scale_factor - 0
        return new_a

    def flip_x(self,b):
        new_b = wid - b
        return new_b

    def flip_y(self,c):
        new_c = hei - c
        return new_c

    def read_data(self,fn):
        self.data = pd.read_csv(fn)
        print("Successfully read in "+fn)

    def generate_time_frames(self):
        column_titles =[]
        for line_list in self.data:
            column_titles.append(line_list)

        #for i in range(self.data.shape[0]):
        for i in range(500):
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
    wid = 800
    hei = 600
    root.wm_title("Kinetics")
    root.geometry(str(wid) + "x" + str(hei) + "+100+100")
    app = Kinetics(root)
    root.mainloop()
