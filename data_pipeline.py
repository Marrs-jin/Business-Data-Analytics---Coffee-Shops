"""
Data Pipeline
Data cleaning and transformation pipeline.

Originally developed in Deepnote. Deepnote "module import" blocks are
marked with # DEEPNOTE MODULE IMPORT comments — replace with standard
Python imports in a local environment.
"""

# ============================================================
# DEEPNOTE MODULE IMPORT
# In Deepnote, this block runs notebook 'Functions Read-in' as a module,
# making its variables and functions available in this notebook.
# In standard Python, import the equivalent module:
#   from functions_read-in import *
# or copy the relevant function definitions from that notebook.
# ============================================================

# ============================================================
# DEEPNOTE MODULE IMPORT
# In Deepnote, this block runs notebook 'Inventory Read-in' as a module,
# making its variables and functions available in this notebook.
# In standard Python, import the equivalent module:
#   from inventory_read-in import *
# or copy the relevant function definitions from that notebook.
# ============================================================

import pandas as pd
import numpy as np
import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation

import zipfile
from datetime import datetime
import calendar

import re
import unicodedata
# %matplotlib inline  # Jupyter magic: run `matplotlib.use("Agg")` or remove in a script context

# Test Data
#Input which months to analyze
months_to_analyze = ['September', 'October', 'November', 'December']
years_to_analyze = 2025

# # Costs, Menu Prices, Profit % of Menu Items
# menu_ProfitAnalysis_df = menu_PricesandCosts.copy()

# menu_data = load_ProductMix_MenuData(months_to_analyze, years_to_analyze)

sales_data = load_ItemSelectionDetails_SalesData(months_to_analyze, years_to_analyze)


# Discussion Topics

# - 1. I am dropping all items entered manually instead of cleaning them. This can be changed, but it would be messy

# - 2. I am grouping all teas together right now, so they can be compared with coffees. I can have them be individual instead however

def clean_data_labels(df, item_name_column="Item Name"):
    """
    Cleans the data labels in the given DataFrame.
    This function replaces incorrect item names with the correct ones 
    based on a predefined replacement map.
    It also drops rows with incorrect labels and rows that do not have a menu group, 
    menu, or sales category.
    """
    
    replacement_map = {

        # retail
        "water bottle": "bottled water",
        "bottled water evian": "bottled water",
        "deer park": "bottled water",
        "havanna dulce deleche": "havanna dulce de leche",
        "san benedetto sparkling": "sparkling water",
        "sparkling plastic water san pellegrino": "sparkling water",

        # pastry case
        "chipá (sweet - 3 quantity)": "chipá (sweet - 2 quantity)",
        'almond cake (one loaf)': 'almond cake',

        # food
        "hand cut steak empanadas": "hand cut steak empanada",
        "chicken picante": "chicken empanada",
        '3 empanadas - combo price': '3 empanada combo',

        # drinks
        "16oz" : "16 oz take out loose leaf tea",
        '16 oz dine in nitro cold brew': '16 oz iced nitro cold brew',
        "16 oz nitro cold brew": "16 oz iced nitro cold brew",
        "16 oz take out nitro vanilla matcha": "16 oz iced nitro vanilla matcha",
        "16 oz nitro vanilla matcha": "16 oz iced nitro vanilla matcha",
        "16oz americano": "16 oz take out americano",
        "10 oz take out capuccino": "10 oz take out cappuccino",
        
        "americano": "dine in americano",
        "affogato": "dine in affogato",
        "babyccino": "8 oz take out babyccino",
        "cafe au lait": "dine in cafe au lait",
        "capuccino": "dine in cappuccino",
        "café au lait": "dine in café au lait",

        "chai latte": "dine in chai latte",
        "clarity mushroom tea": "dine in loose leaf tea",
        "cold brew": "16 oz iced cold brew",
        '16 oz take out cold brew': "16 oz iced cold brew",
        "cortado": "dine in cortado",

        "dine out flat white": "8 oz take out flat white",
        "dine in capuccino": "dine in cappuccino",
        "dine in hot chocolate": "dine in submarino",
        "drip coffee": "dine in drip coffee", 
        "espresso": "dine in espresso",
        'el principito': "dine in el principito",
        "flat white": "dine in flat white",

        "hot chocolate 10oz": "10 oz submarino",
        "hot chocolate 16oz": "16 oz submarino",
        "hot chocolate 16 oz": "16 oz submarino",
        "iced americano": "16 oz iced americano",
        "iced americano ": "16 oz iced americano",
        "iced chai latte": "16 oz iced chai latte",
        "iced latte": "16 oz iced latte",

        "iced london fog": "16 oz iced london fog",
        "iced loose leaf tea": "16 oz iced loose leaf tea",
        "iced loose leaf tea ": "16 oz iced loose leaf tea",
        "iced matcha latte": "16 oz iced matcha latte",

        "jasmine pearls": "dine in loose leaf tea",
        "latte": "dine in latte",
        "machiato": "dine in macchiato",
        "macchiato": "dine in macchiato",
        "macchiato ": "dine in macchiato",
        "matcha": "dine in matcha latte",
        "matcha latte": "dine in matcha latte",
        "moms recipe medialuna": "medialuna",

        "nitro cold brew": "16 oz iced nitro cold brew",
        "nitro cold brew ": "16 oz iced nitro cold brew",
        "nitro vanilla matcha": "16 oz iced nitro vanilla matcha",
        "organic earl gray": "dine in loose leaf tea",
        "seasonal flavor": "affogato",
        
        "submarino / hot choco 10oz": "10 oz take out submarino",
        "saratoga water": "bottled water",
        "take out 10 oz latte": "10 oz take out latte",
        "take out 10 oz london fog": "10 oz take out london fog",
        "take out 16 oz latte": "16 oz take out latte",

        "take out 10 oz hot chocolate": "10 oz take out submarino",
        "take out 16 oz hot chocolate": "16 oz take out submarino",

        "take out 16 oz london fog": "16 oz take out london fog",
        "take out espresso": "8 oz take out espresso",
        "uplift mushroom tea": "dine in loose leaf tea",
        "white peach": "dine in loose leaf tea",

        # books
        "emotional inteligence": "emotional intelligence",

        # candles
        "piscis candle": "candley piscis candle"
    }

    # Normalize the item names to lowercase for comparison
    df_cleaned = df.copy()
    df_cleaned[item_name_column] = df_cleaned[item_name_column].str.lower()

    #strip white leading and trailing white spaces
    df_cleaned[item_name_column] = df_cleaned[item_name_column].str.strip()

    # Replace the item names based on the replacement map
    df_cleaned[item_name_column] = df_cleaned[item_name_column].replace(replacement_map)

    # Drop rows with incorrect labels
    incorrect_labels = {
        "16oz", "take out", "total", "return", "seasonal flavour", "vanilla"
    }
    df_cleaned = df_cleaned[~df_cleaned[item_name_column].isin(incorrect_labels)]

    # Drop items that do not have a menu group, menu, or sales category (entered manually)
    #the possible categories items could be modified with
    category_columns = ['Menu Group', 'Menu', 'Sales Category']
    category_columns_present = [col for col in category_columns if col in df_cleaned.columns]
    df_cleaned = df_cleaned.dropna(subset=category_columns_present)

    return df_cleaned
