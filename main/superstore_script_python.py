import pandas as pd
pd.set_option('display.float_format', lambda x: '{:.15f}'.format(x).rstrip('0').rstrip('.'))

import warnings
warnings.filterwarnings('ignore')

df=pd.read_csv(r'data_csv\superstore.csv').dropna(how='all').drop_duplicates(keep='last')
df = df.reset_index(drop=True)


# Create a DataFrame for 'Country':

df_country = pd.DataFrame(columns=["country_id", "country"])

# INSERT DATA : COUNTRY
unique_countries = df["Country"].dropna().unique()
df_country = pd.DataFrame({
    "country_id": range(1, len(unique_countries) + 1),
    "country":    unique_countries
})


# Create a DataFrame for 'Region':

df_region = pd.DataFrame(columns=["region_id", "region", "country_id"])

#INSERT DATA : REGION
unique_regions = (
    df[["Country", "Region"]]
    .dropna()
    .drop_duplicates()
    .merge(df_country, left_on="Country", right_on="country")
    .rename(columns={"country_id": "country_id"})
    [["Region", "country_id"]]
)
df_region = unique_regions.reset_index(drop=True)
df_region.insert(0, "region_id", range(1, len(df_region) + 1))
df_region = df_region.rename(columns={"Region": "region"})


# Create a DataFrame for 'State':

df_state = pd.DataFrame(columns=["state_id", "state", "region_id"])

# INSERT DATA : STATE
unique_states = (
    df[["State", "Region"]]
    .dropna()
    .drop_duplicates()
    .merge(df_region, left_on="Region", right_on="region")
    [["State", "region_id"]]
)
df_state = unique_states.reset_index(drop=True)
df_state.insert(0, "state_id", range(1, len(df_state) + 1))
df_state = df_state.rename(columns={"State": "state"})
 


# Create a DataFrame for 'City':

df_city = pd.DataFrame(columns=["city_id", "city", "state_id"])

# INSERT DATA : CITY
unique_cities = (
    df[["City", "State"]]
    .dropna()
    .drop_duplicates()
    .merge(df_state, left_on="State", right_on="state")
    [["City", "state_id"]]
)
df_city = unique_cities.reset_index(drop=True)
df_city.insert(0, "city_id", range(1, len(df_city) + 1))
df_city = df_city.rename(columns={"City": "city"})


# Create a DataFrame for 'Postal Code':

df_postal_code = pd.DataFrame(columns=["postal_code_id", "postal_code"])

# INSERT DATA : POSTAL CODE
unique_postcodes = df["Postal Code"].dropna().unique()
df_postal_code = pd.DataFrame({
    "postal_code_id": range(1, len(unique_postcodes) + 1),
    "postal_code":    unique_postcodes
})
 

# Create a DataFrame for 'Postal Code - City':

df_postalcode_city = pd.DataFrame(
    columns=["postalcode_city_id", "postal_code_id", "city_id"]
)

# INSERT DATA : POSTAL CODE - CITY
pc_city_pairs = (
    df[["Postal Code", "City"]]
    .dropna()
    .drop_duplicates()
    .merge(df_postal_code, left_on="Postal Code", right_on="postal_code")
    .merge(df_city,        left_on="City",         right_on="city")
    [["postal_code_id", "city_id"]]
)
df_postalcode_city = pc_city_pairs.reset_index(drop=True)
df_postalcode_city.insert(0, "postalcode_city_id", range(1, len(df_postalcode_city) + 1))



# Create a DataFrame for 'Segment':

df_segment = pd.DataFrame(columns=["segment_id", "segment"])

# INSERT DATA : SEGMENT
unique_segments = df["Segment"].dropna().unique()
df_segment = pd.DataFrame({
    "segment_id": range(1, len(unique_segments) + 1),
    "segment":    unique_segments
})



# Create a DataFrame for 'Customer':

df_customer = pd.DataFrame(
    columns=["customer_id", "customer_name", "segment_id"]
)

