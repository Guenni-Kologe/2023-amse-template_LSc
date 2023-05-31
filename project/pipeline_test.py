import os

def test_output_files_exist():
    output_files = ["data.sqlite"] 
    for file in output_files:
        if os.path.exists(file):
            print(f"echo Output file '{file}' exists.")
        else:
            assert False, f"Output file '{file}' does not exist."