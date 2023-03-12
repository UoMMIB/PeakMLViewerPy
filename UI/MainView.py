import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import ttkwidgets as ttkw
#If package only available as pip, install with anaconda prompt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter

import json
import pandas as pd

from PIL import ImageTk, Image
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import inchi
import time
import threading
import os
import base64
import numpy as np
import sys
import platform
import subprocess
import re

from UI.ProgressDialog import ProgressDialog
from UI.LogDialog import LogDialog
from UI.EditIdentityDialog import EditIdentityDialog
from UI.FilterMassDialog import FilterMassDialog
from UI.FilterIntensityDialog import FilterIntensityDialog
from UI.FilterRetentionTimeDialog import FilterRetentionTimeDialog
from UI.FilterNumberDetectionsDialog import FilterNumberDetectionsDialog
from UI.FilterAnnotationsDialog import FilterAnnotationsDialog
from UI.FilterProbabilityDialog import FilterProbabilityDialog
from UI.SortDialog import SortDialog
from UI.SortTimeSeriesDialog import SortTimeSeriesDialog
from UI.PreferencesDialog import PreferencesDialog
from UI.PeakSplitDialog import PeakSplitDialog
from UI.SetIPAParamsDialog import SetIPAParamsDialog
from Data.PeakML.SampleFragmentsItem import SampleFragmentsItem
from Data.PeakML.SampleFragmentsItem import ConsensusSpec
from UI.FragmentComparisonDialog import FragmentComparisonDialog
import Icon as i
import Enums as e
import Utilities as u
import Logger as lg
import Progress as p

