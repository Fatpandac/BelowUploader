import os, csv
from datetime import datetime
from enum import Enum
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import WriteApi, InfluxDBClient

class FieldType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"


type Field = tuple[str, FieldType]


class Uploader:
    token: str
    bucket: str
    org: str
    url: str
    interval: int
    write_api: WriteApi

    def __init__(self):
        self.token = os.getenv("INFLUXDB_TOKEN")
        self.bucket = os.getenv("INFLUXDB_BUCKET")
        self.org = os.getenv("INFLUXDB_ORG")
        self.url = os.getenv("INFLUXDB_URL")
        self.interval = int(os.getenv("UPLOAD_INTERVAL_SECONDS", "60"))
        write_client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = write_client.write_api(write_options=SYNCHRONOUS)

    def escape_string_value(self, value: str) -> str:
        if value == "?" or value == "":
            return '""'
        escaped_value = (
            str(value)
            .strip()
            .replace("\\", "\\\\")
            .replace(" ", r"\ ")
            .replace(",", r"\,")
            .replace("=", r"\=")
        )
        return escaped_value

    def format_value(self, value: str, field_type: FieldType) -> str:
        switcher = {
            FieldType.INTEGER: lambda v: f"{int(v)}i" if v != "?" and v != "" else "0i",
            FieldType.FLOAT: lambda v: str(float(v)) if v != "?" and v != "" else "0.0",
            FieldType.STRING: lambda v: f'"{self.escape_string_value(v)}"',
        }

        return f'{switcher[field_type](value)}'

    def format_key(self, key: str) -> str:
        return key.strip().replace("(", "_").replace(")", "").replace("/", "_").replace(" ", "_")

    def csv_to_line_protocol(
        self,
        raw_csv: str,
        measurement: str,
        tags: list[str],
        fields: list[tuple[str, FieldType]],
    ) -> list[str]:
        reader = csv.DictReader(raw_csv.splitlines())
        lines = []
        for row in reader:
            try:
                timestamp = int(row.get("Timestamp")) * 1_000_000_000
            except (TypeError, ValueError):
                timestamp = int(datetime.now().timestamp()) * 1_000_000_000

            tags_str = []
            for tag in tags:
                if tag in row:
                    tags_str.append(
                        f"{self.format_key(tag)}={self.escape_string_value(row[tag])}"
                    )
            field_str = []
            for field in fields:
                (field_name, field_type) = field
                if field_name in row:
                    field_str.append(
                        f"{self.format_key(field_name)}={self.format_value(row[field_name], field_type)}"
                    )

            line = f"{measurement},{','.join(tags_str)} {','.join(field_str)} {timestamp}"
            lines.append(line)

        return lines

    def upload_lines(self, lines: list[str]):
        resp = self.write_api.write(
            bucket=self.bucket, org=self.org, record="\n".join(lines)
        )
        if resp is None:
            print(f"Uploaded {len(lines)} lines to InfluxDB")
