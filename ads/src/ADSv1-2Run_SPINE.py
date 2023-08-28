# Script designed to run ADS 1.2 in SPINE with docker image micheletgregory/ads:1.2-ubuntu_jammy-python3.7.7
# 1. Prepare input folder
# 2. Prepare config file
# 3. Run ADS
# 4. Move results to output folder

import argparse
import shutil
import os
from pathlib import Path
import pandas as pd
import subprocess
from distutils.dir_util import copy_tree

OUTPUT_DIR = "/output"
SUBJECTS_DIR = "/input/SPINE_SUBJECTS/"
SUBJECT_DIR = "/input/SPINE_SUBJECTS/Subject/"
TEMPLATE_CONFIG_PATH = "/app/ADSv1.2/Configuration.xlsx"
NEW_CONFIG_PATH = Path(SUBJECT_DIR,"Configuration.xlsx")
SUBJECT_DIR_PATH_LIST_PATH = Path(SUBJECTS_DIR,"subject_directory_path_list.txt")

def move_outputs():
    #move everything from subject to output dir so they are exposed to spine
    copy_tree(Path(SUBJECT_DIR), OUTPUT_DIR)

def run_ADS_v1_2():
    try:
        # Run the script as a subprocess
        subprocess.run(["python", "/app/ADSv1.2/codes/ADSv1Run.py", "-Configuration_path", str(NEW_CONFIG_PATH)], check=True)
        print("Script executed successfully.")
    except subprocess.CalledProcessError:
        print("Script execution failed.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_conf_file(args):

    with open(SUBJECT_DIR_PATH_LIST_PATH, "w") as file:
        # Write the content to the file
        file.write(SUBJECT_DIR)
    Config_df = pd.read_excel(open(TEMPLATE_CONFIG_PATH, 'rb'))
    Config_df['selected_option'][0] = SUBJECT_DIR_PATH_LIST_PATH
    Config_df['selected_option'][1] = args.segmentation_model
    Config_df['selected_option'][2] = args.bvalue
    Config_df['selected_option'][3] = args.generate_mni_files
    Config_df['selected_option'][4] = args.mni_domain_spec
    Config_df['selected_option'][5] = args.non_linear_registration
    Config_df['selected_option'][6] = args.generate_brain_mask
    #Config_df['selected_option'][7]
    Config_df['selected_option'][8] = args.generate_les_volume_report
    Config_df['selected_option'][9] = args.generate_seg_png
    Config_df['selected_option'][10] = args.generate_auto_radiological_report
    #Config_df['selected_option'][11]
    Config_df['selected_option'][12] = args.generate_auto_asses_report_shap
    Config_df['selected_option'][13] = args.nonlinear_if_hydrocephalus
    #Config_df['selected_option'][14]
    #Config_df['selected_option'][15]
    #Config_df['selected_option'][16]
    Config_df.to_excel(NEW_CONFIG_PATH, index=False)


def move_inputs(dwi_path, b0_path, adc_path):
    os.makedirs(SUBJECTS_DIR, exist_ok=True)
    os.makedirs(SUBJECT_DIR, exist_ok=True)
    shutil.copy(dwi_path, Path(SUBJECT_DIR,"Subject_DWI.nii.gz"))
    shutil.copy(b0_path, Path(SUBJECT_DIR,"Subject_b0.nii.gz"))
    shutil.copy(adc_path, Path(SUBJECT_DIR,"Subject_ADC.nii.gz"))

def main(args):
    move_inputs(args.dwi, args.b0, args.adc)
    create_conf_file(args)
    run_ADS_v1_2()
    move_outputs()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prepare inputs for ADS v1.2, run it and move outputs.')
    parser.add_argument("dwi", type=str, help="Path to DWI image (nifti)")
    parser.add_argument("b0", type=str, help="Path to b0 image (nifti)")
    parser.add_argument("adc", type=str, help="Path to ADC image (nifti)")
    parser.add_argument(
        "--segmentation-model",
        choices=[
                        "DAGMNet_CH3",
                        "DAGMNet_CH2",
                        "UNet_CH3",
                        "UNet_CH2",
                        "FCN_CH3",
                        "FCN_CH2"
                    ],
        help="Segmentation DL model",
        default="DAGMNet_CH3"
    )
    parser.add_argument(
        "--bvalue",
        type=str,
        default="1000",
        help="B value"
    )
    parser.add_argument(
        "--generate-mni-files",
        action="store_true",
        help="Generate MNI files?"
    )
    parser.add_argument(
        "--mni-domain-spec",
        type=str,
        default="JHU_MNI_181",
        choices=[
            "JHU_MNI_181",
            "JHU_MNI_182",
            "MNI152_181",
            "MNI152_182"
        ],
        help="MNI domain spec"
    )
    parser.add_argument(
        "--non-linear-registration",
        action="store_true",
        help="Non linear registration?"
    )
    parser.add_argument(
        "--generate-brain-mask",
        action="store_true",
        help="Generate brain mask?"
    )
    parser.add_argument(
        "--generate-les-volume-report",
        action="store_true",
        help="Generate lesion volume report?"
    )
    parser.add_argument(
        "--generate-seg-png",
        action="store_true",
        help="Generate segmentation PNG?"
    )
    parser.add_argument(
        "--generate-auto-radiological-report",
        action="store_true",
        help="Generate automatic radiological report?"
    )
    parser.add_argument(
        "--generate-auto-asses-report-shap",
        action="store_true",
        help="Generate auto assessment report SHAP explanation?"
    )
    parser.add_argument(
        "--nonlinear-if-hydrocephalus",
        action="store_true",
        help="Nonliear registration if hydrocephalus is detected"
    )
    args = parser.parse_args()
    main(args)
