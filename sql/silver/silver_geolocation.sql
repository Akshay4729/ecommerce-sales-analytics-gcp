-- Raw geolocation has many observations per ZIP prefix.
-- Keep unique observations and provide a safe one-row-per-ZIP lookup.
CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.geolocation` AS
SELECT DISTINCT
  SAFE_CAST(geolocation_zip_code_prefix AS INT64) AS geolocation_zip_code_prefix,
  SAFE_CAST(geolocation_lat AS FLOAT64) AS geolocation_lat,
  SAFE_CAST(geolocation_lng AS FLOAT64) AS geolocation_lng,
  LOWER(TRIM(geolocation_city)) AS geolocation_city,
  UPPER(TRIM(geolocation_state)) AS geolocation_state,
  CURRENT_TIMESTAMP() AS transformed_at
FROM `seventh-botany-506408-i1.bronze.geolocation`;

CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.geolocation_zip_lookup` AS
SELECT
  geolocation_zip_code_prefix,
  AVG(geolocation_lat) AS geolocation_lat,
  AVG(geolocation_lng) AS geolocation_lng,
  ARRAY_AGG(geolocation_city IGNORE NULLS ORDER BY geolocation_city LIMIT 1)[SAFE_OFFSET(0)] AS geolocation_city,
  ARRAY_AGG(geolocation_state IGNORE NULLS ORDER BY geolocation_state LIMIT 1)[SAFE_OFFSET(0)] AS geolocation_state,
  COUNT(*) AS source_observation_count
FROM `seventh-botany-506408-i1.silver.geolocation`
GROUP BY geolocation_zip_code_prefix;
