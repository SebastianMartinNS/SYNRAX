"""db/connection.py — Database connection pool and query execution.

exports: get_connection() -> Connection | execute_raw(sql: str) -> list
used_by: models/inventory.py -> check_stock | models/order.py -> create_order
rules:   Connection pool max size = 20. Always return connections to pool after use.
         Raw SQL MUST use parameterized queries — never string interpolation.
agent:   claude-opus-4 | anthropic | 2026-03-10 | Initial connection pool.
"""


def get_connection():
    """Get a database connection from the pool.

    Rules: Caller MUST close/return connection in finally block.
    """
    pass


def execute_raw(sql: str) -> list:
    """Execute raw SQL with parameter binding.

    Rules: NEVER use f-strings or .format() for SQL. Always use ? placeholders.
    """
    return []
