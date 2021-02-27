import os
from datetime import date
from pathlib import Path
from zipfile import ZipFile
import requests
import pandas as pd

class MasterData :
    
    def __init__(self, master_data, edgar_prefix) :
        self._edgar_prefix = edgar_prefix
        self._master_data_df = self._to_master_data_df(master_data)
        
    @property
    def df(self) -> pd.DataFrame :
        return self._master_data_df
    
    def _to_master_data_df(self, content:str)-> pd.DataFrame :
        result = []
        headers_start = False
        headers_done = False
        for line in content.split("\n") :
            line = line.strip()
            if line == "":
                headers_start = True
            if headers_start and line != "" :
                headers_done = True
            if headers_done:
                result.append(line)
        
        header = [l.replace(" ", "_")for l in result[0].split('|')]
        content = [line.split("|") for line in result[2:-1]]
        
        df = pd.DataFrame(content, columns=header) 
        df["Filename"] = df["Filename"].apply(lambda x: self._edgar_prefix + x)
        return df


class Edgar :
    EDGAR_PREFIX = "https://www.sec.gov/Archives/"
    
    def __init__(self, dest_folder:Path=Path("/tmp/")) :
        self._dest_folder = dest_folder
    
    def _download_master_data(self, year:int, quarter:int) :
        assert quarter in range(1, 5), "quarter can be in [1,4]"
        
        src_path = f"{self.EDGAR_PREFIX}edgar/full-index/{year}/QTR{quarter}/master.zip"
        dest_path = self._dest_folder/f"{year}-QTR{quarter}.zip"
        if not os.path.exists(dest_path) :
            _response = requests.get(src_path, allow_redirects=True)
            open(dest_path, 'wb').write(_response.content)
        
        return dest_path
    
    def get_master_data(self, year:int=None, quarter:int=None) :
        if year is None :
            year = date.today().year
        if quarter is None :
            quarter = date.today().month // 3 + 1
        dest_path = self._download_master_data(year, quarter)
        
        with ZipFile(dest_path) as master_zip:
            with master_zip.open('master.idx') as master_idx:
                content = master_idx.read().decode("latin-1")
        
        return MasterData(content, self.EDGAR_PREFIX)

"""
from edgar from Edgar

ed = Edgar("download_dir")
master_data = ed.get_master_data(2020, 1)
df = master_data.df
"""