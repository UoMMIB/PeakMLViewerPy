import base64
import Utilities as u
from typing import List

class PeakData():
    def __init__(self, type: str, size: int):

        self.type = type
        self.size = size

        self._scan_ids = []
        self._retention_times = []
        self._masses = []
        self._intensities = []
        self._relative_intensities = []
        self._pattern_ids = []
        self._measurement_ids = []
        self._fragments = []

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, type: str):
        self._type = type

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size

    @property
    def scan_ids(self) -> List[int]:
        return self._scan_ids

    @scan_ids.setter
    def scan_ids(self, scan_ids: List[int]):
        self._scan_ids = scan_ids

    @property
    def retention_times(self) -> List[float]:
        return self._retention_times

    @retention_times.setter
    def retention_times(self, retention_times: List[float]):
        self._retention_times = retention_times

    @property
    def masses(self) -> List[float]:
        return self._masses

    @masses.setter
    def masses(self, masses: List[float]):
        self._masses = masses

    @property
    def fragments(self) -> list[str]:
        return self._fragments

    @fragments.setter
    def fragments(self, fragments: list[str]):
        self._fragments = fragments

    @property
    def intensities(self) -> List[float]:
        return self._intensities

    @intensities.setter
    def intensities(self, intensities: List[float]):
        self._intensities = intensities

    @property
    def relative_intensities(self) -> List[float]:
        return self._relative_intensities

    @relative_intensities.setter
    def relative_intensities(self, relative_intensities: List[float]):
        self._relative_intensities = relative_intensities

    @property
    def pattern_ids(self) -> List[int]:
        return self._pattern_ids

    @pattern_ids.setter
    def pattern_ids(self, pattern_ids: List[int]):
        self._pattern_ids = pattern_ids

    @property
    def measurement_ids(self) -> List[int]:
        return self._measurement_ids

    @measurement_ids.setter
    def measurement_ids(self, measurement_ids: List[int]):
        self._measurement_ids = measurement_ids

    def get_encoded_scan_ids(self) -> str:
        encoded = base64.b64encode(self.scan_ids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_retention_times(self) -> str:
        encoded = base64.b64encode(self.retention_times)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_masses(self) -> str:
        encoded = base64.b64encode(self.masses)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_intensities(self) -> str:
        encoded = base64.b64encode(self.intensities)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_relative_intensities(self) -> str:
        encoded = base64.b64encode(self.relative_intensities)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_pattern_ids(self) -> str:
        encoded = base64.b64encode(self.pattern_ids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_measurement_ids(self) -> str:
        encoded = base64.b64encode(self.measurement_ids)
        return encoded.decode("UTF-8")  #Converts from bytes to string

    def get_encoded_fragments(self) -> str:
        encoded = base64.b64encode(self.fragments)
        return encoded.decode("UTF-8")

    def add_scan_id(self, scan_id: str):
        self.scan_ids.append(scan_id)

    def add_retention_time(self, retention_time: str):
        self.retention_times.append(retention_time)

    def add_mass(self, mass: str):
        self.masses.append(mass)

    def add_intensity(self, intensity: str):
        self.intensities.append(intensity)

    def add_relative_intensity(self, relative_intensity: str):
        self.relative_intensities.append(relative_intensity)

    def add_pattern_id(self, patternid: str):
        self.pattern_ids.append(patternid)

    def add_measurement_id(self, measurement_id: str):
        self.measurement_ids.append(measurement_id)

    def add_fragment(self,fragment:(float,float)):
        self.fragments.append(fragment)

    def get_retention_times_formatted_string(self) -> List[str]:
        rts = list(map(u.format_time_string,self.retention_times))
        return rts

    def get_retention_times_formatted_datetime(self) -> List[str]:
        rts = list(map(u.format_time_datetime,self.retention_times))
        return rts

    def get_intensities(self) -> List[str]:
        intensities = list(map(float,self.intensities))
        return intensities  #Converts from bytes to string

    def get_measurement_ids(self) -> List[str]:
        measurement_ids = list(map(float,self.measurement_ids))
        return measurement_ids  #Converts from bytes to string
