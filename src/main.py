from clinical_trials import *
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    run_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_path = f"logs/{run_stamp}_full_clinical_trials.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
    )
    logger = logging.getLogger(__name__)

    df = pd.read_excel(r"C:\DonneesLocales\vsc\sbim_browse\data\ATMP_NCT.xlsx")
    df = df[~df.nct.isna()]
    df["nct"] = df["nct"].str.replace("KCT", "NCT", regex=False)
    print(df.nct.nunique())

    for nct in tqdm(df.nct.tolist()):
        request_study_id(
            study_id=nct.strip(),
            api_server="https://clinicaltrials.gov/api/v2",
            data_dir="data/full_nct_extract",
            logger=logger,
        )
