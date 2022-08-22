"""Structural Properties module"""
import subprocess
from random import random
from os.path import basename
import os
import pandas as pd
import shutil

data_folder = "data"
output_folder = "processed_tables"
temp_folder = "./temp"
try:
    os.mkdir(output_folder)
except:
    pass

class StructuralCharacterization():
    """Structural Properties Class"""
    def __init__(self, sequence):
        self.sequence = sequence
        self.temp_folder = temp_folder
        try:
            os.mkdir(self.temp_folder)
        except:
            pass
        self.rand_number = str(round(random() * 10**20))
        self.output_path = f"{self.temp_folder}/{self.rand_number}"
        self.temp_file_path = f"{self.temp_folder}/{self.rand_number}.fasta"
        self.predictions = ["ss3", "ss8", "acc", "diso", "tm2", "tm8"]
        self.options = {
            "ss3": 1,
            "ss8": 1,
            "acc": 1,
            "tm2": 1,
            "tm8": 1,
            "diso": 1
        }
    
    def create_file(self):
        with open(self.temp_file_path, "w", encoding = "utf-8") as fasta_file:
            fasta_file.write(f">{self.rand_number}\n{self.sequence}")

    def execute_predict_property(self):
        """Execute Predict Property software"""
        command = [
            "./Predict_Property/Predict_Property.sh",
            "-i",
            self.temp_file_path,
            "-o",
            self.output_path,
        ]
        subprocess.check_output(command)

    def parse_results(self):
        """Parse output files"""
        all_file = basename(self.temp_file_path).replace("fasta", "all")
        with open(f"{self.output_path}/{all_file}", "r", encoding = "utf-8") as file:
            lines = file.readlines()
        self.name = lines[0].split(" ")[0].replace(">", "")[:-1]
        self.alignment = [{"id": 1, "label": self.name, "sequence": lines[1].replace("\n", "")}]
        for index, prediction_name in enumerate(self.predictions):
            if self.options[prediction_name]:
                self.alignment.append({
                    "id": index + 2,
                    "label": prediction_name,
                    "sequence": lines[index + 2].replace("\n", "")
                })

            
    def delete_files(self):
        try:
            os.remove(self.temp_file_path)
        except:
            pass
        try:
            shutil.rmtree(self.output_path)
        except:
            pass


    def run_process(self):
        """Run all process"""
        try:
            self.create_file()
            self.execute_predict_property()
            self.parse_results()
            self.delete_files()
            return self.alignment
        except Exception as e:
            print(e)
            self.delete_files()
            return None

def process(file):
    data = pd.read_csv(f"{data_folder}/{file}")
    data = data[0:20] ##Comentar esta linea al tirar el script con todos los datos
    data.fillna("")
    for index, row in data.iterrows():
        if row.is_aa_seq:
            struct_obj = StructuralCharacterization(row.sequence)
            res = struct_obj.run_process()
            if res is not None:
                for col in res[1:]:
                    data.loc[index, col["label"]] = col["sequence"]
    data.to_csv(f"{output_folder}/{file}")

if __name__ == "__main__":
    for file in os.listdir(data_folder):
        process(file)
    os.rmdir(temp_folder)