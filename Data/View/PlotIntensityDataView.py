import Logger as lg
import Utilities as u
import statistics as stats

from Data.View.BaseDataView import BaseDataView
from Data.View.PlotIntensityItem import PlotIntensityItem
from Data.PeakML.Peak import Peak
from Data.PeakML.Header import Header
import pandas as pd

class PlotIntensityDataView(BaseDataView):
    def __init__(self):
        super().__init__(['SetID', 'SetID_Label', 'Intensity', 'Intensities_Mean', 'Intensities_Neg_Conf', 'Intensities_Pos_Conf'])

    def load_plot_data_for_selected_peak(self, selected_peak: Peak, peak_header: Header):
        try: 
            self.clear_datalist()

            for set in peak_header.sets:
                intensities = []
                for peak in selected_peak.peaks:
                    if peak.measurement_id in set.linked_peak_measurement_ids:                  
                        if u.is_float(peak.intensity):
                            intensities.append(float(peak.intensity))

                if len(intensities):
                    intensities_mean = stats.mean(intensities)
                    intensities_neg_conf = intensities_mean - min(intensities)
                    intensities_pos_conf = max(intensities) - intensities_mean
                                  
                for i in range(len(intensities)):
                    self.add_item(set.id, f"{set.id}-{i+1}", intensities[i], intensities_mean, intensities_neg_conf, intensities_pos_conf)

            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to update plot intensity data: {err}')

    def add_item(self, set_id: str, set_id_label: str, intensity: float, intensities_mean: float, intensities_neg_conf: float, intensities_pos_conf: float):
        self.datalist.append(PlotIntensityItem(set_id, set_id_label, intensity, intensities_mean, intensities_neg_conf, intensities_pos_conf))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            dr = pd.DataFrame({
                                "UID": item.uid,
                                "SetID": item.set_id,
                                "SetID_Label": item.set_id_label,
                                "Intensity": item.intensity,
                                "Intensities_Mean": item.intensities_mean,
                                "Intensities_Neg_Conf": item.intensities_neg_conf,
                                "Intensities_Pos_Conf": item.intensities_pos_conf,
                                "Selected": item.selected,
                                "Checked": item.checked,
                            }, index=[0])
            self.dataframe = pd.concat([self.dataframe, dr], ignore_index=True)