# esg_ml/adaptadores/entrada/leitor_kaggle.py
import os
import shutil
import pandas as pd


class LeitorKaggle:
    DATASET = 'alistairking/public-company-esg-ratings-dataset'

    def carregar(self, destino: str) -> pd.DataFrame:
        """Retorna o DataFrame do dataset ESG.

        Se `destino` já existir (bind mount persistente), usa o arquivo local
        sem fazer nenhuma chamada de rede. Só baixa do Kaggle quando ausente.
        """
        if not os.path.exists(destino):
            self._baixar(destino)
        return pd.read_csv(destino)

    def _baixar(self, destino: str) -> None:
        os.makedirs(os.path.dirname(destino), exist_ok=True)

        usuario = os.getenv('KAGGLE_USERNAME', '')
        chave   = os.getenv('KAGGLE_KEY', '')
        if not usuario or not chave:
            raise RuntimeError(
                "Dataset ausente e credenciais Kaggle não encontradas.\n"
                "Opção 1 — defina no .env:\n"
                "  KAGGLE_USERNAME=seu_usuario\n"
                "  KAGGLE_KEY=sua_chave_api\n"
                "Opção 2 — copie o arquivo manualmente para data/raw/data.csv\n"
                "  (baixe em: https://www.kaggle.com/datasets/"
                f"{self.DATASET})"
            )

        try:
            import kagglehub
            path = kagglehub.dataset_download(self.DATASET)
        except Exception as exc:
            raise RuntimeError(
                f"Falha ao baixar '{self.DATASET}' do Kaggle: {exc}\n"
                "Verifique se KAGGLE_USERNAME e KAGGLE_KEY estão corretos, "
                "ou copie data/raw/data.csv manualmente."
            ) from exc

        csvs = sorted(f for f in os.listdir(path) if f.lower().endswith('.csv'))
        if not csvs:
            raise FileNotFoundError(
                f"Nenhum CSV encontrado no pacote Kaggle baixado em: {path}"
            )
        shutil.copy(os.path.join(path, csvs[0]), destino)
