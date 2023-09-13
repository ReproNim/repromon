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
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9." \
               "eyJzdWIiOiJwb3dlcnVzZXIiLCJleHAiOjE3MjIzNjI4NzR9." \
               "jwbOzIVemgzxV6A2HHR-iBtNyGYXQA1B4S4uFj6x-9A"
API_KEY = "343c5.vssTjxCNnOIwgzXmmOWQw870AogZp8JxEjqOd3MB"
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
        "level": MessageLevelId.WARNING,
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
        "level": MessageLevelId.WARNING,
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

        # sample for OAuth2+JWT access token
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }

        # sample for API Key auth
        # headers = {
        #     "X-Api-Key": API_KEY
        # }

        response = requests.post(f"{API_BASE_URL}/message/send_message",
                                 params=params,
                                 headers=headers)

        if response.status_code == 200:
            logger.debug("Message sent successfully")
            count_success += 1
        else:
            logger.error(f"Message sending failed, {response.status_code}: "
                         f"{response.content}")
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
