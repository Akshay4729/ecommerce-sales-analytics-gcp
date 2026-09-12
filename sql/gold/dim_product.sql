CREATE OR REPLACE TABLE
  `seventh-botany-506408-i1.gold.dim_product` AS

SELECT
    ROW_NUMBER() OVER (
        ORDER BY p.product_id
    ) AS product_key,

    p.product_id,

    c.category_key,

    p.product_name_length,
    p.product_description_length,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm

FROM
  `seventh-botany-506408-i1.silver.products` AS p

LEFT JOIN
  `seventh-botany-506408-i1.gold.dim_category` AS c

ON
  p.product_category_name = c.product_category_name;