# INSERT DATA : CUSTOMER
unique_customers = (
    df[["Customer ID", "Customer Name", "Segment"]]
    .dropna()
    .drop_duplicates(subset=["Customer ID"])
    .merge(df_segment, left_on="Segment", right_on="segment")
    [["Customer ID", "Customer Name", "segment_id"]]
)
df_customer = unique_customers.reset_index(drop=True)
df_customer = df_customer.rename(columns={
    "Customer ID":   "customer_id",
    "Customer Name": "customer_name"
})
 




# Create a DataFrame for 'Customer - Postal Code - City':

df_customer_postalcode_city = pd.DataFrame(
    columns=["customer_postalcode_city_id", "customer_id", "postalcode_city_id"]
)

# INSERT DATA : CUSTOMER - POSTAL CODE - CITY
cust_loc = (
    df[["Customer ID", "Postal Code", "City"]]
    .dropna()
    .drop_duplicates()
    .merge(df_postalcode_city
           .merge(df_postal_code, on="postal_code_id")
           .merge(df_city,        on="city_id")[["postalcode_city_id", "postal_code", "city"]],
           left_on=["Postal Code", "City"],
           right_on=["postal_code", "city"])
    [["Customer ID", "postalcode_city_id"]]
)
df_customer_postalcode_city = cust_loc.reset_index(drop=True)
df_customer_postalcode_city.insert(
    0, "customer_postalcode_city_id",
    range(1, len(df_customer_postalcode_city) + 1)
)
df_customer_postalcode_city = df_customer_postalcode_city.rename(
    columns={"Customer ID": "customer_id"}
)




# Create a DataFrame for 'Category':

df_category = pd.DataFrame(columns=["category_id", "category"])
  
# INSERT DATA : CATEGORY
unique_categories = df["Category"].dropna().unique()
df_category = pd.DataFrame({
    "category_id": range(1, len(unique_categories) + 1),
    "category":    unique_categories
})



# Create a DataFrame for 'Sub-Category':

df_sub_category = pd.DataFrame(
    columns=["sub_category_id", "sub_category", "category_id"]
)

# INSERT DATA : SUB_CATEGORY
unique_subcats = (
    df[["Sub-Category", "Category"]]
    .dropna()
    .drop_duplicates()
    .merge(df_category, left_on="Category", right_on="category")
    [["Sub-Category", "category_id"]]
)
df_sub_category = unique_subcats.reset_index(drop=True)
df_sub_category.insert(0, "sub_category_id", range(1, len(df_sub_category) + 1))
df_sub_category = df_sub_category.rename(columns={"Sub-Category": "sub_category"})



# Create a DataFrame for 'Product':

df_product = pd.DataFrame(
    columns=["product_id", "product_name", "sub_category_id"]
)
  
# INSERT DATA : PRODUCT
unique_products = (
    df[["Product ID", "Product Name", "Sub-Category"]]
    .dropna()
    .drop_duplicates(subset=["Product ID"])
    .merge(df_sub_category, left_on="Sub-Category", right_on="sub_category")
    [["Product ID", "Product Name", "sub_category_id"]]
)
df_product = unique_products.reset_index(drop=True)
df_product = df_product.rename(columns={
    "Product ID":   "product_id",
    "Product Name": "product_name"
})


# Create a DataFrame for 'Ship Mode':

df_ship_mode = pd.DataFrame(columns=["ship_mode_id", "ship_mode"])
  
# INSERT DATA : SHIP_MODE
unique_ship_modes = df["Ship Mode"].dropna().unique()
df_ship_mode = pd.DataFrame({
    "ship_mode_id": range(1, len(unique_ship_modes) + 1),
    "ship_mode":    unique_ship_modes
})



# Create a DataFrame for 'Order':

df_order = pd.DataFrame(columns=[
    "order_id", "customer_id", "product_id", "ship_mode_id",
    "order_date", "ship_date", "sales", "quantity", "discount", "profit"
])
 
