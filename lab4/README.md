# Lab 4 — GoF Strategy Pattern

Implementation of the ** GoF Strategy** design pattern for outputting data to multiple storages.

**Dataset (variant 28):** NCDC Storm Events Database  
https://catalog.data.gov/dataset/ncdc-storm-events-database

## Project structure

```
lab4/
├── main.py                          ← Entry point
├── download_data.py                 ← Downloads dataset from NCEI
├── config/
│   └── app.yml                      ← Strategy selection + connection settings
├── data/
│   └── storm_events.csv             ← Downloaded dataset (generated)
├── requirements.txt
└── app/
    ├── reader.py                    ← Reads CSV file, yields dicts (no output logic)
    ├── factory.py                   ← Creates strategy instance from config
    └── strategy/
        ├── base.py                  ← IOutputStrategy (ABC)
        ├── console_strategy.py      ← Prints rows to stdout
        ├── kafka_strategy.py        ← Sends rows as JSON to Kafka topic
        └── redis_strategy.py        ← Appends rows as JSON to Redis list
```

---

## Setup

### 1. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2. Download the dataset

```bash
python download_data.py              # downloads 2025 storm events
python download_data.py --year 2023  # or choose a different year
```

The CSV is saved to `data/storm_events.csv`.

### 3. Configure output strategy

Edit `config/app.yml`:

```yaml
output:
  strategy: console   # ← change to: kafka | redis
```

### 4. Run

```bash
python main.py
```

---

## Switching strategies (config only)

### Console (default)
```yaml
output:
  strategy: console
```

### Kafka
```yaml
output:
  strategy: kafka

kafka:
  bootstrap_servers: "localhost:9092"
  topic: "storm-events"
```

### Redis
```yaml
output:
  strategy: redis

redis:
  host: "localhost"
  port: 6379
  key: "storm-events"
```

---

## How the Strategy pattern is applied

| Component | Role |
|---|---|
| `IOutputStrategy` | Abstract strategy interface (`output`, `close`) |
| `ConsoleOutputStrategy` | Concrete strategy — stdout |
| `KafkaOutputStrategy` | Concrete strategy — Kafka topic |
| `RedisOutputStrategy` | Concrete strategy — Redis list |
| `create_strategy(config)` | Factory that selects the concrete strategy |
| `read_csv(...)` | Context-independent data source, knows nothing about output |
| `main.py` | Context — wires reader + strategy together |
