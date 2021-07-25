import pandas as pd
import Utilities as u
import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.PlotDerivativesItem import PlotDerivativesItem

class PlotDerivativesDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Label','RT_values','Intensity_values','Colour'])

    def load_plot_data_for_selected_peak(self, selected_peak, peak_dic):
        try:
            self.clear_datalist()

            peakset_annotation_relation_id = selected_peak.get_specific_annotation('relation.id')

            related_peaks = []

            for peakml_peak_key in peak_dic.keys():
                peakml_peak = peak_dic[peakml_peak_key]
                peak_annotation_relation_id = peakml_peak.get_specific_annotation('relation.id')

                if peak_annotation_relation_id:
                    if peakset_annotation_relation_id.value == peak_annotation_relation_id.value:
                        related_peaks.append(peakml_peak)
                
            for rel_peak in related_peaks:

                mass = rel_peak.mass
                intensity = rel_peak.intensity

                ann_relation = rel_peak.get_specific_annotation('relation.ship')
                ann_reaction = rel_peak.get_specific_annotation('reaction')

                if ann_reaction:
                    description = ann_reaction.value
                elif ann_relation:
                    description = ann_relation.value
                else:
                    description = ""
                
                self.add_item(mass, intensity, description)

            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to update plot derivative data: {err}')


    def add_item(self, mass, intensity, description):
        self.datalist.append(PlotDerivativesItem(mass, intensity, description))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            self.dataframe = self.dataframe.append({
                                                    "UID": item.uid,
                                                    "Mass": item.mass,
                                                    "Intensity": item.intensity,
                                                    "Description": item.description,
                                                    "Selected": item.selected,
                                                    "Checked": item.checked,
                                                }, ignore_index=True)




