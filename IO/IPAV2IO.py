from ipaPy2 import ipa, util, iterations
import pandas as pd
import os

import Logger as lg
from Data.PeakML.Annotation import Annotation
from Data.IPAParams import IPAParams
from Data.PeakML.Peak import Peak

import time
import math
import multiprocessing
from functools import partial

from typing import Dict

def generate_ipa_input(peakml_peaks):
    try:
        df = pd.DataFrame(columns=["ids","rel.ids","mzs","RTs","Int"])
        for peak in peakml_peaks:
            peak_id = int(peak.get_specific_annotation("id").value)
            peak_relation_id = int(peak.get_specific_annotation("relation.id").value)
            peak_mass = float(peak.mass)
            peak_retention_time = float(peak.retention_time)
            peak_intensity = float(peak.intensity)

            dr = pd.DataFrame({"ids": peak_id, "rel.ids": peak_relation_id, "mzs": peak_mass, "RTs": peak_retention_time, "Int": peak_intensity }, index=[0])
            df = pd.concat([df, dr], ignore_index=True)

        return df

    except Exception as err:
        lg.log_error(f'Error exporting entries file for IPA: {err}')

def update_peak_with_annotations(peakml_peaks: Dict[str, Peak], annot_dict: Dict[str, pd.DataFrame]):
    try:

#Index(['id', 'name', 'formula', 'adduct', 'm/z', 'charge', 'RT range', 'ppm',
#       'isotope pattern score', 'fragmentation pattern score', 'prior', 'post',
#       'post Gibbs', 'chi-square pval']

        for peak_key in peakml_peaks.keys():
            lg.log_error(f"Update peak {peak_key}")
            peak = peakml_peaks[peak_key]
            id = peak.get_specific_annotation('id')

            annot_entry = annot_dict.get(int(id.value))
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

                    iden_value = annot_entry['id'][i]
                    iden_values.append(iden_value)

                    if iden_value != "unknown":
                        name_value = annot_entry['name'][i]
                        if name_value:
                            name_values.append(str(name_value))
                        else:
                            name_values.append("")

                        formula_value = annot_entry['formula'][i]
                        if formula_value:
                            formula_values.append(str(formula_value))
                        else:
                            formula_values.append("")


                        adduct_value = annot_entry['adduct'][i]
                        if adduct_value:
                            adduct_values.append(adduct_value)
                        else:
                            adduct_values.append("")

                        ppm_value = annot_entry['ppm'][i]
                        if ppm_value:
                            ppm_values.append(str(ppm_value))
                        else:
                            ppm_values.append("")

                        mz_value = annot_entry['m/z'][i]
                        if mz_value:
                            mz_values.append(str(mz_value))
                        else:
                            mz_values.append("")

                        charge_value = annot_entry['charge'][i]
                        if charge_value:
                            charge_values.append(str(charge_value))
                        else:
                            charge_values.append("")

                    isops_value = annot_entry['isotope pattern score'][i]
                    if isops_value:
                        isops_values.append(str(isops_value))
                    else:
                        isops_values.append("")

                    fragps_value = annot_entry['fragmentation pattern score'][i]  
                    if fragps_value:
                        fragps_values.append(str(fragps_value))
                    else:
                        fragps_values.append("")
                    
                    prior_value = annot_entry['prior'][i]      
                    if prior_value:
                        prior_values.append(str(prior_value))
                    else:
                        prior_values.append("")

                    post_value = annot_entry['post'][i]
                    if post_value:
                        post_values.append(str(post_value))
                    else:
                        post_values.append("")

                    postgibbs_value = annot_entry['post Gibbs'][i]
                    if postgibbs_value:
                        postgibbs_values.append(str(postgibbs_value))
                    else:
                        postgibbs_values.append("")

                    chisp_value = annot_entry['chi-square pval'][i]
                    if chisp_value:
                        chisp_values.append(str(chisp_value))
                    else:
                        chisp_values.append("")

                update_annotation(peak, 'identification', ", ".join(iden_values))
                update_annotation(peak, 'adduct', ", ".join(adduct_values))
                update_annotation(peak, 'ppm', ", ".join(ppm_values))
                update_annotation(peak, 'prior', ", ".join(prior_values))
                update_annotation(peak, 'post', ", ".join(post_values))
                update_annotation(peak, 'IPA_id', ", ".join(iden_values))
                update_annotation(peak, 'IPA_name', ", ".join(name_values))
                update_annotation(peak, 'IPA_formula', ", ".join(formula_values))
                update_annotation(peak, 'IPA_adduct', ", ".join(adduct_values))
                update_annotation(peak, 'IPA_mz', ", ".join(mz_values))
                update_annotation(peak, 'IPA_charge', ", ".join(charge_values))
                update_annotation(peak, 'IPA_ppm', ", ".join(ppm_values))
                update_annotation(peak, 'IPA_isotope_pattern_score', ", ".join(isops_values))
                update_annotation(peak, 'IPA_fragmentation_pattern_score', ", ".join(fragps_values))
                update_annotation(peak, 'IPA_prior', ", ".join(prior_values))
                update_annotation(peak, 'IPA_post', ", ".join(post_values))
                update_annotation(peak, 'IPA_post_Gibbs', ", ".join(postgibbs_values))
                update_annotation(peak, 'IPA_post_chi_square_pval', ", ".join(chisp_values))

    except Exception as err:
        lg.log_error(f'Error importing IPA file: {err}')

