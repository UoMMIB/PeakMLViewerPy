import tkinter as tk
import tkinter.ttk as ttk
from UI.ViewerDialog import ViewerDialog

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
    
    def body(self, frame: tk.Frame):

        #Set up tabs.

        self.tabs_ipaparams = ttk.Notebook(frame)
        self.tab_ipa = ttk.Frame(self.tabs_ipaparams)
        self.tab_additional1 = ttk.Frame(self.tabs_ipaparams)
        self.tab_additional2 = ttk.Frame(self.tabs_ipaparams)
        self.tab_connections = ttk.Frame(self.tabs_ipaparams)

        self.tabs_ipaparams.add(self.tab_ipa, text = "IPA")
        self.tabs_ipaparams.add(self.tab_additional1, text = "Additional 1")
        self.tabs_ipaparams.add(self.tab_additional2, text = "Additional 2")
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
        self.rad_ion_neg_one = tk.Radiobutton(self.tab_ipa, width=2, text = "-1", variable=self.ion_optionSV, value=1)
        self.rad_ion_one = tk.Radiobutton(self.tab_ipa, width=2, text = "1", variable=self.ion_optionSV, value=2)
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
        self.spbx_burn = tk.Spinbox(self.tab_ipa, width=5, from_=0, to=1000000, state='readonly', textvariable=self.burnSV)
        self.spbx_burn.grid(row=3, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_delta_add = tk.Label(self.tab_ipa, width=40, text="Adducts weight when computing priors:")
        self.lbl_delta_add.grid(row=4, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_delta_add = tk.Spinbox(self.tab_ipa, width=5, from_=1, to=1000000, state='readonly', textvariable=self.deltaaddSV)
        self.spbx_delta_add.grid(row=4, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_delta_bio = tk.Label(self.tab_ipa, width=40, text="Bio matrix weight when computing priors:")
        self.lbl_delta_bio.grid(row=5, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_delta_bio = tk.Spinbox(self.tab_ipa, width=5, from_=0, to=1000000, state='readonly', textvariable=self.deltabioSV)
        self.spbx_delta_bio.grid(row=5, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_mode = tk.Label(self.tab_ipa, width=40, text="Mode:")
        self.lbl_mode.grid(row=6, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_reactions = tk.Radiobutton(self.tab_ipa, width=10, text = "reactions", variable=self.mode_optionSV, value=1)
        self.rad_connections = tk.Radiobutton(self.tab_ipa, width=10, text = "connections", variable=self.mode_optionSV, value=2)
        self.rad_reactions.grid(row=6, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_connections.grid(row=6, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_CSunk = tk.Label(self.tab_ipa, width=40, text="Cosine similarity score for 'Unknown':")
        self.lbl_CSunk.grid(row=7, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_CSunk = tk.Spinbox(self.tab_ipa, width=5, from_=0, to=1000000, state='readonly', textvariable=self.csunkSV, increment=.01)
        self.spbx_CSunk.grid(row=7, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ncores = tk.Label(self.tab_ipa, width=40, text="Number of cores:")
        self.lbl_ncores.grid(row=8, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ncores = tk.Spinbox(self.tab_ipa, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ncoresSV)
        self.spbx_ncores.grid(row=8, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        # Additional1 params

        self.isodiffSV = tk.StringVar(value=self.isodiff)
        self.ppmisoSV = tk.StringVar(value=self.ppmiso)
        # self.meSV = tk.StringVar(value=self.me)
        self.ratiosdSV = tk.StringVar(value=self.ratiosd)
        self.ppmunkSV = tk.StringVar(value=self.ppmunk)
        self.ratiounkSV = tk.StringVar(value=self.ratiounk)
        self.ppmthrSV = tk.StringVar(value=self.ppmthr)

        self.lbl_isodiff = tk.Label(self.tab_additional1, width=40, text="Differences between isotopes of charge 1:")
        self.lbl_isodiff.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_isodiff = tk.Spinbox(self.tab_additional1, width=5, from_=0, to=1000000, state='readonly', textvariable=self.isodiffSV)
        self.spbx_isodiff.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppmiso = tk.Label(self.tab_additional1, width=40, text="Max ppm between two isotopes:")
        self.lbl_ppmiso.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmiso = tk.Spinbox(self.tab_additional1, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmisoSV)
        self.spbx_ppmiso.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_me = tk.Label(self.tab_additional1, width=40, text="Mass of electron:")
        self.lbl_me.grid(row=2, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.ent_me = tk.Entry(self.tab_additional1, width=10)
        self.ent_me.insert('end', self.me)
        self.ent_me.grid(row=2, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ratiosd = tk.Label(self.tab_additional1, width=40, text= "Isotope predicted/observed intensity ratio:")
        self.lbl_ratiosd.grid(row=3, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ratiosd = tk.Spinbox(self.tab_additional1, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ratiosdSV, increment=.1)
        self.spbx_ratiosd.grid(row=3, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppmunk = tk.Label(self.tab_additional1, width=40, text="'Unknown' annotation ppm:")
        self.lbl_ppmunk.grid(row=4, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmunk = tk.Spinbox(self.tab_additional1, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmunkSV, increment=.1)
        self.spbx_ppmunk.grid(row=4, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ratiounk = tk.Label(self.tab_additional1, width=40, text="'Unknown' annotation Isotope ratio:")
        self.lbl_ratiounk.grid(row=5, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ratiounk = tk.Spinbox(self.tab_additional1, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ratiounkSV, increment=.1)
        self.spbx_ratiounk.grid(row=5, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppmthr = tk.Label(self.tab_additional1, width=40, text="Maximum ppm possible for the annotations:")
        self.lbl_ppmthr.grid(row=6, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmthr = tk.Spinbox(self.tab_additional1, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmthrSV, increment=.1)
        self.spbx_ppmthr.grid(row=6, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        # Additional2 params

        self.pRTNoneSV = tk.StringVar(value=self.pRTNone)
        self.pRToutSV = tk.StringVar(value=self.pRTout)
        self.mzdCSSV = tk.StringVar(value=self.mzdCS)
        self.ppmCSSV = tk.StringVar(value=self.ppmCS)
        self.evfilt_optionSV = tk.StringVar(value=self.evfilt)

        self.lbl_pRTNone = tk.Label(self.tab_additional2, width=40, text="RT multiplicative factor if no RTrange present:")
        self.lbl_pRTNone.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_pRTNone = tk.Spinbox(self.tab_additional2, width=5, from_=0, to=1000000, state='readonly', textvariable=self.pRTNoneSV, increment=.1)
        self.spbx_pRTNone.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_pRTout = tk.Label(self.tab_additional2, width=40, text="RT multiplicative factor if outside RTrange:")
        self.lbl_pRTout.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_pRTout = tk.Spinbox(self.tab_additional2, width=5, from_=0, to=1000000, state='readonly', textvariable=self.pRToutSV, increment=.1)
        self.spbx_pRTout.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_mzdCS = tk.Label(self.tab_additional2, width=40, text="Cosine similarity score max m/z diff:")
        self.lbl_mzdCS.grid(row=2, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_mzdCS = tk.Spinbox(self.tab_additional2, width=5, from_=0, to=1000000, state='readonly', textvariable=self.mzdCSSV, increment=.1)
        self.spbx_mzdCS.grid(row=2, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_ppmCS = tk.Label(self.tab_additional2, width=40, text="Cosine similarity score max ppm:")
        self.lbl_ppmCS.grid(row=3, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_ppmCS = tk.Spinbox(self.tab_additional2, width=5, from_=0, to=1000000, state='readonly', textvariable=self.ppmCSSV, increment=.1)
        self.spbx_ppmCS.grid(row=3, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_evfilt = tk.Label(self.tab_additional2, width=40, text="Only spectra acquired with the same collision energy:")
        self.lbl_evfilt.grid(row=4, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_evfilt_true = tk.Radiobutton(self.tab_additional2, width=10, text = "True", variable=self.evfilt_optionSV, value=1)
        self.rad_evfilt_false = tk.Radiobutton(self.tab_additional2, width=10, text = "False", variable=self.evfilt_optionSV, value=2)
        self.rad_evfilt_true.grid(row=4, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.rad_evfilt_false.grid(row=4, column=2, padx=(2,2), pady=(5,5),sticky="NEWS")

        #Connections params

        # self.connectionsSV = tk.StringVar(value=self.connections)

        self.lbl_connections = tk.Label(self.tab_connections, width=40, text="Connections:")
        self.lbl_connections.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.ent_connections = tk.Entry(self.tab_connections, width=10)
        self.ent_connections.insert('end', self.connections)
        self.ent_connections.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='Run', width=5, command=self.run_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.run_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def run_btn_clicked(self):
        self.ionisation = self.ion_optionSV.get()
        self.ppm = self.ppmSV.get()
        self.noits = self.noitsSV.get()
        self.burn = self.burnSV.get()
        self.delta_add = self.deltaaddSV.get()
        self.delta_bio = self.deltabioSV.get()
        self.mode = self.mode_optionSV.get()
        self.CSunk = self.csunkSV.get()
        self.ncores = self.ncoresSV.get()

        self.isodiff = self.isodiffSV.get()
        self.ppmiso = self.ppmisoSV.get()
        self.me = self.me
        self.ratiosd = self.ratiosdSV.get()
        self.ppmunk = self.ppmunkSV.get()
        self.ratiounk = self.ratiounkSV.get()
        self.ppmthr = self.ppmthrSV.get()
        self.pRTNone = self.pRTNoneSV.get()
        self.pRTout = self.pRToutSV.get()
        self.mzdCS = self.mzdCSSV.get()
        self.ppmCS = self.ppmCSSV.get()
        self.evfilt = self.evfilt_optionSV.get()
        self.connections = self.connections

        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    # def disable_save_during_entry(self, event):   
    #     self.btn_ok["state"] = "disabled"
            