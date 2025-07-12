# Apache Hive PostgreSQL Driver Fix
```bash
mkdir -p lib
wget -O lib/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.2.jar
```

```yaml
version: '3.8'

services:
  postgres:
    ...
    volumes:
      - ./data/hive_db:/var/lib/postgresql/data

  metastore:
    volumes:
      - ./lib/postgresql.jar:/opt/hive/lib/postgresql.jar  # ← Add this line
    ports:
      - "9083:9083"

  hiveserver2:
    ...
    volumes:
      - ./data/warehouse:/opt/hive/data/warehouse
      - ./lib/postgresql.jar:/opt/hive/lib/postgresql.jar  # ← Add this line
    ports:
      - "10000:10000"
      - "10002:10002"

volumes:
  warehouse:
  hive_db:
```