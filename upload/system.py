from enum import Enum
import subprocess

from upload.uploader import Uploader, FieldType


class SystemStatTags(Enum):
    HOSTNAME = ("Hostname", FieldType.STRING)
    USAGE = ("Usage", FieldType.FLOAT)
    SYSTEM = ("System", FieldType.FLOAT)
    USER = ("User", FieldType.FLOAT)
    TOTAL = ("Total", FieldType.INTEGER)
    FREE = ("Free", FieldType.INTEGER)
    AVAILABLE = ("Available", FieldType.INTEGER)
    PAGE_IN = ("Page In", FieldType.FLOAT)
    PAGE_OUT = ("Page Out", FieldType.FLOAT)
    SWAP_IN = ("Swap In", FieldType.FLOAT)
    SWAP_OUT = ("Swap Out", FieldType.FLOAT)
    PGSTEAL_KSWAPD = ("Pgsteal Kswapd", FieldType.FLOAT)
    PGSTEAL_DIRECT = ("Pgsteal Direct", FieldType.FLOAT)
    PGSCAN_KSWAPD = ("Pgscan Kswapd", FieldType.FLOAT)
    PGSCAN_DIRECT = ("Pgscan Direct", FieldType.FLOAT)
    OOM_KILLS = ("OOM Kills", FieldType.FLOAT)
    TOTAL_INTERRUPTS = ("Total Interrupts", FieldType.INTEGER)
    CONTEXT_SWITCHES = ("Context Switches", FieldType.INTEGER)
    BOOT_TIME_EPOCH = ("Boot Time Epoch", FieldType.INTEGER)
    TOTAL_PROCS = ("Total Procs", FieldType.INTEGER)
    RUNNING_PROCS = ("Running Procs", FieldType.FLOAT)
    BLOCKED_PROCS = ("Blocked Procs", FieldType.FLOAT)


class SystemStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = [
            "below",
            "dump",
            "system",
            "-d",
            "--begin",
            f"{self.interval}s",
            "--raw",
            "-O",
            "csv",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error collecting system stats:", result.stderr)
            return None
        return result.stdout

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        upload_tags = self.get_upload_tags(
            "SYSTEM_UPLOAD_TAGS",
            SystemStatTags,
        )
        formatted_data = self.csv_to_line_protocol(
            raw_data,
            "system_stats",
            ["Hostname"],
            upload_tags,
        )
        self.upload_lines(formatted_data)
