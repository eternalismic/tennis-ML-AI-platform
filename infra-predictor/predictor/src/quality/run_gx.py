import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.core import ExpectationSuite
from sqlalchemy import create_engine
import os, json
def main():
    db_url = os.getenv("DATABASE_URL","postgresql+psycopg://tennis:tennispass@tennis-data-db-rw.data.svc:5432/tennis")
    engine = create_engine(db_url, future=True)
    context = gx.get_context(mode="ephemeral")
    context.add_datasource(
        name="pg",
        class_name="Datasource",
        execution_engine={"class_name":"SqlAlchemyExecutionEngine","connection_string":db_url},
        data_connectors={"default_runtime_data_connector_name":{"class_name":"RuntimeDataConnector","batch_identifiers":["query","limit"]}}
    )
    suite = ExpectationSuite(expectation_suite_name="raw_matches_basic")
    context.add_or_update_expectation_suite(expectation_suite=suite)
    batch_request = RuntimeBatchRequest(
        datasource_name="pg",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="raw.matches",
        runtime_parameters={"query":"SELECT * FROM raw.matches"},
        batch_identifiers={"query":"raw.matches","limit":"all"}
    )
    validator = context.get_validator(batch_request=batch_request, expectation_suite_name="raw_matches_basic")
    validator.expect_column_values_to_not_be_null("date")
    validator.expect_column_values_to_not_be_null("player_a")
    validator.expect_column_values_to_not_be_null("player_b")
    validator.expect_column_values_to_be_in_set("surface", ["hard","clay","grass","carpet", None])
    validator.expect_column_values_to_be_between("rank_a", min_value=1, max_value=3000, mostly=0.99)
    validator.expect_column_values_to_be_between("rank_b", min_value=1, max_value=3000, mostly=0.99)
    results = validator.validate(); print(json.dumps(results.to_json_dict(), indent=2))
if __name__=="__main__": main()
