## Data cleaning and Exploratory Data Analysis of retail datasets

### Intended Purpose

The intended purpose of this Python script is to clean and analyze transaction data from the `project_transactions.csv` file and product data from the `product.csv` file. This involves data type optimization, column creation, calculating overall statistics, and performing household and product-level analyses.

### Key Objectives

1. **Data Type Optimization**: Reduce memory usage by downcasting data types.
2. **Missing Data Check**: Identify and handle any missing data.
3. **Column Creation**: Create new columns for analysis.
4. **Overall Statistics Calculation**: Compute key metrics such as total sales, total discount, and quantities sold.
5. **Household Analysis**: Analyze sales and quantities at the household level.
6. **Product Analysis**: Examine sales and discount rates at the product level.

### Section Objectives

1. **Reading in Necessary Data**
   - **Objective**: Read the `project_transactions.csv` file into a DataFrame.

2. **Data Type Optimization**
   - **Objective**: Downcast data types to reduce memory usage.

3. **Missing Data Check**
   - **Objective**: Check for and report any missing data.
   - 
4. **Unique Values Check**
   - **Objective**: Check for unique household and product values.

5. **Column Creation**
   - **Objective**: Create `TOTAL_DISC` and `PERC_DISC` columns.

6. **Overall Statistics Calculation**
   - **Objective**: Calculate total sales, total discount, overall percentage discount, total quantity sold, max quantity sold in a single row, total sales per basket, and total sales per household.

7. **Household Analysis**
   - **Objective**: Analyze the distribution of sales value at the household level, identify top households by quantity and sales value, and plot total sales value for top households.

8. **Product Analysis**
   - **Objective**: Read `product.csv`, merge it with transaction data, and analyze the top products by sales value and discount rate.

### Precautionary Steps Taken

- **Memory Usage Reduction**: Effective memory usage reduction by downcasting data types, which is crucial for handling large datasets efficiently.
- **Interim Verification Steps**: Implementing the use of Several print statements and queries to verify the intermediate results of data cleaning and transformation steps, ensuring the correctness of each operation.
- **Comprehensive Analysis**: Performance of detailed analysis at both household and product levels, providing insights into sales patterns and discount rates.
