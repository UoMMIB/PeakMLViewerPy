import tkinter as tk
import tkinter.ttk as ttk
from UI.ViewerDialog import ViewerDialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

import Utilities as u

class PeakSplitDialog(ViewerDialog):
    def __init__(self, parent, title, rt, df):

        self.rt = rt
        self.rt_sec = 0
        self.rt_min = 0
        self.group_split = 0
        self.group_split_variable = 0


        self.df = df

        if rt:
            rt_split = rt.split(":")
            self.rt_sec = rt_split[1]
            self.rt_min = rt_split[0]

        self.retention_time_sec = None
        self.retention_time_min = None
        self.submit = False

        super().__init__(parent, title, width=640, height=620, take_focus=True, extendable=True)

    def body(self, frame):

        self._containing_frame = tk.Frame(frame, padx=5, pady=5)
        self._containing_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._rt_frame = tk.Frame(self._containing_frame, padx=0, pady=0)
        self._rt_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.val_sec = tk.StringVar(self._rt_frame, value=self.rt_sec)
        self.val_min = tk.StringVar(self._rt_frame, value=self.rt_min)

        self.lbl_sec = tk.Label(self._rt_frame, width=5, text="Second:")
        self.lbl_min = tk.Label(self._rt_frame, width=5, text="Minute:")

        self.spbx_sec = ttk.Spinbox(self._rt_frame, width=5, from_=0, to=59, state='readonly', textvariable=self.val_sec, command=self._spinbox_changed)
        self.spbx_min = ttk.Spinbox(self._rt_frame, width=5, from_=0, to_=100, state='readonly',  textvariable=self.val_min, command=self._spinbox_changed)

        self.lbl_min.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_min.grid(row=0, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_sec.grid(row=0, column=3, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_sec.grid(row=0, column=4, padx=(2,2), pady=(5,5), sticky="NEWS")

        self._figure_frame = tk.Frame(self._containing_frame, padx=10, pady=10)
        self._figure_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._figure, self._axes, self._line = None, None, None
        self._figure = plt.Figure(figsize=(7,5))
        self._figure.canvas.mpl_connect('button_press_event', self._on_click)

        self._axes = self._figure.add_subplot(111)

        self._update_set_datetime(u.format_time_datetime(u.format_time_int(self.rt)))

        self._update_plot()

        canvas = FigureCanvasTkAgg(self._figure, self._figure_frame)
        canvas.get_tk_widget().pack(side="top", fill ='both', expand=True)
        canvas.draw()



    def buttonbox(self):
        self.group_split_variable = tk.IntVar()
        self.checkbox = tk.Checkbutton(self, text = "Split all members of the cluster",variable=self.group_split_variable)
        self.checkbox.pack(side="left", padx=(5,10), pady=(5,10))
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.retention_time_sec = self.val_sec.get()
        self.retention_time_min = self.val_min.get()
        self.group_split = self.group_split_variable.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def _update_plot(self):
        self._axes.clear()

        for i in range(len(self.df)):
            RT_values_arr = self.df.iloc[i]['RT_values']
            Intensity_values_arr = self.df.iloc[i]['Intensity_values']
            plot_label = self.df.iloc[i]["Label"]
            colour = self.df.iloc[i]["Colour"]

            self._axes.plot(RT_values_arr, Intensity_values_arr, marker='', color=colour, linewidth=0.5, label=plot_label)

        self._axes.axvline(self._datetime_x)
        self._axes.set_xlabel("Retention Time")
        self._axes.set_ylabel("Intensity")
        self._axes.xaxis.set_major_formatter(DateFormatter("%M:%S"))

        self._figure.canvas.draw()

    def _update_set_datetime(self, x):
        self._datetime_x = x
        return x

    def _on_click(self, event):

        # On click within range of plot
        if event.button == 1 and event.inaxes in [self._axes]:

            self._update_set_datetime(mdates.num2date(event.xdata))
            self._update_retention_time()
            self._update_plot()

    def _spinbox_changed(self):
        self._update_set_datetime(u.format_time_datetime(u.format_time_int(f"{self.val_min.get()}:{self.val_sec.get()}")))
        self._update_plot()

    def _update_retention_time(self):
        self.val_min.set(self._datetime_x.minute)
        self.val_sec.set(self._datetime_x.second)
