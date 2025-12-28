import os
import time
from dotenv import load_dotenv

from upload import (
    DiskStatsUploader,
    SystemStatsUploader,
    ProcessStatsUploader,
    InterfaceStatsUploader,
)

load_dotenv()


def main():
    upload_interval = int(os.getenv("UPLOAD_INTERVAL_SECONDS", 5))
    uploader = [
        InterfaceStatsUploader(),
        ProcessStatsUploader(),
        SystemStatsUploader(),
        DiskStatsUploader(),
    ]

    while True:
        start_time = time.time()
        for uploader_instance in uploader:
            uploader_instance.collect_and_upload()
        print("All uploaders have completed their tasks.")

        elapsed_time = time.time() - start_time
        sleep_time = max(0, upload_interval - elapsed_time)
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
