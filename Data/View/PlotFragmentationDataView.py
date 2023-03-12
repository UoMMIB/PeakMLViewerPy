import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.PlotFragmentationItem import PlotFragmentationItem

from Data.PeakML.Peak import Peak
from Data.PeakML.Header import Header
from Data.PeakML.PeakData import PeakData
import pandas as pd

from typing import List

class PlotFragmentationDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Label','Fragments','Colour'])

    def load_plot_data_for_selected_peak(self, Peak: Peak, peakml_header: Header, colours):
        try:
            self.clear_datalist()

            for peak in Peak.peaks:
                measurement = peakml_header.get_measurement_by_id(peak.measurement_id)
                label = measurement.label
                fragments = peak.peak_data.fragments
                if fragments != []:
                    self.add_item(label,fragments,colours[f"M-{measurement.id}"])

            self.refresh_dataframe()

        except Exception as err:
            lg.log_error(f'Unable to update plot Fragmentation data: {err}')

    def add_item(self, label:str , fragments: List[str], color: str):
        self.datalist.append(PlotFragmentationItem(label,fragments,color))

    def refresh_dataframe(self):
        self.clear_dataframe()
        for item in self.datalist:
            dr = pd.DataFrame({
                                "UID": item.uid,
                                "Label": item.label,
                                "Fragments" : item.fragments,
                                #"Colour": item.colour,
                                "Selected": item.selected,
                                "Checked": item.checked,
                            }, index=[0])
            self.dataframe = pd.concat([self.dataframe, dr], ignore_index=True)

