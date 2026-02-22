from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from models import Base, Agent, AgentRole, AgentStatus
import os
from pathlib import Path
import logging

# Get the directory where this script lives
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR.parent / "data"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Default to local SQLite in the data folder
DEFAULT_DB = f"sqlite:///{DATA_DIR}/mission_control.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables and migrate missing columns."""
    Base.metadata.create_all(bind=engine)
    
    # Auto-migrate missing columns for existing databases
    _run_migrations()
    
    print("Database initialized. Add agents via the Agent Management panel.")

def _run_migrations():
    """Add any missing columns to existing tables (SQLite compatible)."""
    with engine.connect() as conn:
        # Get existing columns in tasks table
        result = conn.execute(text("PRAGMA table_info(tasks)"))
        task_columns = [row[1] for row in result.fetchall()]
        
        # Define migrations: (column_name, column_type, default_value)
        task_migrations = [
            ("reviewer_id", "VARCHAR", None),
            ("due_at", "DATETIME", None),
            ("task_definition", "TEXT", None),
            ("parameters", "TEXT", None),
            ("owner_id", "VARCHAR", None),
        ]
        
        for col_name, col_type, default in task_migrations:
            if col_name not in task_columns:
                try:
                    sql = f"ALTER TABLE tasks ADD COLUMN {col_name} {col_type}"
                    if default is not None:
                        sql += f" DEFAULT {default}"
                    conn.execute(text(sql))
                    print(f"Migration: Added '{col_name}' column to tasks table")
                except Exception as e:
                    print(f"Migration warning for {col_name}: {e}")
        
        # Get existing columns in agents table
        result = conn.execute(text("PRAGMA table_info(agents)"))
        agent_columns = [row[1] for row in result.fetchall()]
        
        agent_migrations = [
            ("token", "VARCHAR", None),
            ("primary_model", "VARCHAR", None),
            ("fallback_model", "VARCHAR", None),
            ("current_model", "VARCHAR", None),
            ("model_failure_count", "INTEGER", "0"),
        ]
        
        for col_name, col_type, default in agent_migrations:
            if col_name not in agent_columns:
                try:
                    sql = f"ALTER TABLE agents ADD COLUMN {col_name} {col_type}"
                    if default is not None:
                        sql += f" DEFAULT {default}"
                    conn.execute(text(sql))
                    print(f"Migration: Added '{col_name}' column to agents table")
                except Exception as e:
                    print(f"Migration warning for {col_name}: {e}")

        # Get existing columns in recurring_tasks table
        result = conn.execute(text("PRAGMA table_info(recurring_tasks)"))
        rt_columns = [row[1] for row in result.fetchall()]

        rt_migrations = [
            ("task_definition", "TEXT", None),
            ("parameters", "TEXT", None),
            ("owner_id", "VARCHAR", None),
        ]

        for col_name, col_type, default in rt_migrations:
            if col_name not in rt_columns:
                try:
                    sql = f"ALTER TABLE recurring_tasks ADD COLUMN {col_name} {col_type}"
                    if default is not None:
                        sql += f" DEFAULT {default}"
                    conn.execute(text(sql))
                    print(f"Migration: Added '{col_name}' column to recurring_tasks table")
                except Exception as e:
                    print(f"Migration warning for {col_name}: {e}")

        # Get existing columns in recurring_task_runs table
        result = conn.execute(text("PRAGMA table_info(recurring_task_runs)"))
        run_columns = [row[1] for row in result.fetchall()]

        if "execution_time" not in run_columns:
            try:
                # If run_at exists, we could try to rename it, but simpler to just add execution_time
                conn.execute(text("ALTER TABLE recurring_task_runs ADD COLUMN execution_time DATETIME"))
                print("Migration: Added 'execution_time' column to recurring_task_runs table")
                # Copy data if run_at exists
                if "run_at" in run_columns:
                    conn.execute(text("UPDATE recurring_task_runs SET execution_time = run_at"))
                    print("Migration: Copied data from 'run_at' to 'execution_time'")
            except Exception as e:
                print(f"Migration warning for execution_time: {e}")
        
        conn.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
