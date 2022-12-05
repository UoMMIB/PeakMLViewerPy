from ipaPy2 import ipa
import pandas as pd
import os
import pickle

import Logger as lg
from Data.PeakML.Annotation import Annotation
from Data.PeakML.Peak import Peak

from typing import Dict

def generate_ipa_input(peakml_peaks):
    try:
        df = pd.DataFrame(columns=["ids","rel.ids","mzs","RTs","Int"])
        lg.log_error("peakml_peaks")
        for peak in peakml_peaks:
            peak_id = int(peak.get_specific_annotation("id").value)
            peak_relation_id = int(peak.get_specific_annotation("relation.id").value)
            peak_mass = float(peak.mass)
            peak_retention_time = float(peak.retention_time)
            peak_intensity = float(peak.intensity)
            
            df = df.append({"ids": peak_id, "rel.ids": peak_relation_id, "mzs": peak_mass, "RTs": peak_retention_time, "Int": peak_intensity }, ignore_index=True)

        return df

    except Exception as err:
        lg.log_error(f'Error exporting entries file for IPA: {err}')

def update_peak_with_annotations(peakml_peaks: Dict[str, Peak], annot_dict: Dict[str, pd.DataFrame]):
    try:

#Index(['id', 'name', 'formula', 'adduct', 'm/z', 'charge', 'RT range', 'ppm',
#       'isotope pattern score', 'fragmentation pattern score', 'prior', 'post',
#       'post Gibbs', 'chi-square pval']

        for peak_key in peakml_peaks.keys():
            # lg.log_error(peak_key)
            peak = peakml_peaks[peak_key]
            id = peak.get_specific_annotation('id')
            # lg.log_error("Peak_Key")
            # lg.log_error(peak_key)
            # lg.log_error("peak_annotation_id")
            # lg.log_error(id.value)

            annot_entry = annot_dict.get(int(id.value))
 
            # lg.log_error("Annot_entry")
            # lg.log_error("Start " + id.value)

            # Check dataframe has rows
            if annot_entry is not None and not annot_entry.empty:

                iden_values = []
                adduct_values = []
                ppm_values = []
                isops_values = []
                fragps_values = []
                prior_values = []
                post_values = []
                postgibbs_values = []
                chisp_values = []

                name_values = []
                formula_values = []
                mz_values = []
                charge_values = []

                for i in range(annot_entry.shape[0]):
                    # lg.log_error("ID: " + id.value + " Row: " + str(i))

                    iden_value = annot_entry['id'][i]
                    # lg.log_error("iden: " + iden_value)
                    iden_values.append(iden_value)

                    if iden_value != "unknown":
                        name_value = annot_entry['name'][i]
                        if name_value:
                            # lg.log_error("name: " + name_value)
                            name_values.append(str(name_value))
                        else:
                            name_values.append("")

                        formula_value = annot_entry['formula'][i]
                        if formula_value:
                            # lg.log_error("formula_values: " + formula_values_value)
                            formula_values.append(str(formula_value))
                        else:
                            formula_values.append("")


                        adduct_value = annot_entry['adduct'][i]
                        if adduct_value:
                            # lg.log_error("adduct: " + adduct_value)
                            adduct_values.append(adduct_value)
                        else:
                            adduct_values.append("")

                        ppm_value = annot_entry['ppm'][i]
                        if ppm_value:
                            # lg.log_error("ppm: " + str(ppm_value))
                            ppm_values.append(str(ppm_value))
                        else:
                            ppm_values.append("")

                        mz_value = annot_entry['m/z'][i]
                        if mz_value:
                            # lg.log_error("ppm: " + str(ppm_value))
                            mz_values.append(str(mz_value))
                        else:
                            mz_values.append("")

                        charge_value = annot_entry['charge'][i]
                        if charge_value:
                            # lg.log_error("ppm: " + str(ppm_value))
                            charge_values.append(str(charge_value))
                        else:
                            charge_values.append("")

                    # lg.log_error("Isotope pattern score")
                    isops_value = annot_entry['isotope pattern score'][i]
                    # lg.log_error("Isotope pattern score: " + str(isops_value))
                    if isops_value:
                        # lg.log_error("Isotope pattern score: " + str(isops_value))
                        isops_values.append(str(isops_value))
                    else:
                        isops_values.append("")

                    fragps_value = annot_entry['fragmentation pattern score'][i]  
                    if fragps_value:
                        # lg.log_error("Fragmentation pattern score: " + str(fragps_value))
                        fragps_values.append(str(fragps_value))
                    else:
                        fragps_values.append("")
                    
                    prior_value = annot_entry['prior'][i]      
                    if prior_value:
                        # lg.log_error("Prior: " + str(prior_value))
                        prior_values.append(str(prior_value))
                    else:
                        prior_values.append("")

                    post_value = annot_entry['post'][i]
                    if post_value:
                        # lg.log_error("Post: " + str(post_value))
                        post_values.append(str(post_value))
                    else:
                        post_values.append("")

                    postgibbs_value = annot_entry['post Gibbs'][i]
                    if postgibbs_value:
                        # lg.log_error("Post Gibbs: " + str(postgibbs_value))
                        postgibbs_values.append(str(postgibbs_value))
                    else:
                        postgibbs_values.append("")

                    chisp_value = annot_entry['chi-square pval'][i]
                    if chisp_value:
                        # lg.log_error("chi-square pval: " + str(chisp_value))
                        chisp_values.append(str(chisp_value))
                    else:
                        chisp_values.append("")

                lg.log_error("Start update annotation")

                update_annotation(peak, 'identification', ", ".join(iden_values))
                # lg.log_error("identification")
                update_annotation(peak, 'adduct', ", ".join(adduct_values))
                # lg.log_error("adduct")
                update_annotation(peak, 'ppm', ", ".join(ppm_values))
                # lg.log_error("ppm")
                # update_annotation(peak, 'isotope pattern score', ", ".join(isops_values))
                # update_annotation(peak, 'fragmentation pattern score', ", ".join(fragps_values))
                update_annotation(peak, 'prior', ", ".join(prior_values))
                # lg.log_error("prior")
                update_annotation(peak, 'post', ", ".join(post_values))
                # lg.log_error("post")
                # update_annotation(peak, 'post Gibbs', ", ".join(postgibbs_values))
                # update_annotation(peak, 'chi-square pval', ", ".join(chisp_values))

                update_annotation(peak, 'IPA_id', ", ".join(iden_values))
                # lg.log_error("IPA_id")
                update_annotation(peak, 'IPA_name', ", ".join(name_values))
                # lg.log_error("IPA_name")
                update_annotation(peak, 'IPA_formula', ", ".join(formula_values))
                # lg.log_error("IPA_formula")
                update_annotation(peak, 'IPA_adduct', ", ".join(adduct_values))
                # lg.log_error("IPA_adduct")
                update_annotation(peak, 'IPA_mz', ", ".join(mz_values))
                # lg.log_error("IPA_mz")
                update_annotation(peak, 'IPA_charge', ", ".join(charge_values))
                # lg.log_error("IPA_charge")
                update_annotation(peak, 'IPA_ppm', ", ".join(ppm_values))
                # lg.log_error("IPA_ppm")
                update_annotation(peak, 'IPA_isotope_pattern_score', ", ".join(isops_values))
                # lg.log_error("IPA_isotope_pattern_score")
                update_annotation(peak, 'IPA_fragmentation_pattern_score', ", ".join(fragps_values))
                # lg.log_error("IPA_fragmentation_pattern_score")
                update_annotation(peak, 'IPA_prior', ", ".join(prior_values))
                # lg.log_error("IPA_prior")
                update_annotation(peak, 'IPA_post', ", ".join(post_values))
                # lg.log_error("IPA_post")
                update_annotation(peak, 'IPA_post_Gibbs', ", ".join(postgibbs_values))
                # lg.log_error("IPA_post_Gibbs")
                update_annotation(peak, 'IPA_post_chi_square_pval', ", ".join(chisp_values))
                # lg.log_error("IPA_post_chi_square_pval")
                # lg.log_error("End update annotation")

    except Exception as err:
        lg.log_error(f'Error importing IPA file: {err}')

