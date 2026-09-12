CREATE OR REPLACE TABLE
  `seventh-botany-506408-i1.gold.dim_date` AS

SELECT
    CAST(FORMAT_DATE('%Y%m%d', date) AS INT64) AS date_key,
    date,

    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(MONTH FROM date) AS month,

    FORMAT_DATE('%B', date) AS month_name,

    EXTRACT(WEEK FROM date) AS week,

    EXTRACT(DAY FROM date) AS day,

    FORMAT_DATE('%A', date) AS day_name

FROM
    UNNEST(
        GENERATE_DATE_ARRAY(
            DATE '2016-09-04',
            DATE '2018-10-17'
        )
    ) AS date;