# Globals
configure_timer = None
class MainView():

    @property
    def filter_options(self) -> "dict[e.Filter, str]":
        return self._filter_options

    @property
    def set_width(self) -> int:
        return self._set_width

    @set_width.setter
    def set_width(self, width: int):
        self._set_width = width

    @property
    def set_height(self) -> int:
        return self._set_height

    @set_height.setter
    def set_height(self, height: int):
        self._set_height = height

    @property
    def set_vf0(self) -> int:
        return self._set_vf0

    @set_vf0.setter
    def set_vf0(self, vf0: int):
        self._set_vf0 = vf0

    @property
    def set_vf1(self) -> int:
        return self._set_vf1

    @set_vf1.setter
    def set_vf1(self, vf1: int):
        self._set_vf1 = vf1

    @property
    def set_mf0(self) -> int:
        return self._set_mf0

    @set_mf0.setter
    def set_mf0(self, mf0: int):
        self._set_mf0 = mf0

    @property
    def set_mf1(self) -> int:
        return self._set_mf1

    @set_mf1.setter
    def set_mf1(self, mf1: int):
        self._set_mf1 = mf1

    @property
    def set_mlf0(self) -> int:
        return self._set_mlf0

    @set_mlf0.setter
    def set_mlf0(self, mlf0: int):
        self._set_mlf0 = mlf0

    @property
    def set_mrf0(self) -> int:
        return self._set_mrf0

    @set_mrf0.setter
    def set_mrf0(self, mrf0: int):
        self._set_mrf0 = mrf0

    @property
    def set_mrf1(self) -> int:
        return self._set_mrf1

    @set_mrf1.setter
    def set_mrf1(self, mrf1: int):
        self._set_mrf1 = mrf1

    @property
    def selected_tab_plot(self) -> str:
        return self._selected_tab_plot

    @selected_tab_plot.setter
    def selected_tab_plot(self, selected_tab_plot: str):
        self._selected_tab_plot = selected_tab_plot

    @property
    def selected_tab_der(self) -> str:
        return self._selected_tab_der

    @selected_tab_der.setter
    def selected_tab_der(self, selected_tab_der: str):
        self._selected_tab_der = selected_tab_der

    @property
    def selected_tab_int(self) -> str:
        return self._selected_tab_int

    @selected_tab_int.setter
    def selected_tab_int(self, selected_tab_int: str):
        self._selected_tab_int = selected_tab_int

    @property
    def selected_tab_frag(self) -> str:
        return self._selected_tab_frag

    @selected_tab_frag.setter
    def selected_tab_frag(self, selected_tab_frag: str):
        self._selected_tab_frag = selected_tab_frag

    @property
    def visible_plot(self) -> str:
        if self.selected_tab_plot == "Peak":
            return "Peak"

        elif self.selected_tab_plot == "Derivatives":
            if self.selected_tab_der == "All":
                return "Der_All"

            elif self.selected_tab_der == "Log":
                return "Der_Log"

        elif self.selected_tab_plot == "Intensity Pattern":
            if self.selected_tab_int == "All":
                return "Int_All"

            elif self.selected_tab_int == "Log":
                return "Int_Log"

        elif self.selected_tab_plot == "Fragmentation":
            if self.selected_tab_frag == "Consensus":
                return "Frag_Consensus"

            elif self.selected_tab_frag == "Sample":
                return "Frag_Sample"

    @property
    def plot_peak_loaded(self) -> bool:
        return self._plot_peak_loaded

    @plot_peak_loaded.setter
    def plot_peak_loaded(self, plot_peak_loaded: bool):
        self._plot_peak_loaded = plot_peak_loaded

    @property
    def plot_der_all_loaded(self) -> bool:
        return self._plot_der_all_loaded

    @plot_der_all_loaded.setter
    def plot_der_all_loaded(self, plot_der_all_loaded: bool):
        self._plot_der_all_loaded = plot_der_all_loaded

    @property
    def plot_der_log_loaded(self) -> bool:
        return self._plot_der_log_loaded

    @plot_der_log_loaded.setter
    def plot_der_log_loaded(self, plot_der_log_loaded: bool):
        self._plot_der_log_loaded = plot_der_log_loaded

    @property
    def plot_int_all_loaded(self) -> bool:
        return self._plot_int_all_loaded

    @plot_int_all_loaded.setter
    def plot_int_all_loaded(self, plot_int_all_loaded: bool):
        self._plot_int_all_loaded = plot_int_all_loaded

    @property
    def plot_int_log_loaded(self) -> bool:
        return self._plot_int_log_loaded

    @plot_int_log_loaded.setter
    def plot_int_log_loaded(self, plot_int_log_loaded: bool):
        self._plot_int_log_loaded = plot_int_log_loaded

    @property
    def current_entry(self) -> int:
        return self._current_entry

    @current_entry.setter
    def current_entry(self, current_entry: int):
        self._current_entry = current_entry

    @property
    def annotation_params_path(self) -> str:
        return self._annotation_params_path

    @annotation_params_path.setter
    def annotation_params_path(self, annotation_params_path: str):
        self._annotation_params_path = annotation_params_path


    def __init__(self, data, peakml_file_path, annotation_params):

        self.data = data

        self.selected_identities_tab = 0

        self.frag_threshold = 80
        self.mzd = 0.02
        self.fragPPM = 10
        self.frag_option = 1
        self.blank = ""

        self.last_plot = ""
        self.frag_update = 0

        self.annotation_params_path = ""

        #comparison database:
        #self.id_db = None
        #self.id_samples = None
        #self.update_fragmentation_dbs()

        ## Populate class properties
        # Set initial widget layout values
        self._set_width = 1280
        self._set_height = 720
        self._set_vf0 = 43
        self._set_vf1 = 551
        self._set_mf0 = 303
        self._set_mf1 = 1011
        self._set_mlf0 = 303
        self._set_mrf0 = 153
        self._set_mrf1 = 261

        self._selected_tab_plot = "Peak"
        self._selected_tab_der = "All"
        self._selected_tab_int = "All"
        self._selected_tab_frag = "Consensus"

        self._plot_peak_loaded = False
        self._plot_der_all_loaded = False
        self._plot_der_log_loaded = False
        self._plot_int_all_loaded = False
        self._plot_int_log_loaded = False

        self._filter_options = {}
        self._filter_options[e.Filter.Mass] = "Filter mass range"
        self._filter_options[e.Filter.Intensity] = "Filter minimum intensity"
        self._filter_options[e.Filter.RetentionTime] = "Filter retention time range"
        self._filter_options[e.Filter.NumberDetections] = "Filter to sample count"
        self._filter_options[e.Filter.Annotations] = "Filter by annotation"
        self._filter_options[e.Filter.Probability] = "Filter by probability"
        self._filter_options[e.Filter.Sort] = "Sort"
        self._filter_options[e.Filter.SortTimeSeries] = "Sort time-series"

        self._current_entry = 0

        # Initialize Application window
        self.root = tk.Tk()

        self.root.title('PeakMLViewerPy')

        if (sys.platform.startswith('win')):
            #Read icon details and set
            icon_ico_data = base64.b64decode(i.img_ico)
            temp_ico_file = "temp.ico"
            icon_ico_file = open(temp_ico_file, "wb")
            icon_ico_file.write(icon_ico_data)
            icon_ico_file.close()
            self.root.wm_iconbitmap(True, temp_ico_file)
            os.remove(temp_ico_file)
        else:
            icon_png_data = base64.b64decode(i.img_png)
            temp_png_file = "temp.png"
            icon_png_file = open(temp_png_file, "wb")
            icon_png_file.write(icon_png_data)
            icon_png_file.close()

            logo = tk.PhotoImage(file=temp_png_file)
            self.root.tk.call('wm', 'iconphoto', self.root._w, logo)

            os.remove(temp_png_file)

        # Required for accessing menu items in Mac
        if platform.system() == 'Darwin':
            subprocess.call(["/usr/bin/osascript", "-e", 'tell app "Finder" to set frontmost of process "Finder" to true'])
            subprocess.call(["/usr/bin/osascript", "-e", 'tell app "Finder" to set frontmost of process "python" to true'])

        self.root.resizable(None, None)

        self.first_resize_occurred = False

        self.root.geometry(f"{self.set_width}x{self.set_height}")

        self.style = ttk.Style()
        self.style.map('Treeview', foreground = self.fixed_map('foreground'), background = self.fixed_map('background'))
        self.style.map('Treeview', background=[('selected', 'blue')])

        self.menubar = tk.Menu(self.root)

        self.filename_text = tk.StringVar()
        self.peak_number_text = tk.StringVar()
        self.warning_text = tk.StringVar()
        self.filter_option_selected = tk.StringVar(self.root)
        self.filter_option_selected.set("Filter mass range")

        self.progress_text = tk.StringVar()
        self.progress_text.set("No file imported.")

        self.progress_val = tk.DoubleVar()
        self.progress_val.set(0)

        self.current_layout = ""
        self.last_resize_initiated = time.time()

        ## Setup Menu
        #Add 'File' menu item
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Add 'Edit' menu item
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Check all entries", command=self.entries_view_check_all)
        self.editmenu.add_command(label="Uncheck all entries", command=self.entries_view_uncheck_all)
        self.editmenu.add_command(label="Invert entry check status", command=self.entries_view_invert_check)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Split peak", command=self.open_peak_split_dialog)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # Add 'IPA' menu item
        self.ipamenu = tk.Menu(self.menubar, tearoff=0)
        self.ipamenu.add_command(label="Export entries as IPA input", command=self.export_ipa_file)
        self.ipamenu.add_command(label="Import IPA results", command=self.import_ipa_file)
        self.ipamenu.add_separator()
        self.ipamenu.add_command(label="Run annotation", command=self.open_set_ipa_params_dialog)
        self.menubar.add_cascade(label="IPA", menu=self.ipamenu)

        # Add 'User' menu item
        self.usermenu = tk.Menu(self.menubar, tearoff=0)
        self.usermenu.add_command(label="View Log", command=self.open_log_dialog)
        self.usermenu.add_command(label="Preferences", command=self.open_preferences_dialog)
        self.menubar.add_cascade(label="User", menu=self.usermenu)

        # Disable 'Save'
        self.filemenu.entryconfig(1, state=tk.DISABLED)

        # Disable 'Save as...'
        self.filemenu.entryconfig(2, state=tk.DISABLED)

        # Disable 'Check all'
        self.editmenu.entryconfig(0, state=tk.DISABLED)

        # Disable 'Uncheck all'
        self.editmenu.entryconfig(1, state=tk.DISABLED)

        # Disable 'Invert check status'
        self.editmenu.entryconfig(2, state=tk.DISABLED)

        # Disable 'Split peak'
        self.editmenu.entryconfig(4, state=tk.DISABLED)

        # Disable 'Export entries as IPA input'
        self.ipamenu.entryconfig(0, state=tk.DISABLED)

        # Disable 'Import IPA results'
        self.ipamenu.entryconfig(1, state=tk.DISABLED)

        # Initialise Layout
        self.root_frame = tk.Frame(self.root, padx=0, pady=0)
        self.root_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.root_frame.bind("<Configure>", self.reset_configure_timer)

        self.viewer_frame = tk.PanedWindow(self.root_frame, orient=tk.VERTICAL)
        self.viewer_frame.pack(fill=tk.BOTH, expand = tk.TRUE, padx=(5,5), pady=(5,5))

        # Top - Info View
        self.top_frame = tk.Frame(self.viewer_frame, padx=0, pady=0)
        self.viewer_frame.add(self.top_frame)

        # Middle - Paned (3x1)
        self.mid_frame = tk.PanedWindow(self.viewer_frame, orient=tk.HORIZONTAL)
        self.viewer_frame.add(self.mid_frame)

        # Bottom - Identification Viewce
        self.bot_frame = tk.LabelFrame(self.viewer_frame, padx=10, pady=10, text="Identities")
        self.viewer_frame.add(self.bot_frame)

        # Middle Left - Paned (1x2)
        self.mid_left_frame = tk.PanedWindow(self.mid_frame, orient=tk.VERTICAL)
        self.mid_frame.add(self.mid_left_frame)

        # Middle Centre - Plots View
        self.mid_cen_frame = tk.LabelFrame(self.mid_frame, text="Summary Plots")
        self.mid_frame.add(self.mid_cen_frame)

        # Middle Right - Paned (1x3)
        self.mid_right_frame = tk.PanedWindow(self.mid_frame, orient=tk.VERTICAL)
        self.mid_frame.add(self.mid_right_frame)

        # Middle Left Top - Entries View
        self.mid_left_top_frame = tk.LabelFrame(self.mid_left_frame, padx=10, pady=10, text="Entries")
        self.mid_left_frame.add(self.mid_left_top_frame)

        # Middle Left Bottom - Filters View
        self.mid_left_bot_frame = tk.LabelFrame(self.mid_left_frame, padx=10, pady=10, text="Filters")
        self.mid_left_frame.add(self.mid_left_bot_frame)

        # Middle Right Top - Sets View
        self.mid_right_top_frame = tk.LabelFrame(self.mid_right_frame, padx=10, pady=10, text="Sets")
        self.mid_right_frame.add(self.mid_right_top_frame)

        # Middle Right Mid - Details View
        self.mid_right_mid_frame = tk.LabelFrame(self.mid_right_frame, padx=10, pady=10, text="Details")
        self.mid_right_frame.add(self.mid_right_mid_frame)

        # Middle Right Bottom - Molecule Viewer
        self.mid_right_bot_frame = tk.LabelFrame(self.mid_right_frame, padx=10, pady=10, text="Molecule View")
        self.mid_right_frame.add(self.mid_right_bot_frame)

        # Info View
        filename_lbl = tk.Label(self.top_frame, text = "Filename:")
        filename_lbl.grid(row=0, column=0)
        peak_nr_lbl = tk.Label(self.top_frame, text = "Nr peaks:")
        peak_nr_lbl.grid(row=1, column=0)
        filename_val = tk.Label(self.top_frame, textvariable = self.filename_text)
        filename_val.grid(row=0, column=1)
        peak_nr_val = tk.Label(self.top_frame, textvariable = self.peak_number_text)
        peak_nr_val.grid(row=1, column=1)
        warning_val = tk.Label(self.top_frame, fg= "#ff0000", textvariable = self.warning_text)
        warning_val.grid(row=0, column=2)

        # Entry View
        entry_control_frame = tk.Frame(self.mid_left_top_frame)
        entry_control_frame.pack(side=tk.BOTTOM)
        self.entry_delete_checked_btn = tk.Button(entry_control_frame, text="Delete Checked", command=self.delete_checked_entries)
        self.entry_delete_checked_btn["state"] = "disabled"
        self.entry_delete_checked_btn.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEWS")

        self.entry_tree = self.initialize_grid(self.mid_left_top_frame, True, [("Selected", 40), ("Retention time", 100), ("Mass", 80), ("Intensity", 80), ("Samples", 50)])

        self.entry_tree.bind('<ButtonRelease-1>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Up>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Down>', self.select_entry)
        self.entry_tree.tag_configure("has_ann_not_focus", foreground="black")
        self.entry_tree.tag_configure("no_ann_not_focus", foreground="grey")
        self.entry_tree.tag_configure("has_ann_is_focus", foreground="white", background="blue")
        self.entry_tree.tag_configure("no_ann_is_focus", foreground="white", background="blue")

        # Filter View
        option_list = [
            self.filter_options[e.Filter.Mass],
            self.filter_options[e.Filter.Intensity],
            self.filter_options[e.Filter.RetentionTime],
            self.filter_options[e.Filter.NumberDetections],
            self.filter_options[e.Filter.Annotations],
            self.filter_options[e.Filter.Probability],
            self.filter_options[e.Filter.Sort],
            self.filter_options[e.Filter.SortTimeSeries]
            ]
        filter_control_frame = tk.Frame(self.mid_left_bot_frame)
        filter_control_frame.pack(side=tk.BOTTOM)
        self.filter_opm = tk.OptionMenu(filter_control_frame, self.filter_option_selected, *option_list)
        self.filter_opm.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEWS")
        self.filter_add_btn = tk.Button(filter_control_frame, text="Add", command=self.add_filter)
        self.filter_add_btn["state"] = "disabled"
        self.filter_add_btn.grid(row=0, column=1, padx=(2,2), pady=(2,2), sticky="NEWS")
        self.filter_remove_btn = tk.Button(filter_control_frame, text="Remove", command=self.remove_filter)
        self.filter_remove_btn["state"] = "disabled"
        self.filter_remove_btn.grid(row=0, column=2, padx=(2,2), pady=(2,2), sticky="NEWS")
        self.filter_tree = self.initialize_grid(self.mid_left_bot_frame, False, [("Selected", 10), ("Type", 100), ("Settings", 100)])

        self.filter_tree.bind('<ButtonRelease-1>', self.select_filter)
        self.filter_tree.tag_configure("not_focus", foreground="black")
        self.filter_tree.tag_configure("is_focus", foreground="white", background="blue")

        # Plot View
        self.tabs_plot = ttk.Notebook(self.mid_cen_frame)
        self.tab_peak = ttk.Frame(self.tabs_plot)
        self.tab_derivatives = ttk.Frame(self.tabs_plot)
        self.tab_intensity_pattern = ttk.Frame(self.tabs_plot)
        self.tab_fragmentation = ttk.Frame(self.tabs_plot)

        self.tabs_plot.add(self.tab_peak, text = "Peak")
        self.tabs_plot.add(self.tab_derivatives, text = "Derivatives")
        self.tabs_plot.add(self.tab_intensity_pattern, text = "Intensity Pattern")
        self.tabs_plot.add(self.tab_fragmentation, text = "Fragmentation")

        self.tabs_plot.bind("<<NotebookTabChanged>>", self.change_plot_tab)

        self.tabs_plot.pack(expand = 1, fill = "both")

        self.tabs_der = ttk.Notebook(self.tab_derivatives)
        self.tab_der_all = ttk.Frame(self.tabs_der)
        self.tab_der_log = ttk.Frame(self.tabs_der)

        self.tabs_der.add(self.tab_der_all, text = "All")
        self.tabs_der.add(self.tab_der_log, text = "Log")

        self.tabs_der.bind("<<NotebookTabChanged>>", self.change_der_tab)

        self.tabs_der.pack(expand = 1, fill = "both")

        self.tabs_int = ttk.Notebook(self.tab_intensity_pattern)
        self.tab_int_all = ttk.Frame(self.tabs_int)
        self.tab_int_log = ttk.Frame(self.tabs_int)

        self.tabs_int.add(self.tab_int_all, text = "All")
        self.tabs_int.add(self.tab_int_log, text = "Log")

        self.tabs_int.bind("<<NotebookTabChanged>>", self.change_int_tab)

        self.tabs_int.pack(expand = 1, fill = "both")

        self.tabs_frag = ttk.Notebook(self.tab_fragmentation)
        self.tab_frag_con = ttk.Frame(self.tabs_frag)
        self.tab_frag_sample = ttk.Frame(self.tabs_frag)

        self.tabs_frag.add(self.tab_frag_con, text = "Consensus")
        self.tabs_frag.add(self.tab_frag_sample, text = "Sample")

        self.tabs_frag.bind("<<NotebookTabChanged>>", self.change_frags_tab)

        self.tabs_frag.pack(expand = 1, fill = "both")

        #TEST


        self.figure_peak, self.axes_peak = self.initialize_plot(self.tab_peak)
        self.figure_der_all, self.axes_der_all = self.initialize_plot(self.tab_der_all)
        self.figure_der_log, self.axes_der_log = self.initialize_plot(self.tab_der_log)
        self.figure_int_all, self.axes_int_all = self.initialize_plot(self.tab_int_all)
        self.figure_int_log, self.axes_int_log = self.initialize_plot(self.tab_int_log)
        self.figure_frag_con, self.axes_frag_con = self.initialize_plot(self.tab_frag_con)
        self.figure_frag_sample, self.axes_frag_sample = self.initialize_plot(self.tab_frag_sample)

        # Select initial selected plot
        default_plot = self.data.get_settings_preference_by_name("defplot")

        if default_plot == "Peak":
            self.tabs_plot.select(0)
            self.tabs_der.select(0)
            self.tabs_int.select(0)
        elif default_plot == "Derivatives:All":
            self.tabs_plot.select(1)
            self.tabs_der.select(0)
            self.tabs_int.select(0)
        elif default_plot == "Derivatives:Log":
            self.tabs_plot.select(1)
            self.tabs_der.select(0)
            self.tabs_int.select(1)
        elif default_plot == "Intensity:All":
            self.tabs_plot.select(2)
            self.tabs_der.select(0)
            self.tabs_int.select(0)
        elif default_plot == "Intensity:Log":
            self.tabs_plot.select(2)
            self.tabs_der.select(0)
            self.tabs_int.select(1)
        elif default_plot == "Fragmentation:Consensus":
            self.tabs_plot.select(3)
            self.tabs_der.select(0)
            self.tabs_int.select(0)
        elif default_plot == "Fragmentation:Sample":
            self.tabs_plot.select(3)
            self.tabs_der.select(0)
            self.tabs_int.select(1)

        # Set View
        self.set_tree = self.initialize_grid(self.mid_right_top_frame, True, [("Selected", 60), ("Name", 150)])
        self.set_tree.bind('<ButtonRelease-1>', self.update_sets_view)

        # Annotation View
        self.ann_tree = self.initialize_grid(self.mid_right_mid_frame, False, [("Selected", 10), ("Label", 80), ("Value", 120)])

        # Molecule View
        self.molecule_canvas = tk.Canvas(self.mid_right_bot_frame, bg="white")

        molecule_canvas_vsb = ttk.Scrollbar(self.mid_right_bot_frame, orient="vertical")

        molecule_canvas_vsb.pack(side=tk.RIGHT, fill="y")
        molecule_canvas_hsb = ttk.Scrollbar(self.mid_right_bot_frame, orient="horizontal")

        molecule_canvas_hsb.pack(side=tk.BOTTOM, fill="x")
        self.molecule_canvas.configure(yscrollcommand=molecule_canvas_vsb.set, xscrollcommand=molecule_canvas_hsb.set)

        self.molecule_canvas.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.TRUE)
        molecule_canvas_vsb.config(command=self.molecule_canvas.yview)
        molecule_canvas_hsb.config(command=self.molecule_canvas.xview)

        # Identification View
        iden_control_frame = tk.Frame(self.bot_frame)
        iden_control_frame.pack(side=tk.RIGHT)
        self.iden_edit_selected_btn = tk.Button(iden_control_frame, text="Edit Selected", command=self.edit_selected_identity)
        self.iden_edit_selected_btn["state"] = "disabled"
        self.iden_edit_selected_btn.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEW")
        self.iden_frag_comp_btn = tk.Button(iden_control_frame, text="Fragment Comparison", command=self.open_fragment_comparison_dialog)
        self.iden_frag_comp_btn["state"] = "disabled"
        self.iden_frag_comp_btn.grid(row=1, column=0, padx=(2,2), pady=(2,2), sticky="NEW")
        self.iden_delete_checked_btn = tk.Button(iden_control_frame, text="Delete Checked", command=self.delete_checked_identities)
        self.iden_delete_checked_btn["state"] = "disabled"
        self.iden_delete_checked_btn.grid(row=2, column=0, padx=(2,2), pady=(2,2), sticky="NEW")

        self.identities = ttk.Notebook(self.bot_frame)
        self.general_tree = ttk.Frame(self.identities)
        self.IPA_tree = ttk.Frame(self.identities)
        self.identities.add(self.general_tree, text = "General")
        self.identities.add(self.IPA_tree, text = "IPA")

        self.identities.pack()
        self.identities.bind("<<NotebookTabChanged>>", self.iden_tab_changed)

        #api tree
        self.IPA_iden_tree = self.initialize_grid(self.IPA_tree, True, [("Selected", 40), ("ID", 100), ("Name", 150), ("Formula", 150), ("Adduct", 80), ("M/Z", 150), ("Charge", 50), ("PPM", 100), ("Isotope pattern score", 150), ("Fragmentation pattern score", 200), ("Prior", 100), ("Post", 100), ("Post Gibbs", 100), ("\u03A7^2 pval", 100)])
        self.IPA_iden_tree.tag_configure("not_focus", foreground="black")
        self.IPA_iden_tree.tag_configure("is_focus", foreground="white", background="blue")
        self.IPA_iden_tree.bind('<ButtonRelease-1>', self.IPA_select_iden)

        #general tree
        self.iden_tree = self.initialize_grid(self.general_tree, True, [("Selected", 40), ("ID", 100), ("Formula", 150), ("PPM", 100), ("Adduct", 150), ("Name", 150), ("Class", 150), ("Description", 200), ("Prior", 100), ("Post", 100), ("Notes", 200)])
        self.iden_tree.bind('<ButtonRelease-1>', self.select_iden)
        self.iden_tree.bind('<KeyRelease-Up>', self.select_iden)
        self.iden_tree.bind('<KeyRelease-Down>', self.select_iden)
        self.iden_tree.tag_configure("not_focus", foreground="black")
        self.iden_tree.tag_configure("is_focus", foreground="white", background="blue")

        # Set initial widget layout vf_0, vf_1, mf_0, mf_1, mlf_0, mrf_0, mrf_1
        self.update_layout(self._set_vf0, self._set_vf1, self._set_mf0, self._set_mf1, self._set_mlf0, self._set_mrf0, self._set_mrf1)

        self.root.config(menu=self.menubar)

        #Set initial configure timer running.
        self.reset_configure_timer()

        # If provided import annotation params file     
        if annotation_params:
            if os.path.exists(annotation_params):
                self.annotation_params_path = annotation_params

        # If provided import .peakml file
        if peakml_file_path:
            if os.path.exists(peakml_file_path):
                try:
                    self.data.import_peakml_filepath = peakml_file_path
                    self.run_process_with_progress(self.import_peakml_file)
                except IOError as ioerr:
                    self.handle_error("Unable to open PeakML file.", ioerr)
                except Exception as err:
                    self.handle_error("Unable to open PeakML file.", err)

        # Run GUI until event occurs.
        self.root.mainloop()

    # Fix to bug with tkinter
    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled","!selected")]

    def iden_tab_changed(self,event):
        self.selected_identities_tab = self.identities.index(self.identities.select())
        self.refresh_identification_grid()


