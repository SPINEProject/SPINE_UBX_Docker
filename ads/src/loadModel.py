import h5py
import sys
from tensorflow.keras.models import model_from_json, load_model

def is_valid_hdf5_file(file_path):
    try:
        MaskNet = load_model(file_path, compile=False)
        return True
    except Exception as e:
        print(e)
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python isHD5Valid.py <file_path>")
        return

    file_path = sys.argv[1]

    if is_valid_hdf5_file(file_path):
        print("The HDF5 file is valid.")
    else:
        print("The HDF5 file is not valid.")

if __name__ == "__main__":
    main()
