import subprocess

from upload.uploader import Uploader, FieldType


class DiskStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = ["below", "dump", "disk", "--begin", "1m", "--raw", "-O", "csv"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error collecting disk stats:", result.stderr)
            return None
        return result.stdout

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        formatted_data = self.csv_to_line_protocol(
            raw_data,
            "disk_stats",
            ["Name"],
            [
                ("Disk", FieldType.STRING),
                ("Major", FieldType.INTEGER),
                ("Minor", FieldType.INTEGER),
                ("Read", FieldType.FLOAT),
                ("Read Completed", FieldType.INTEGER),
                ("Read Merged", FieldType.INTEGER),
                ("Read Sectors", FieldType.INTEGER),
                ("Time Spend Read", FieldType.INTEGER),
                ("Write", FieldType.FLOAT),
                ("Write Completed", FieldType.INTEGER),
                ("Write Merged", FieldType.INTEGER),
                ("Write Sectors", FieldType.INTEGER),
                ("Time Spend Write", FieldType.INTEGER),
                ("Discard", FieldType.FLOAT),
                ("Discard Completed", FieldType.INTEGER),
                ("Discard Merged", FieldType.INTEGER),
                ("Discard Sectors", FieldType.INTEGER),
                ("Time Spend Discard", FieldType.INTEGER),
                ("Disk Usage", FieldType.FLOAT),
                ("Partition Size", FieldType.INTEGER),
                ("Filesystem Type", FieldType.STRING),
            ],
        )
        self.upload_lines(formatted_data)
