from enum import Enum
import subprocess

from upload.uploader import Uploader, FieldType


class ProcessStatTags(Enum):
    PPID = ("Ppid", FieldType.INTEGER)
    PID = ("Pid", FieldType.INTEGER)
    COMM = ("Comm", FieldType.STRING)
    STATE = ("State", FieldType.STRING)
    CPU = ("CPU", FieldType.FLOAT)
    RSS = ("RSS", FieldType.INTEGER)
    READS = ("Reads", FieldType.FLOAT)
    WRITES = ("Writes", FieldType.FLOAT)
    UPTIME = ("Uptime(sec)", FieldType.FLOAT)
    CGROUP = ("Cgroup", FieldType.STRING)
    CMDLINE = ("Cmdline", FieldType.STRING)
    EXE_PATH = ("Exe Path", FieldType.STRING)


class ProcessStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = [
            "below",
            "dump",
            "process",
            "--begin",
            f"{self.interval}s",
            "--raw",
            "-O",
            "csv",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error collecting process stats:", result.stderr)
            return None
        return result.stdout

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        upload_tags = self.get_upload_tags(
            "PROCESS_UPLOAD_TAGS",
            ProcessStatTags,
        )
        formatted_data = self.csv_to_line_protocol(
            raw_data,
            "process_stats",
            ["Pid", "Comm"],
            upload_tags,
        )
        self.upload_lines(formatted_data)
