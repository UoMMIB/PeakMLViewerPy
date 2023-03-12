import tkinter as tk
import tkinter.ttk as ttk
from UI.ViewerDialog import ViewerDialog
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import os
import json
import Logger as lg

class SetIPAParamsDialog(ViewerDialog):
    def __init__(self, parent, title, ipaparams):

        self.ionisation = ipaparams.ionisation
        self.ppm = ipaparams.ppm
        self.noits = ipaparams.noits
        self.burn = ipaparams.burn
        self.delta_add = ipaparams.delta_add
        self.delta_bio = ipaparams.delta_bio
        self.mode = ipaparams.mode
        self.CSunk = ipaparams.CSunk
        self.ncores = ipaparams.ncores

        self.isodiff = ipaparams.isodiff
        self.ppmiso = ipaparams.ppmiso
        self.me = ipaparams.me
        self.ratiosd = ipaparams.ratiosd
        self.ppmunk = ipaparams.ppmunk
        self.ratiounk = ipaparams.ratiounk
        self.ppmthr = ipaparams.ppmthr
        self.pRTNone = ipaparams.pRTNone
        self.pRTout = ipaparams.pRTout
        self.mzdCS = ipaparams.mzdCS 
        self.ppmCS = ipaparams.ppmCS
        self.evfilt = ipaparams.evfilt
        self.connections = ipaparams.connections

        self.submit = False
        # self.validate_prior_details = tk.StringVar()
        # self.validate_notes_details = tk.StringVar()
        super().__init__(parent, title, width=700, height=500, take_focus=True, extendable=False)

    def handle_error(self, error_message, error_details):
        lg.log_error(f'{error_message}: {error_details}')
        mb.showerror("Error", error_message)

    def body(self, frame: tk.Frame):

        #Set up tabs.

        self.tabs_ipaparams = ttk.Notebook(frame)
        self.tab_ipa = ttk.Frame(self.tabs_ipaparams)
        self.tab_additional = ttk.Frame(self.tabs_ipaparams)
        self.tab_optional = ttk.Frame(self.tabs_ipaparams)
        self.tab_connections = ttk.Frame(self.tabs_ipaparams)

        self.tabs_ipaparams.add(self.tab_ipa, text = "IPA")
        self.tabs_ipaparams.add(self.tab_additional, text = "Additional")
        self.tabs_ipaparams.add(self.tab_optional, text = "Optional")
        self.tabs_ipaparams.add(self.tab_connections, text = "Connections")
        self.tabs_ipaparams.pack(expand = 1, fill = "both")

        # IPA params

        self.ion_optionSV = tk.StringVar(value=self.ionisation)
        self.ppmSV = tk.StringVar(value=self.ppm)
        self.noitsSV = tk.StringVar(value=self.noits)
        self.burnSV = tk.StringVar(value=self.burn)
        self.deltaaddSV = tk.StringVar(value=self.delta_add)
        self.deltabioSV = tk.StringVar(value=self.delta_bio)
        self.mode_optionSV = tk.StringVar(value=self.mode)
        self.csunkSV = tk.StringVar(value=self.CSunk)
        self.ncoresSV = tk.StringVar(value=self.ncores)

        # Register validation methods
        # validate_ppm = frame.register(self.confirm_ppm_valid)
        # validate_prior = frame.register(self.confirm_prior_valid)

        self.lbl_ionisation = tk.Label(self.tab_ipa, width=40, text="Ionisation:")
        self.lbl_ionisation.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_ion_neg_one = tk.Radiobutton(self.tab_ipa, width=2, text = "-1", variable=self.ion_optionSV, value="-1")
        self.rad_ion_one = tk.Radiobutton(self.tab_ipa, width=2, text = "1", variable=self.ion_optionSV, value="1")
        self.rad_ion_neg_one.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_ion_one.grid(row=0, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppm = tk.Label(self.tab_ipa, width=40, text="MS Accuracy (ppm):")
        self.lbl_ppm.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppm = tk.Spinbox(self.tab_ipa, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmSV)
        self.spbx_ppm.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_noits = tk.Label(self.tab_ipa, width=40, text="Gibbs Sampler iterations:")
        self.lbl_noits.grid(row=2, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_noits = tk.Spinbox(self.tab_ipa, width=5, from_=1, to=1000000, state='readonly', textvariable=self.noitsSV)
        self.spbx_noits.grid(row=2, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_burn = tk.Label(self.tab_ipa, width=40, text="Iterations to ignore when computing posterior:")
        self.lbl_burn.grid(row=3, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_burn = tk.Spinbox(self.tab_ipa, width=5, from_=1, to=1000000, state='readonly', textvariable=self.burnSV)
        self.spbx_burn.grid(row=3, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_delta_add = tk.Label(self.tab_ipa, width=40, text="Adducts weight when computing priors:")
        self.lbl_delta_add.grid(row=4, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_delta_add = tk.Spinbox(self.tab_ipa, width=5, from_=1, to=1000000, state='readonly', textvariable=self.deltaaddSV)
        self.spbx_delta_add.grid(row=4, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_delta_bio = tk.Label(self.tab_ipa, width=40, text="Bio matrix weight when computing priors:")
        self.lbl_delta_bio.grid(row=5, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_delta_bio = tk.Spinbox(self.tab_ipa, width=5, from_=1, to=1000000, state='readonly', textvariable=self.deltabioSV)
        self.spbx_delta_bio.grid(row=5, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_mode = tk.Label(self.tab_ipa, width=40, text="Mode:")
        self.lbl_mode.grid(row=6, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_reactions = tk.Radiobutton(self.tab_ipa, width=10, text = "reactions", variable=self.mode_optionSV, value="reactions")
        self.rad_connections = tk.Radiobutton(self.tab_ipa, width=10, text = "connections", variable=self.mode_optionSV, value="connections")
        self.rad_reactions.grid(row=6, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_connections.grid(row=6, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_CSunk = tk.Label(self.tab_ipa, width=40, text="Cosine similarity score for 'Unknown':")
        self.lbl_CSunk.grid(row=7, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_CSunk = tk.Spinbox(self.tab_ipa, width=5, from_=0, to=1000000, state='readonly', textvariable=self.csunkSV, increment=.01)
        self.spbx_CSunk.grid(row=7, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ncores = tk.Label(self.tab_ipa, width=40, text="Number of cores:")
        self.lbl_ncores.grid(row=8, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ncores = tk.Spinbox(self.tab_ipa, width=5, from_=1, to=1000000, state='readonly', textvariable=self.ncoresSV)
        self.spbx_ncores.grid(row=8, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        # Additional1 params

        self.isodiffSV = tk.StringVar(value=self.isodiff)
        self.ppmisoSV = tk.StringVar(value=self.ppmiso)
        self.meSV = tk.StringVar(value=self.me)
        self.ratiosdSV = tk.StringVar(value=self.ratiosd)
        self.mzdCSSV = tk.StringVar(value=self.mzdCS)
        self.ppmCSSV = tk.StringVar(value=self.ppmCS)
        self.evfilt_optionSV = tk.StringVar(value=self.evfilt)

        self.lbl_isodiff = tk.Label(self.tab_additional, width=40, text="Differences between isotopes of charge 1:")
        self.lbl_isodiff.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_isodiff = tk.Spinbox(self.tab_additional, width=5, from_=0, to=1000000, state='readonly', textvariable=self.isodiffSV)
        self.spbx_isodiff.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppmiso = tk.Label(self.tab_additional, width=40, text="Max ppm between two isotopes:")
        self.lbl_ppmiso.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmiso = tk.Spinbox(self.tab_additional, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmisoSV)
        self.spbx_ppmiso.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_me = tk.Label(self.tab_additional, width=40, text="Mass of electron:")
        self.lbl_me.grid(row=2, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.ent_me = tk.Entry(self.tab_additional, width=10, textvariable=self.meSV)
        #self.ent_me.insert('end', self.me)
        self.ent_me.grid(row=2, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ratiosd = tk.Label(self.tab_additional, width=40, text= "Isotope predicted/observed intensity ratio:")
        self.lbl_ratiosd.grid(row=3, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ratiosd = tk.Spinbox(self.tab_additional, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ratiosdSV, increment=.1)
        self.spbx_ratiosd.grid(row=3, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_mzdCS = tk.Label(self.tab_additional, width=40, text="Cosine similarity score max m/z diff:")
        self.lbl_mzdCS.grid(row=4, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_mzdCS = tk.Spinbox(self.tab_additional, width=5, from_=0, to=1000000, state='readonly', textvariable=self.mzdCSSV, increment=.1)
        self.spbx_mzdCS.grid(row=4, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppmCS = tk.Label(self.tab_additional, width=40, text="Cosine similarity score max ppm:")
        self.lbl_ppmCS.grid(row=5, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmCS = tk.Spinbox(self.tab_additional, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmCSSV, increment=.1)
        self.spbx_ppmCS.grid(row=5, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_evfilt = tk.Label(self.tab_additional, width=40, text="Only spectra acquired with the same collision energy:")
        self.lbl_evfilt.grid(row=6, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_evfilt_true = tk.Radiobutton(self.tab_additional, width=10, text = "True", variable=self.evfilt_optionSV, value=True)
        self.rad_evfilt_false = tk.Radiobutton(self.tab_additional, width=10, text = "False", variable=self.evfilt_optionSV, value=False)
        self.rad_evfilt_true.grid(row=6, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_evfilt_false.grid(row=6, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        # Optional params
        self.ppmunkSV = tk.StringVar(value=self.ppmunk)
        self.ratiounkSV = tk.StringVar(value=self.ratiounk)
        self.ppmthrSV = tk.StringVar(value=self.ppmthr)
        self.pRTNoneSV = tk.StringVar(value=self.pRTNone)
        self.pRToutSV = tk.StringVar(value=self.pRTout)

        self.incl_ppmunk = tk.IntVar()
        self.incl_ratiounk = tk.IntVar()
        self.incl_ppmthr = tk.IntVar()
        self.incl_pRTNone = tk.IntVar()
        self.incl_pRTout = tk.IntVar()
        
        self.lbl_incl = tk.Label(self.tab_optional, width=5, text="Incl.")
        self.lbl_incl.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.chx_ppmunk = ttk.Checkbutton(self.tab_optional, command=self.chx_ppmunk_onchange, variable=self.incl_ppmunk)
        self.chx_ppmunk.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.lbl_ppmunk = tk.Label(self.tab_optional, width=40, text="'Unknown' annotation ppm:")
        self.lbl_ppmunk.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmunk = tk.Spinbox(self.tab_optional, width=5, from_=0, to=1000000, state=tk.DISABLED, textvariable=self.ppmunkSV, increment=.1)
        self.spbx_ppmunk.grid(row=1, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.chx_ratiounk = ttk.Checkbutton(self.tab_optional, command=self.chx_ratiounk_onchange, variable=self.incl_ratiounk)
        self.chx_ratiounk.grid(row=2, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.lbl_ratiounk = tk.Label(self.tab_optional, width=40, text="'Unknown' annotation Isotope ratio:")
        self.lbl_ratiounk.grid(row=2, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ratiounk = tk.Spinbox(self.tab_optional, width=5, from_=0, to=1000000, state=tk.DISABLED, textvariable=self.ratiounkSV, increment=.1)
        self.spbx_ratiounk.grid(row=2, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.chx_ppmthr = ttk.Checkbutton(self.tab_optional, command=self.chx_ppmthr_onchange, variable=self.incl_ppmthr)
        self.chx_ppmthr.grid(row=3, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.lbl_ppmthr = tk.Label(self.tab_optional, width=40, text="Maximum ppm possible for the annotations:")
        self.lbl_ppmthr.grid(row=3, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmthr = tk.Spinbox(self.tab_optional, width=5, from_=0, to=1000000, state=tk.DISABLED, textvariable=self.ppmthrSV, increment=.1)
        self.spbx_ppmthr.grid(row=3, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.chx_pRTNone = ttk.Checkbutton(self.tab_optional, command=self.chx_pRTNone_onchange, variable=self.incl_pRTNone)
        self.chx_pRTNone.grid(row=4, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.lbl_pRTNone = tk.Label(self.tab_optional, width=40, text="RT multiplicative factor if no RTrange present:")
        self.lbl_pRTNone.grid(row=4, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_pRTNone = tk.Spinbox(self.tab_optional, width=5, from_=0, to=1000000, state=tk.DISABLED, textvariable=self.pRTNoneSV, increment=.1)
        self.spbx_pRTNone.grid(row=4, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.chx_pRTout = ttk.Checkbutton(self.tab_optional, command=self.chx_pRTout_onchange, variable=self.incl_pRTout)
        self.chx_pRTout.grid(row=5, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.lbl_pRTout = tk.Label(self.tab_optional, width=40, text="RT multiplicative factor if outside RTrange:")
        self.lbl_pRTout.grid(row=5, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_pRTout = tk.Spinbox(self.tab_optional, width=5, from_=0, to=1000000, state=tk.DISABLED, textvariable=self.pRToutSV, increment=.1)
        self.spbx_pRTout.grid(row=5, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        #Connections params
        self.connectionnewSV = tk.StringVar()
        self.connections_items = tk.Variable(value=self.connections)

        self.lbl_connections = tk.Label(self.tab_connections, width=20, text="Connections:")
        self.lbl_connections.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbx_connections = tk.Listbox(self.tab_connections, listvariable=self.connections_items, width=20)
        self.lbx_connections.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.btn_remove = tk.Button(self.tab_connections, text='Remove', width=5, command=self.remove_btn_clicked)
        self.btn_remove.grid(row=0, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.ent_connectionnew = tk.Entry(self.tab_connections, width=20, textvariable=self.connectionnewSV)
        #self.ent_connectionnew.insert('end', self.connectionnew)
        self.ent_connectionnew.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.btn_addnew = tk.Button(self.tab_connections, text='Add New', width=5, command=self.addnew_btn_clicked)
        self.btn_addnew.grid(row=1, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='Run', width=5, command=self.run_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_export = tk.Button(self, text='Export parameters', width=12, command=self.export_btn_clicked)
        self.btn_export.pack(side="left", padx=(5,10), pady=(5,10))
        self.btn_import = tk.Button(self, text='Import parameters', width=12, command=self.import_btn_clicked)
        self.btn_import.pack(side="left", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.run_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def export_btn_clicked(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".json")
            if filepath:
                with open(filepath, "w") as output_params:  
                    output_params.write(json.dumps(self.export_params_file()))

        except IOError as ioerr:
            self.handle_error("Unable to save .json file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to save .json file.", err)


    def import_btn_clicked(self):
        try:
            filepath = fd.askopenfilename()
            if filepath:
                if os.path.exists(filepath):
                    with open(filepath) as params_json:
                        self.import_params_file(json.load(params_json))

        except IOError as ioerr:
            self.handle_error("Unable to open .json file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open .json file.", err)


    def import_params_file(self, annotation_params):

        self.ion_optionSV.set(annotation_params["ionisation"])
        self.ppmSV.set(annotation_params["ppm"])
        self.noitsSV.set(annotation_params["noits"])
        self.burnSV.set(annotation_params["burn"])
        self.deltaaddSV.set(annotation_params["delta_add"])
        self.deltabioSV.set(annotation_params["delta_bio"])
        self.mode_optionSV.set(annotation_params["mode"])
        self.csunkSV.set(annotation_params["CSunk"])
        self.ncoresSV.set(annotation_params["ncores"])
        self.isodiffSV.set(annotation_params["isodiff"])
        self.ppmisoSV.set(annotation_params["ppmiso"])
        self.me = annotation_params["me"]
        self.ratiosdSV.set(annotation_params["ratiosd"])
        self.mzdCSSV.set(annotation_params["mzdCS"])
        self.ppmCSSV.set(annotation_params["ppmCS"])
        self.evfilt_optionSV.set(annotation_params["evfilt"])
        self.ppmunkSV.set(annotation_params["ppmunk"])
        self.ratiounkSV.set(annotation_params["ratiounk"])
        self.ppmthrSV.set(annotation_params["ppmthr"])
        self.pRTNoneSV.set(annotation_params["pRTNone"])
        self.pRToutSV.set(annotation_params["pRTout"])
        self.connections = annotation_params["connections"]

    def export_params_file(self):
        params = {}

        # IPA Params
        params["ionisation"] = self.ion_optionSV.get()
        params["ppm"] = self.ppmSV.get()
        params["noits"] = self.noitsSV.get()
        params["burn"] = self.burnSV.get()
        params["delta_add"] = self.deltaaddSV.get()
        params["delta_bio"] = self.deltabioSV.get()
        params["mode"] = self.mode_optionSV.get()
        params["CSunk"] = self.csunkSV.get()
        params["ncores"] = self.ncoresSV.get()
        params["isodiff"] = self.isodiffSV.get()
        params["ppmiso"] = self.ppmisoSV.get()
        params["me"] = self.me
        params["ratiosd"] = self.ratiosdSV.get()
        params["mzdCS"] = self.mzdCSSV.get()
        params["ppmCS"] = self.ppmCSSV.get()
        params["evfilt"] = self.evfilt_optionSV.get()
        params["ppmunk"] = self.ppmunkSV.get()
        params["ratiounk"] = self.ratiounkSV.get()
        params["ppmthr"] = self.ppmthrSV.get()
        params["pRTNone"] = self.pRTNoneSV.get()
        params["pRTout"] = self.pRToutSV.get()
        params["connections"] = self.connections

        return params



    def run_btn_clicked(self):

        # IPA Params

        self.ionisation = self.ion_optionSV.get()
        self.ppm = self.ppmSV.get()
        self.noits = self.noitsSV.get()
        self.burn = self.burnSV.get()
        self.delta_add = self.deltaaddSV.get()
        self.delta_bio = self.deltabioSV.get()
        self.mode = self.mode_optionSV.get()
        self.CSunk = self.csunkSV.get()
        self.ncores = self.ncoresSV.get()

        # Additional Params
        self.isodiff = self.isodiffSV.get()
        self.ppmiso = self.ppmisoSV.get()
        self.me = self.me
        self.ratiosd = self.ratiosdSV.get()
        self.mzdCS = self.mzdCSSV.get()
        self.ppmCS = self.ppmCSSV.get()
        self.evfilt = self.evfilt_optionSV.get()

        # Optional Params
        if self.incl_pRTout.get() == 1:
            self.ppmunk = self.ppmunkSV.get()
        else:
            self.ppmunk = None

        if self.incl_ratiounk.get() == 1:
            self.ratiounk = self.ratiounkSV.get()
        else:
            self.ratiounk = None

        if self.incl_ppmthr.get() == 1:
            self.ppmthr = self.ppmthrSV.get()
        else:
            self.ppmthr = None

        if self.incl_pRTNone.get() == 1:
            self.pRTNone = self.pRTNoneSV.get()
        else:
            self.pRTNone = None

        if self.incl_pRTout.get() == 1:
            self.pRTout = self.pRToutSV.get()
        else:
            self.pRTout = None

        # Connections
        self.connections = self.connections

        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    # def disable_save_during_entry(self, event):   
    #     self.btn_ok["state"] = "disabled"

    def addnew_btn_clicked(self):
        self.lbx_connections.insert('end',self.connectionnewSV.get())

    def remove_btn_clicked(self):
        for selection in self.lbx_connections.curselection():
            self.lbx_connections.delete(selection)

    def chx_ppmunk_onchange(self):
        if self.incl_ppmunk.get() == 0:
            self.spbx_ppmunk.config(state=tk.DISABLED)
        elif self.incl_ppmunk.get() == 1:
            self.spbx_ppmunk.config(state=tk.NORMAL)

    def chx_ratiounk_onchange(self):
        if self.incl_ratiounk.get() == 0:
            self.spbx_ratiounk.config(state=tk.DISABLED)
        elif self.incl_ratiounk.get() == 1:
            self.spbx_ratiounk.config(state=tk.NORMAL)

    def chx_ppmthr_onchange(self):
        if self.incl_ppmthr.get() == 0:
            self.spbx_ppmthr.config(state=tk.DISABLED)
        elif self.incl_ppmthr.get() == 1:
            self.spbx_ppmthr.config(state=tk.NORMAL)

    def chx_pRTNone_onchange(self):
        if self.incl_pRTNone.get() == 0:
            self.spbx_pRTNone.config(state=tk.DISABLED)
        elif self.incl_pRTNone.get() == 1:
            self.spbx_pRTNone.config(state=tk.NORMAL)

    def chx_pRTout_onchange(self):
        if self.incl_pRTout.get() == 0:
            self.spbx_pRTout.config(state=tk.DISABLED)
        elif self.incl_pRTout.get() == 1:
            self.spbx_pRTout.config(state=tk.NORMAL)