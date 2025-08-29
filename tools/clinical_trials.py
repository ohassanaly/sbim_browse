import os
import requests
import json
import logging
from datetime import datetime
from requests.exceptions import RequestException

run_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

log_path = f"logs/{run_stamp}_clinical_trials.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),]
)
logger = logging.getLogger(__name__)

def request_study_id(study_id : str, api_server : str, data_dir : str) :
    """
    Based on a NCT Trial ID, Fetch a study JSON from ClinicalTrials.gov API sand save it to disk

    Logs:
        INFO on success, WARNING/ERROR on different failure modes.
    """
    url = f"{api_server}/studies/{study_id}"
    try :
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except RequestException as e:
        logger.error("HTTP error fetching %s: %s", url, e)
        return
    
    try : 
        data = resp.json()
    except ValueError as e:
        logger.error("Invalid JSON for study %s: %s", study_id, e)
        return
    
    try :
        out_path = f"{data_dir}/{study_id}.json"
        with open(out_path, "w",  encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Saved study %s to %s", study_id, out_path)
            return
    except OSError as e:
        logger.error("Filesystem error saving %s: %s", study_id, e)
        return


if __name__ == "__main__":
    api_server = "https://clinicaltrials.gov/api/v2"
    data_dir = "data"
    study_id =  "NCT03540771"
    request_study_id(study_id, api_server, data_dir)