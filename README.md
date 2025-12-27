# BelowUploader

BelowUploader is a Python tool that uploads dump data to [InfluxDB](https://www.influxdata.com/) and enables data visualization via [Grafana](https://grafana.com/).

## Quick Start

### 1. Install Dependencies

Make sure you have [`uv`](https://github.com/astral-sh/uv) installed. Then run:

```bash
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory. Example configuration:

```ini
INFLUXDB_URL=http://localhost:8086        # Your InfluxDB instance URL
INFLUXDB_TOKEN=my-influxdb-token          # InfluxDB API token
INFLUXDB_ORG=my-org                       # InfluxDB organization name
INFLUXDB_BUCKET=my-bucket                 # InfluxDB bucket name

UPLOAD_INTERVAL_SECONDS=5                 # Data upload interval in seconds. 
```

### 3. Start the Uploader

```bash
uv run main.py
```

---

## Visualization with Grafana

You can use Grafana to visualize the data stored in InfluxDB:

1. **Add InfluxDB as a Data Source**:  
   [Guide: Adding InfluxDB to Grafana](https://grafana.com/docs/grafana/latest/datasources/influxdb/)

2. **Create a Dashboard and Panels**:  
   Design panels and queries to visualize your uploaded data as you need.

> Example Grafana Panel  
> ![Grafana Example](/assets/grafana_example.png)

## Contribution

Pull requests, issues, and suggestions welcome!
