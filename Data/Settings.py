import IO.SettingsIO as SetIO
from typing import List

class Settings():
    def __init__(self, preferences: List[str] = [], databases: List[str] = [], frag_databases_1: List[str] = [], frag_databases_2: List[str] = []):
        self.preferences = preferences

        self.appearance_smooth = None
        self.appearance_decdp = None
        self.appearance_defplot = None

        for preference in self.preferences:
            if preference[0] == "smooth":
                self.appearance_smooth = preference[1]
            elif preference[0] == "decdp":
                self.appearance_decdp = preference[1]
            elif preference[0] == "defplot":
                self.appearance_defplot = preference[1]

        self.databases = databases
        self.frag_databases_1 = frag_databases_1
        self.frag_databases_2 = frag_databases_2

    def get_preference_by_name(self, name: str) -> str:
        if name == "smooth":
            return self.appearance_smooth
        elif name == "decdp":
            return self.appearance_decdp
        elif name == "defplot":
            return self.appearance_defplot

    def set_preference_by_name(self, name: str, value: str):
        if name == "smooth":
            self.appearance_smooth = value
        elif name == "decdp":
            self.appearance_decdp = value
        elif name == "defplot":
            self.appearance_defplot = value

    def get_database_paths(self) -> List[str]:
        return self.databases

    def get_frag_databases_1_paths(self) -> List[str]:
        return self.frag_databases_1

    def get_frag_databases_2_paths(self) -> List[str]:
        return self.frag_databases_2

    def set_database_paths(self, databases: List[str]):
        self.databases = databases

    def set_frag_databases_1_paths(self, databases: List[str]):
        self.frag_databases_1 = databases

    def set_frag_databases_2_paths(self, databases: List[str]):
        self.frag_databases_2 = databases
