import subprocess

from upload.uploader import Uploader, FieldType


class SystemStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = ["below", "dump", "system", "-d", "--begin", f"{self.interval}s", "--raw", "-O", "csv"]
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
            "system_stats",
            ["Hostname"],
            [
                ("Usage", FieldType.FLOAT),
                ("User", FieldType.FLOAT),
                ("System", FieldType.FLOAT),
                ("Total", FieldType.INTEGER),
                ("Free", FieldType.INTEGER),
                ("Available", FieldType.INTEGER),
                ("Page In", FieldType.FLOAT),
                ("Page Out", FieldType.FLOAT),
                ("Swap In", FieldType.FLOAT),
                ("Swap Out", FieldType.FLOAT),
                ("Pgsteal Kswapd", FieldType.FLOAT),
                ("Pgsteal Direct", FieldType.FLOAT),
                ("Pgscan Kswapd", FieldType.FLOAT),
                ("Pgscan Direct", FieldType.FLOAT),
                ("OOM Kills", FieldType.FLOAT),
                ("Total Interrupts", FieldType.INTEGER),
                ("Context Switches", FieldType.INTEGER),
                ("Boot Time Epoch", FieldType.INTEGER),
                ("Total Procs", FieldType.INTEGER),
                ("Running Procs", FieldType.FLOAT),
                ("Blocked Procs", FieldType.FLOAT),
            ],
        )
        self.upload_lines(formatted_data)
