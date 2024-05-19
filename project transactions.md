
section 1 ``first objectives

	- FIRST READ IN TRANSACIONS DATA AND EXPLORE IT
 
	- TAKE A LOOK AS THE RAW DATA,THE DATATYPES 
 
	- CAST DAY,QUANTITY,STORE_ID AND WEEK_NO COLUMNS TO THE SMALLEST APPROPRIATE DATATYPE
 
	- CHECK THE MEMORY REDUCTION BY DOING SO
 
	- question 1 ``check for missing data``
 
		- IS THERE ANY MISSING DATA?
  
	-question 2 ``check for unique values``
 
		- HOW MANY UNIQUE HOUSEHOLDS AND PRODUCTS ARE THERE IN THE DATA?

section 2 ``COLUMN CREATION

	- create two columns
 
	- A column thatcaptures the total_discount by row(``sum of [retail_disc],[coupon_disc]``)
 
	- The percentage discount(``[total_discount]/[sales_value]),Make sure this is positive (try '.abs()'``)
 
	- If the percentage discount is greater than 1,set it equal to 1, if it is less than 0, set it to 0.
 
	- Drop the individual discount columns(``retail_disc, coupon_disc , coupon_match_disc``)

section 3 ``overall statistics``

	``CALCULATE:
 
	    - THE TOTAL SALES (``SUM OF SALES_VALUE``)
     
	    - TOTAL DISCOUNT (``SUM OF TOTAL_DISCOUNT``)
     
	    - OVERALL PERCENTAGE DISCOUNT(``SUM OF TOTAL_DISCOUNT/SUM OF SALES VALUE``)
     
	    - TOTAL QUANTITY SOLD (``SUM OF QUANTITY``)
     
	    - MAX QUANTITY SOLD IN A SINGLE ROW . (``INSPECT THE ROW AS WELL , DOES THIS HAVE A HIGH DISCOUNT PERCENTAGE``)
     
	    - TOTAL SALES VALUE PER BASKET(``SUM OF SALES_VALUE/NUNIQUE BASKET_ID``)
     
	    - TOTAL SALES VALUE PER HOUSEHOLD(``SUM OF SALES VALUE/NUNIQUE HOUSE HOLD KEY``)
     
    
section  4 ``Household analysis``

	- distribution plot of total sales value purchased at the household level
 
	- what were the top 10 households by quantity purchased?
 
	- what were th etop 10 households by sales value?
 
	- total sales value plot for top 10 house holds by value, order from highest to lowest
 

section 5 ``product analysis``

	- which product had the most sales by value? plot a horizintal bar chart
 
	- did the top 10 seling items have a higher than average discount rate?
 
	- what was the most common [product_id]among rows with the households in the top 10 households by sales value
 
	- names of the top 10 products by sales in the [product.csv]dataset
 
	- product name of  the item that had the highest quantity sold in a single row
