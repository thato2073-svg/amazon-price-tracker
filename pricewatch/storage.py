from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd
from pricewatch.models import ProductSnapshot

DB_PATH = Path("pricewatch.db")

def initialize(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS products (
            url TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            currency TEXT NOT NULL,
            target_price REAL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            captured_at TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(url) REFERENCES products(url)
        )""")

def save_snapshot(snapshot: ProductSnapshot, target_price: float | None = None, db_path: Path = DB_PATH) -> None:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """INSERT INTO products(url,title,currency,target_price) VALUES(?,?,?,?)
               ON CONFLICT(url) DO UPDATE SET title=excluded.title,currency=excluded.currency,
               target_price=COALESCE(excluded.target_price, products.target_price)""",
            (snapshot.url, snapshot.title, snapshot.currency, target_price),
        )
        conn.execute(
            "INSERT INTO observations(url,captured_at,price) VALUES(?,?,?)",
            (snapshot.url, snapshot.captured_at.isoformat(), snapshot.price),
        )

def history(url: str, db_path: Path = DB_PATH) -> pd.DataFrame:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        frame = pd.read_sql_query(
            "SELECT captured_at, price FROM observations WHERE url=? ORDER BY captured_at",
            conn, params=(url,),
        )
    if not frame.empty:
        frame["captured_at"] = pd.to_datetime(frame["captured_at"], utc=True)
        frame = frame.set_index("captured_at")
    return frame

def products(db_path: Path = DB_PATH) -> pd.DataFrame:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(
            """SELECT p.url,p.title,p.currency,p.target_price,
               o.price AS current_price,o.captured_at
               FROM products p
               LEFT JOIN observations o ON o.id=(
                 SELECT id FROM observations WHERE url=p.url ORDER BY captured_at DESC LIMIT 1
               ) ORDER BY p.title""", conn,
        )