#region Layout methods

    # def update_fragmentation_dbs(self):
    #     type1 = self.data.get_settings_frag_database_type_1_paths()["Path"].tolist()
    #     type2 = self.data.get_settings_frag_database_type_2_paths()["Path"].tolist()


    #     dbs = []
    #     for i in type1:
    #         dbs.append(pd.read_csv(i, header=0))
    #     self.id_db = pd.concat(dbs)

    #     dbs = []
    #     for i in type2:
    #         dbs.append(pd.read_csv(i, header=0))
    #     self.id_samples = pd.concat(dbs)



#   https://stackoverflow.com/questions/38600625/do-something-after-a-period-of-gui-user-inactivity-tkinter
    def reset_configure_timer(self, event=None):
        global configure_timer

        # cancel previous event
        if configure_timer is not None:
            self.root.after_cancel(configure_timer)

        # create new
        configure_timer = self.root.after(200, self.update_layout_if_resize)



    def update_layout(self, vf_0, vf_1, mf_0, mf_1, mlf_0, mrf_0, mrf_1):

        # VF
        self.viewer_frame.update()
        self.viewer_frame.sash_place(0, 1, vf_0)
        self.viewer_frame.update()
        self.viewer_frame.sash_place(1, 1, vf_1)

        # MF
        self.mid_frame.update()
        self.mid_frame.sash_place(0, mf_0, 1)
        self.mid_frame.update()
        self.mid_frame.sash_place(1, mf_1, 1)

        # MLF
        self.mid_left_frame.update()
        self.mid_left_frame.sash_place(0, 1, mlf_0)

        # MRF
        self.mid_right_frame.update()
        self.mid_right_frame.sash_place(0, 1, mrf_0)
        self.mid_right_frame.update()
        self.mid_right_frame.sash_place(1, 1, mrf_1)

        self.set_vf0 = vf_0
        self.set_vf1 = vf_1
        self.set_mf0 = mf_0
        self.set_mf1 = mf_1
        self.set_mlf0 = mlf_0
        self.set_mrf0 = mrf_0
        self.set_mrf1 = mrf_1

    def get_current_layout(self):

        height = self.root_frame.winfo_height()
        width = self.root_frame.winfo_width()

        vf0 = self.viewer_frame.sash_coord(0)[1]
        vf1 = self.viewer_frame.sash_coord(1)[1]
        mf0 = self.mid_frame.sash_coord(0)[0]
        mf1 = self.mid_frame.sash_coord(1)[0]
        mlf0 = self.mid_left_frame.sash_coord(0)[1]
        mrf0 = self.mid_right_frame.sash_coord(0)[1]
        mrf1 = self.mid_right_frame.sash_coord(1)[1]

        print(f"Layout: height: {height}, width: {width}, VF0: {vf0}, VF1: {vf1}, MF0: {mf0}, MF1: {mf1}, MLF0: {mlf0}, MRF0: {mrf0}, MRF1: {mrf1}")

    def update_layout_if_resize(self):

        current_height = self.root_frame.winfo_height()
        current_width = self.root_frame.winfo_width()

        # Update layout, if overall window size has changed.
        if (current_height != self.set_height or current_width != self.set_width):

            height_change = current_height - self.set_height
            width_change = current_width - self.set_width

            self.set_height = current_height
            self.set_width = current_width

            # Fixed height, not modified
            vf0_u = self.set_vf0
            # Increasing the height should be able to increase this an unlimited amount.
            vf1_u = self.set_vf1 + height_change
            mf0_u = self.set_mf0
            # Increasing the width should be able to increase this an unlimited amount.
            mf1_u = self.set_mf1 + width_change
            mlf0_u = self.set_mlf0
            mrf0_u = self.set_mrf0
            mrf1_u = self.set_mrf1

            if 1117 == current_height and 1920 == current_width:
                self.update_layout(43, 852, 400, 1565, 576, 379, 565)

            elif 720 == current_height and 1280 == current_width:
                self.update_layout(43, 551, 303, 1011, 303, 153, 261)

            else:
                self.update_layout(vf0_u, vf1_u, mf0_u, mf1_u, mlf0_u, mrf0_u, mrf1_u)

