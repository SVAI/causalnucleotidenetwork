from __future__ import unicode_literals, division
from collections import OrderedDict
import utils


class Patient(OrderedDict):
    """Convenience class to wrap TCGA xmls->ordered dictionary. Helper func and attributes

    Constructor:
        clinical_obj `OrderedDict`: TCGA clinical XML as ordered dictionary

    Todo:
        - Use utils.get_or_default in place of try.. except KeyError logic
    """
    def __init__(self, clinical_obj):
        self._patient_uuid = clinical_obj['kirp:patient']['shared:bcr_patient_uuid']['#text']
        super(Patient, self).__init__(clinical_obj['kirp:patient'])
        self._age = None
        self._censored = None
        self._clinical_stage = None
        self._histological_type = None
        self._gender = None
        self._pathologic_stage = None
        self._survival_time = None
        self._tumor_tissue_site = None

    @property
    def age(self):
        if self._age is None:
            age_data = utils.get_or_default(self["clin_shared:days_to_birth"], '#text')
            if age_data != 'UNK':
                age_data = -int(age_data) / 365.25
            self._age = age_data
        return self._age

    @property
    def censored(self):
        if self._censored is None:
            _ = self.survival_time  # censored is set here
        return self._censored

    @property
    def clinical_stage(self):
        if self._clinical_stage is None:
            self._clinical_stage = utils.get_or_default(
                self['shared_stage:stage_event']['shared_stage:clinical_stage'], '#text')
        return self._clinical_stage

    @property
    def histological_type(self):
        if self._histological_type is None:
            self._histological_type = utils.get_or_default(
                self['shared:histological_type'], '#text')
        return self._histological_type

    @property
    def gender(self):
        if self._gender is None:
            self._gender = utils.get_or_default(self['shared:gender'], '#text')
        return self._gender

    @property
    def pathologic_stage(self):
        if self._pathologic_stage is None:
            self._pathologic_stage = utils.get_or_default(
                self['shared_stage:stage_event']['shared_stage:pathologic_stage'], '#text')
        return self._pathologic_stage

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
    def tumor_tissue_site(self):
        if self._tumor_tissue_site is None:
            self._tumor_tissue_site = utils.get_or_default(
                self['clin_shared:tumor_tissue_site'], '#text')
        return self._tumor_tissue_site

    @property
    def unique_ID(self):
        return self._patient_uuid
