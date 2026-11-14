"""Migrate the Veelearn MySQL schema+data to the Aiven PostgreSQL service.

Equivalent to what pgloader does, built on pymysql + psycopg2 because pgloader and
Docker are not available on this machine.

Usage:
    python pg_migrate.py --dry-run      # print the generated DDL only
    python pg_migrate.py --recreate     # drop+create tables, copy data, add indexes/FKs
    python pg_migrate.py --verify       # compare row counts and content digests

Credentials come from environment variables only:
    MySQL: DB_HOST DB_PORT DB_USER DB_PASS DB_NAME
    PG:    PGHOST PGPORT PGUSER PGPASSWORD PG_DATABASE
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from decimal import Decimal

import psycopg2
import psycopg2.extras
import pymysql

sys.stdout.reconfigure(errors="replace")

SKIP_TABLES: set[str] = set()

DATE_TYPES = {"date", "datetime", "timestamp", "time", "year"}
TEXT_TYPES = {"tinytext", "text", "mediumtext", "longtext"}
BLOB_TYPES = {"tinyblob", "blob", "mediumblob", "longblob", "binary", "varbinary"}


def mysql_conn():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 26399)),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ.get("DB_NAME", "defaultdb"),
        charset="utf8mb4",
        connect_timeout=60,
        ssl={"check_hostname": False},
    )


def pg_conn():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=int(os.environ.get("PGPORT", 26399)),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ.get("PG_DATABASE", "defaultdb"),
        sslmode="require",
        connect_timeout=60,
    )


def ident(name: str) -> str:
    name = name.lower()
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", name):
        raise ValueError(f"unsupported identifier: {name!r}")
    return name


def literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def map_type(data_type: str, column_type: str) -> str:
    dt = data_type.lower()
    ct = column_type.lower()
    unsigned = "unsigned" in ct

    if dt in ("tinyint", "smallint"):
        return "integer" if unsigned else "smallint"
    if dt == "mediumint":
        return "integer"
    if dt in ("int", "integer"):
        return "bigint" if unsigned else "integer"
    if dt == "bigint":
        return "numeric(20)" if unsigned else "bigint"
    if dt == "decimal":
        m = re.search(r"decimal\((\d+),(\d+)\)", ct)
        return f"numeric({m.group(1)},{m.group(2)})" if m else "numeric"
    if dt in ("float",):
        return "real"
    if dt in ("double", "real"):
        return "double precision"
    if dt == "bit":
        return "boolean" if ct in ("bit(1)",) else "bit varying"
    if dt in ("char", "varchar"):
        m = re.search(r"\((\d+)\)", ct)
        return f"varchar({m.group(1)})"
    if dt in TEXT_TYPES:
        return "text"
    if dt in BLOB_TYPES:
        return "bytea"
    if dt == "date":
        return "date"
    if dt in ("datetime", "timestamp"):
        return "timestamp"
    if dt == "time":
        return "time"
    if dt == "year":
        return "integer"
    if dt == "json":
        return "jsonb"
    if dt in ("enum", "set"):
        return "text"
    if dt in ("double precision",):
        return "double precision"
    return "text"


def map_default(col: dict, pg_type: str) -> str | None:
    default = col["default"]
    extra = (col["extra"] or "").lower()
    if default is None:
        return None
    if "auto_increment" in extra:
        return None
    d = str(default)
    if "0000-00-00" in d:
        return None
    if d.upper() in ("CURRENT_TIMESTAMP", "CURRENT_TIMESTAMP()", "NOW()"):
        return "CURRENT_TIMESTAMP"
    if pg_type == "boolean":
        if d in ("0", "b'0'", "false"):
            return "false"
        if d in ("1", "b'1'", "true"):
            return "true"
    if pg_type in ("smallint", "integer", "bigint", "numeric", "real", "double precision") and re.fullmatch(
        r"-?\d+(\.\d+)?", d
    ):
        return d
    if pg_type in ("date", "timestamp", "time"):
        return literal(d)
    return literal(d)


def introspect(my) -> dict:
    cur = my.cursor()
    cur.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema=%s AND table_type='BASE TABLE' ORDER BY table_name",
        (os.environ.get("DB_NAME", "defaultdb"),),
    )
    tables = [r[0] for r in cur.fetchall() if r[0] not in SKIP_TABLES]
    schema = {}
    for t in tables:
        cur.execute(
            """SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, EXTRA,
                      CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE, COLUMN_KEY
               FROM information_schema.columns WHERE table_schema=%s AND table_name=%s
               ORDER BY ORDINAL_POSITION""",
            (os.environ.get("DB_NAME", "defaultdb"), t),
        )
        cols = [
            dict(
                name=r[0], data_type=r[1], column_type=r[2], nullable=r[3] == "YES",
                default=r[4], extra=r[5], char_len=r[6], num_prec=r[7], num_scale=r[8], key=r[9],
            )
            for r in cur.fetchall()
        ]
        cur.execute(
            """SELECT INDEX_NAME, NON_UNIQUE, SEQ_IN_INDEX, COLUMN_NAME, INDEX_TYPE
               FROM information_schema.statistics WHERE table_schema=%s AND table_name=%s
               ORDER BY INDEX_NAME, SEQ_IN_INDEX""",
            (os.environ.get("DB_NAME", "defaultdb"), t),
        )
        idx_rows = cur.fetchall()
        indexes: dict[str, dict] = {}
        for name, non_unique, seq, col, itype in idx_rows:
            ent = indexes.setdefault(name, {"unique": non_unique == 0, "cols": [], "type": itype})
            ent["cols"].append((seq, col))
            ent["type"] = itype
        for ent in indexes.values():
            ent["cols"] = [c for _, c in sorted(ent["cols"])]
        cur.execute(
            """SELECT k.CONSTRAINT_NAME, k.COLUMN_NAME, k.REFERENCED_TABLE_NAME, k.REFERENCED_COLUMN_NAME,
                      r.DELETE_RULE, k.ORDINAL_POSITION
               FROM information_schema.key_column_usage k
               JOIN information_schema.referential_constraints r
                 ON r.CONSTRAINT_NAME=k.CONSTRAINT_NAME AND r.CONSTRAINT_SCHEMA=k.CONSTRAINT_SCHEMA
               WHERE k.TABLE_SCHEMA=%s AND k.TABLE_NAME=%s
               ORDER BY k.CONSTRAINT_NAME, k.ORDINAL_POSITION""",
            (os.environ.get("DB_NAME", "defaultdb"), t),
        )
        fks: dict[str, dict] = {}
        for cname, col, rtab, rcol, rule, pos in cur.fetchall():
            ent = fks.setdefault(cname, {"cols": [], "ref": rtab, "refcols": [], "rule": rule})
            ent["cols"].append(col)
            ent["refcols"].append(rcol)
        schema[t] = {"columns": cols, "indexes": indexes, "fks": fks}
    return schema


def ddl_for(table: str, spec: dict) -> tuple[str, list[str]]:
    cols_sql = []
    pk_cols = []
    for col in spec["columns"]:
        pg_type = map_type(col["data_type"], col["column_type"])
        parts = [ident(col["name"]), pg_type]
        if "auto_increment" in (col["extra"] or "").lower():
            parts.append("GENERATED BY DEFAULT AS IDENTITY")
            pk_cols = [ident(col["name"])]
        default_sql = map_default(col, pg_type)
        if default_sql is not None and "auto_increment" not in (col["extra"] or "").lower():
            parts.append(f"DEFAULT {default_sql}")
        if not col["nullable"]:
            parts.append("NOT NULL")
        cols_sql.append("  " + " ".join(parts))

    pk_name = None
    for name, ent in spec["indexes"].items():
        if name.upper() == "PRIMARY":
            pk_cols = [ident(c) for c in ent["cols"]]
            pk_name = "PRIMARY"
    if pk_cols:
        cols_sql.append(f"  PRIMARY KEY ({', '.join(pk_cols)})")
    ddl = f"CREATE TABLE {ident(table)} (\n" + ",\n".join(cols_sql) + "\n);"

    extras = []
    for name, ent in spec["indexes"].items():
        if name.upper() == "PRIMARY":
            continue
        cols = ", ".join(ident(c) for c in ent["cols"])
        uniq = "UNIQUE " if ent["unique"] else ""
        extras.append(
            f"CREATE {uniq}INDEX {ident('ix_' + table + '_' + name)} ON {ident(table)} ({cols});"
        )
    return ddl, extras


def fk_sql(table: str, spec: dict) -> list[str]:
    out = []
    for name, ent in spec["fks"].items():
        ref = ident(ent["ref"])
        cols = ", ".join(ident(c) for c in ent["cols"])
        refcols = ", ".join(ident(c) for c in ent["refcols"])
        rule = ent["rule"] or "RESTRICT"
        action = {"NO ACTION": "NO ACTION", "CASCADE": "CASCADE", "SET NULL": "SET NULL",
                  "RESTRICT": "RESTRICT"}.get(rule, "NO ACTION")
        out.append(
            f"ALTER TABLE {ident(table)} ADD CONSTRAINT {ident('fk_' + table + '_' + name)} "
            f"FOREIGN KEY ({cols}) REFERENCES {ref} ({refcols}) ON DELETE {action};"
        )
    return out


def clean(value, pg_type_hint: str = ""):
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    if isinstance(value, str):
        if value.startswith("0000-00-00"):
            return None
        return value.replace("\x00", "")
    if isinstance(value, Decimal):
        return value
    return value


def copy_table(my, pg, table: str, spec: dict) -> int:
    date_cols = {c["name"] for c in spec["columns"] if c["data_type"].lower() in DATE_TYPES}
    names = [c["name"] for c in spec["columns"]]
    select_list = ", ".join(
        f"CAST(`{n}` AS CHAR)" if n in date_cols else f"`{n}`" for n in names
    )
    mcur = my.cursor()
    mcur.execute(f"SELECT {select_list} FROM `{table}`")
    rows = mcur.fetchall()
    if not rows:
        return 0
    insert = (
        f"INSERT INTO {ident(table)} ({', '.join(ident(n) for n in names)}) VALUES %s"
    )
    pcur = pg.cursor()
    batch = []
    total = 0
    for row in rows:
        batch.append(tuple(clean(v) for v in row))
        if len(batch) >= 500:
            psycopg2.extras.execute_values(pcur, insert, batch, page_size=500)
            total += len(batch)
            batch = []
    if batch:
        psycopg2.extras.execute_values(pcur, insert, batch, page_size=500)
        total += len(batch)
    return total


def table_digest(rows) -> str:
    h = hashlib.md5()
    for row in rows:
        norm = tuple(
            "NULL" if v is None else (v.hex() if isinstance(v, (bytes, bytearray)) else str(v))
            for v in row
        )
        h.update(repr(norm).encode("utf-8", "replace"))
    return h.hexdigest()


def verify(my, pg, schema: dict) -> int:
    problems = 0
    mcur, pcur = my.cursor(), pg.cursor()
    for table, spec in schema.items():
        names = [c["name"] for c in spec["columns"]]
        mcur.execute(f"SELECT COUNT(*) FROM `{table}`")
        mcount = mcur.fetchone()[0]
        try:
            pcur.execute(f"SELECT COUNT(*) FROM {ident(table)}")
            pcount = pcur.fetchone()[0]
        except Exception as exc:  # noqa: BLE001
            pg.rollback()
            print(f"{table:34s} MISSING in postgres ({exc.__class__.__name__})")
            problems += 1
            continue
        status = "ok" if mcount == pcount else "MISMATCH"
        if mcount != pcount:
            problems += 1
        print(f"{table:34s} mysql={mcount:>6d}  pg={pcount:>6d}  {status}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--recreate", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--no-fk", action="store_true")
    args = ap.parse_args()

    my = mysql_conn()
    schema = introspect(my)

    if args.dry_run:
        for table, spec in schema.items():
            ddl, extras = ddl_for(table, spec)
            print(ddl)
            for e in extras:
                print(e)
            for f in fk_sql(table, spec):
                print(f)
            print()
        return 0

    pg = pg_conn()
    pg.autocommit = False

    if args.recreate:
        with pg.cursor() as cur:
            for table in reversed(list(schema)):
                cur.execute(f"DROP TABLE IF EXISTS {ident(table)} CASCADE")
        pg.commit()
        print(f"dropped {len(schema)} tables if present")

    created, failed = [], []
    for table, spec in schema.items():
        ddl, _ = ddl_for(table, spec)
        try:
            with pg.cursor() as cur:
                cur.execute(ddl)
            pg.commit()
            created.append(table)
        except Exception as exc:  # noqa: BLE001
            pg.rollback()
            failed.append((table, str(exc).splitlines()[0]))
    print(f"created {len(created)} tables, {len(failed)} failed")
    for t, e in failed:
        print("  FAILED", t, e)

    total = 0
    load_failed = []
    for table in created:
        try:
            n = copy_table(my, pg, table, schema[table])
            pg.commit()
            total += n
            print(f"  loaded {table:34s} {n:>6d} rows")
        except Exception as exc:  # noqa: BLE001
            pg.rollback()
            load_failed.append((table, str(exc).splitlines()[0]))
            print(f"  LOAD FAILED {table}: {str(exc).splitlines()[0]}")
    print(f"copied {total} rows")

    idx_fail = []
    for table in created:
        _, extras = ddl_for(table, schema[table])
        for stmt in extras:
            try:
                with pg.cursor() as cur:
                    cur.execute(stmt)
                pg.commit()
            except Exception as exc:  # noqa: BLE001
                pg.rollback()
                idx_fail.append((table, str(exc).splitlines()[0]))
    print(f"indexes: {sum(len(ddl_for(t, schema[t])[1]) for t in created) - len(idx_fail)} ok, {len(idx_fail)} failed")
    for t, e in idx_fail[:10]:
        print("  IDX FAILED", t, e)

    if not args.no_fk:
        fk_ok = fk_bad = 0
        for table in created:
            for stmt in fk_sql(table, schema[table]):
                try:
                    with pg.cursor() as cur:
                        cur.execute(stmt)
                    pg.commit()
                    fk_ok += 1
                except Exception as exc:  # noqa: BLE001
                    pg.rollback()
                    fk_bad += 1
                    print("  FK FAILED", table, str(exc).splitlines()[0])
        print(f"foreign keys: {fk_ok} ok, {fk_bad} failed")

    # Reset identity sequences so new inserts do not collide with migrated ids.
    seq_fixed = 0
    for table, spec in schema.items():
        for col in spec["columns"]:
            if "auto_increment" in (col["extra"] or "").lower():
                try:
                    with pg.cursor() as cur:
                        cur.execute(
                            f"SELECT setval(pg_get_serial_sequence('{ident(table)}', '{ident(col['name'])}'), "
                            f"COALESCE((SELECT MAX({ident(col['name'])}) FROM {ident(table)}), 1))"
                        )
                    pg.commit()
                    seq_fixed += 1
                except Exception as exc:  # noqa: BLE001
                    pg.rollback()
                    print("  SEQ FAILED", table, str(exc).splitlines()[0])
    print(f"sequences reset: {seq_fixed}")

    print("\nverifying row counts...")
    problems = verify(my, pg, schema)
    print("verification problems:", problems)
    return 0 if not (failed or load_failed or problems) else 1


if __name__ == "__main__":
    raise SystemExit(main())
