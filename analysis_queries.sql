-- SQL practice queries for Automobile Sales Analysis
-- Table name assumed: automobile_sales

-- 1. Total units and revenue
SELECT SUM(Units_Sold) AS total_units,
       SUM(Revenue_INR) AS total_revenue
FROM automobile_sales;

-- 2. Most popular car models by units sold
SELECT Model, SUM(Units_Sold) AS units_sold
FROM automobile_sales
GROUP BY Model
ORDER BY units_sold DESC;

-- 3. Revenue by region
SELECT Region, SUM(Revenue_INR) AS total_revenue
FROM automobile_sales
GROUP BY Region
ORDER BY total_revenue DESC;

-- 4. Monthly sales trend (syntax may vary by SQL database)
SELECT EXTRACT(MONTH FROM Date) AS sales_month,
       SUM(Units_Sold) AS units_sold
FROM automobile_sales
GROUP BY EXTRACT(MONTH FROM Date)
ORDER BY sales_month;

-- 5. Average listed unit price by category
SELECT Category, AVG(Unit_Price_INR) AS average_price
FROM automobile_sales
GROUP BY Category;