def update_annotation(parent, ann_label, ann_value):
    # lg.log_error("UA:" + ann_label + " " + ann_value)
    if parent.get_specific_annotation(ann_label):
        parent.update_specific_annotation(ann_label, ann_value)  
    else:
        parent.add_annotation(Annotation("", "", ann_label, ann_value, "STRING"))

def generate_ipa_annotation(peakml_peaks):

    #anno = pd.read_pickle('ipa_annotations.pickle')

    # Ionisation (Positive = 1, Negative = -1)
    ionisation_val = 1

    peakml_df = generate_ipa_input(list(peakml_peaks.values()))
    #lg.log_error(peakml_df.head())

    anno = run_ipa_simple(peakml_df)

    #lg.log_error(anno[1].columns)
    update_peak_with_annotations(peakml_peaks, anno)

# Uses MS1 and MS2, does not use Gibbs sampler
def run_whole_scenario_one(peakml_df, ms1_db, adducts_db, ms2_db, ms2_df):  
    annotations = ipa.simpleIPA( peakml_df,
                                 ionisation = 1, 
                                 DB = ms1_db,
                                 adductsAll = adducts_db,
                                 ppm = 3,
                                 dfMS2 = ms2_df,
                                 DBMS2 = ms2_db,
                                 noits = 5000,
                                 delta_add = 0.1)
    return annotations

