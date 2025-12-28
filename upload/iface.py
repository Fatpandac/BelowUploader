import subprocess

from upload.uploader import Uploader, FieldType


class InterfaceStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = ["below", "dump", "iface", "-d", "--begin", f"{self.interval}s", "--raw", "-O", "csv"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error collecting system stats:", result.stderr)
            return None
        return result.stdout

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        formatted_data = self.csv_to_line_protocol(
            raw_data,
            "iface_stats",
            ["Interface"],
            [
                ("I/O Bytes/s", FieldType.STRING),
                ("RX Bytes", FieldType.INTEGER),
                ("RX Bytes/s", FieldType.FLOAT),
                ("RX Dropped", FieldType.INTEGER),
                ("RX Errors", FieldType.INTEGER),
                ("TX Bytes", FieldType.INTEGER),
                ("TX Bytes/s", FieldType.FLOAT),
                ("TX Dropped", FieldType.INTEGER),
                ("TX Errors", FieldType.INTEGER),
            ],
        )
        self.upload_lines(formatted_data)
