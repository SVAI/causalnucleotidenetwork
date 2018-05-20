from __future__ import unicode_literals, division
from collections import OrderedDict


class Patient(OrderedDict):
    """Convenience class to wrap TCGA xmls->ordered dictionary. Helper func and attributes

    Constructor:
        clinical_obj `OrderedDict`: TCGA clinical XML as ordered dictionary
    """
    def __init__(self, clinical_obj):
        self.patient_uuid = clinical_obj['kirp:patient']['shared:bcr_patient_uuid']['#text']
        super(Patient, self).__init__(clinical_obj['kirp:patient'])
        self._age = None
        self._survival_time = None
        self._censored = None

    @property
    def age(self):
        if self._age is None:
            age_data = self["clin_shared:days_to_birth"]["#text"]
            self._age = -int(age_data) / 365.25
        return self._age

    @property
    def survival_time(self):
        """Survival time at inception of study (verify?)

        In the right censoring case returns time of last observation
        """
        if self._survival_time is None:
            try:
                self._survival_time = int(self['clin_shared:days_to_death']['#text']) / 365.25
                self._censored = False
            except KeyError as ke:
                if ke.message != '#text':
                    raise
                # Right censored case
                self._survival_time = int(self["clin_shared:days_to_last_followup"]["#text"]) / 365.25
                self._censored = False

        return self._survival_time

    @property
    def censored(self):
        if self._censored is None:
            _ = self.survival_time  # censored is set here
        return self._censored
