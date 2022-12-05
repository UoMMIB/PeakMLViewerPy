from Data.PeakML.Peak import Peak
from Data.PeakML.Header import Header

import IO.PeakMLIO as PeakMLIO
import IO.IPAIO as IPAIO
import IO.IPAV2IO as IPAV2IO

import Logger as lg
import gzip

from xml.dom import minidom

from typing import Dict, List

class PeakML():
    def __init__(self, header: Header = None, peaks: List[Peak] = None, peak_order: List[str] = None):
        self.header = None
        self.peaks = None
        self.peak_order = None

    @property
    def header(self) -> Header:
        return self._header
    
    @header.setter
    def header(self, header: Header):
        self._header = header

    @property
    def peaks(self) -> Dict[str, Peak]:
        return self._peaks

    @peaks.setter
    def peaks(self, peaks: Dict[str, Peak]):
        self._peaks = peaks

    @property
    def peak_order(self) -> List[str]:
        return self._peak_order

    @peak_order.setter
    def peak_order(self, peak_order: List[str]):
        self._peak_order = peak_order

    @property
    def set_intensities(self) -> List[float]:
        return self._set_intensities

    @set_intensities.setter
    def set_intensities(self, set_intensities: List[float]):
        self._set_intensities = set_intensities

    def get_peak_by_uid(self, uid: str) -> Peak:
        return self.peaks[uid]

    def remove_peak_by_uid(self, uid: str):
        del self.peaks[uid]

        if uid in self._peak_order:
            self._peak_order.remove(uid)

    def import_from_file(self, filepath: str) -> bool:
        success = False
        tree_data = None

        # Files can be gzipped, so if unable to read file directly, a second attempt is made with decompression.
        attempt_compressed = False

        try:
            # If errors while attempt to read, requires conversion.
            with open(filepath) as f:
                tree_data = f.read().encode()
        except:
            attempt_compressed = True
            
        if attempt_compressed:
            try:
                with gzip.open(filepath) as g:
                    tree_data = g.read()
                    tree_data = tree_data.decode()
                    tree_data = tree_data.replace('\n','')
                    tree_data = tree_data.replace('\t','')
                    tree_data = tree_data.encode()

                    ## Section for debugging and testing by comparing decoded version with output version.
                    # md_string = minidom.parseString(tree_data)
                    # decoded_output = md_string.toprettyxml(indent="\t")
                    # decoded_output = decoded_output.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>\n\n\n<?xml-stylesheet type="text/xml" href=""?>\n')
                    # decoded_output = decoded_output.replace("/>"," />")
                    # w = open(self.get_path() + "decoded_" + self.get_filename(), "w")
                    # w.write(decoded_output)
                    # w.close()
            except Exception as err:
                lg.log_error(f'Unable to open compressed file: {err}')

        if tree_data is not None:
            try:
                header, peaks, peak_order = PeakMLIO.import_element_tree_from_peakml_file(tree_data)
                self.header = header
                self.peaks = peaks
                self.peak_order = peak_order

                success = True

            except Exception as err:
                lg.log_error(f'Unable to convert file to PeakML class stucture: {err}')

        return success

    def import_ipa_from_file(self, filepath: str) -> bool:

        success = False

        try:
            IPAIO.import_ipa_rdata_from_filepath(filepath=filepath, peakml_peaks=self.peaks)
            return True
        except Exception as err:
            lg.log_error(f'Unable to convert file to PeakML class stucture: {err}')
        
        return success

    def generate_ipa_annotations(self, import_peakml_filename) -> bool:

        success = False

        try:
            lg.log_error("Start IPA generate")
            IPAV2IO.generate_ipa_annotation(self.peaks)
            lg.log_error("End IPA generate")

            # for peak in list(self.peaks.values()):

            #     if peak.get_specific_annotation('id'):
            #         lg.log_error(peak.get_specific_annotation('id').value)

            #     if peak.get_specific_annotation('post'):
            #         lg.log_error(peak.get_specific_annotation('post').value)

            #     if peak.get_specific_annotation('post Gibbs'):
            #         lg.log_error(peak.get_specific_annotation('post Gibbs').value)

            # self.peaks = peakml_peaks_annotated

            #temp_filepath_for_annotation = import_peakml_filename
            #Write IPA file to temporary location
            #self.export(temp_filepath_for_annotation)
            #lg.log_error("E")
            #Update annotations for file
            
            #lg.log_error("F")
            #Import updated local file.
            #self.import_from_file(temp_filepath_for_annotation)
            #lg.log_error("G")
            return True
        except Exception as err:
            lg.log_error(f'Unable to add IPA annotations to PeakML class stucture: {err}')
        
        return success
    
    def export(self, filepath: str):

        #Select peaks to include based on checks and filters.

        #Save raw
        r = gzip.open(filepath, "w")
        # Pass header and peaks list
        
        r.write(PeakMLIO.create_xml_from_peakml(self.header, list(self.peaks.values())).encode())
        r.close()

        #Save zipped

    def export_ipa(self, filepath: str):

        IPAIO.export_ipa_input_data(filepath, list(self.peaks.values()))

    def export_ipa_priors(self, filepath: str):

        IPAIO.export_ipa_input_priors_data(filepath, list(self.peaks.values()))
    