# Use only MS1, considers adduct connections in the Gibbs sampler
def run_whole_scenario_two(peakml_df, ms1_db, adducts_db):  
    annotations = ipa.simpleIPA( peakml_df,
                                 ionisation = 1, 
                                 DB = ms1_db,
                                 adductsAll = adducts_db,
                                 ppm = 3,
                                 noits = 5000,
                                 delta_add = 0.1)
    return annotations

# Uses MS1 and MS2, considers both adducts and biochemical connections in the Gibbs sampler.
def run_whole_scenario_three(peakml_df, ms1_db, adducts_db, allbioreactions_db):  
    annotations= ipa.simpleIPA( peakml_df, 
                                ionisation=1, 
                                DB = ms1_db,
                                adductsAll = adducts_db,
                                ppm = 3,
                                dfMS2 = dfMS2,
                                DBMS2 = DBMS2,
                                noits = 5000,
                                Bio = allbioreactions_db,
                                delta_add = 0.1, 
                                delta_bio = 0.4)
    return annotations


def run_ipa_simple(peakml_df):
    ms1_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","IPA_MS1.csv"))
    adducts_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","adducts.csv"))
    allbioreactions_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","allBIO_reactions.csv"))

    annotations = ipa.simpleIPA(df=peakml_df,
                                ionisation=1,
                                DB=ms1_db,
                                adductsAll=adducts_db,
                                ppm=3,
                                ppmthr=5,
                                Bio=allbioreactions_db,
                                delta_add=0.1,
                                delta_bio=0.1,
                                burn=1000,
                                noits=5000,
                                ncores=70)

    return annotations
#     df=peakml_df,
#                                 ionisation=1,
#                                 DB=ms1_db,
#                                 adductsAll=adducts_db,
#                                 ppm=3,
#                                 ppmthr=5,
#                                 Bio=allbioreactions_db,
#                                 delta_add=0.1,
#                                 delta_bio=0.1,
#                                 burn=1000,
#                                 noits=5000,
#                                 ncores=70)

#    run_ipa()

#def run_ipa(peakml_df: pd.DataFrame ):

#     ms1_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","IPA_MS1.csv"))
#     adducts_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","adducts.csv"))
#     allbioreactions_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","allBIO_reactions.csv"))


