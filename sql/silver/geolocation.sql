CREATE OR REPLACE TABLE `seventh-botany-506408-i1.silver.geolocation` AS

SELECT
    SAFE_CAST(geolocation_zip_code_prefix AS INT64)
        AS geolocation_zip_code_prefix,

    SAFE_CAST(geolocation_lat AS FLOAT64)
        AS geolocation_lat,

    SAFE_CAST(geolocation_lng AS FLOAT64)
        AS geolocation_lng,

    TRIM(LOWER(geolocation_city))
        AS geolocation_city,

    UPPER(TRIM(geolocation_state))
        AS geolocation_state

FROM `seventh-botany-506408-i1.bronze.geolocation`;