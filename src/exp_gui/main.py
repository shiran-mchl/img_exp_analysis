# A module that will run a live tkinter gui which will plot data based on an updateable TrainingData object.
# import tkinter as tk
# import matplotlib as plt
# plt.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
# import pandas as pd

# class LivePlotter(tk.Tk):
    
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         self.title("Experiment GUI")
#         self.geometry("800x600")
#         self.eval('tk::PlaceWindow . center')

#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand = True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         frame = PlotPage(self) 
#         frame.grid(row=0, column=0, sticky="nsew")
#         self.show_frame(PlotPage)


# class PlotPage(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Training Plot")
#         label.pack(pady=10,padx=10)

#         # Create a frame for the plot
#         self.plot_frame = tk.Frame(self)
#         self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#         self.plot_frame.grid_rowconfigure(0, weight=1)
#         self.plot_frame.grid_columnconfigure(0, weight=1)
#         self.plot_frame.pack(padx=20, pady=20)

#         # Create a frame for the buttons
#         self.button_frame = tk.Frame(self)
#         self.button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#         # self.button_frame.grid_rowconfigure(0, weight=1)
#         # self.button_frame.grid_columnconfigure(0, weight=1)
#         self.button_frame.pack(padx=20, pady=20)
        
#         # Create a button to close the window
#         self.close_button = tk.Button(self.button_frame, text="Close", command=self.destroy)
#         self.close_button.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
#         self.plot_frame.pack(padx=10, pady=10)

#         # Create a button to update the plot
#         #self.update_button = tk.Button(self.button_frame, text="Update", command=self.update_plot)
#         #self.update_button.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

#         # Create a button to clear the plot
#         #self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_plot)
#         #self.clear_button.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

#         f = Figure(figsize=(5,5), dpi=100)
#         a = f.add_subplot(111)
#         a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

#         canvas = FigureCanvasTkAgg(f, self)
#         canvas.draw()
#         canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#         toolbar = NavigationToolbar2TkAgg(canvas, self)
#         toolbar.update()
#         canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



# window = LivePlotter()
# # Hold the window so it won't disappear
# window.mainloop()

import matplotlib
import pandas as pd
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys
from config import ConfigParams

class Application(tk.Frame):
    def __init__(self, config: ConfigParams, master=None):
        tk.Frame.__init__(self,master)
        fig1=plt.figure(figsize=(8,8))
        self.lick_rate_ax=fig1.add_axes([0.1,0.1,0.8,0.8])
        self.canvas1=FigureCanvasTkAgg(fig1,master=root)
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        '''fig2=plt.figure(figsize=(8,8))
        self.lick_bars_ax=fig2.add_axes([0.1,0.1,0.8,0.8])
        self.canvas2=FigureCanvasTkAgg(fig2,master=root)
        self.canvas2.get_tk_widget().pack(side=tk.RIGHT, expand=True)'''
        
        self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.update())
        self.plotbutton.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.config: ConfigParams = config
        self.data = None


    def plot(self):
        # Check if the data is empty
        if self.data is None:
            print("data is empty")
            return
        # draw some random stuff and plot it
        print("plotting")
        # Plot a moving percentage of the cells of the `mouseResponse` column from self.data which contain the value 'Lick'. The window size is 10.
        licks = self.data['mouseResponse'] == 'Lick'
        # Take the last 200 rows of the data
        licks = licks[-200:]
        licks = licks.rolling(window=10).mean()
        self.lick_rate_ax.plot(licks)
        self.lick_rate_ax.set_title("Lick Rate")
        self.canvas1.draw()
        self.lick_rate_ax.clear()

    # Reads the data from the and updates the GUI
    def update(self):
        print("updating")
        # TODO: Consider maintaining a pointer to the last row read and only read the new rows.
        # Read the config csv file into self.data as a pandas dataframe
        self.data = pd.read_csv(self.config.training_data_path)
        self.plot()
        self.after(1000,self.update)
        print("updated, data shape: ", self.data.shape)


root=tk.Tk()
root.title("Training Plot- R13")
config = ConfigParams()
app=Application(config, master=root)
app.mainloop()