import subprocess

from upload.uploader import Uploader, FieldType


class ProcessStatsUploader(Uploader):
    def __init__(self):
        super().__init__()

    def collect(self):
        cmd = ["below", "dump", "process", "--begin", "1m", "--raw", "-O", "csv"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error collecting process stats:", result.stderr)
            return None
        return result.stdout

    def collect_and_upload(self):
        raw_data = self.collect()
        if raw_data is None:
            return
        formatted_data = self.csv_to_line_protocol(
            raw_data,
            "process_stats",
            ["Pid", "Comm"],
            [
                ("Ppid", FieldType.INTEGER),
                ("State", FieldType.STRING),
                ("CPU", FieldType.FLOAT),
                ("RSS", FieldType.INTEGER),
                ("Reads", FieldType.FLOAT),
                ("Writes", FieldType.FLOAT),
                ("Uptime(sec)", FieldType.FLOAT),
                ("Cgroup", FieldType.STRING),
                ("Cmdline", FieldType.STRING),
                ("Exe Path", FieldType.STRING),
            ],
        )
        self.upload_lines(formatted_data)