# INSERT DATA : ORDER
df_order = (
    df[["Order ID", "Customer ID", "Product ID", "Ship Mode",
         "Order Date", "Ship Date", "Sales", "Quantity", "Discount", "Profit"]]
    .dropna(subset=["Order ID"])
    .merge(df_ship_mode, left_on="Ship Mode", right_on="ship_mode")
    [["Order ID", "Customer ID", "Product ID", "ship_mode_id",
      "Order Date", "Ship Date", "Sales", "Quantity", "Discount", "Profit"]]
)
df_order = df_order.rename(columns={
    "Order ID":   "order_id",
    "Customer ID": "customer_id",
    "Product ID":  "product_id",
    "Order Date":  "order_date",
    "Ship Date":   "ship_date",
    "Sales":       "sales",
    "Quantity":    "quantity",
    "Discount":    "discount",
    "Profit":      "profit"
})
 


# Export DataFrames to Excel files:
df_country.to_excel('country.xlsx', index=False)
df_region.to_excel('region.xlsx', index=False)
df_state.to_excel('state.xlsx', index=False)
df_city.to_excel('city.xlsx', index=False)
df_postal_code.to_excel('postal code.xlsx', index=False)
df_postalcode_city.to_excel('postalcode city.xlsx', index=False)
df_segment.to_excel('segment.xlsx', index=False)
df_customer.to_excel('customer.xlsx', index=False)
df_customer_postalcode_city.to_excel('customer postalcode city.xlsx', index=False)
df_category.to_excel('category.xlsx', index=False)
df_sub_category.to_excel('sub category.xlsx', index=False)
df_product.to_excel('product.xlsx', index=False)
df_ship_mode.to_excel('ship mode.xlsx', index=False)
df_order.to_excel('order.xlsx', index=False)


# Export DataFrames to Excel file:
with pd.ExcelWriter('superstore_data.xlsx') as writer:
    df_country.to_excel(writer, sheet_name='Country', index=False)
    df_region.to_excel(writer, sheet_name='Region', index=False)
    df_state.to_excel(writer, sheet_name='State', index=False)
    df_city.to_excel(writer, sheet_name='City', index=False)
    df_postal_code.to_excel(writer, sheet_name='Postal Code', index=False)
    df_postalcode_city.to_excel(writer, sheet_name='PostalCode City', index=False)
    df_segment.to_excel(writer, sheet_name='Segment', index=False)
    df_customer.to_excel(writer, sheet_name='Customer', index=False)
    df_customer_postalcode_city.to_excel(writer, sheet_name='Customer PostalCode City', index=False)
    df_category.to_excel(writer, sheet_name='Category', index=False)
    df_sub_category.to_excel(writer, sheet_name='Sub Category', index=False)
    df_product.to_excel(writer, sheet_name='Product', index=False)
    df_ship_mode.to_excel(writer, sheet_name='Ship Mode', index=False)
    df_order.to_excel(writer, sheet_name='Order', index=False)



print("Outputs generated as Excel files. Completed successfully!")

# Export DataFrames to CSV files:

df_country.to_csv('country.csv', index=False)
df_region.to_csv('region.csv', index=False)
df_state.to_csv('state.csv', index=False)
df_city.to_csv('city.csv', index=False)
df_postal_code.to_csv('postal code.csv', index=False)
df_postalcode_city.to_csv('postalcode city.csv', index=False)
df_segment.to_csv('segment.csv', index=False)
df_customer.to_csv('customer.csv', index=False)
df_customer_postalcode_city.to_csv('customer postalcode city.csv', index=False)
df_category.to_csv('category.csv', index=False)
df_sub_category.to_csv('sub category.csv', index=False)
df_product.to_csv('product.csv', index=False)
df_ship_mode.to_csv('ship mode.csv', index=False)
df_order.to_csv('order.csv', index=False)

print("Outputs generated as CSV files. Completed successfully!")