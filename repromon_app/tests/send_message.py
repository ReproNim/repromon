import copy
import json
import logging.config
import random
import time
from datetime import datetime, timedelta

import requests

from repromon_app.config import app_config_init
from repromon_app.model import (DataProviderId, MessageCategoryId,
                                MessageLevelId)

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


API_BASE_URL = "http://localhost:9095/api/1"
SAMPLE_MESSAGES = [
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.INFO,
        "device": 1,
        "provider": DataProviderId.REPROSTIM,
        "description": "stimuli display dis-connected",
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.INFO,
        "device": 1,
        "provider": DataProviderId.REPROSTIM,
        "description": "stimuli display connected(1024x768, …)",
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.ERROR,
        "device": 1,
        "provider": DataProviderId.REPROSTIM,
        "description": "stimuli display error",
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.WARN,
        "device": 1,
        "provider": DataProviderId.REPROSTIM,
        "description": "stimuli display caution",
    },
    {
        "study": "Halchenko/Horea/1020_animal_mri",
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.ERROR,
        "device": 1,
        "provider": DataProviderId.NOISSEUR,
        "description": "subject 'John' is not conformant, must match "
                       "[0-9]{6} regular expression. [link to screen with highlight]"
    },
    {
        "study": "Halchenko/Horea/1020_animal_mri",
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.INFO,
        "device": 1,
        "provider": DataProviderId.NOISSEUR,
        "description": "proceeded with compliant data on study "
                       "Halchenko/Horea/1020_animal_mri"
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.INFO,
        "device": 1,
        "provider": DataProviderId.REPROEVENTS,
        "description": "MRI trigger event received"
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.ERROR,
        "device": 1,
        "provider": DataProviderId.REPROEVENTS,
        "description": "MRI trigger unexpected error"
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.INFO,
        "device": 1,
        "provider": DataProviderId.DICOM_QA,
        "description": "MRI data lacks rear head coils data "
                       "[link to PACS recording to review]"
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.ERROR,
        "device": 1,
        "provider": DataProviderId.DICOM_QA,
        "description": "Some DICOM/QA error"
    },
    {
        "study": None,
        "category": MessageCategoryId.FEEDBACK,
        "level": MessageLevelId.WARN,
        "device": 1,
        "provider": DataProviderId.DICOM_QA,
        "description": "Warning in DICOM/QA"
    },

]

count_all: int = 0
count_success: int = 0


def send_message():
    print("send_message()")
    global count_all, count_success
    count_all += 1
    try:
        # Define your query parameters
        params = copy.copy(random.choice(SAMPLE_MESSAGES))

        # set sporadically event_on/registered_on time manually
        if random.choice([False, True, False]):
            dt_sec = random.randint(10, 600)
            params["event_on"] = (datetime.now() - timedelta(seconds=dt_sec)).isoformat()
            if random.choice([True, False, True]):
                params["registered_on"] = \
                    (datetime.now() - timedelta(seconds=int(dt_sec / 2))).isoformat()

        logger.debug(f"params={json.dumps(params, indent=4)}")

        response = requests.post(f"{API_BASE_URL}/message/send_message", params=params)

        if response.status_code == 200:
            logger.debug("Message sent successfully")
            count_success += 1
        else:
            logger.error("Message sending failed")
    except BaseException as ex:
        logger.error(f"UNHANDLED ERROR: {str(ex)}")

    logger.info(f"Total count: {count_all}, success count: {count_success}, "
                f"error_count: {str(count_all-count_success)}")


def main():
    app_config_init()

    while True:
        send_message()
        time.sleep(random.randint(1, 5))


if __name__ == "__main__":
    main()
