import os
import json
import pandas as pd
from tqdm import tqdm

folder_path = r"C:\DonneesLocales\vsc\sbim_browse\data\full_nct_extract"
# List all JSON files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

os.chdir(folder_path)

# testing for one study
# with open("NCT03575351.json", 'r', encoding="utf-8") as file:
#         data = json.load(file)
#         print(data.get("protocolSection", {}).get("statusModule", {}).get("lastUpdateSubmitDate"))

records = []

for file_name in tqdm(files):
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

        nct_id = (
            data.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
        )

        last_update = (
            data.get("protocolSection", {})
            .get("statusModule", {})
            .get("lastUpdateSubmitDate")
        )

        primary_outcomes = (
            data.get("protocolSection", {})
            .get("outcomesModule", {})
            .get("primaryOutcomes")
        )

        records.append(
            {
                "nct_id": nct_id,
                "last_update_submit_date": last_update,
                "primary_outcomes": primary_outcomes,
            }
        )

# formatting output
xdf = pd.DataFrame(records)
src_df = pd.read_excel(r"C:\DonneesLocales\vsc\sbim_browse\data\ATMP_NCT.xlsx")
src_df = src_df[~src_df.nct.isna()]
src_df["nct"] = src_df["nct"].str.replace("KCT", "NCT", regex=False)
src_df["nct"] = src_df["nct"].astype(str).str.strip()

df = src_df.merge(xdf, left_on="nct", right_on="nct_id", how="left")

df.to_csv(r"C:\DonneesLocales\vsc\sbim_browse\data\extracted.csv", sep=";")
