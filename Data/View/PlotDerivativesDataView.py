import Logger as lg
import Utilities as u
from Data.View.BaseDataView import BaseDataView
from Data.View.PlotDerivativesItem import PlotDerivativesItem
from Data.PeakML.Peak import Peak
import pandas as pd

from typing import Dict

class PlotDerivativesDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Mass','Intensity','Description'])

    def load_plot_data_for_selected_peak(self, selected_peak: Peak, peak_dic: Dict[str, Peak]):
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

                if u.is_float(rel_peak.mass):
                    mass = float(rel_peak.mass)
                else:
                    mass = 0

                if u.is_float(rel_peak.intensity):
                    intensity = float(rel_peak.intensity)
                else:
                    intensity = 0

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


    def add_item(self, mass: float, intensity: float, description: str):
        self.datalist.append(PlotDerivativesItem(mass, intensity, description))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            dr = pd.DataFrame({
                                "UID": item.uid,
                                "Mass": item.mass,
                                "Intensity": item.intensity,
                                "Description": item.description,
                                "Selected": item.selected,
                                "Checked": item.checked,
                            }, index=[0])
            self.dataframe = pd.concat([self.dataframe, dr], ignore_index=True)





