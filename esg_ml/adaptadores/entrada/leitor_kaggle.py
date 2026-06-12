# esg_ml/adaptadores/entrada/leitor_kaggle.py
# Porta: RepositorioDadosBrutos → KaggleHub
import os, shutil
import pandas as pd

class LeitorKaggle:
    DATASET = 'alistairking/public-company-esg-ratings-dataset'

    def carregar(self, destino: str) -> pd.DataFrame:
        import kagglehub
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        path = kagglehub.dataset_download(self.DATASET)
        shutil.copy(os.path.join(path, os.listdir(path)[0]), destino)
        return pd.read_csv(destino)
