"""PostgreSQL records for the advanced API; never required by core lessons."""

from __future__ import annotations

import json
import os

from workshop.control import validate_report
from workshop.schemas import DecisionReport


class PostgresRunStore:
    def __init__(self, dsn: str):
        if not dsn:
            raise ValueError("PostgreSQL DSN is required")
        self.dsn = dsn

    def _connect(self):
        import psycopg

        return psycopg.connect(self.dsn, connect_timeout=5)

    def initialize(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workshop_runs (
                    run_id UUID PRIMARY KEY,
                    customer_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    requested_action BOOLEAN NOT NULL,
                    report JSONB,
                    output TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workshop_approvals (
                    run_id UUID PRIMARY KEY REFERENCES workshop_runs(run_id),
                    approved_by TEXT NOT NULL,
                    approved_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)

    def save_run(self, *, run_id: str, customer_id: str, question: str,
                 requested_action: bool, report: DecisionReport | None, output: str) -> None:
        self.initialize()
        status = "pending_approval" if requested_action and report else "complete"
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO workshop_runs
                  (run_id, customer_id, question, requested_action, report, output, status)
                VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s)
            """, (run_id, customer_id, question, requested_action,
                  report.model_dump_json() if report else None, output, status))

    def approve_mock_action(self, run_id: str, *, approved_by: str) -> str:
        """Atomically record instructor approval once; no real email is sent."""
        from psycopg.rows import dict_row

        with self._connect() as conn:
            row = conn.execute(
                "SELECT requested_action, report FROM workshop_runs WHERE run_id = %s FOR UPDATE",
                (run_id,), row_factory=dict_row,
            ).fetchone()
            if row is None:
                raise KeyError(run_id)
            if not row["requested_action"] or not row["report"]:
                raise ValueError("run has no approvable report or requested action")
            report = DecisionReport.model_validate(row["report"])
            valid, reason = validate_report(report)
            if not valid:
                raise ValueError(reason)
            inserted = conn.execute("""
                INSERT INTO workshop_approvals (run_id, approved_by)
                VALUES (%s, %s) ON CONFLICT DO NOTHING RETURNING run_id
            """, (run_id, approved_by)).fetchone()
            if inserted is None:
                return "ALREADY_RECORDED: mock action was not repeated"
            conn.execute("UPDATE workshop_runs SET status = 'approved' WHERE run_id = %s", (run_id,))
            return "RECORDED: mock action approval only; no email sent"

    def ping(self) -> bool:
        with self._connect() as conn:
            return conn.execute("SELECT 1").fetchone() == (1,)


def configured_store() -> PostgresRunStore | None:
    dsn = os.getenv("WORKSHOP_DATABASE_URL", "").strip()
    return PostgresRunStore(dsn) if dsn else None
