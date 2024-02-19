import pandas as pd
from fastapi import UploadFile
import joblib
from io import StringIO
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


class CSVDataProcessor:
    def __init__(self, scaler_path=None):
        self.scaler_path = scaler_path
        self.scaler = None
        self.df = None

    async def process(self, file: UploadFile):
        contents = await file.read()
        self.df = pd.read_csv(StringIO(contents.decode('utf-8')))
        self.load_scaler()
        self.validate_numeric_columns()
        self.clean_data()
        self.encode_binary_columns()
        self.one_hot_encode()
        self.normalize()
        return self.df

    def load_scaler(self):
        if self.scaler_path:
            try:
                self.scaler = joblib.load(self.scaler_path)
            except FileNotFoundError:
                print(f"Scaler file {self.scaler_path} not found. A new scaler will be created.")

    def validate_numeric_columns(self):
        numeric_columns = self.df.select_dtypes(include=[float, int]).columns
        for column in numeric_columns:
            if self.df[column].apply(lambda x: not pd.to_numeric(x, errors='coerce').notnull().all()):
                raise ValueError(f"Non-numeric values found in column: {column}")

    def clean_data(self):
        self.df = self.df.replace('--', None)
        self.df = self.df.dropna(axis=0, how='any')

        if 'Grade' in self.df.columns:
            self.df = self.df.drop(columns=['Grade'])

        self.df['age'] = self.df['Age_at_diagnosis'].apply(lambda x: int(x.split(' ')[0]))
        drop_columns = ['Project', 'Case_ID', 'Primary_Diagnosis', 'FUBP1', 'Age_at_diagnosis']
        self.df = self.df.drop(columns=drop_columns)

    def encode_binary_columns(self):
        binary_columns = ['Gender', 'IDH1', 'TP53', 'ATRX', 'PTEN', 'EGFR',
                          'CIC', 'MUC16', 'PIK3CA', 'NF1', 'PIK3R1', 'RB1',
                          'NOTCH1', 'BCOR', 'CSMD3', 'SMARCA4', 'GRIN2A',
                          'IDH2', 'FAT4', 'PDGFRA']
        for column in binary_columns:
            if column in self.df.columns:
                label_encoder = LabelEncoder()
                self.df[column] = label_encoder.fit_transform(self.df[column])

    def one_hot_encode(self):
        self.df = pd.get_dummies(self.df, columns=['Race'])
        self.df = self.df.apply(lambda x: x.map({True: 1, False: 0}) if x.dtype == 'bool' else x)

    def normalize(self):
        if 'age' in self.df.columns:
            if self.scaler is None:
                self.scaler = MinMaxScaler()
                self.df['age'] = self.scaler.fit_transform(self.df[['age']])
            else:
                self.df['age'] = self.scaler.transform(self.df[['age']])


file = open("file.csv", "r")
csv_processor = CSVDataProcessor()
csv_processor.process(file)
