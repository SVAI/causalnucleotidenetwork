"""This module focuses on:
- Consuming a cluster
- Have a cluster tell you about itself
"""
from Patient import Patient  # Add func to take id and populate
from collections import defaultdict
import utils


class PatientCluster(list):
    """Cluster of Patients from tSNE or PCA, whichever alg wins out"""
    def __init__(self, patients):
        super(PatientCluster, self).__init__(patients)
        self._assumed_consistent_props = utils.get_property_names(self[0])
        self._cluster_scores = defaultdict(int)

    @property
    def cluster_scores(self):
        if not self._cluster_scores:
            self._compute_descriptors()
        return self._cluster_scores

    def cluser_descriptors(self, skip_properties=[]):
        threshold_score = len(self) * 0.60
        props_sorted = sorted(
            k for k in self.cluster_scores.iterkeys()
            if self.cluster_scores[k] > threshold_score and k not in skip_properties)
        return props_sorted[:3]

    def load_patients(patients):
        pass

    def _compute_descriptors(self):
        """Assumes properties on objects have compareto implementation"""
        for i, curr_p in enumerate(self):
            for other_p in self[i + 1:]:
                self._score_patients_compr(curr_p, other_p)

    def _score_patients_compr(self, a, b):
        for prop_name in self._assumed_consistent_props:
            a_prop = getattr(a, prop_name)
            b_prop = getattr(b, prop_name)

            if a_prop == "UNK":
                continue

            if a_prop == b_prop:
                self._cluster_scores[prop_name] += 1
