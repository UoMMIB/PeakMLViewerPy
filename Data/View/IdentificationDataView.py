import Utilities as u
import Logger as lg
import pandas as pd

from Data.View.BaseDataView import BaseDataView
from Data.View.IdentificationItem import IdentificationItem

class IdentificationDataView(BaseDataView):
    def __init__(self):
        super().__init__(['ID','Formula','PPM','Adduct','Name','Class','Description','Prior','Post','Smiles','InChi','Notes','IPA_id','IPA_name','IPA_formula','IPA_adduct','IPA_mz','IPA_charge','IPA_ppm','IPA_isotope_pattern_score','IPA_fragmentation_pattern_score','IPA_prior','IPA_post','IPA_post_Gibbs','IPA_post_chi_square_pval'])

    def load_data_for_selected_peak(self, peak, molecule_database):

        try:

            self.clear_datalist()


            iden_ids = []
            iden_ppms = []
            iden_adducts = []
            iden_priors = []
            iden_posts = []
            iden_IPA_id = []
            iden_IPA_name = []
            iden_IPA_formula = []
            iden_IPA_adduct = []
            iden_IPA_mz = []
            iden_IPA_charge = []
            iden_IPA_ppm = []
            iden_IPA_isotope_pattern_score = []
            iden_IPA_fragmentation_pattern_score = []
            iden_IPA_prior = []
            iden_IPA_post = []
            iden_IPA_post_Gibbs = []
            iden_IPA_post_chi_square_pval = []


            # Get peak identification of label 'identification', value is multiple ids
            iden_ann = peak.get_specific_annotation('identification')

            if iden_ann:
                print("iden_ann")
            else:
                print("no iden_ann")

            if iden_ann:

                # Get list of PPM values from annotation
                iden_ppm = peak.get_specific_annotation('ppm')
                if iden_ppm:
                    iden_ppms = iden_ppm.value.split(', ')

                # Get list of adduct values from annotation
                iden_adduct = peak.get_specific_annotation('adduct')
                if iden_adduct:
                    iden_adducts = iden_adduct.value.split(', ')

                # Get list of prior probability values from annotation
                iden_prior = peak.get_specific_annotation('prior')
                if iden_prior:
                    iden_priors = iden_prior.value.split(', ')

                # Get list of posterior probability values from annotation
                iden_post = peak.get_specific_annotation('post')
                if iden_post:
                    iden_posts = iden_post.value.split(', ')

                # Get list of notes values from annotation
                iden_notes = peak.get_specific_annotation('notes')
                if iden_notes:
                    iden_notes = iden_notes.value.split(', ')

                # Get list of IPA_id values from annotation
                iden_IPA_id = peak.get_specific_annotation('IPA_id')
                if iden_IPA_id:
                    iden_IPA_id = iden_IPA_id.value.split(', ')

                # Get list of IPA_name values from annotation
                iden_IPA_name = peak.get_specific_annotation('IPA_name')
                if iden_IPA_name:
                    iden_IPA_name = iden_IPA_name.value.split(', ')

                # Get list of IPA_formula values from annotation
                iden_IPA_formula = peak.get_specific_annotation('IPA_formula')
                if iden_IPA_formula:
                    iden_IPA_formula = iden_IPA_formula.value.split(', ')

                # Get list of IPA_adduct values from annotation
                iden_IPA_adduct = peak.get_specific_annotation('IPA_adduct')
                if iden_IPA_adduct:
                    iden_IPA_adduct = iden_IPA_adduct.value.split(', ')

                # Get list of IPA_mz values from annotation
                iden_IPA_mz = peak.get_specific_annotation('IPA_mz')
                if iden_IPA_mz:
                    iden_IPA_mz = iden_IPA_mz.value.split(', ')

                # Get list of IPA_charge values from annotation
                iden_IPA_charge = peak.get_specific_annotation('IPA_charge')
                if iden_IPA_charge:
                    iden_IPA_charge = iden_IPA_charge.value.split(', ')

                # Get list of IPA_ppm values from annotation
                iden_IPA_ppm = peak.get_specific_annotation('IPA_ppm')
                if iden_IPA_ppm:
                    iden_IPA_ppm = iden_IPA_ppm.value.split(', ')

                # Get list of IPA_isotope_pattern_score values from annotation
                iden_IPA_isotope_pattern_score = peak.get_specific_annotation('IPA_isotope_pattern_score')
                if iden_IPA_isotope_pattern_score:
                    iden_IPA_isotope_pattern_score = iden_IPA_isotope_pattern_score.value.split(', ')

                # Get list of IPA_fragmentation_pattern_score values from annotation
                iden_IPA_fragmentation_pattern_score = peak.get_specific_annotation('IPA_fragmentation_pattern_score')
                if iden_IPA_fragmentation_pattern_score:
                    iden_IPA_fragmentation_pattern_score = iden_IPA_fragmentation_pattern_score.value.split(', ')

                # Get list of IPA_prior values from annotation
                iden_IPA_prior = peak.get_specific_annotation('IPA_prior')
                if iden_IPA_prior:
                    iden_IPA_prior = iden_IPA_prior.value.split(', ')

                # Get list of IPA_post values from annotation
                iden_IPA_post = peak.get_specific_annotation('IPA_post')
                if iden_IPA_post:
                    iden_IPA_post = iden_IPA_post.value.split(', ')

                # Get list of IPA_post_Gibbs values from annotation
                iden_IPA_post_Gibbs = peak.get_specific_annotation('IPA_post_Gibbs')
                if iden_IPA_post_Gibbs:
                    iden_IPA_post_Gibbs = iden_IPA_post_Gibbs.value.split(', ')

                # Get list of IPA_post_chi_square_pval values from annotation
                iden_IPA_post_chi_square_pval = peak.get_specific_annotation('IPA_post_chi_square_pval')
                if iden_IPA_post_chi_square_pval:
                    iden_IPA_post_chi_square_pval = iden_IPA_post_chi_square_pval.value.split(', ')

                iden_ids = iden_ann.value.split(', ')
                iden_count = len(iden_ids)

                if iden_IPA_id:
                    if len(iden_IPA_id) > iden_count:
                        iden_count = len(iden_IPA_id)



                lg.log_progress(f'{iden_count} identities found.')

                for i in range(iden_count):
                    formula = ""
                    ppm = ""
                    adduct = ""
                    name = ""
                    class_desc = ""
                    description = ""
                    prior = ""
                    post = ""
                    smiles = ""
                    inchi = ""
                    notes = ""
                    IPA_id = ""
                    IPA_name = ""
                    IPA_formula = ""
                    IPA_adduct = ""
                    IPA_mz = ""
                    IPA_charge = ""
                    IPA_ppm = ""
                    IPA_isotope_pattern_score = ""
                    IPA_fragmentation_pattern_score = ""
                    IPA_prior = ""
                    IPA_post = ""
                    IPA_post_Gibbs = ""
                    IPA_post_chi_square_pval = ""


                    #id
                    if iden_ids and len(iden_ids) > 0:
                        if i < len(iden_ids):
                            id = iden_ids[i]
                        else:
                            id = ""

                    if iden_IPA_id and len(iden_IPA_id) > 0:
                        if i < len(iden_IPA_id):
                            IPA_id = iden_IPA_id[i]
                        else:
                            IPA_id = ""



                    if molecule_database.get(id,False):
                        molecule = molecule_database[id]
                    else:
                        molecule = None

                    if molecule_database.get(IPA_id,False):
                        IPA_mol = molecule_database[IPA_id]
                    else:
                        IPA_mol = None


                    # Populate details from molecule database.
                    if molecule is not None:
                        formula = molecule.formula
                        name = molecule.name
                        class_desc = molecule.class_description if molecule.class_description is not None else ""
                        description = molecule.description if molecule.description is not None else ""
                        smiles = molecule.smiles
                        inchi = molecule.inchi
                    else:
                        formula = ""
                        name = ""
                        class_desc = ""
                        description = ""
                        smiles = ""
                        inchi = ""

                    if IPA_mol is not None:
                        IPA_smiles = IPA_mol.smiles
                        IPA_inchi = IPA_mol.inchi
                    else:
                        IPA_smiles = ""
                        IPA_inchi = ""

                    if iden_ppms and len(iden_ppms) > 0:
                        if len(iden_ppms) == 1:
                            ppm = u.convert_float_to_sf(iden_ppms[0])
                        elif i < len(iden_ppms):
                            ppm = u.convert_float_to_sf(iden_ppms[i])

                    if iden_adducts and len(iden_adducts) > 0:
                        if len(iden_adducts) == 1:
                            adduct = iden_adducts[0]
                        elif i < len(iden_adducts):
                            adduct = iden_adducts[i]

                    if iden_priors and len(iden_priors) > 0:
                        if i < len(iden_priors):
                            prior = u.to_float(iden_priors[i])
                        else:
                            prior = ""

                    if iden_posts and len(iden_posts) > 0:
                        if i < len(iden_posts):
                            post = u.to_float(iden_posts[i])
                        else:
                            post = ""

                    if iden_notes and len(iden_notes) > 0:
                        if i < len(iden_notes):
                            notes = iden_notes[i]
                        else:
                            notes = ""

                    if iden_IPA_name and len(iden_IPA_name) > 0:
                        if i < len(iden_IPA_name):
                            IPA_name = iden_IPA_name[i]
                        else:
                            IPA_name = ""

                    if iden_IPA_formula and len(iden_IPA_formula) > 0:
                        if i < len(iden_IPA_formula):
                            IPA_formula = iden_IPA_formula[i]
                        else:
                            IPA_formula = ""

                    if iden_IPA_adduct and len(iden_IPA_adduct) > 0:
                        if i < len(iden_IPA_adduct):
                            IPA_adduct = iden_IPA_adduct[i]
                        else:
                            IPA_adduct = ""

                    if iden_IPA_mz and len(iden_IPA_mz) > 0:
                        if i < len(iden_IPA_mz):
                            IPA_mz = iden_IPA_mz[i]
                        else:
                            IPA_mz = ""

                    if iden_IPA_charge and len(iden_IPA_charge) > 0:
                        if i < len(iden_IPA_charge):
                            IPA_charge = iden_IPA_charge[i]
                        else:
                            IPA_charge = ""

                    if iden_IPA_ppm and len(iden_IPA_ppm) > 0:
                        if i < len(iden_IPA_ppm):
                            IPA_ppm = iden_IPA_ppm[i]
                        else:
                            IPA_ppm = ""

                    if iden_IPA_isotope_pattern_score and len(iden_IPA_isotope_pattern_score) > 0:
                        if i < len(iden_IPA_isotope_pattern_score):
                            IPA_isotope_pattern_score = iden_IPA_isotope_pattern_score[i]
                        else:
                            IPA_isotope_pattern_score = ""

                    if iden_IPA_fragmentation_pattern_score and len(iden_IPA_fragmentation_pattern_score) > 0:
                        if i < len(iden_IPA_fragmentation_pattern_score):
                            IPA_fragmentation_pattern_score = iden_IPA_fragmentation_pattern_score[i]
                        else:
                            IPA_fragmentation_pattern_score = ""

                    if iden_IPA_prior and len(iden_IPA_prior) > 0:
                        if i < len(iden_IPA_prior):
                            IPA_prior = iden_IPA_prior[i]
                        else:
                            IPA_prior = ""

                    if iden_IPA_post and len(iden_IPA_post) > 0:
                        if i < len(iden_IPA_post):
                            IPA_post = iden_IPA_post[i]
                        else:
                            IPA_post = ""

                    if iden_IPA_post_Gibbs and len(iden_IPA_post_Gibbs) > 0:
                        if i < len(iden_IPA_post_Gibbs):
                            IPA_post_Gibbs = iden_IPA_post_Gibbs[i]
                        else:
                            IPA_post_Gibbs = ""

                    if iden_IPA_post_chi_square_pval and len(iden_IPA_post_chi_square_pval) > 0:
                        if i < len(iden_IPA_post_chi_square_pval):
                            IPA_post_chi_square_pval = iden_IPA_post_chi_square_pval[i]
                        else:
                            IPA_post_chi_square_pval = ""

                    self.add_item(id, formula, ppm, adduct, name, class_desc, description, prior, post, smiles, inchi, notes, IPA_id, IPA_name, IPA_formula, IPA_adduct, IPA_mz, IPA_charge, IPA_ppm, IPA_isotope_pattern_score, IPA_fragmentation_pattern_score, IPA_prior, IPA_post, IPA_post_Gibbs, IPA_post_chi_square_pval, IPA_smiles, IPA_inchi)
            else:
                lg.log_progress(f'No "identification" annotation found.')

            self.sort_datalist_by_probabilities()
            # Reload dataframe after all added.
            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to load identification data from peakML object: {err}')


    def add_item(self, id: int, formula: str, ppm: float, adduct: str, name: str, class_desc: str, description: str, prior: float, post: float, smiles: str, inchi: str, notes: str, IPA_id: str, IPA_name: str, IPA_formula: str, IPA_adduct: str, IPA_mz: str, IPA_charge: str, IPA_ppm: str, IPA_isotope_pattern_score: str, IPA_fragmentation_pattern_score: str, IPA_prior: str, IPA_post: str, IPA_post_Gibbs: str, IPA_post_chi_square_pval: str, IPA_smiles: str, IPA_inchi: str):
        self.datalist.append(IdentificationItem(id, formula, ppm, adduct, name, class_desc, description, prior, post, smiles, inchi, notes, IPA_id, IPA_name, IPA_formula, IPA_adduct, IPA_mz, IPA_charge, IPA_ppm, IPA_isotope_pattern_score, IPA_fragmentation_pattern_score, IPA_prior, IPA_post, IPA_post_Gibbs, IPA_post_chi_square_pval, IPA_smiles, IPA_inchi))


    def sort_datalist_by_probabilities(self):
        if len(self.datalist) > 0:
            # If the identifications have posterior values then
            if self.datalist[0].post != "":

                self.datalist.sort(key=lambda x: x.prior, reverse=True)
                self.datalist.sort(key=lambda x: x.post, reverse=True)

    def refresh_dataframe(self):
        self.clear_dataframe()
        #print(len(self.datalist))

        if len(self.datalist) > 0:
            for item in self.datalist:
                dr = pd.DataFrame({
                                    "UID": item.uid,
                                    "ID": item.id,
                                    "Formula": item.formula,
                                    "PPM": item.ppm,
                                    "Adduct": item.adduct,
                                    "Name": item.name,
                                    "Class": item.class_desc,
                                    "Description": item.description,
                                    "Prior": round(item.prior,2) if item.prior is not None and item.prior != "" and item.prior != "None" else "",
                                    "Post": round(item.post,2) if item.post is not None and item.post != "" and item.post != "None" else "",
                                    "Smiles": item.smiles,
                                    "InChi": item.inchi,
                                    "Notes": item.notes,
                                    "IPA_id": item.IPA_id,
                                    "IPA_name": item.IPA_name,
                                    "IPA_formula": item.IPA_formula,
                                    "IPA_adduct": item.IPA_adduct,
                                    "IPA_mz": round(float(item.IPA_mz),3) if item.IPA_mz is not None and item.IPA_mz != "" and item.IPA_mz != "None" else "",
                                    "IPA_charge": item.IPA_charge,
                                    "IPA_ppm": round(float(item.IPA_ppm),3) if item.IPA_ppm is not None and item.IPA_ppm != "" and item.IPA_ppm != "None" else "",
                                    "IPA_isotope_pattern_score": round(float(item.IPA_isotope_pattern_score),5) if item.IPA_isotope_pattern_score is not None and item.IPA_isotope_pattern_score != "" and item.IPA_isotope_pattern_score != "None" else "",
                                    "IPA_fragmentation_pattern_score": round(float(item.IPA_fragmentation_pattern_score),5) if item.IPA_fragmentation_pattern_score is not None and item.IPA_fragmentation_pattern_score != "" and item.IPA_fragmentation_pattern_score != "None" else "",
                                    "IPA_prior": round(float(item.IPA_prior),3) if item.IPA_prior is not None and item.IPA_prior != "" and item.IPA_prior != "None" else "",
                                    "IPA_post": round(float(item.IPA_post),3) if item.IPA_post is not None and item.IPA_post != "" and item.IPA_post != "None" else "",
                                    "IPA_post_Gibbs": round(float(item.IPA_post_Gibbs),3) if item.IPA_post_Gibbs is not None and item.IPA_post_Gibbs != "" and item.IPA_post_Gibbs != "None" else "",
                                    "IPA_post_chi_square_pval": round(float(item.IPA_post_chi_square_pval),3) if item.IPA_post_chi_square_pval is not None and item.IPA_post_chi_square_pval != "" and item.IPA_post_chi_square_pval != "None" else "",
                                    "IPA_smiles": item.IPA_smiles,
                                    "IPA_inchi": item.IPA_inchi,
                                    "Selected": item.selected,
                                    "Checked": item.checked,
                                }, index=[0])
                self.dataframe = pd.concat([self.dataframe, dr], ignore_index=True)


            # If no items are selected,
            if len(self.dataframe.loc[self.dataframe["Selected"] == True]) == 0:
                # set the first one as selected.
                self.dataframe.at[0, 'Selected'] = True


    def get_details(self, uid: str):
        row = self.dataframe.loc[self.dataframe["UID"] == uid]
        return uid, row["ID"].values[0], row["Prior"].values[0], row["Notes"].values[0]

    def update_details(self, uid: str, prior: str, notes: str):

        if u.is_float(prior):
            prior_val = float(prior)
        else:
            prior_val = None

        prior_changed = False

        for item in self.datalist:
            if item.uid == uid:
                if prior_val != None:
                    if prior_val != round(item.prior,2):
                        prior_changed = True
                        item.prior = prior_val
                item.notes = notes

                break

        if prior_changed:
            self.recalculate_priors(uid)

        self.refresh_dataframe()

        return prior_changed


    def remove_checked(self, ipa_imported: bool, IPA: int):
        current_list = self.datalist
        amended_list = []

        for item in current_list:
            if item.checked == False:
                amended_list.append(item)
            else:
                if IPA == 0:
                    item.id = ""
                    item.formula = ""
                    item.ppm = ""
                    item.adduct = ""
                    item.name = ""
                    item.class_desc = ""
                    item.description = ""
                    item.prior = ""
                    item.post = ""
                    item.smiles = ""
                    item.inchi = ""
                    item.notes = ""
                else:
                    item.IPA_id = ""
                    item.IPA_name = ""
                    item.IPA_formula = ""
                    item.IPA_adduct = ""
                    item.IPA_mz = ""
                    item.IPA_charge = ""
                    item.IPA_ppm = ""
                    item.IPA_isotope_pattern_score = ""
                    item.IPA_fragmentation_pattern_score = ""
                    item.IPA_prior = ""
                    item.IPA_post = ""
                    item.IPA_post_Gibbs = ""
                    item.IPA_post_chi_square_pval = ""
                    item.IPA_smiles = ""
                    item.IPA_inchi = ""
                amended_list.append(item)

        self.datalist = amended_list

        if ipa_imported:
            self.recalculate_priors(None)

        self.refresh_dataframe()

        # Deletion after IPA import will update prior.
        return ipa_imported

    def check_if_any_checked(self):
        for item in self.datalist:
            if item.checked == True:
                return True

        return False

    def get_identification_annotations(self):

        ann_identification = ", ".join(self.dataframe["ID"].tolist())

        ann_ppm = str(self.dataframe.at[0,"PPM"])
        ann_adduct = str(self.dataframe.at[0,"Adduct"])

        ann_prior = ", ".join([str(x) for x in self.dataframe["Prior"].tolist()])
        ann_post = ", ".join([str(x) for x in self.dataframe["Post"].tolist()])

        ann_notes = ", ".join(self.dataframe["Notes"].tolist())

        return ann_identification, ann_ppm, ann_adduct, ann_prior, ann_post, ann_notes


    def recalculate_priors(self, updated_identification_uid: str):

        # Need to be able to handle the total being 0.
        updated_item_list = []
        curr_prior_total = 0
        empty_values = 0
        target = 1
        updated_value = 0

        for item in self.datalist:

            if item.uid == updated_identification_uid:
                updated_value = item.prior

            if item.prior is None:
                # Get number of identities without set prior probability
                empty_values += 1
            else:
                # Get total of all priors.
                curr_prior_total += (item.prior if item.prior is not None else 0)

        # If any identification without prior probability values set.
        if empty_values > 0:
            for item in self.datalist:
                updated_item = item

                if item.prior is None:
                    # Update all rows without value with missing prior probability percentage divided between them
                    updated_item.prior = (target - curr_prior_total)/empty_values

                updated_item_list.append(updated_item)

        elif updated_value is None:
            #If updated value is none then deletion has occured so all remaining rows can be used for calculation
            for item in self.datalist:
                updated_item = item

                # Apply adjustment to each prior value.
                updated_item.prior = (target/curr_prior_total)*updated_item.prior

                updated_item_list.append(updated_item)

        else:
            #Update target all other values are adjusting to to account for manually updated.
            target = 1-updated_value

            for item in self.datalist:
                updated_item = item

                # Apply adjustment to each prior value, aside from updated.
                if item.uid != updated_identification_uid:
                    updated_item.prior = (target/(curr_prior_total-updated_value))*updated_item.prior

                updated_item_list.append(updated_item)

        self.datalist = updated_item_list

        tot_prob = 0
        for item in self.datalist:
            lg.log_progress(f"{item.id} is {item.prior}")
            tot_prob += item.prior

        lg.log_progress(f"Total is {tot_prob}")

        # Check if all other prior values are blank
        # If so set the all to the remaining slices of the pie
        # If a value has been updated remove from the outstanding calculation.
        # It is possible that all values rather than the added are blank.
        # If an edited value sets it 0 it should be set to 0 probability.