#endregion

#region Control initialise methods

    def initialize_plot(self, tab):
        figure = plt.Figure(figsize=(12,12))
        axes = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, tab)
        toolbar_frame = tk.Frame(tab)
        toolbar_frame.pack(side="top",fill ='x', expand=True)
        NavigationToolbar2Tk(canvas, toolbar_frame)
        canvas.get_tk_widget().pack(side="top", fill ='both', expand=True)
        canvas.draw()

        return figure, axes

    def initialize_grid(self, frame, is_checkbox, columns):
        if is_checkbox:
            tree = ttkw.CheckboxTreeview(frame, selectmode="browse", columns=len(columns))
        else:
            tree = ttk.Treeview(frame, columns=len(columns))

        tree.update()

        tree["columns"] = [i[0] for i in columns]

        for i in range(len(columns)):
            column_name = columns[i][0] if columns[i][0] != "Selected" else ""
            tree.heading("#{0}".format(i), text=column_name)
            tree.column("#{0}".format(i), width = columns[i][1], stretch = False, anchor=tk.CENTER)

        tree_vsb = ttk.Scrollbar(frame, orient="vertical")

        tree_vsb.pack(side=tk.RIGHT, fill="y")
        tree_hsb = ttk.Scrollbar(frame, orient="horizontal")

        tree_hsb.pack(side=tk.BOTTOM, fill="x")
        tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)

        tree.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.TRUE)
        tree_vsb.config(command=tree.yview)
        tree_hsb.config(command=tree.xview)

        tree['show'] = ('headings','tree')

        tree.update()

        return tree

#endregion

#region Logging methods

    def handle_error(self, error_message, error_details):
        lg.log_error(f'{error_message}: {error_details}')
        mb.showerror("Error", error_message)

#endregion

#region Progress bar methods

    def check_progress(self):
        if self.thread.is_alive():
            self.update_progress_details()
            self.root.after(100, self.check_progress) # Calls this method after 100 ms.
        else:
            self.show_progressbar(False)

    def show_progressbar(self, start):
        if start:
            self.start_progress_dialog()
        else:
            self.progress_text.set("Completed")

    def start_progress_dialog(self):
        self.progress_dlg = ProgressDialog(self.root, self.progress_text, self.progress_val)

    def run_process_with_progress(self, func):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=func, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def update_progress_details(self):
        self.progress_text.set(p.progress_text_global)
        self.progress_val.set(p.progress_value_global)

#endregion

#region IO Methods

    def import_peakml_file(self):
        p.update_progress("Importing file", 0)

        try:
            # Load data objects
            self.data.import_peakml_data()

            # Enable disabled menu items.
            self.filemenu.entryconfig(1, state=tk.NORMAL)
            self.filemenu.entryconfig(2, state=tk.NORMAL)
            self.editmenu.entryconfig(0, state=tk.NORMAL)
            self.editmenu.entryconfig(1, state=tk.NORMAL)
            self.editmenu.entryconfig(2, state=tk.NORMAL)
            self.editmenu.entryconfig(4, state=tk.NORMAL)
            self.ipamenu.entryconfig(0, state=tk.NORMAL)
            self.ipamenu.entryconfig(1, state=tk.NORMAL)

            if self.annotation_params_path:
                self.import_ipa_annotations_file()

            # Update UI widgets
            self.load_data_from_views()

        except Exception as err:
            self.handle_error("Unable to import PeakML file.", err)
            p.update_progress("Completed", 100)

        p.update_progress("File imported.", 100)


    def import_ipa_annotations_file(self):
        p.update_progress("Applying annotation parameters", 0)
        try:
            # Load parameters from file
            with open(self.annotation_params_path, "r") as ann_params:
                ann = json.load(ann_params)
            print(ann)
            # Load data objects
            self.data.update_ipa_params(
                    ann["ionisation"], 
                    ann["ppm"], 
                    ann["noits"], 
                    ann["burn"], 
                    ann["delta_add"], 
                    ann["delta_bio"], 
                    ann["mode"], 
                    ann["CSunk"], 
                    ann["ncores"], 
                    ann["isodiff"], 
                    ann["ppmiso"], 
                    ann["me"], 
                    ann["ratiosd"], 
                    ann["ppmunk"], 
                    ann["ratiounk"], 
                    ann["ppmthr"], 
                    ann["pRTNone"], 
                    ann["pRTout"], 
                    ann["mzdCS"], 
                    ann["ppmCS"], 
                    ann["evfilt"], 
                    ann["connections"])

        except Exception as err:
            self.handle_error("Unable to import annotation file.", err)

            p.update_progress("Completed", 100)

        # Generate annotation
        self.generate_annotation_for_peakml()


    def import_ipa_rdata_file(self):
        p.update_progress("Importing IPA data", 0)

        try:
            # Load data objects
            self.data.import_ipa_data()

            # Update UI widgets
            self.load_data_from_views()

        except Exception as err:
            self.handle_error("Unable to import IPA file.", err)

            p.update_progress("Completed", 100)

        p.update_progress("IPA data imported.", 100)

    def generate_annotation_for_peakml(self):
        p.update_progress("Running annotation", 0)

        try:
            # Load data objects
            self.data.generate_annotation_with_ipav2()

            # Update UI widgets
            self.load_data_from_views()

        except Exception as err:
            self.handle_error("Unable to annotate current PeakML.", err)

            p.update_progress("Completed", 100)

        p.update_progress("IPA annotation complete.", 100)

    def export_peakml_file(self):
        p.update_progress("Exporting file", 0)

        try:
            self.data.export_peakml()

        except Exception as err:
            self.handle_error("Unable to export PeakML file.", err)

        p.update_progress("File exported.", 100)

    def export_ipa_rdata_file(self):
        p.update_progress("Exporting file", 0)

        try:
            self.data.export_ipa()

        except Exception as err:
            self.handle_error("Unable to export IPA file.", err)

        p.update_progress("File exported.", 100)

    def export_ipa_priors_rdata_file(self):
        p.update_progress("Exporting file", 0)

        try:
            self.data.export_ipa_priors()

        except Exception as err:
            self.handle_error("Unable to export IPA file.", err)

        p.update_progress("File exported.", 100)

#endregion

