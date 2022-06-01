import tkinter as tk
from UI.ViewerDialog import ViewerDialog
from Data.PeakML.SampleFragmentsItem import SampleFragmentsItem
from Data.PeakML.SampleFragmentsItem import compareSpectra

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

class FragmentComparisonDialog(ViewerDialog):
    def __init__(self,parent,title,peakFragments,peakID,database1,database2,mzd,ppm):
        self.fragments = peakFragments
        self.loaded_fragments = None
        self.id = peakID
        self.id_to_compound = database1
        self.compound_to_tests = database2
        self.data = None
        self.instrument = tk.StringVar()
        self.energy = tk.StringVar()
        self.precursor = tk.StringVar()
        self.sim = tk.StringVar()
        self.mzd = mzd
        self.ppm = ppm

        super().__init__(parent, title, width=1000, height=760, take_focus=True, extendable=False)


    def body(self, frame):
        # load option_list
        try:
            ms2 = self.id_to_compound.loc[self.id_to_compound['id'] == self.id]
            samples = self.compound_to_tests[self.compound_to_tests["MonaID"] == ms2["MS2"].values[0]]

            self.data = samples


            options_instrument = samples["instrument"].tolist()
            options_energy = samples["collision.energy"].tolist()
            options_precursor = samples["precursorType"].tolist()
        except:
            options_instrument = ["N/A"]
            options_energy = ["N/A"]
            options_precursor = ["N/A"]
        #----#


        options_instrument = list(dict.fromkeys(options_instrument))
        options_instrument.sort()

        options_energy = list(dict.fromkeys(options_energy))
        options_energy.sort()

        options_precursor = list(dict.fromkeys(options_precursor))
        options_precursor.sort()

        try:
            self.instrument.set(options_instrument[0])
            self.energy.set(options_energy[0])
            self.precursor.set(options_precursor[0])
        except:
            self.instrument.set("N/A")
            self.energy.set("N/A")
            self.precursor.set("N/A")

        self._containing_frame = tk.Frame(frame, padx=5, pady=5)
        self._containing_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._options = tk.Frame(self._containing_frame, padx=0, pady=0)
        self._options.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._figure, self._axes, self._line = None, None, None
        self._figure = plt.Figure(figsize=(10,6))

        self._axes = self._figure.add_subplot(111)

        self._ins_lbl = tk.Label(self._options, width=15, text="Instrument")
        self._ins_lbl.grid(row=0,column=1,padx=(2,2), pady=(5,5), sticky="NEWS")

        self._instrument = tk.OptionMenu(self._options, self.instrument, *options_instrument,command=self._update_plot)
        self._instrument.grid(row=0,column=2,padx=(2,2), pady=(5,5), sticky="NEWS")

        self._energy_lbl = tk.Label(self._options, width=15, text="Collision energy")
        self._energy_lbl.grid(row=0,column=3,padx=(2,2), pady=(5,5), sticky="NEWS")

        self._energy = tk.OptionMenu(self._options, self.energy, *options_energy,command=self._update_plot)
        self._energy.grid(row=0,column=4,padx=(2,2), pady=(5,5), sticky="NEWS")

        self._precursor_lbl = tk.Label(self._options, width=15, text="Adduct")
        self._precursor_lbl.grid(row=0,column=5,padx=(2,2), pady=(5,5), sticky="NEWS")

        self._precursor = tk.OptionMenu(self._options, self.precursor, *options_precursor,command=self._update_plot)
        self._precursor.grid(row=0,column=6,padx=(2,2), pady=(5,5), sticky="NEWS")

        self._plot = tk.Frame(self._containing_frame, padx=10, pady=10)
        self._plot.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._update_plot(5)

        canvas = FigureCanvasTkAgg(self._figure, self._plot)
        canvas.get_tk_widget().pack(side="top", fill ='both', expand=True)
        canvas.draw()

        self._simularity_frame = tk.Frame(frame, padx=5, pady=5)
        self._simularity_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.sim.set(str(compareSpectra(self.fragments, self.loaded_fragments,self.mzd,self.ppm)))

        self._simularity_lbl = tk.Label(self._simularity_frame, width=15, text="Similarity Score :")
        self._simularity_lbl.grid(row=0,column=1,padx=(2,2), pady=(5,5), sticky="NEWS")

        self.simularity_lb = tk.Label(self._simularity_frame, width=20, textvariable=self.sim)
        self.simularity_lb.grid(row=0, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

    def _update_plot(self,b):
        self._axes.clear()

        frag_counter = 0
        try:
            xAxis = max(self.fragments.mz) + 1
        except:
            xAxis = 0

        while frag_counter < len(self.fragments.mz):
            x = [float(self.fragments.mz[frag_counter]),self.fragments.mz[frag_counter]]
            y = [0,float(self.fragments.intensity[frag_counter])]
            self._axes.plot(x,y,linewidth=1, color="blue")
            frag_counter += 1

        selected_sample = self.data.loc[(self.data["instrument"] == self.instrument.get())]
        selected_sample = selected_sample.loc[(selected_sample["precursorType"] == self.precursor.get())]
        selected_sample = selected_sample.loc[(selected_sample["collision.energy"] == int(self.energy.get()))]

        sample_fragments = selected_sample["spectrum"].values[0]

        fragments = sample_fragments.split()

        mz = []
        ints = []

        for f in fragments:
            a = f.split(":")
            mz.append(float(a[0]))
            ints.append(float(a[1]))

        self.loaded_fragments = SampleFragmentsItem(mz,ints)

        self.sim.set(str(compareSpectra(self.fragments, self.loaded_fragments,self.mzd,self.ppm)))

        # str("{:.6f}".format(compareSpectra(self.fragments, self.loaded_fragments)))
        print(self.sim)

        if max(self.loaded_fragments.mz) > xAxis:
            xAxis = max(self.loaded_fragments.mz) + 1

        x = [0,xAxis]
        y = [0,0]
        self._axes.plot(x,y,linewidth=1, color="black")


        frag_counter = 0

        while frag_counter < len(self.loaded_fragments.mz):
            x = [float(self.loaded_fragments.mz[frag_counter]),self.loaded_fragments.mz[frag_counter]]
            y = [0,(float(self.loaded_fragments.intensity[frag_counter])*-1)]
            self._axes.plot(x,y,linewidth=1, color="red")
            frag_counter += 1

        self._axes.set_xlabel("m/z")
        self._axes.set_ylabel("Intensity")

        self._figure.canvas.draw()