#             (df,
#             ionisation,
#             DB,
#             adductsAll,
#             ppm,
#             dfMS2 = None,
#             DBMS2 = None,
#             noits = 100,
#             burn = None,
#             delta_add=None,
#             delta_bio=None,
#             Bio=None,
#             mode='reactions',
#             CSunk=0.5,
#             isodiff=1,
#             ppmiso=100,
#             ncores=1,
#             me=5.48579909065e-04,
#             ratiosd=0.9,
#             ppmunk=None,
#             ratiounk=None,
#             ppmthr=None,
#             pRTNone=None,
#             pRTout=None,
#             mzdCS=0, 
#             ppmCS=10,
#             evfilt=False,
#             connections = ["C3H5NO", "C6H12N4O", "C4H6N2O2", "C4H5NO3",
#                              "C3H5NOS", "C6H10N2O3S2","C5H7NO3","C5H8N2O2",
#                              "C2H3NO","C6H7N3O","C6H11NO","C6H11NO","C6H12N2O",
#                              "C5H9NOS","C9H9NO","C5H7NO","C3H5NO2","C4H7NO2",
#                              "C11H10N2O","C9H9NO2","C5H9NO","C4H4O2","C3H5O",
#                              "C10H12N5O6P","C10H15N2O3S","C10H14N2O2S","CH2ON",
#                              "C21H34N7O16P3S","C21H33N7O15P3S","C10H15N3O5S",
#                              "C5H7","C3H2O3","C16H30O","C8H8NO5P","CH3N2O",
#                              "C5H4N5","C10H11N5O3","C10H13N5O9P2",
#                              "C10H12N5O6P","C9H13N3O10P2","C9H12N3O7P",
#                              "C4H4N3O","C10H13N5O10P2","C10H12N5O7P","C5H4N5O",
#                              "C10H11N5O4","C10H14N2O10P2","C10H12N2O4",
#                              "C5H5N2O2","C10H13N2O7P","C9H12N2O11P2",
#                              "C9H11N2O8P","C4H3N2O2","C9H10N2O5","C2H3O2",
#                              "C2H2O","C2H2","CO2","CHO2","H2O","H3O6P2","C2H4",
#                              "CO","C2O2","H2","O","P","C2H2O","CH2","HPO3",
#                              "NH2","PP","NH","SO3","N","C6H10O5",
#                "C6H10O6","C5H8O4","C12H20O11","C6H11O8P","C6H8O6","C6H10O5",
#                "C18H30O15"]):

#     # Mapping isotope patterns (Output: relationship, isotope pattern, charge)
#     #isotope_patterns = ipa.map_isotope_patterns(peakml_df, ionisation_val)

#     # mapping isotopes
#     ipa.map_isotope_patterns(peakml_df, 
#                             isoDiff = isodiff_val, 
#                             ppm = ppmiso_val, 
#                             ionisation = ionisation_val)
    
#     # computing all adducts
#     allAdds = ipa.compute_all_adducts(adductsAll = adducts_db, 
#                                         DB = DB, 
#                                         ionisation = ionisation_val,
#                                         ncores = ncores_val)
     


#     # computing priors
#     if (dfMS2 is None) or (DBMS2 is None):
#         annotations = ipa.MS1annotation(df = peakml_df,
#                                         allAdds = allAdds,
#                                         ppm = ppm,
#                                         me = me,
#                                         ratiosd = ratiosd,
#                                         ppmunk = ppmunk,
#                                         ratiounk = ratiounk,
#                                         ppmthr = ppmthr,
#                                         pRTNone = pRTNone,
#                                         pRTout = pRTout,
#                                         ncores = ncores)
#     else:
    
#         annotations = MSMSannotation(df=peakml_df,dfMS2=dfMS2,allAdds=allAdds,DBMS2=DBMS2,ppm=ppm,me=me,ratiosd=ratiosd,
#         ppmunk=ppmunk,ratiounk=ratiounk,ppmthr=ppmthr,pRTNone=pRTNone,pRTout=pRTout,mzdCS=mzdCS,ppmCS=ppmCS,
#         CSunk=CSunk,evfilt=evfilt,ncores=ncores)

#     # computing Bio matrix (if necessary)
#     if (Bio is None) and (delta_bio is not None):
#         Bio=Compute_Bio(DB=DB,annotations=annotations,mode=mode,connections=connections,ncores=ncores)
        
    # Computing posterior probabilities integrating biochemical connections

#     # Gibbs sampler (if needed). Which one based on the inputs
#     if (Bio is not None) and (delta_bio is not None) and (delta_add is not None):
#         Gibbs_sampler_bio_add(df=peakml_df,annotations=annotations,Bio=Bio,noits=noits,burn=burn,delta_bio=delta_bio,delta_add=delta_add)
#     elif (Bio is not None) and (delta_bio is not None) and (delta_add is None):
#         Gibbs_sampler_bio(df=peakml_df,annotations=annotations,Bio=Bio,noits=noits,burn=burn,delta_bio=delta_bio)
#     elif (Bio is None) and (delta_bio is None) and (delta_add is not None):
#         Gibbs_sampler_add(df=peakml_df,annotations=annotations,noits=noits,burn=burn,delta_add=delta_add)