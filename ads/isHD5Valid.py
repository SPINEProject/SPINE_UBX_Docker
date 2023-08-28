import h5py
import sys

def is_valid_hdf5_file(file_path):
    try:
        with h5py.File(file_path, "r") as f:
            # Try accessing something in the file to ensure it's valid
            _ = f["/"]
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