def update_annotation(parent, ann_label, ann_value):
    # lg.log_error("UA:" + ann_label + " " + ann_value)
    if parent.get_specific_annotation(ann_label):
        parent.update_specific_annotation(ann_label, ann_value)  
    else:
        parent.add_annotation(Annotation("", "", ann_label, ann_value, "STRING"))

def run_ipa(peakml_df: pd.DataFrame, params: IPAParams):
    ms1_db, adducts_db, allbioreactions_db, allbioreactions_db, ms2_db, dbms2_db = load_databases()

    peakml_df = cluster_features(peakml_df)
    map_isotope_patterns(peakml_df, params)
    computed_adducts = run_adducts(params, ms1_db, adducts_db)
    annotation_priors = run_priors(peakml_df, params, computed_adducts, ms2_db, dbms2_db)
    bio_matrix = run_bio_matrix(annotation_priors, params, ms1_db, allbioreactions_db)
    run_gibbs_sampler(peakml_df, params, annotation_priors, bio_matrix)

    return annotation_priors

def load_databases():
    ms1_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","IPA_MS1.csv"))
    adducts_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","adducts.csv"))
    allbioreactions_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","allBIO_reactions.csv"))
    ms2_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","IPA_MS2_QTOF6550.csv"))
    dbms2_db = pd.read_csv(os.path.join(lg.current_directory,"IPADatabases","DBMS2_test_pos.csv"))

    return ms1_db, adducts_db, allbioreactions_db, allbioreactions_db, ms2_db, dbms2_db

def cluster_features(peakml_df: pd.DataFrame):
    # Cluster features
    peakml_df = ipa.clusterFeatures(peakml_df)
    return peakml_df

def map_isotope_patterns(peakml_df: pd.DataFrame, params: IPAParams):
    # Mapping isotope patterns (Output: relationship, isotope pattern, charge)
    ipa.map_isotope_patterns(peakml_df, 
                            isoDiff = float(params.isodiff), 
                            ppm = float(params.ppmiso), 
                            ionisation = float(params.ionisation))

def run_adducts(params: IPAParams, ms1_db: pd.DataFrame, adducts_db: pd.DataFrame):    
    # computing all adducts
    computed_adducts = ipa.compute_all_adducts(adductsAll = adducts_db, 
                                        DB = ms1_db, 
                                        ionisation = params.ionisation,
                                        ncores = params.ncores)
    return computed_adducts

def run_priors(peakml_df: pd.DataFrame, params: IPAParams, computed_adducts: pd.DataFrame, ms2_db: pd.DataFrame, dbms2_db: pd.DataFrame):

    # computing priors
    if (ms2_db is None) or (dbms2_db is None):
        annotation_priors = ipa.MS1annotation(df = peakml_df,
                                        allAdds = computed_adducts,
                                        ppm = params.ppm,
                                        me = params.me,
                                        ratiosd = params.ratiosd,
                                        ppmunk = params.ppmunk,
                                        ratiounk = params.ratiounk,
                                        ppmthr = params.ppmthr,
                                        pRTNone = params.pRTNone,
                                        pRTout = params.pRTout,
                                        ncores = params.ncores)
    else:
        annotation_priors = ipa.MSMSannotation(df = peakml_df,
                                        dfMS2 = ms2_db,
                                        allAdds = computed_adducts,
                                        DBMS2 = dbms2_db,
                                        ppm = params.ppm,
                                        me = params.me,
                                        ratiosd = params.ratiosd,
                                        ppmunk = params.ppmunk,
                                        ratiounk = params.ratiounk,
                                        ppmthr = params.ppmthr,
                                        pRTNone = params.pRTNone,
                                        pRTout = params.pRTout,
                                        mzdCS = params.mzdCS,
                                        ppmCS = params.ppmCS,
                                        CSunk = params.CSunk,
                                        evfilt = params.evfilt,
                                        ncores=  params.ncores)

    return annotation_priors

# Computing posterior probabilities integrating biochemical connections
def run_bio_matrix(annotations: pd.DataFrame, params: IPAParams, ms1_db: pd.DataFrame, allbioreactions_db: pd.DataFrame):
        # computing Bio matrix (if necessary)
        if (allbioreactions_db is None) and (params.delta_bio is not None):
            bio_matrix = ipa.Compute_Bio(DB = ms1_db,
                                                annotations = annotations,
                                                mode = params.mode,
                                                connections = params.connections,
                                                ncores = params.ncores)

            return bio_matrix
        else:
            return allbioreactions_db

def run_gibbs_sampler(peakml_df: pd.DataFrame, params: IPAParams, annotations: pd.DataFrame, bio_matrix: pd.DataFrame):
    # Gibbs sampler (if needed). Which one based on the inputs
    if (bio_matrix is not None) and (params.delta_bio is not None) and (params.delta_add is not None):
        ipa.Gibbs_sampler_bio_add(df = peakml_df,
                                    annotations = annotations,
                                    Bio = bio_matrix,
                                    noits = params.noits,
                                    burn = params.burn,
                                    delta_bio = params.delta_bio,
                                    delta_add = params.delta_add)
    elif (bio_matrix is not None) and (params.delta_bio is not None) and (params.delta_add is None):
        ipa.Gibbs_sampler_bio(df = peakml_df,
                                annotations = annotations,
                                Bio = bio_matrix,
                                noits = params.noits,
                                burn = params.burn,
                                delta_bio = params.delta_bio)
    elif (bio_matrix is None) and (params.delta_bio is None) and (params.delta_add is not None):
        ipa.Gibbs_sampler_add(df=peakml_df,
                                annotations = annotations,
                                noits = params.noits,
                                burn = params.burn,
                                delta_add = params.delta_add)