#region Menu Methods

    def file_open(self):
        try:
            filepath = fd.askopenfilename()
            if filepath:
                self.data.import_peakml_filepath = filepath
                self.run_process_with_progress(self.import_peakml_file)
        except IOError as ioerr:
            self.handle_error("Unable to open PeakML file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open PeakML file.", err)

    def file_save(self):
        try:
            reply = mb.askokcancel(title="Update Imported File", message=f"Are you sure you want to update the imported file '{self.data.import_peakml_filename}'?")
            if reply == True:
                self.data.export_filepath = self.data.import_peakml_filepath
                self.run_process_with_progress(self.export_peakml_file)
        except IOError as ioerr:
            self.handle_error("Unable to save PeakML file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to save PeakML file.", err)

    def file_save_as(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".peakml")
            if filepath:
                self.data.export_filepath = filepath
                self.run_process_with_progress(self.export_peakml_file)
        except IOError as ioerr:
            self.handle_error("Unable to save PeakML file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to save PeakML file.", err)

    def import_ipa_file(self):
        try:
            ipa_filepath = fd.askopenfilename(defaultextension=".Rdata")
            if ipa_filepath:
                self.data.import_ipa_filepath = ipa_filepath
                self.run_process_with_progress(self.import_ipa_rdata_file)
        except IOError as ioerr:
            self.handle_error("Unable to open IPA file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open IPA file.", err)

    def generate_annotation(self):
        try:
        #    ipa_filepath = fd.askopenfilename(defaultextension=".Rdata")
        #    if ipa_filepath:
        #        self.data.import_ipa_filepath = ipa_filepath

            self.run_process_with_progress(self.generate_annotation_for_peakml)
        #except IOError as ioerr:
        #    self.handle_error("Unable to open IPA file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to annotate.", err)

    def export_ipa_file(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".Rdata")
            if filepath:
                self.data.export_filepath = filepath
                self.run_process_with_progress(self.export_ipa_rdata_file)
        except IOError as ioerr:
            self.handle_error("Unable to open IPA file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open IPA file.", err)

    def export_ipa_priors_file(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".Rdata")
            if filepath:
                self.data.export_filepath = filepath
                self.run_process_with_progress(self.export_ipa_priors_rdata_file)
        except IOError as ioerr:
            self.handle_error("Unable to open IPA file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open IPA file.", err)

    def open_preferences_dialog(self):
        dlg = PreferencesDialog(self.root,"Preferences", self.data, self.frag_threshold, self.fragPPM, self.mzd, self.frag_option, self.blank)
        if dlg.submit:
            self.data.update_settings(dlg.decdp, dlg.defplot, dlg.databases, dlg.frag_databases_type_1, dlg.frag_databases_type_2)
            self.run_process_with_progress(self.refresh_entry_selected)
            self.frag_threshold = dlg.threshold
            self.mzd = dlg.frag_absolute
            self.fragPPM = dlg.frag_ppm
            self.frag_option = dlg.frag_option
            self.blank = dlg.blank
            #self.update_fragmentation_dbs()
            self.data.import_fragment_databases()

    
    def open_set_ipa_params_dialog(self):
        print("INPUTS")
        print("ionistation: " + str(self.data.ipa_params.ionisation))
        print("ppm: " + str(self.data.ipa_params.ppm))
        print("noits: " + str(self.data.ipa_params.noits))
        print("burn: " + str(self.data.ipa_params.burn))
        print("delta_add: " + str(self.data.ipa_params.delta_add))
        print("delta_bio: " + str(self.data.ipa_params.delta_bio))
        print("mode: " + str(self.data.ipa_params.mode))
        print("CSunk: " + str(self.data.ipa_params.CSunk))
        print("ncores: " + str(self.data.ipa_params.ncores))

        print("isodiff: " + str(self.data.ipa_params.isodiff))
        print("ppmiso: " + str(self.data.ipa_params.ppmiso))
        print("me: " + str(self.data.ipa_params.me))
        print("ratiosd: " + str(self.data.ipa_params.ratiosd))
        print("ppmunk: " + str(self.data.ipa_params.ppmunk))
        print("ratiounk: " + str(self.data.ipa_params.ratiounk))
        print("ppmthr: " + str(self.data.ipa_params.ppmthr))
        print("pRTNone: " + str(self.data.ipa_params.pRTNone))
        print("pRTout: " + str(self.data.ipa_params.pRTout))
        print("mzdCS: " + str(self.data.ipa_params.mzdCS))
        print("ppmCS: " + str(self.data.ipa_params.ppmCS))
        print("evfilt: " + str(self.data.ipa_params.evfilt))
        print("connections: " + ", ".join(str(val) for val in self.data.ipa_params.connections))

        dlg = SetIPAParamsDialog(self.root,"Set IPA Parameters", self.data.ipa_params)
        if dlg.submit:
            print("OUTPUTS")
            print("ionistation: " + dlg.ionisation)
            print("ppm: " + dlg.ppm)
            print("noits: " + dlg.noits)
            print("burn: " + dlg.burn)
            print("delta_add: " + dlg.delta_add)
            print("delta_bio: " + dlg.delta_bio)
            print("mode: " + dlg.mode)
            print("CSunk: " + dlg.CSunk)
            print("ncores: " + dlg.ncores)

            print("isodiff: " + dlg.isodiff)
            print("ppmiso: " + dlg.ppmiso)
            print("me: " + str(dlg.me))
            print("ratiosd: " + dlg.ratiosd)

            if dlg.ppmunk:
                print("ppmunk: " + dlg.ppmunk)
            else:
                print("ppmunk: " + "None")

            if dlg.ratiounk:
                print("ratiounk: " + dlg.ratiounk)
            else:
                print("ratiounk: " + "None")

            if dlg.ppmthr:
                print("ppmthr: " + dlg.ppmthr)
            else:
                print("ppmthr: " + "None")

            if dlg.pRTNone:
                print("pRTNone: " + dlg.pRTNone)
            else:
                print("pRTNone: " + "None")

            if dlg.pRTout:
                print("pRTout: " + dlg.pRTout)
            else:
                print("pRTout: " + "None")

            print("mzdCS: " + dlg.mzdCS)
            print("ppmCS: " + dlg.ppmCS)
            print("evfilt: " + dlg.evfilt)
            print("connections: " + ", ".join(str(val) for val in dlg.connections))

            self.data.update_ipa_params(dlg.ionisation, dlg.ppm, dlg.noits, dlg.burn, dlg.delta_add, dlg.delta_bio, dlg.mode, dlg.CSunk, dlg.ncores, dlg.isodiff, dlg.ppmiso, dlg.me, dlg.ratiosd, dlg.ppmunk, dlg.ratiounk, dlg.ppmthr, dlg.pRTNone, dlg.pRTout, dlg.mzdCS, dlg.ppmCS, dlg.evfilt, dlg.connections)
            self.run_process_with_progress(self.generate_annotation_for_peakml)

    def open_log_dialog(self):
        LogDialog(self.root)

    def open_peak_split_dialog(self):
        rt_mean = self.data.selected_retention_time
        dlg = PeakSplitDialog(self.root, "Set Retention Time for Peak Split", rt_mean, self.data.plot_peak_view_dataframe)
        if dlg.submit:
            self.data.peak_split_retention_time = f"{dlg.retention_time_min}:{dlg.retention_time_sec}"
            self.data.group_split_peak = dlg.group_split
            self.run_process_with_progress(self.split_peak_on_retention_time)

    def open_fragment_comparison_dialog(self):

        selected = self.data.identification_view_dataframe.loc[self.data.identification_view_dataframe["Selected"] == True]


        fragment_samples = []

        if self.blank == "":
            self.blank = "############"

        data = self.data.plot_frag_view_dataframe
        for index, row in data.iterrows():
            if self.blank not in row['Label']:
                frags = list(dict.fromkeys(row['Fragments']))
                con_mz = []
                con_ints = []

                for fragment in frags:
                    a = fragment.split(',')
                    con_mz.append(float(a[0]))
                    con_ints.append(float(a[1]))

                fragment_samples.append(SampleFragmentsItem(con_mz,con_ints))

        if self.blank == "############":
            self.blank = ""

        if self.frag_option == 2:
            con = ConsensusSpec(fragment_samples,float(self.frag_threshold)/100,self.mzd,0)
        else:
            con = ConsensusSpec(fragment_samples,float(self.frag_threshold)/100,0,self.fragPPM)




        if self.selected_identities_tab == 0:
            if self.frag_option == 2:
                dlg = FragmentComparisonDialog(self.root,"Fragment Comparison",con,selected["ID"].values[0],self.data.fragment_id_db,self.data.fragment_id_samples,self.mzd,0)
            else:
                dlg = FragmentComparisonDialog(self.root,"Fragment Comparison",con,selected["ID"].values[0],self.data.fragment_id_db,self.data.fragment_id_samples,0,self.fragPPM)
        else:
            if self.frag_option == 2:
                dlg = FragmentComparisonDialog(self.root,"Fragment Comparison",con,selected["IPA_id"].values[0],self.data.fragment_id_db,self.data.fragment_id_samples,self.mzd,0)
            else:
                dlg = FragmentComparisonDialog(self.root,"Fragment Comparison",con,selected["IPA_id"].values[0],self.data.fragment_id_db,self.data.fragment_id_samples,0,self.fragPPM)

    def split_peak_on_retention_time(self):
        p.update_progress("Splitting peak", 0)
        group_split = self.data.group_split_peak
        try:
            # Load data objects
            #self.data.split_selected_peak_on_retention_time()
            #self.data.group_split_selected_peak_on_retention_time()
            if group_split == 1:
                self.data.group_split_selected_peak_on_retention_time()
            else:
                self.data.split_selected_peak_on_retention_time()


            # Update UI widgets
            self.load_data_from_views()

        except Exception as err:
            self.handle_error("Unable to split peak.", err)
            p.update_progress("Completed", 100)

        p.update_progress("Peak split.", 100)

    def entries_view_check_all(self):
        self.data.update_entry_check_all()
        self.refresh_entry_grid()

    def entries_view_uncheck_all(self):
        self.data.update_entry_uncheck_all()
        self.refresh_entry_grid()

    def entries_view_invert_check(self):
        self.data.update_entry_invert_check_all()
        self.refresh_entry_grid()
#endregion

