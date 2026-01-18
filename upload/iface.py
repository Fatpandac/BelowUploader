from enum import Enum
import subprocess

from upload.uploader import Uploader, FieldType


class InterfaceStatTags(Enum):
    INTERFACE = ("Interface", FieldType.STRING)
    RX_PACKETS = ("RX Packets", FieldType.INTEGER)
    TX_PACKETS = ("TX Packets", FieldType.INTEGER)
    RX_ERRORS = ("RX Errors", FieldType.INTEGER)
    TX_ERRORS = ("TX Errors", FieldType.INTEGER)
    RX_DROPPED = ("RX Dropped", FieldType.INTEGER)
    TX_DROPPED = ("TX Dropped", FieldType.INTEGER)
    RX_BYTES = ("RX Bytes", FieldType.INTEGER)
    TX_BYTES = ("TX Bytes", FieldType.INTEGER)


class InterfaceStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = [
            "below",
            "dump",
            "iface",
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

    def get_tags(self):
        upload_tags = self.get_upload_tags(
            "IFACE_UPLOAD_TAGS",
            InterfaceStatTags,
        )
        print("Upload tags:", upload_tags)

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        upload_tags = self.get_upload_tags(
            "IFACE_UPLOAD_TAGS",
            InterfaceStatTags,
        )
        formatted_data = self.csv_to_line_protocol(
            raw_data, "iface_stats", ["Interface"], upload_tags
        )
        self.upload_lines(formatted_data)
