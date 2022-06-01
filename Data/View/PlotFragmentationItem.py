from Data.View.BaseItem import BaseItem

class PlotFragmentationItem(BaseItem):
    def __init__(self, label: str,fragments: str, colour: str):
        super().__init__()

        self.label = label
        self.fragments = fragments

    @property
    def set_label(self) -> str:
        return self._set_label

    @set_label.setter
    def set_label(self, set_label: str):
        self._set_label = set_label

    @property
    def set_fragments(self) -> str:
        return self._set_fragments

    @set_fragments.setter
    def set_fragments(self, set_fragments: str):
        self._set_fragments = set_fragments

    @property
    def colour(self) -> str:
        return self._colour

    @colour.setter
    def colour(self, colour: str):
        self._colour = colour
