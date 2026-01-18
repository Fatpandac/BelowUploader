from enum import Enum
import subprocess

from upload.uploader import Uploader, FieldType


class DiskStatTags(Enum):
    DISK = ("Disk", FieldType.STRING)
    MAJOR = ("Major", FieldType.INTEGER)
    MINOR = ("Minor", FieldType.INTEGER)
    READ = ("Read", FieldType.FLOAT)
    READ_COMPLETED = ("Read Completed", FieldType.INTEGER)
    READ_MERGED = ("Read Merged", FieldType.INTEGER)
    READ_SECTORS = ("Read Sectors", FieldType.INTEGER)
    TIME_SPEND_READ = ("Time Spend Read", FieldType.INTEGER)
    WRITE = ("Write", FieldType.FLOAT)
    WRITE_COMPLETED = ("Write Completed", FieldType.INTEGER)
    WRITE_MERGED = ("Write Merged", FieldType.INTEGER)
    WRITE_SECTORS = ("Write Sectors", FieldType.INTEGER)
    TIME_SPEND_WRITE = ("Time Spend Write", FieldType.INTEGER)
    DISCARD = ("Discard", FieldType.FLOAT)
    DISCARD_COMPLETED = ("Discard Completed", FieldType.INTEGER)
    DISCARD_MERGED = ("Discard Merged", FieldType.INTEGER)
    DISCARD_SECTORS = ("Discard Sectors", FieldType.INTEGER)
    TIME_SPEND_DISCARD = ("Time Spend Discard", FieldType.INTEGER)
    DISK_USAGE = ("Disk Usage", FieldType.FLOAT)
    PARTITION_SIZE = ("Partition Size", FieldType.INTEGER)
    FILESYSTEM_TYPE = ("Filesystem Type", FieldType.STRING)


class DiskStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = [
            "below",
            "dump",
            "disk",
            "--begin",
            f"{self.interval}s",
            "--raw",
            "-O",
            "csv",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error collecting disk stats:", result.stderr)
            return None
        return result.stdout

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        upload_tags = self.get_upload_tags(
            "DISK_UPLOAD_TAGS",
            DiskStatTags,
        )
        formatted_data = self.csv_to_line_protocol(
            raw_data, "disk_stats", ["Name"], upload_tags
        )
        self.upload_lines(formatted_data)
