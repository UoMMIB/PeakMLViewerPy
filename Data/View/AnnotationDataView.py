import pandas as pd
import Utilities as u
import Logger as lg

from Data.View.BaseDataView import BaseDataView
from Data.View.AnnotationItem import AnnotationItem
from Data.PeakML.Peak import Peak

class AnnotationDataView(BaseDataView):
    def __init__(self):
        super().__init__(['Label','Value'])

    def load_data_for_selected_peak(self, peak: Peak):
        self.clear_datalist()
        try:
            for annotation in peak.annotations:
                self.add_item(annotation.label, annotation.value)
            self.refresh_dataframe()
        except Exception as err:
            lg.log_error(f'Unable to load annotation data: {err}')

    def add_item(self, label: str, value: str):
        self.datalist.append(AnnotationItem(label, value))

    def refresh_dataframe(self):
        # Excluded from annotation grid as used in the identification grid.
        exclude_labels = ["identification", "ppm", "adduct", "notes", "prior", "post"]

        self.clear_dataframe()

        for item in self.datalist:
            if item.label not in exclude_labels:
                self.dataframe = self.dataframe.append({
                                                        "UID": item.uid,
                                                        "Label": item.label,
                                                        "Value": item.value,
                                                        "Selected": item.selected,
                                                        "Checked": item.checked,
                                                    }, ignore_index=True)
