from Data.PeakML.Annotation import Annotation
from typing import List
class AnnotatableEntity():
    def __init__(self):
        self._annotations = []

    @property
    def annotations(self) -> List[Annotation]:
        return self._annotations

    @annotations.setter
    def annotations(self, annotations: List[Annotation]):
        self._annotations = annotations

    def add_annotation(self, annotation: Annotation):
        self._annotations.append(annotation)

    def get_specific_annotation(self, ann_label: str) -> Annotation:
        for ann in self._annotations:
            if ann.label == ann_label:
                return ann
        return None

    def update_specific_annotation(self, ann_label: str, ann_value: str):
        value_updated = False
        #Check if existing to update
        for ann in self._annotations:
            if ann.label == ann_label:
                ann.value = ann_value
                value_updated = True

        # If not existing create.
        if not value_updated:
            self._annotations.append(Annotation(label=ann_label, value=ann_value))
