from pathlib import Path


ROOT = Path(__file__).parents[1]


def read_sql(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


def test_gold_order_model_aggregates_one_to_many_sources_first() -> None:
    sql = read_sql("sql/gold/fact_orders.sql")

    assert "with item_totals as" in sql
    assert "payment_totals as" in sql
    assert "review_totals as" in sql
    assert "group by order_id" in sql
    assert "customer_unique_id" in sql


def test_primary_gold_models_use_documented_delivered_filter() -> None:
    for path in ("sql/gold/daily_sales.sql", "sql/gold/customer_metrics.sql"):
        sql = read_sql(path)
        assert "where order_status = 'delivered'" in sql


def test_geolocation_has_a_safe_zip_level_lookup() -> None:
    sql = read_sql("sql/silver/silver_geolocation.sql")

    assert "select distinct" in sql
    assert "geolocation_zip_lookup" in sql
    assert "group by geolocation_zip_code_prefix" in sql