#region Info/Entry View Methods

    def load_data_from_views(self):
        p.update_progress("Loading filter grid", 100)
        self.refresh_filters_grid()

        self.load_peak_data_from_views()

    def load_peak_data_from_views(self):
        p.update_progress("Loading entry grid", 50)
        self.refresh_info_values()
        self.refresh_entry_grid()
        lg.log_progress("Entry grid loaded.")

        p.update_progress("Loading sets grid", 60)
        self.refresh_set_grid()
        lg.log_progress("Sets grid loaded.")

        self.refresh_to_selected_entry()

    def refresh_to_selected_entry(self):

        p.update_progress("Loading annotation grid", 65)
        self.refresh_annotation_grid()
        lg.log_progress("Annotation grid loaded.")

        p.update_progress("Loading identification grid", 70)
        self.refresh_identification_grid()
        lg.log_progress("Identification grid loaded.")

        p.update_progress("Loading plot", 75)

        self.plot_peak_loaded = False
        self.plot_der_all_loaded = False
        self.plot_der_log_loaded = False
        self.plot_int_all_loaded = False
        self.plot_int_log_loaded = False
        self.plot_frag_con_loaded = False
        self.plot_frag_sample_loaded = False

        self.load_plot()

        lg.log_progress("Plot loaded.")

    def refresh_info_values(self):
        self.filename_text.set(self.data.import_peakml_filename)
        self.peak_number_text.set(self.data.nr_peaks_details)

        if self.data.prior_probabilities_modified:
            self.warning_text.set("Warning: Prior values have been updated since import, so posterior probabilities will need to be recalculated.")

    def refresh_entry_grid(self):

        # Clear grid
        self.entry_tree.delete(*self.entry_tree.get_children())

        # Get view object dataframe
        self.df_entry = self.data.entry_view_dataframe

        #If values, populate grid
        if self.df_entry is not None:
            for i in range(len(self.df_entry)):
                entry_row = self.df_entry.iloc[i]

                # Set focus string
                if entry_row["HasAnnotation"] == True:
                    focus = "has_ann_is_focus" if entry_row["Selected"] == True else "has_ann_not_focus"
                else:
                    focus = "no_ann_is_focus" if entry_row["Selected"] == True else "no_ann_not_focus"

                # Update current entry based on selected entry.
                if entry_row["Selected"] == True:
                    self.current_entry = i

                # Add entries to tree
                self.entry_tree.insert("",i,i, values=(entry_row["RT"], entry_row["Mass"], entry_row["Intensity"], entry_row["Nrpeaks"]), tags=(entry_row["UID"], focus, "checked" if entry_row["Checked"] == True else "unchecked"))

                p.update_progress(f"Populating peak {(i+1)} of {len(self.df_entry)} to Entry View")

        # If any entries, enable button for adding filters.
        if len(self.entry_tree.get_children()) > 0:
            self.filter_add_btn["state"] = "normal"
        else:
            self.filter_add_btn["state"] = "disabled"

        # If any checked entries, enable button for deleting checked entries.
        if self.data.check_if_any_checked_entries():
            self.entry_delete_checked_btn["state"] = "normal"
        else:
            self.entry_delete_checked_btn["state"] = "disabled"

        #update frg comparison button


    def select_entry(self, event):

        lg.log_progress("Begin selecting entry.")

        # Use currently focused row to update the tags on that one.
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        checked_item = self.entry_tree.identify("item", x, y)


        if "image" in elem:
            # Save check status of each list
            uid = self.entry_tree.item(checked_item)["tags"][0]
            selected_status = False if self.entry_tree.item(checked_item)["tags"][2] == "unchecked" else True
            self.data.update_entry_checked_status(uid, selected_status)

            if self.data.check_if_any_checked_entries():
                self.entry_delete_checked_btn["state"] = "normal"
            else:
                self.entry_delete_checked_btn["state"] = "disabled"
        else:
            lg.log_progress("Changing currently selected entry.")
            # Get focused entry
            focused_entry = self.entry_tree.item(self.entry_tree.focus())
            selected_item = self.entry_tree.focus()
            #If exists, update selected entry property
            if focused_entry["tags"]:

                # Short circuit if selecting currently selected
                if self.data.selected_entry_uid != focused_entry["tags"][0]:
                    prev_item = self.current_entry

                    # Update tags to remove focus from previously selected row and add to row being selected
                    self.update_selected_entry_grid_row(selected_item, prev_item)

                    self.current_entry = selected_item

                    self.data.selected_entry_uid = focused_entry["tags"][0]

                lg.log_progress("Load selected entry details.")
                #Attempt to load details of record, if unable revert to previously selected record.
                try:
                    self.refresh_entry_selected()

                except Exception as err:
                    #Restore previous selection by updating tags
                    self.update_selected_entry_grid_row(prev_item, selected_item)
                    self.handle_error("Unable to load entry", err)

            lg.log_progress("Entry selected.")


    def update_selected_entry_grid_row(self, new_item, prev_item):

        # Prev row
        if self.entry_tree.item(prev_item)["tags"][1] == "has_ann_is_focus":
            self.entry_tree.item(prev_item, tags=(self.entry_tree.item(prev_item)["tags"][0], "has_ann_not_focus", self.entry_tree.item(prev_item)["tags"][2]))
        elif self.entry_tree.item(prev_item)["tags"][1] == "no_ann_is_focus":
            self.entry_tree.item(prev_item, tags=(self.entry_tree.item(prev_item)["tags"][0], "no_ann_not_focus", self.entry_tree.item(prev_item)["tags"][2]))

        # New row
        if self.entry_tree.item(new_item)["tags"][1] == "has_ann_not_focus":
            self.entry_tree.item(new_item, tags=(self.entry_tree.item(new_item)["tags"][0], "has_ann_is_focus", self.entry_tree.item(new_item)["tags"][2]))
        elif self.entry_tree.item(new_item)["tags"][1] == "no_ann_not_focus":
            self.entry_tree.item(new_item, tags=(self.entry_tree.item(new_item)["tags"][0], "no_ann_is_focus", self.entry_tree.item(new_item)["tags"][2]))

    def refresh_entry_selected(self):

        # Reloads data view objects for new selected entry.
        self.data.update_selected_entry()

        # Refreshes grids and plots from view object data (identification/annotation/plots)
        self.refresh_to_selected_entry()

    def delete_checked_entries(self):
        reply = mb.askokcancel(title="Delete Checked", message="Do you wish to delete all checked entries?")
        if reply == True:
            self.data.remove_checked_entries()
            self.load_data_from_views()

#endregion

