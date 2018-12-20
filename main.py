from tkinter import *
import pandas as pd
import time
#from tkinter import filedialog
#from tkinter import ttk

colors = ['red','orange','gold','lime green','navy','dodger blue','dark violet']

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

        # draw time frames
        print("Start drawing time frames")
        position_offset = 300
        start_frame = 0
        end_frame = 1000
        drawing_counter = 0
        for i in range(len(self.time_frames)):
            if i % 2 == 0 and start_frame <= i <= end_frame: # 200 Hz -> lower frequency
                t = self.time_frames[i]
                self.draw_time_frame([t.info['X1']+position_offset,t.info['Y1'],t.info['X2']+position_offset,t.info['Y2'],t.info['X3']+position_offset,t.info['Y3'],t.info['X4']+position_offset,t.info['Y4'],t.info['X5']+position_offset,t.info['Y5']],colors[drawing_counter%7])
                print("Time frame "+str(t.number)+" drawn.")
                drawing_counter += 1

                self.canvas.update()
                time.sleep(0.1)



    def draw_time_frame(self,pts,color):

        scale_factor = 1 # enlarge by 5 times
        pts_scaled=[]
        for p in pts:
            pts_scaled.append((p*scale_factor)-0) # enlarge by 5 times then offset backward
        self.canvas.create_line(pts_scaled[0], pts_scaled[1], pts_scaled[2], pts_scaled[3], pts_scaled[4], pts_scaled[5], pts_scaled[6], pts_scaled[7], pts_scaled[8], pts_scaled[9], fill=color, width=2)


    def read_data(self,fn):
        self.data = pd.read_csv(fn)
        print("Successfully read in "+fn)

    def generate_time_frames(self):
        column_titles =[]
        for line_list in self.data:
            column_titles.append(line_list)

        for i in range(self.data.shape[0]):
            information = {}
            for title in column_titles:
                if len(title)<=4: # only take N, N', and N''
                    information[title]=self.data[title].tolist()[i]
            self.time_frames.append(TimeFrame(i,information))


class TimeFrame():

    """A frame of kinetics, depicting a certain time point"""

    def __init__(self,n,i):
        self.number = n
        self.info = i
        print("Added time frame number "+str(n))


if __name__ == '__main__':
    root = Tk()
    wid = 800
    hei = 600
    app = Kinetics(root)
    root.wm_title("Kinetics")
    root.geometry(str(wid) + "x" + str(hei) + "+100+100")
    root.mainloop()
