# 🛒 FastAPI Product Microservice

...

## 🧩 Master-Slave Architecture (Optional Advanced)

To implement master-slave DB read/write separation:

1. Use SQLAlchemy's bind feature for two engines:
   - `master_engine` → write operations
   - `slave_engine` → read operations

2. Example:
```python
# db/database.py
from sqlalchemy import create_engine
master_engine = create_engine(settings.DB_URL)
slave_engine = create_engine(settings.READ_REPLICA_URL)  # Add to .env

def get_master_session():
    return sessionmaker(bind=master_engine)()

def get_slave_session():
    return sessionmaker(bind=slave_engine)()
```

3. Modify services to choose between read/write session.

> Note: You must configure DB replication between master and replica.

...