#region Sets View Methods

    def refresh_set_grid(self):
        try:
            self.set_tree.delete(*self.set_tree.get_children())
        except:
            pass

        # Load set view data
        df_sets = self.data.set_view_dataframe


        if df_sets is not None:
            # Filter to sets which have no parent value (so are the parents)
            df_sets_parent = df_sets.loc[df_sets['Parent'].isnull()]

            if df_sets_parent is not None:
                for i in range(len(df_sets_parent)):
                    set_parent_row = df_sets_parent.iloc[i]
                    name_parent = set_parent_row["Name"]

                    select_parent = "checked" if set_parent_row["Checked"] else "unchecked"

                    colour_tag = "colour_" + name_parent

                    self.set_tree.tag_configure(colour_tag, foreground=set_parent_row["Color"])
                    folder = self.set_tree.insert("", i, f"P-{name_parent}", values=(name_parent), tags=("uid",select_parent, colour_tag))


                    df_sets_child = df_sets.loc[df_sets['Parent'] == name_parent]
                    data = self.data.plot_frag_view_dataframe
                    if df_sets_child is not None:

                        for j in range(len(df_sets_child)):
                            set_child_row = df_sets_child.iloc[j]
                            select_child = "checked" if set_child_row["Checked"] else "unchecked"

                            name_child = set_child_row["Name"]

                            self.set_tree.insert(folder, "end", f"C-{name_child}", values=(name_child), tags=(set_child_row["UID"], select_child, colour_tag))


    def update_sets_view(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # Save check status of each list
            for item in self.set_tree.get_children():
                for child_item in self.set_tree.get_children(item):
                    uid = self.set_tree.item(child_item)["tags"][0]
                    selected_status = False if self.set_tree.item(child_item)["tags"][2] == "unchecked" else True
                    self.data.update_set_checked_status(uid, selected_status)
            # Refresh grid
            self.frag_update = 1
            self.generate_plot_peak()
            self.generate_plot_frag_sample()
            self.generate_plot_frag_con()
            self.frag_update = 0

    def refresh_sets_for_samples(self):
        # Clear grid
        self.set_tree.delete(*self.set_tree.get_children())

        # Load set view data
        df_sets = self.data.set_view_dataframe


        if df_sets is not None:
            # Filter to sets which have no parent value (so are the parents)
            df_sets_parent = df_sets.loc[df_sets['Parent'].isnull()]

            if df_sets_parent is not None:
                for i in range(len(df_sets_parent)):
                    selected = self.data.plot_frag_view_dataframe["Label"].tolist()
                    set_parent_row = df_sets_parent.iloc[i]
                    name_parent = set_parent_row["Name"]

                    select_parent = "checked" if set_parent_row["Checked"] else "unchecked"

                    colour_tag = "colour_" + name_parent
                    self.set_tree.tag_configure(colour_tag, foreground=set_parent_row["Color"])

                    if any(name_parent in s for s in selected):
                        folder = self.set_tree.insert("", i, f"P-{name_parent}", values=(name_parent), tags=("uid",select_parent, colour_tag))
                    else:
                        folder = self.set_tree.insert("", i, f"P-{name_parent}", values=(name_parent), tags=("uid",select_parent, "#4d4a4b"))

                    df_sets_child = df_sets.loc[df_sets['Parent'] == name_parent]



                    if df_sets_child is not None:

                        for j in range(len(df_sets_child)):
                            set_child_row = df_sets_child.iloc[j]
                            select_child = "checked" if set_child_row["Checked"] else "unchecked"

                            name_child = set_child_row["Name"]


                            if name_child in selected:
                                self.set_tree.insert(folder, "end", f"C-{name_child}", values=(name_child), tags=(set_child_row["UID"], select_child, colour_tag))
                            else:
                                self.set_tree.insert(folder, "end", f"C-{name_child}", values=(name_child), tags=(set_child_row["UID"], select_child, "#4d4a4b"))

#endregion

#region Annotation Methods

    def refresh_annotation_grid(self):
        self.ann_tree.delete(*self.ann_tree.get_children())
        df_annotation = self.data.annotation_view_dataframe

        if df_annotation is not None:
            for i in range(len(df_annotation)):
                ann_row = df_annotation.iloc[i]
                if "IPA" not in ann_row["Label"]:
                    self.ann_tree.insert("", i, i, values=(ann_row["Label"], ann_row["Value"]))

#endregion

#region Identification View methods
    def refresh_identification_grid(self):
        #general tree
        try:
            self.iden_tree.delete(*self.iden_tree.get_children())
            self.IPA_iden_tree.delete(*self.IPA_iden_tree.get_children())
        except:
            pass
        df_identification = self.data.identification_view_dataframe

        smiles_details = inchi_details = None

        if df_identification is not None:
            for i in range(len(df_identification)):
                iden_row = df_identification.iloc[i]
                focus = "is_focus" if iden_row["Selected"] == True else "not_focus"
                checked = "checked" if iden_row["Checked"] == True else "unchecked"
                if iden_row["ID"] != "":
                    self.iden_tree.insert("",i,i, values=(iden_row["ID"],iden_row["Formula"],iden_row["PPM"],iden_row["Adduct"],iden_row["Name"],iden_row["Class"],iden_row["Description"],iden_row["Prior"],iden_row["Post"],iden_row["Notes"]), tags=(iden_row["UID"], focus, checked))

                if iden_row["Selected"] == True:
                    smiles_details = iden_row["Smiles"]
                    inchi_details = iden_row["InChi"]

        try:
            if len(self.iden_tree.get_children()) > 0:
                self.iden_edit_selected_btn["state"] = "normal"
            else:
                self.iden_edit_selected_btn["state"] = "disabled"

            if self.data.check_if_any_checked_identifications():
                self.iden_delete_checked_btn["state"] = "normal"
            else:
                self.iden_delete_checked_btn["state"] = "disabled"
        except:
            self.iden_edit_selected_btn["state"] = "disabled"
            self.iden_delete_checked_btn["state"] = "disabled"

        #IPA tree
        if df_identification is not None:
            for i in range(len(df_identification)):
                iden_row = df_identification.iloc[i]
                focus = "is_focus" if iden_row["Selected"] == True else "not_focus"
                checked = "checked" if iden_row["Checked"] == True else "unchecked"
                if iden_row["IPA_id"] != "":
                    self.IPA_iden_tree.insert("",i,i, values=(iden_row["IPA_id"],iden_row["IPA_name"],iden_row["IPA_formula"],iden_row["IPA_adduct"],iden_row["IPA_mz"],iden_row["IPA_charge"],iden_row["IPA_ppm"],iden_row["IPA_isotope_pattern_score"],iden_row["IPA_fragmentation_pattern_score"],iden_row["IPA_prior"],iden_row["IPA_post"],iden_row["IPA_post_Gibbs"],iden_row["IPA_post_chi_square_pval"]), tags=(iden_row["UID"], focus, checked))

                if iden_row["Selected"] == True:
                    if self.selected_identities_tab == 0:
                        smiles_details = iden_row["Smiles"]
                        inchi_details = iden_row["InChi"]
                    else:
                        smiles_details = iden_row["IPA_smiles"]
                        inchi_details = iden_row["IPA_inchi"]

        self.refresh_molecule_canvas(inchi_details, smiles_details)


    def refresh_molecule_canvas(self, inchi_data, smiles_data):
        self.molecule_canvas.delete("all")

        if inchi_data is not None and inchi_data != '':
            mol = inchi.MolFromInchi(inchi_data)
            mol_image = Draw.MolToImage(mol, size=(300,200))

        elif smiles_data is not None and inchi_data != '':
            mol = Chem.MolFromSmiles(smiles_data)
            mol_image = Draw.MolToImage(mol, size=(300,200))
        else:
            mol_image = Image.new(mode="RGB", size=(300,200), color = (255, 255, 255))

        self.mol_img = ImageTk.PhotoImage(mol_image)
        self.molecule_canvas.create_image(150, 100, image=self.mol_img)

    def IPA_select_iden(self, event):
        selected_item = self.IPA_iden_tree.item(self.IPA_iden_tree.focus())
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        checked_item = self.IPA_iden_tree.identify("item", x, y)
        if "image" in elem:
            uid = self.IPA_iden_tree.item(checked_item)["tags"][0]
            selected_status = False if self.IPA_iden_tree.item(checked_item)["tags"][2] == "unchecked" else True
            self.data.update_identification_checked_status(uid, selected_status)

            if self.data.check_if_any_checked_identifications():
                self.iden_delete_checked_btn["state"] = "normal"
            else:
                self.iden_delete_checked_btn["state"] = "disabled"

        else:
            self.refresh_iden_selected()

    def select_iden(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        checked_item = self.iden_tree.identify("item", x, y)
        if "image" in elem:
            uid = self.iden_tree.item(checked_item)["tags"][0]
            selected_status = False if self.iden_tree.item(checked_item)["tags"][2] == "unchecked" else True
            self.data.update_identification_checked_status(uid, selected_status)

            if self.data.check_if_any_checked_identifications():
                self.iden_delete_checked_btn["state"] = "normal"
            else:
                self.iden_delete_checked_btn["state"] = "disabled"
        else:
            self.refresh_iden_selected()

    def refresh_iden_selected(self):
        if self.selected_identities_tab == 0:
            focused_iden = self.iden_tree.item(self.iden_tree.focus())
        else:
            focused_iden = self.IPA_iden_tree.item(self.IPA_iden_tree.focus())




        if focused_iden["tags"]:
            focused_id = focused_iden["tags"][0]
            self.data.selected_identification_uid = focused_id
            "focused"



        self.refresh_identification_grid()

        selected = self.data.identification_view_dataframe.loc[self.data.identification_view_dataframe["Selected"] == True]


        if self.selected_identities_tab == 0:
            ms2 = self.data.fragment_id_db.loc[self.data.fragment_id_db['id'] == selected["ID"].values[0]]
        else:
            ms2 = self.data.fragment_id_db.loc[self.data.fragment_id_db['id'] == selected["IPA_id"].values[0]]

        try:
            sample_data = self.data.fragment_id_samples[self.data.fragment_id_samples["MonaID"] == ms2["MS2"].values[0]]
        except:
            sample_data = None

        if sample_data is not None:
            if (sample_data.empty) or (self.data.plot_frag_view_dataframe['Fragments'].empty):
                self.iden_frag_comp_btn["state"] = "disabled"
            else:
                self.iden_frag_comp_btn["state"] = "normal"
        else:
            self.iden_frag_comp_btn["state"] = "disabled"

    def delete_checked_identities(self):
        if self.data.ipa_imported:
            warning_message = "Are you sure you wish to remove selected identities? Prior probabilities of remaining identities will be updated."
        else:
            warning_message = "Do you wish to delete all checked identifications?"

        reply = mb.askokcancel(title="Delete Checked", message=warning_message)
        if reply == True:
            self.data.remove_checked_identifications(self.selected_identities_tab)
            self.refresh_identification_grid()
            self.refresh_info_values()

    def edit_selected_identity(self):
        self.open_edit_identity_dialog()

    def open_edit_identity_dialog(self):
        uid, id, prior, notes = self.data.get_selected_identification_details()

        dlg = EditIdentityDialog(self.root,"Edit Identity", id, prior, notes, self.data.ipa_imported)
        if dlg.submit:
            self.data.update_identification_details(uid, dlg.prior, dlg.notes)
            self.refresh_identification_grid()
            self.refresh_info_values()

#endregion

#region Plots Methods

    def change_plot_tab(self, event):
        self.selected_tab_plot = self.tabs_plot.tab(self.tabs_plot.select(), "text")
        self.load_plot()

    def change_der_tab(self, event):
        self.selected_tab_der = self.tabs_der.tab(self.tabs_der.select(), "text")
        self.load_plot()

    def change_int_tab(self, event):
        self.selected_tab_int = self.tabs_int.tab(self.tabs_int.select(), "text")
        self.load_plot()

    def change_frags_tab(self, event):
        self.selected_tab_frag = self.tabs_frag.tab(self.tabs_frag.select(), "text")
        self.load_plot()

    def load_plot(self):
        if self.visible_plot == "Peak":
            if not self.plot_peak_loaded:
                self.generate_plot_peak()

        elif self.visible_plot == "Der_All":
            if not self.plot_der_all_loaded:
                self.generate_plot_der_all()

        elif self.visible_plot == "Der_Log":
            if not self.plot_der_log_loaded:
                self.generate_plot_der_log()

        elif self.visible_plot == "Int_All":
            if not self.plot_int_all_loaded:
                self.generate_plot_int_all()

        elif self.visible_plot == "Int_Log":
            if not self.plot_int_log_loaded:
                self.generate_plot_int_log()

        elif self.visible_plot == "Frag_Consensus":
            if not self.plot_frag_con_loaded:
                self.generate_plot_frag_con()


        elif self.visible_plot == "Frag_Sample":
            if not self.plot_frag_sample_loaded:
                self.generate_plot_frag_sample()


    def generate_plot_peak(self):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        df = self.data.plot_peak_view_dataframe
        plot_count = len(df)
        self.axes_peak.clear()
        for i in range(plot_count):
            RT_values_arr = df.iloc[i]['RT_values']
            Intensity_values_arr = df.iloc[i]['Intensity_values']
            plot_label = df.iloc[i]["Label"]
            colour = df.iloc[i]["Colour"]

            visible = self.data.get_set_checked_status(plot_label)

            if visible:
                self.axes_peak.plot(RT_values_arr, Intensity_values_arr, marker='', color=colour, linewidth=0.5, label=plot_label)

        self.axes_peak.set_xlabel("Retention Time")
        self.axes_peak.set_ylabel("Intensity")

        date_format = DateFormatter("%M:%S")
        self.axes_peak.xaxis.set_major_formatter(date_format)

        self.figure_peak.canvas.draw()

    def generate_plot_der_all(self):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        df = self.data.plot_der_view_dataframe
        self.generate_plot_der(df, "All", self.figure_der_all, self.axes_der_all)

    def generate_plot_der_log(self):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        df = self.data.plot_der_view_dataframe
        self.generate_plot_der(df, "Log", self.figure_der_log, self.axes_der_log)

    def generate_plot_der(self, data, type, figure_der, axes_der):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        axes_der.clear()

        mass_values = np.array(data['Mass'])
        intensity_values = np.array(data['Intensity'])
        label_values = np.array(data['Description'])

        if len(mass_values) > 0:

            axes_der.stem(mass_values, intensity_values, markerfmt=" ")

            for i in range(len(data)):
                axes_der.annotate(text=label_values[i], xy=(mass_values[i], intensity_values[i]), xytext=(5,5), textcoords='offset points', horizontalalignment='left', verticalalignment='top')

            axes_der.set_xscale('linear')

            if type == "Log":
                axes_der.set_yscale('log')
            else:
                axes_der.set_yscale('linear')

            axes_der.set_xlabel("Mass")
            axes_der.set_ylabel("Intensity")

            figure_der.canvas.draw()

        #figure_der.tight_layout()

    def generate_plot_int_all(self):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        data = self.data.plot_int_view_dataframe
        self.axes_int_all.clear()

        set_id_label_values = data['SetID_Label']
        intensity_values = data['Intensity']

        self.axes_int_all.plot(set_id_label_values, intensity_values, marker='', linewidth=0.5)

        self.axes_int_all.set_xlabel("Set")
        self.axes_int_all.set_ylabel("Intensity")

        # Rotate labels so do overlap
        for tick in self.axes_int_all.get_xticklabels():
            tick.set_rotation(90)

        self.figure_int_all.canvas.draw()

    def generate_plot_int_log(self):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        data = self.data.plot_int_view_dataframe
        self.axes_int_log.clear()

        data = data.drop_duplicates(subset=["SetID"])

        set_id_values = data['SetID']
        intensities_mean_values = data['Intensities_Mean']
        intensities_neg_conf_values = data['Intensities_Neg_Conf']
        intensities_pos_conf_values = data['Intensities_Pos_Conf']

        self.axes_int_log.errorbar(set_id_values, intensities_mean_values, yerr=[intensities_neg_conf_values, intensities_pos_conf_values])

        self.axes_int_log.set_xlabel("Set")
        self.axes_int_log.set_ylabel("Intensity")

        # Rotate labels so do overlap
        for tick in self.axes_int_log.get_xticklabels():
            tick.set_rotation(305)

        self.figure_int_log.canvas.draw()

    def generate_plot_frag_con(self):
        if self.last_plot == "sample" and self.frag_update == 0:
            self.refresh_set_grid()
            self.last_plot = ""

        data = self.data.plot_frag_view_dataframe
        self.axes_frag_con.clear()


        fragment_samples = []

        if self.blank == "":
            self.blank = "############"



        for i in range(len(data)):
            plot_label = data.iloc[i]['Label']
            visible = self.data.get_set_checked_status(plot_label)
            if visible:
                if self.blank not in plot_label:
                    con_mz = []
                    con_ints = []

                    frags = data.iloc[i]['Fragments']

                    for f in frags:
                        a = f.split(',')
                        con_mz.append(float(a[0]))
                        con_ints.append(float(a[1]))

                    fragment_samples.append(SampleFragmentsItem(con_mz,con_ints))


        if self.blank == "############":
            self.blank = ""

        if fragment_samples:
            if self.frag_option == 2:
                con = ConsensusSpec(fragment_samples,float(self.frag_threshold)/100,self.mzd,0)
            else:
                con = ConsensusSpec(fragment_samples,float(self.frag_threshold)/100,0,self.fragPPM)

            frag_counter = 0

            while frag_counter < len(con.mz):
                x = [float(con.mz[frag_counter]),con.mz[frag_counter]]
                y = [0,float(con.intensity[frag_counter])]
                self.axes_frag_con.plot(x,y,linewidth=2, color="black")
                frag_counter += 1

        self.axes_frag_con.set_ylim(bottom=0)
        self.axes_frag_con.set_xlabel("m/z")
        self.axes_frag_con.set_ylabel("relative intensity")

        self.figure_frag_con.canvas.draw()


    def generate_plot_frag_sample(self):
        if self.last_plot == "" and self.frag_update == 0:
            self.refresh_sets_for_samples()
            self.last_plot = "sample"



        data = self.data.plot_frag_view_dataframe
        self.axes_frag_sample.clear()



        for i in range(len(data)):
            plot_label = data.iloc[i]['Label']
            visible = self.data.get_set_checked_status(plot_label)
            if visible:
                frags = data.iloc[i]['Fragments']
                xs = []
                ys = []
                for j in frags:
                    frag = j.split(',')
                    xs.append(float(frag[0]))
                    ys.append(float(frag[1]))

                maxim= max(ys)
                new_ys = []
                for j in ys:
                    new_ys.append((j/maxim)*100)

                frags = []
                for j in range(len(new_ys)):
                    frags.append(str(xs[j]) + "," + str(new_ys[j]))


                for fragment in frags:
                    frag_data = fragment.split(',')
                    x = [float(frag_data[0]),float(frag_data[0])]
                    y = [0,float(frag_data[1])]
                    if visible:
                        self.axes_frag_sample.plot(x,y,linewidth=2, color="black",label=plot_label)

        self.axes_frag_sample.set_ylim(bottom=0)
        self.axes_frag_sample.set_xlabel("m/z")
        self.axes_frag_sample.set_ylabel("relative intensity")

        self.figure_frag_sample.canvas.draw()
#endregion

#region Filter methods

    def refresh_filters_grid(self):
        self.filter_tree.delete(*self.filter_tree.get_children())
        df_filters = self.data.filter_view_dataframe

        if df_filters is not None:
            for i in range(len(df_filters)):
                filter_row = df_filters.iloc[i]

                focus = "is_focus" if filter_row["Selected"] == True else "not_focus"
                self.filter_tree.insert("", i, i, values=(filter_row["Type"], filter_row["Settings"]), tags=(filter_row["UID"], focus))

        # Toggle disability of remove filter button depending on if filter values exist.
        if len(self.filter_tree.get_children()) > 0:
            self.filter_remove_btn["state"] = "normal"
        else:
            self.filter_remove_btn["state"] = "disabled"

    def select_filter(self, event):
        self.refresh_filter_selected()

    def refresh_filter_selected(self):
        focused_filter = self.filter_tree.item(self.filter_tree.focus())

        if focused_filter["tags"]:
            focused_id = focused_filter["tags"][0]
            self.data.selected_filter_uid = focused_id

        self.refresh_filters_grid()

    def add_filter(self):
        refresh = False

        option = self.filter_option_selected.get()
        if option == self.filter_options[e.Filter.Mass]:
            refresh = self.open_filter_mass_dialog()
        elif option == self.filter_options[e.Filter.Intensity]:
            refresh = self.open_filter_intensity_dialog()
        elif option == self.filter_options[e.Filter.RetentionTime]:
            refresh = self.open_filter_retention_time_dialog()
        elif option == self.filter_options[e.Filter.NumberDetections]:
            refresh = self.open_filter_number_detections_dialog()
        elif option == self.filter_options[e.Filter.Annotations]:
            refresh = self.open_filter_annotations_dialog()
        elif option == self.filter_options[e.Filter.Probability]:
            refresh = self.open_filter_probability_dialog()
        elif option == self.filter_options[e.Filter.Sort]:
            refresh = self.open_filter_sort_dialog()
        elif option == self.filter_options[e.Filter.SortTimeSeries]:
            # Check if time series filter already exists.
            if self.data.check_if_existing_time_series_filter():
                mb.showwarning("Warning","Only one Sort time-series filter can be added at the same time.")
                refresh = False
            else:
                refresh = self.open_filter_sort_time_series_dialog()

        if refresh:
            self.run_process_with_progress(self.load_data_from_views)

    def remove_filter(self):
        # Need to include progress on this section
        self.data.remove_filter_by_id(self.data.selected_filter_uid)

        self.run_process_with_progress(self.load_data_from_views)

    def open_filter_mass_dialog(self):
        title = self.filter_options[e.Filter.Mass]
        mass_min, mass_max = self.data.get_min_max_mass()
        dlg = FilterMassDialog(self.root, title, mass_min, mass_max)

        # Need to include progress on this section
        if dlg.submit:
            self.data.add_filter_mass(dlg.mass_min, dlg.mass_max) #, dlg.formula, dlg.formula_ppm, dlg.mass_charge, dlg.filter_option
            return True
        else:
            return False

    def open_filter_intensity_dialog(self) -> bool:
        title = self.filter_options[e.Filter.Intensity]
        intensity_min, intensity_max = self.data.get_min_max_intensity()
        dlg = FilterIntensityDialog(self.root, title, intensity_min)
        if dlg.submit:
            self.data.add_filter_intensity(dlg.intensity_min)
            return True
        else:
            return False

    def open_filter_retention_time_dialog(self) -> bool:
        title = self.filter_options[e.Filter.RetentionTime]
        rt_min, rt_max = self.data.get_min_max_retention_time()
        dlg = FilterRetentionTimeDialog(self.root, title, rt_min, rt_max)
        if dlg.submit:
            self.data.add_filter_retention_time(dlg.retention_time_min_sec, dlg.retention_time_max_sec, dlg.retention_time_min_minu, dlg.retention_time_max_minu)
            return True
        else:
            return False

    def open_filter_number_detections_dialog(self) -> bool:
        title = self.filter_options[e.Filter.NumberDetections]
        sample_count_min, sample_count_max = self.data.get_min_max_samples_count()
        dlg = FilterNumberDetectionsDialog(self.root, title, sample_count_min, sample_count_max)
        if dlg.submit:
            self.data.add_filter_number_detections(dlg.sample_count)
            return True
        else:
            return False

    def open_filter_annotations_dialog(self) -> bool:
        title = self.filter_options[e.Filter.Annotations]
        dlg = FilterAnnotationsDialog(self.root, title)
        if dlg.submit:
            self.data.add_filter_annotations(dlg.annotation_name, dlg.annotation_relation, dlg.annotation_value)
            return True
        else:
            return False

    def open_filter_probability_dialog(self) -> bool:
        title = self.filter_options[e.Filter.Probability]
        dlg = FilterProbabilityDialog(self.root, title)
        if dlg.submit:
            self.data.add_filter_probability(dlg.prior_min, dlg.prior_max, dlg.post_min, dlg.post_max)
            return True
        else:
            return False

    def open_filter_sort_dialog(self) -> bool:
        title = self.filter_options[e.Filter.Sort]
        dlg = SortDialog(self.root, title)
        if dlg.submit:
            self.data.add_filter_sort(dlg.sort_type, dlg.sort_direction)
            return True
        else:
            return False

    def open_filter_sort_time_series_dialog(self) -> bool:
        title = self.filter_options[e.Filter.SortTimeSeries]
        sets = self.data.get_sets_list()
        dlg = SortTimeSeriesDialog(self.root, title, sets)
        if dlg.submit:
            self.data.add_filter_sort_times_series(dlg.set_values)
            return True
        else:
            return False

#endregion