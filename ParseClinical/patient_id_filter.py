"""Parse and aggregate patient info rom TCGA


Note:
    - Easy performance improvement, use generators
"""

from __future__ import print_function
from utils import find_all_matches
from tsv_tools import create_property_tsv
from Patient import Patient
import xmltodict
import argparse
import json
import sys
import os


def _parse_args():
    parser = argparse.ArgumentParser(description='Generate Release Version Report',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('clinical_path', help="Path to file or folder containing clinical xmls from TCGA.")
    parser.add_argument('tcga_fpkm_summary_path', help="Path to TCGA FPKM summary JSON.")
    parser.add_argument('-t', help="Run script test", action="store_true", dest="testing")
    return parser.parse_args()


def get_FPKM_case_ids(tcga_json_path):
    """Parse FPKM files for patient ids

    Example:
        >>> test_num = get_FPKM_case_ids("Test_Data/files.2018-05-19.json")
        >>> len(test_num)
        291
    """
    with open(tcga_json_path, "r") as f:
        tcga_json_descr = json.load(f)

    case_ids = set()

    for mapping in tcga_json_descr:
        try:
            for case in mapping['cases']:
                case_ids.add(case['case_id'].strip())
        except KeyError:
            print("Error that shouldn't happen, happeneded", file=sys.stderr)

    return case_ids


def xml_to_raw_clinical_patient(clinical_xml_path):
    """Turn clinical xml to ClinicalObj (TBD)"""
    with open(clinical_xml_path, 'r') as f:
        obj = xmltodict.parse(f)
    return obj['kirp:tcga_bcr']


def is_clinical_in_cases(clinical_obj, cases):
    """Checks to see if clinical object representation is part of cases to assess

    Example:
        >>> clin_obj = xml_to_raw_clinical_patient("Test_Data/nationwidechildrens.org_clinical.TCGA-MH-A562.xml")
        >>> cases = set(["ad7ba244-67fa-4155-8f13-424bdcbb12e5", "dc39df39-9945-4cb6-a852-d3b42177ac80", "b877d608-e4e0-4b28-9235-01dd65849cf7"])
        >>> is_clinical_in_cases(clin_obj, cases)
        False
        >>> cases = set(["ad7ba244-67fa-4155-8f13-424bdcbb12e5", "dc39df39-9945-4cb6-a852-d3b42177ac80", "b877d608-e4e0-4b28-9235-01dd65849cf7", "45bdcfd6-1e3f-4be8-b843-ae949e8e43eb"])
        >>> is_clinical_in_cases(clin_obj, cases)
        True
    """
    def get_days_to_birth():
        pass

    def get_days_to_death():
        """This returns either the censored value of the"""
        pass

    patient_uuid = clinical_obj['kirp:patient']['shared:bcr_patient_uuid']['#text']
    patient_uuid = patient_uuid.strip().lower()
    return patient_uuid in cases


def main(args):
    path = args.clinical_path
    tcga_json = args.tcga_fpkm_summary_path

    if os.path.isfile(path):
        print("Lied not supporting files yet")
        return

    target_cases = get_FPKM_case_ids(tcga_json)
    xml_paths = find_all_matches(target_dir=path, filename='*.xml', glob_pattern=True, abs_path=True)
    raw_xml_objs = [xml_to_raw_clinical_patient(xml) for xml in xml_paths]
    valid_raw_xmls = [obj for obj in raw_xml_objs if is_clinical_in_cases(obj, target_cases)]
    patients = [Patient(raw) for raw in valid_raw_xmls]

    create_property_tsv(patients, tsv_path="Patients_Properties.tsv")


if __name__ == '__main__':
    args = _parse_args()
    if args.testing:
        import doctest
        doctest.testmod()
    else:
        main(args)