clean_data_labels

# sales_data2 = sales_data.copy()
# sales_data2 = clean_data_labels(sales_data2)
# sorted(sales_data2['Item Name'].unique())

def standardFormat_data(df, item_name_column="Item Name"):
    """
    Formats the specified column in the dataframe by replacing instances of 
    '# oz' with '#oz',
    'take out' with 'take-out', 
    'dine in' with 'dine-in',
    and removing any leading or trailing whitespace.

    Additionally, if an item has a size token (8oz/10oz/16oz) but lacks both
    'take-out' and 'iced', the function will assume 'take-out' and insert it
    in the Location position of the normalized name.

    Final normalized format:
      Base Item Name [Iced] [Location] [Size]
    where optional parts appear only if present/required.
    """
    import re
    import unicodedata
    import pandas as pd

    # ensure string type
    df[item_name_column] = df[item_name_column].astype(str)

    # normalize common spacing/phrasing
    df[item_name_column] = df[item_name_column].str.replace(r'(\d+)\s*oz', r'\1oz', regex=True)
    df[item_name_column] = df[item_name_column].str.replace('take out', 'take-out', regex=False)
    df[item_name_column] = df[item_name_column].str.replace('dine in', 'dine-in', regex=False)

    # strip
    df[item_name_column] = df[item_name_column].str.strip()

    # Extract tokens from anywhere
    iced = df[item_name_column].str.extract(r"\b(iced)\b", expand=False, flags=re.IGNORECASE)
    location = df[item_name_column].str.extract(r"\b(dine-in|take-out)\b", expand=False)
    size = df[item_name_column].str.extract(r"\b(8oz|10oz|16oz|\d+oz)\b", expand=False)

    # Build base by removing tokens
    base = (
        df[item_name_column]
        .str.replace(r"\biced\b", "", regex=True, flags=re.IGNORECASE)
        .str.replace(r"\b(dine-in|take-out)\b", "", regex=True, flags=re.IGNORECASE)
        .str.replace(r"\b(8oz|10oz|16oz|\d+oz)\b", "", regex=True, flags=re.IGNORECASE)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # CONDITION: If has size but no location and no iced, default to take-out
    needs_take_out = size.notna() & location.isna() & iced.isna()
    # set location where needed
    location = location.where(~needs_take_out, other='take-out')

    # helper to safely append only if present
    def add_part(base_series, part_series, transform=lambda x: x):
        part_series = part_series.fillna("")
        return base_series + part_series.apply(lambda x: f" {transform(x)}" if x else "")

    out = base
    out = add_part(out, iced, lambda x: x.title())
    out = add_part(out, location, lambda x: x.lower())
    out = add_part(out, size, lambda x: x.lower())

    # lower-case final
    df[item_name_column] = out.str.lower()

    # Strip diacritics
    df[item_name_column] = (
        df[item_name_column]
        .apply(lambda x: unicodedata.normalize("NFKD", x)
               .encode("ascii", "ignore")
               .decode("utf-8"))
    )

    return df
standardFormat_data

def cleaning_pipeline(df, item_name_column = "Item Name"):
    df = clean_data_labels(df, item_name_column)
    df = standardFormat_data(df, item_name_column)
    return df
cleaning_pipeline

# menu_ProfitAnalysis_df = menu_PricesandCosts.copy()
# menu2 = clean_data_labels(menu_ProfitAnalysis_df, "Item Name")
# menu3 = standardFormat_data(menu2, "Item Name")
# sorted(menu3["Item Name"].unique())

def aggregate_sales_data(df, item_name_column="Item Name", time_period="Month"):
    """
    Aggregates sales/menu data to item-level by Month (default) or Day.
    - Uses weighted average for Avg Price
    - Sums Quantity and Net Sales
    - If starting from raw sales data (Price), creates Net Sales after aggregation
    - If time_period == 'Day', groups by calendar date and adds 'day_of_the_week'
    """

    # Determine grouping columns based on time_period
    if time_period == "Day":
        # Ensure a date column exists; prefer an existing 'Date' column; otherwise derive from 'Time'
        if 'Date' in df.columns:
            df = df.copy()
            # ensure Date is datetime (date-only for grouping)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
        elif 'Time' in df.columns:
            df = df.copy()
            df['Date'] = pd.to_datetime(df['Time']).dt.date
        else:
            raise ValueError("For time_period='Day', the dataframe must contain a 'Date' or 'Time' column.")

        group_cols = ['Sales Category', 'Menu Group', item_name_column, 'Date']
    else:
        # Default to Month-level grouping
        group_cols = ['Sales Category', 'Menu Group', item_name_column, 'Month', 'Year']

    # ---------- CASE 1: already aggregated / menu-style ----------
    if "Avg Price" in df.columns:
        # use a weighted average for Avg Price
        df = df.groupby(group_cols).apply(
            lambda x: pd.Series({
                "Avg Price": (x.get("Avg Price", pd.Series(dtype=float)) * x["Quantity"]).sum() / x["Quantity"].sum()
                              if x["Quantity"].sum() != 0 else 0,
                "Quantity": x["Quantity"].sum(),
                "Net Sales": x.get("Net Sales", pd.Series(dtype=float)).sum() if "Net Sales" in x else (x.get("Avg Price", 0) * x["Quantity"]).sum()
            })
        ).reset_index()
    # ---------- CASE 2: raw transaction-style ----------
    elif "Price" in df.columns:
        df = df.groupby(group_cols).apply(
            lambda x: pd.Series({
                "Avg Price": (x["Price"] * x["Quantity"]).sum() / x["Quantity"].sum()
                              if x["Quantity"].sum() != 0 else 0,
                "Quantity": x["Quantity"].sum()
            })
        ).reset_index()
        # create Net Sales post-aggregation
        df["Net Sales"] = df["Avg Price"] * df["Quantity"]
    else:
        raise ValueError("Dataframe must contain either 'Avg Price' (aggregated data) or 'Price' (raw data) column.")

    # Add day_of_the_week when grouping by Day
    if time_period == "Day":
        # Convert Date to datetime for weekday name, then keep as date
        df['Date'] = pd.to_datetime(df['Date'])
        df['day_of_the_week'] = df['Date'].dt.day_name()
        # If preferred to keep Date as date (not Timestamp), convert back to date
        df['Date'] = df['Date'].dt.date

    return df
aggregate_sales_data

# # Test data
# months_to_analyze = ['September', 'October', 'November']
# years_to_analyze = 2025
# # #Sample Data
# # Load the sales data for August using the new function
# men_sales = load_and_clean_sales_data_ProductMix(months_to_analyze, years_to_analyze)
# #men_sales.head()

# #Sample Data 2
# sales_data = load_ItemSelectionDetails_SalesData(months_to_analyze, years_to_analyze)
#sales_data.head()

# sales_data_agg = aggregate_sales_data(sales_data, "Item Name", time_period = "Day")
# sales_data_agg

# # Test menu data 
# men_sales_cleaned = clean_data_labels(men_sales, "Item Name")
# men_sales_cleaned = standardFormat_data(men_sales_cleaned, "Item Name")
# men_sales_agg = aggregate_sales_data(men_sales_cleaned, "Item Name")
# #List all unique items in Item Nam e column in alphabetical order
# sorted_unique_menu = sorted(men_sales_cleaned["Item Name"].dropna().unique())
# #display(sorted_unique_menu)


# function that makes every value in every column lowercase, and strips white spaces from ends

## Test individual Sales Data
# sales_data_cleaned = clean_data_labels(sales_data, "Item Name")
# sales_data_cleaned = standardFormat_data(sales_data_cleaned, "Item Name")
# sales_data_agg = aggregate_sales_data(sales_data_cleaned, "Item Name")
# #List all unique items in Item Nam e column in alphabetical order
# #sorted_unique_sales = sorted(sales_data_cleaned["Item Name"].dropna().unique())
# #display(sorted_unique_sales)
