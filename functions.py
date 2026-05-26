"""
Functions
Reusable data loading and analysis functions for the café analytics pipeline.

Originally developed in Deepnote. Deepnote "module import" blocks are
marked with # DEEPNOTE MODULE IMPORT comments — replace with standard
Python imports in a local environment.
"""

# # Function Load In

import pandas as pd
import numpy as np
import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation

import zipfile
from datetime import datetime
import calendar
# %matplotlib inline  # Jupyter magic: run `matplotlib.use("Agg")` or remove in a script context

# # Data Reading Functions

# ## (Archived) load_and_clean_sales_data

# ### Input: (months, year),  'menu-breakdown-month-day-year.csv'
# Output: Sales data

def load_menu_data(months, year):
    """
    Loads and cleans sales data from CSV files for specified months and year.

    Args:
        months: A list of month names (e.g., ['August', 'September']).
        year: The year as an integer (e.g., 2025).

    Returns:
        A pandas DataFrame containing the concatenated and cleaned sales data
        for all specified months.

        Data looks like "Sales Category (food) |	Menu Group (breakfast) |	Item Name	(Salmon Toast) |
        Avg Price	| Quantity |	Net Sales	| Month
    """
    all_months_df = []

    for month in months:
        month_abr = month[:3].lower()
        if month in ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
            total_menu_filename = f'menu-breakdown-{month_abr}1-31-{year}.csv'
        elif month == 'February':
            total_menu_filename = f'/content/menu-breakdown-{month_abr}1-28-{year}.csv'
        else:
            total_menu_filename = f'/content/menu-breakdown-{month_abr}1-30-{year}.csv'
        df = pd.read_csv(total_menu_filename, index_col=False)

        # Rename the 'Menu' column to 'Sales Category' for clarity and consistency
        df = df.rename(columns={'Menu': 'Sales Category'})

        # Change the Menu categories to Food, Drinks, Retail
        df['Sales Category'] = df['Sales Category'].replace({
            'Food Menu': 'Food',
            'Beverages': 'Drinks',
            'Retail': 'Retail'
        })

        # Replace empty 'Menu Group' and 'Item Name' with "Total"
        df['Menu Group'] = df['Menu Group'].fillna('Total')
        df['Item Name'] = df['Item Name'].fillna('Total')


        df['Month'] = month

        # Drop Modifier, Gross Sales and Discount amount columns
        df = df.drop(['Modifier', 'Gross Sales', 'Discount Amount'], axis=1)

        all_months_df.append(df)

    combined_df = pd.concat(all_months_df, ignore_index=True)

    # Separate Food items and other items
    food_items = combined_df[combined_df['Sales Category'] == 'Food'].copy()
    other_categories_df = combined_df[combined_df['Sales Category'] != 'Food'].copy()

    # Group and aggregate Food items
    food_items_aggregated = food_items.groupby(['Sales Category', 'Menu Group', 'Item Name', 'Month']).agg(
        {'Avg Price': 'mean', 'Quantity': 'sum', 'Net Sales': 'sum'}
    ).reset_index()

    # Concatenate the aggregated Food items with the other categories
    combined_df = pd.concat([food_items_aggregated, other_categories_df], ignore_index=True)
    combined_df['Menu Group'] = combined_df['Menu Group'].fillna('Total')
    combined_df['Item Name'] = combined_df['Item Name'].fillna('Total')

    return combined_df

# ## load_and_clean_sales_data_ProductMix

# ### Input: (months, year), ProductMix.zip 
# 
# Output: Product Sales by menu group and item name (pre-grouped)

import zipfile
from datetime import datetime
import calendar

def load_ProductMix_MenuData(months, year):
    """
    Loads and cleans sales data from CSV files within ProductMix zip files
    for specified months and year.

    Args:
        months: A list of month names (e.g., ['August', 'September']).
        year: The year as an integer (e.g., 2025).

    Returns:
        A pandas DataFrame containing the concatenated and cleaned sales data
        for all specified months.

        Data looks like "Sales Category (food) |\tMenu Group (breakfast) |\tItem Name\t(Salmon Toast) |\n        Avg Price\t| Quantity |\tNet Sales\t| Month
    """
    print("Special requests and modifiers are in this dataset, but are being dropped for analysis")
    print("dropping gross sales, refunded items, etc. ")
    all_months_df = []

    for month_name in months:
        month_num = datetime.strptime(month_name, '%B').month
        last_day = calendar.monthrange(year, month_num)[1]

        # Format month and day for filename
        month_str = f'{month_num:02d}'
        start_day_str = '01'
        end_day_str = f'{last_day:02d}'

        # Construct the zip filename based on the new pattern
        zip_filename = f'ProductMix_{year}-{month_str}-{start_day_str}_{year}-{month_str}-{end_day_str}.zip'
        target_csv_part = 'selected levels.csv' # Part of the filename we are looking for (case-insensitive)

        try:
            with zipfile.ZipFile(zip_filename, 'r') as z:
                actual_csv_filename = None
                for name in z.namelist():
                    if target_csv_part in name.lower():
                        actual_csv_filename = name
                        break

                if actual_csv_filename is None:
                    raise KeyError(f"'{target_csv_part}' (case-insensitive) not found in zip file {zip_filename}")

                with z.open(actual_csv_filename) as f:
                    df = pd.read_csv(f, index_col=False)

            # --- Start cleaning and transformation steps ---

            # Drop items with Type not "NaN", or "menuItem".
            df = df[(df['Type'].isna()) | (df['Type'] == 'menuItem')].reset_index(drop=True)

            

            # Define columns to drop from the raw DataFrame (including the original 'Sales Category' and 'Tax')
            cols_to_drop_from_raw = [
                'Type', 'masterId', 'parentId', 'itemGuid', 'Size modifier',
                'Sales Category', 'Item tags', 'Deferred', 'Avg. item price (not incl. mods)',
                'Refund amount', 'Void amount', 'Waste count', 'Waste amount', 'Tax',
                'Gross sales', 'Discount amount', 'Subgroup', 'Modifiers, special requests' # These are from original data and the comments.
            ]
            existing_cols_to_drop_raw = [col for col in cols_to_drop_from_raw if col in df.columns]
            df = df.drop(existing_cols_to_drop_raw, axis=1)

            # Rename columns for clarity and consistency with previous functions
            df = df.rename(columns={
                'Menu': 'Sales Category', # Rename 'Menu' to 'Sales Category' after dropping the original one
                'Menu group': 'Menu Group',
                'Item, open item': 'Item Name',
                'Qty sold': 'Quantity',
                'Avg. price': 'Avg Price',
                'Net sales': 'Net Sales'# Renaming for consistency, will fillna later
            })

            # Change the Sales Category names
            df['Sales Category'] = df['Sales Category'].replace({
                'Food Menu': 'Food',
                'Beverages': 'Drinks',
                'Retail': 'Retail'
            })

            # Explicitly cast 'Sales Category' to string type to prevent dtype issues with .query()
            df['Sales Category'] = df['Sales Category'].astype(str)

            # Fill NaNs in specific columns with "Total"
            # Ensure columns exist before filling
            if 'Menu Group' in df.columns:
                df['Menu Group'] = df['Menu Group'].fillna('Total')
            if 'Item Name' in df.columns:
                df['Item Name'] = df['Item Name'].fillna('Total')
            if 'Subgroup' in df.columns:
                df['Subgroup'] = df['Subgroup'].fillna('Total')

            df['Month'] = month_name


            # No need for a second drop here, as most drops are handled earlier.
            # Any remaining drops not listed above could be added here if necessary.

            # Explicitly reset index of each DataFrame before appending to ensure uniqueness
            df = df.reset_index(drop=True)
            all_months_df.append(df)

        except FileNotFoundError:
            print(f"Error: Zip file not found for {month_name} {year}: {zip_filename}")
        except KeyError as e:
            print(f"Error: {e}") # Print the specific KeyError message
        except Exception as e:
            print(f"An error occurred while processing {zip_filename}: {e}")


    if not all_months_df:
        return pd.DataFrame() # Return empty DataFrame if no data was loaded

    combined_df = pd.concat(all_months_df, ignore_index=True)
    combined_df = combined_df.reset_index(drop=True) # Ensure index is unique after initial concat

    # Separate Food items and other items using .query() and reset_index() for robustness
    food_items = combined_df.query("`Sales Category` == 'Food'").reset_index(drop=True).copy()
    other_categories_df = combined_df.query("`Sales Category` != 'Food'").reset_index(drop=True).copy()

    # Group and aggregate Food items
    food_items_aggregated = food_items.groupby(['Sales Category', 'Menu Group', 'Item Name', 'Month']).agg(
        {'Avg Price': 'mean', 'Quantity': 'sum', 'Net Sales': 'sum'}
    ).reset_index()

    # Concatenate the aggregated Food items with the other categories
    combined_df = pd.concat([food_items_aggregated, other_categories_df], ignore_index=True)
    combined_df = combined_df.reset_index(drop=True) # Ensure index is unique after final concat

    # Add year column
    combined_df['Year'] = year

    print("Special requests and modifiers are in this dataset, but are being dropped for analysis")
    print("Dropping gross sales, refunded items, etc.")
    
    return combined_df
load_ProductMix_MenuData

# ## load_item_selection_data

# ### input: (months, year), "ItemSelectionDetails-
# 
# Output: Every Conducted Sale Data

import calendar
from datetime import datetime

def load_ItemSelectionDetails_SalesData(months, year):
    """
    Loads and concatenates sales data from "Item Selection Details" CSV files
    for specified months and year, and performs initial cleaning.

    Args:
        months: A list of month names (e.g., ['August', 'September']).
        year: The year as an integer (e.g., 2025).

    Returns:
        A pandas DataFrame containing the concatenated and cleaned sales data
        for all specified months.
    """
    all_months_df = []

    for month_name in months:
        month_num = datetime.strptime(month_name, '%B').month
        last_day = calendar.monthrange(year, month_num)[1]

        # Format month and day for filename
        month_str = f'{month_num:02d}'
        start_day_str = '01'
        end_day_str = f'{last_day:02d}'

        # Construct the filename based on the new pattern
        item_selection_filename = f'ItemSelectionDetails_{year}_{month_str}_{start_day_str}-{year}_{month_str}_{end_day_str}.csv'

        try:
            df = pd.read_csv(item_selection_filename, encoding='latin1')

            # Data Cleaning Steps:
            # Drop 'Order #' column
            df = df.drop('Order #', axis=1)

            # Change 'Sent Date' to 'Time' and convert to datetime format
            df = df.rename(columns={'Sent Date': 'Time'})
            # Assuming the format is 'Month/Day/Year Hour:Minute AM/PM'
            df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%y %I:%M %p')

            # Change 'Net Price' to 'Price'
            df = df.rename(columns={'Net Price': 'Price'})

            # Drop items where 'Void?' is True and then drop the 'Void?' column
            df = df[df['Void?'] == False]
            df = df.drop('Void?', axis=1)

            # Fill NaN 'Sales Category' with 'Menu' category
            df['Sales Category'] = df['Sales Category'].fillna(df['Menu'])

            # Change 'Beverages' to 'Drinks' in the 'Menu' column
            df['Menu'] = df['Menu'].replace('Beverages', 'Drinks')

            # Rename columns for clarity and consistency with previous functions
            df = df.rename(columns={
                'Menu Item': 'Item Name',
                'Qty': 'Quantity'
            })

            df['Month'] = month_name

            all_months_df.append(df)

        except FileNotFoundError:
            print(f"Error: File not found for {month_name} {year}: {item_selection_filename}")
        except Exception as e:
            print(f"An error occurred while reading the file for {month_name} {year}: {e}")
        # Extract the day of the week from the 'Time' column
    # Use dt.day_name() to get the full name of the day
    
    if all_months_df:
        combined_df = pd.concat(all_months_df, ignore_index=True)

        combined_df['Year'] = year
        combined_df['Day_of_Week'] = combined_df['Time'].dt.day_name()
        # Define the desired order of the days of the week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Convert 'Day_of_Week' to a categorical type with the specified order
        combined_df['Day_of_Week'] = pd.Categorical(combined_df['Day_of_Week'], categories=day_order, ordered=True)

        return combined_df
    else:
        return pd.DataFrame() # Return an empty DataFrame if no files were loaded
load_ItemSelectionDetails_SalesData

# # Data Cleaning/massaging Functions

# ## create_category_sales_df

# ### Input: Grouped Sales Data (men_sales)
# 
# Output: Combined into categories

def categorize_group_sales(df, value_column="Net Sales", group_column="Sales Category"):
    """
    Aggregate a sales dataframe by category (or menu group) and optionally by month/year,
    producing totals suitable for plotting, with a "Total" column per category and overall total.

    Parameters:
    - df: pandas DataFrame with at least ['Sales Category','Menu Group','Item Name','Month','Year','Avg Price','Quantity','Net Sales','Profit %','Profit']
    - value_column: 'Profit' or 'Net Sales' (which column to prioritize in grouping)
    - group_column: 'Sales Category' or 'Menu Group' (how to group data)

    Returns:
    - category_sales: grouped DataFrame with totals per category and overall Total row
    """

    import pandas as pd
    import numpy as np

    df = df.copy()

    # Columns to sum or average
    sum_cols = [c for c in ['Quantity', 'Net Sales', 'Profit'] if c in df.columns]
    mean_cols = [c for c in ['Avg Price', 'Profit %'] if c in df.columns]

    # Grouping columns
    grouping_cols = [group_column]
    if 'Month' in df.columns:
        grouping_cols.append('Month')
    if 'Year' in df.columns:
        grouping_cols.append('Year')

    # Aggregate dictionary
    agg_dict = {c: 'sum' for c in sum_cols}
    agg_dict.update({c: 'mean' for c in mean_cols})

    grouped = df.groupby(grouping_cols).agg(agg_dict).reset_index()

    # ---------- Add category-level totals ----------
    category_totals = grouped.groupby(group_column).sum(numeric_only=True).reset_index()
    category_totals['Month'] = 'Total'
    if 'Year' in grouped.columns:
        category_totals['Year'] = df['Year'].min()
    for col in mean_cols:
        if col in category_totals.columns:
            category_totals[col] = np.nan

    # Add totals for each category
    category_sales = pd.concat([grouped, category_totals], axis=0, ignore_index=True)

    # ---------- Add overall total ----------
    overall_total = category_sales.sum(numeric_only=True).to_dict()
    overall_total[group_column] = 'Total'
    overall_total['Month'] = 'Total'
    if 'Year' in df.columns:
        overall_total['Year'] = df['Year'].min()
    for col in mean_cols:
        if col in overall_total:
            overall_total[col] = np.nan

    category_sales = pd.concat([category_sales, pd.DataFrame([overall_total])], ignore_index=True)

    # ---------- Sort nicely ----------
    if 'Month' in category_sales.columns:
        calendar_months = ["January","February","March","April","May","June",
                           "July","August","September","October","November","December"]
        months_present = category_sales['Month'].astype(str).unique().tolist()
        ordered_months = [m for m in calendar_months if m in months_present]
        month_order = ['Total'] + ordered_months if 'Total' in months_present else ordered_months
        category_sales['Month'] = pd.Categorical(category_sales['Month'], categories=month_order, ordered=True)
        category_sales = category_sales.sort_values([group_column,'Month'])
    else:
        category_sales = category_sales.sort_values([group_column])

    return category_sales
categorize_group_sales

def add_day_of_week(df):
    """ 
    takes in dataframe
    returns dataframe, with day of the week added
    """
    df['Day_of_Week'] = df['Time'].dt.day_name()

    # Define the desired order of the days of the week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Convert 'Day_of_Week' to a categorical type with the specified order
    df['Day_of_Week'] = pd.Categorical(df['Day_of_Week'], categories=day_order, ordered=True)

    return df
add_day_of_week

# # Add profit to sales

def add_profit_to_sales(sales_df, profit_df):
    """
    Merge Profit % from profit_df onto sales_df by 'Item Name', apply default Profit % rules,
    compute Profit, and drop drink items with missing Profit %.

    Parameters
    ----------
    sales_df : pd.DataFrame
        Sales data with columns: ['Item Name', 'Sales Category', 'Price' or 'Avg Price', 'Quantity', ...]
    profit_df : pd.DataFrame
        Profit analysis data with columns: ['Item Name', 'Profit %', ...]

    Returns
    -------
    pd.DataFrame
        A copy of sales_df with 'Profit %' merged, 'Profit' calculated, and rows for drink items
        with missing profit removed.
    """
    # Work on a copy to avoid mutating the original sales_df
    merged = sales_df.merge(
        profit_df[["Item Name", "Profit %"]],
        on="Item Name",
        how="left"
    )

    # Apply default Profit % rules
    # - Food: 75%
    # - Retail, Books, Candles, Kinto, Merchandise: 50%
    mask_na_profit = merged["Profit %"].isna()
    merged.loc[mask_na_profit & (merged["Sales Category"] == "Food"), "Profit %"] = 75
    merged.loc[
        mask_na_profit & (merged["Sales Category"].isin(["Retail", "Books", "Candles", "Kinto", "Merchandise"])),
        "Profit %"
    ] = 50

    # Determine which price column to use: prefer 'Price'; if not present, use 'Avg Price'
    if 'Price' in merged.columns:
        price_col = 'Price'
    elif 'Avg Price' in merged.columns:
        price_col = 'Avg Price'
    else:
        raise KeyError("Neither 'Price' nor 'Avg Price' column found in sales_df for profit calculation.")

    # Compute Profit after defaults are filled, using the chosen price column
    merged["Profit"] = (
        merged[price_col] * merged["Quantity"] * merged["Profit %"] / 100
    )

    # Drop drink rows with NaN profit
    unique_drink_items_with_na_profit = merged[merged["Profit %"].isna()]["Item Name"].unique()
    cleaned = merged[~merged["Item Name"].isin(unique_drink_items_with_na_profit)].copy()

    # Example usage replacing the inline code (kept here to preserve original workflow variables):
    # sales_with_profit_pct = add_profit_to_sales(sales_data, menu_ProfitAnalysis_df)
    return cleaned
add_profit_to_sales

# # Create Daily Profit and Expense dataframe

def build_daily_profitability_with_expenses(sales_daily_agg, expenses_df):

    df = sales_daily_agg.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # -------------------------
    # Monthly fixed costs
    # -------------------------
    monthly_overhead_total = (
        expenses_df
        .query("category == 'Monthly Fixed'")
        ["amount"]
        .sum()
    )

    # -------------------------
    # Labor assumptions
    # -------------------------
    def get_amt(item_name):
        return (
            expenses_df
            .loc[expenses_df["item"] == item_name, "amount"]
            .iloc[0]
        )

    weekday_hours = get_amt("Weekday Staff Hours")
    weekend_hours = get_amt("Weekend Staff Hours")
    hourly_wage = get_amt("Hourly Wage")

    # -------------------------
    # Slippage
    # -------------------------
    slippage = (
        expenses_df
        .query("item == 'Slippage Rate'")
        ["amount"]
        .iloc[0]
    )

    # -------------------------
    # Labor lookup
    # -------------------------
    weekday_wage = weekday_hours * hourly_wage
    weekend_wage = weekend_hours * hourly_wage

    weekday_names = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    weekend_names = ["Saturday","Sunday"]

    labor_lookup = {
        **{d: weekday_wage for d in weekday_names},
        **{d: weekend_wage for d in weekend_names},
    }

    # -------------------------
    # Aggregate sales
    # -------------------------
    daily = (
        df.groupby(["Date","day_of_the_week"])
        .agg(
            total_sales=("Net Sales","sum"),
            total_sales_profit=("Profit","sum"),
        )
        .reset_index()
    )

    # -------------------------
    # COGS
    # -------------------------
    cogs = (
        df.assign(cogs=lambda x: x["Net Sales"] - x["Profit"])
        .groupby("Date")["cogs"]
        .sum()
        .reset_index(name="expenses_sales")
    )

    daily = daily.merge(cogs, on="Date", how="left")

    # -------------------------
    # Calendar-accurate fixed overhead
    # -------------------------
    daily["days_in_month"] = daily["Date"].apply(
        lambda d: calendar.monthrange(d.year, d.month)[1]
    )

    daily["daily_fixed_overhead"] = (
        monthly_overhead_total / daily["days_in_month"]
    )

    # -------------------------
    # Labor
    # -------------------------
    daily["labor_cost"] = daily["day_of_the_week"].map(labor_lookup)

    # -------------------------
    # Total overhead
    # -------------------------
    daily["expenses_overhead"] = (
        daily["daily_fixed_overhead"]
        + daily["labor_cost"]
    ) * (1 + slippage)

    # -------------------------
    # Profit metrics
    # -------------------------
    daily["total_profit"] = (
        daily["total_sales_profit"]
        - daily["expenses_overhead"]
    )

    daily["profit_margin"] = (
        daily["total_profit"] / daily["total_sales"]
    )

    return daily[
        [
            "Date",
            "day_of_the_week",
            "total_sales",
            "total_sales_profit",
            "expenses_sales",
            "expenses_overhead",
            "total_profit",
            "profit_margin",
        ]
    ]
build_daily_profitability_with_expenses

# # Plotting Functions

# # Plot daily profit after expenses


def plot_daily_and_cumulative_profit(daily_profit_df: pd.DataFrame,
                                     day_tick_interval: int = 5,
                                     figsize=(14, 6)):
    """
    Plot daily total profit (with weekday annotations) and a separate cumulative profit chart.
    Also overlays daily revenue (total_sales) in purple on the daily profit chart if available.

    Parameters
    ----------
    daily_profit_df : pd.DataFrame
        DataFrame with at least columns ['Date', 'total_profit', 'day_of_the_week'] and optionally 'total_sales'.
    day_tick_interval : int, optional
        Interval for day ticks on the x-axis. Default is 5.
    figsize : tuple, optional
        Figure size for both plots. Default is (14, 6).

    Returns
    -------
    (ax_profit, ax_cumulative) : tuple of matplotlib Axes
        Axes for the daily profit and cumulative profit plots, respectively.
    plot_df : pd.DataFrame
        The processed DataFrame used for plotting (includes 'dow_abbr' and 'cumulative_profit').
    """

    import matplotlib.dates as mdates
    from matplotlib.ticker import FuncFormatter

    # Ensure required columns exist
    required_cols = ['Date', 'total_profit', 'day_of_the_week']
    missing = [c for c in required_cols if c not in daily_profit_df.columns]
    if missing:
        raise ValueError(f"daily_profit_df is missing required columns: {missing}")

    # Prepare data
    plot_df = daily_profit_df.copy().sort_values('Date').reset_index(drop=True)

    # Map full weekday names to two-letter abbreviations
    weekday_map = {
        'Monday': 'Mo', 'Tuesday': 'Tu', 'Wednesday': 'We', 'Thursday': 'Th',
        'Friday': 'Fr', 'Saturday': 'Sa', 'Sunday': 'Su'
    }
    # If day_of_the_week might already be abbreviated, fall back gracefully
    plot_df['dow_abbr'] = plot_df['day_of_the_week'].map(weekday_map).fillna(
        plot_df['day_of_the_week'].astype(str).str[:2]
    )

    # Helper formatter for currency with K suffix
    k_dollar = FuncFormatter(lambda x, pos: f"${x/1000:.0f}k" if abs(x) >= 1000 else f"${x:,.0f}")

    # -------- Figure 1: Daily Profit (+ Revenue overlay) --------
    fig1, ax_profit = plt.subplots(figsize=figsize)
    ax_profit.plot(
        plot_df['Date'], plot_df['total_profit'],
        color='green', label='Daily Profit', linewidth=2, marker='o', markersize=5
    )

    # Overlay revenue in purple if available
    if 'total_sales' in plot_df.columns:
        ax_profit.plot(
            plot_df['Date'], plot_df['total_sales'],
            color='purple', label='Daily Revenue', linewidth=2, alpha=0.8
        )

    # Annotate each daily point with the two-letter weekday abbreviation slightly above the marker
    for x, y_prof, label in zip(plot_df['Date'], plot_df['total_profit'], plot_df['dow_abbr']):
        ax_profit.annotate(label, (x, y_prof), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8, color='black')

    ax_profit.set_title('Daily Total Profit')
    ax_profit.set_xlabel('Date')
    ax_profit.set_ylabel('Amount ($)')
    ax_profit.legend()
    ax_profit.grid(True, which='major', linestyle='--', alpha=0.3)

    # Increase the frequency of x-ticks and format
    ax_profit.xaxis.set_major_locator(mdates.DayLocator(interval=day_tick_interval))
    ax_profit.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax_profit.yaxis.set_major_formatter(k_dollar)
    for label in ax_profit.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')

    fig1.tight_layout()
    plt.show()

    # -------- Figure 2: Cumulative Profit (separate graph) --------
    # Compute cumulative profit
    plot_df['cumulative_profit'] = plot_df['total_profit'].cumsum()

    fig2, ax_cumulative = plt.subplots(figsize=figsize)
    ax_cumulative.plot(plot_df['Date'], plot_df['cumulative_profit'], color='blue', label='Cumulative Profit', linewidth=2)

    ax_cumulative.set_title('Cumulative Profit')
    ax_cumulative.set_xlabel('Date')
    ax_cumulative.set_ylabel('Amount ($)')
    ax_cumulative.legend()
    ax_cumulative.grid(True, which='major', linestyle='--', alpha=0.3)

    ax_cumulative.xaxis.set_major_locator(mdates.DayLocator(interval=day_tick_interval))
    ax_cumulative.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax_cumulative.yaxis.set_major_formatter(k_dollar)
    for label in ax_cumulative.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')

    fig2.tight_layout()
    plt.show()

    return ax_profit, ax_cumulative, plot_df
plot_daily_and_cumulative_profit

# # Plot daily profit and revenue over time - just sales

# Plot daily total profit and overlay daily revenue from a provided dataframe

def plot_daily_profit_and_revenue_sales(input_df):
    """
    Plots daily total profit and daily revenue as two lines on the same axes.

    Args:
        input_df (pd.DataFrame): DataFrame containing at least the columns
            ['Time' or 'Date', 'Price', 'Quantity', 'Profit'].
            - Time/Date should be parseable to datetime.
    Returns:
        pd.DataFrame: The daily aggregated dataframe with columns ['Time','Profit','Revenue']
    """
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    import pandas as pd

    # Ensure required matplotlib utilities are imported
    from matplotlib.ticker import FuncFormatter
    import matplotlib.dates as mdates

    # Work on a copy to avoid mutating caller's data
    df = input_df.copy()

    # Determine the datetime column to use ('Time' preferred, else 'Date')
    time_col = None
    if 'Time' in df.columns:
        time_col = 'Time'
    elif 'Date' in df.columns:
        time_col = 'Date'
    else:
        raise KeyError("Input dataframe must contain a 'Time' or 'Date' column.")

    # Ensure chosen time column is datetime
    df[time_col] = pd.to_datetime(df[time_col])

    # Compute revenue column
    if 'Revenue' not in df.columns:
        if 'Price' in df.columns and 'Quantity' in df.columns:
            df['Revenue'] = df['Price'] * df['Quantity']
        else:
            raise KeyError("To compute 'Revenue', the dataframe must have 'Price' and 'Quantity' columns, or precomputed 'Revenue'.")

    # Aggregate daily profit and revenue
    daily_summary = df.set_index(time_col).resample('D').agg({
        'Profit': 'sum',
        'Revenue': 'sum'
    }).reset_index()

    # For output/plot consistency, rename the datetime column to 'Time'
    if time_col != 'Time':
        daily_summary = daily_summary.rename(columns={time_col: 'Time'})

    # Plot
    plt.figure(figsize=(14, 6))
    ax = sns.lineplot(x='Time', y='Profit', data=daily_summary, marker='o', color='green', label='Daily Profit')
    sns.lineplot(x='Time', y='Revenue', data=daily_summary, marker='o', color='blue', label='Daily Revenue', ax=ax)

    ax.set_title('Daily Total Profit and Revenue')
    ax.set_xlabel('Date')
    ax.set_ylabel('Dollars')
    ax.grid(True)

    currency_fmt = mtick.FuncFormatter(lambda x, _: '${:,.0f}'.format(x))
    ax.yaxis.set_major_formatter(currency_fmt)

    # X-axis formatting
    plt.xticks(rotation=45, ha='right')
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=5))

    plt.tight_layout()
    plt.show()

    return daily_summary
plot_daily_profit_and_revenue_sales

# # Plot daily revenue and volume

def plot_daily_sales_and_volume(df):
    """
    Generates a line graph showing daily net sales and volume over time
    with day of week annotations and a secondary y-axis for volume.

    Args:
        df: A pandas DataFrame with a 'Time', 'Price', and 'Quantity' columns.
            'Time' should be in datetime format.
    """
    # Ensure 'Time' is in datetime format and set it as the index
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.set_index('Time')

    # Calculate daily net sales (sum of Price * Qty for each day) and daily volume (sum of Quantity)
    daily_summary = df.resample('D').apply(lambda x: pd.Series({
        'Net Sales': (x['Price'] * x['Quantity']).sum(),
        'Volume': x['Quantity'].sum()
    })).reset_index()


    # Get the two-letter abbreviation for the day of the week
    daily_summary['Day_of_Week_Abr'] = daily_summary['Time'].dt.strftime('%a').str[:2]


    # Plotting
    plt.figure(figsize=(14, 7))

    # Create the first y-axis for Net Sales
    ax1 = sns.lineplot(x='Time', y='Net Sales', data=daily_summary, marker='o', label='Daily Net Sales', color='blue')
    ax1.set_ylabel('Net Sales')

    # Create a second y-axis for Volume
    ax2 = ax1.twinx()
    sns.lineplot(x='Time', y='Volume', data=daily_summary, marker='o', label='Daily Volume', color='green', ax=ax2, legend=False) # Turn off legend for ax2
    ax2.set_ylabel('Volume')


    plt.title('Daily Net Sales and Volume Over Time with Day of Week Annotations')
    ax1.set_xlabel('Date')
    ax1.grid(True) # Add grid to the first y-axis


    # Format y-axis labels as currency for the first y-axis
    import matplotlib.ticker as mtick
    formatter = mtick.FuncFormatter(lambda x, _: '${:,.0f}'.format(x))
    ax1.yaxis.set_major_formatter(formatter)

    # Improve date formatting on the x-axis
    plt.xticks(rotation=45, ha='right')
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d'))
    ax1.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=5)) # Adjust interval as needed

    # Set x-axis limits to ensure proper date range display
    ax1.set_xlim([daily_summary['Time'].min(), daily_summary['Time'].max()])


    # Add annotations for the day of the week abbreviation
    for i, row in daily_summary.iterrows():
        ax1.annotate(row['Day_of_Week_Abr'], (row['Time'], row['Net Sales']),
                    textcoords="offset points", xytext=(0, 5), ha='center')


    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.show()

plot_daily_sales_and_volume

# # Plot a single item sales by day

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as mtick


def plot_specific_item_by_day(df, item_selection="", time_frame="all"):
    # Translate the DeepnoteChart spec to equivalent Python (pandas + seaborn/matplotlib) code
    # Assumptions: 'sales_data' DataFrame exists with columns including 'Day_of_Week', 'Item Name', and 'Time' (datetime)
    # Goal: Plot bar chart showing count of items sold by Day_of_Week, colored by Item Name (stacked)

    # Validate/prepare time frame filter
    filtered_df = df.copy()
    if time_frame is not None and str(time_frame).strip().lower() != "all":
        try:
            days = int(time_frame)
        except (ValueError, TypeError):
            raise ValueError("time_frame must be 'all' or an integer number of days, e.g., 7")
        if 'Time' not in filtered_df.columns:
            raise ValueError("DataFrame must contain a 'Time' datetime column to use time_frame filtering")
        # Ensure datetime
        filtered_df['Time'] = pd.to_datetime(filtered_df['Time'])
        max_time = filtered_df['Time'].max()
        cutoff = max_time - pd.Timedelta(days=days)
        filtered_df = filtered_df[filtered_df['Time'] >= cutoff]

    # Prepare data: count of Item Name occurrences per Day_of_Week
    counts = (
        filtered_df.groupby(['Day_of_Week', 'Item Name'], observed=False)
        .size()
        .reset_index(name='count')
    )

    # Item selection handling
    if item_selection != "":
        if isinstance(item_selection, (list, tuple, set)):
            selected_items = list(item_selection)
        else:
            selected_items = str(item_selection).split(", ")
        counts = counts[counts['Item Name'].isin(selected_items)]
    else:
        user_input = input("Please enter items to analyze: ")
        selected_items = user_input.split(", ")
        counts = counts[counts['Item Name'].isin(selected_items)]

    # Create a pivot for stacked bars: rows are Day_of_Week, columns are Item Name, values are counts
    pivot_counts = counts.pivot(index='Day_of_Week', columns='Item Name', values='count').fillna(0)
    # Reindex rows by global day_order variable (provided in notebook)
    if 'day_order' in globals():
        pivot_counts = pivot_counts.reindex(day_order)

    # Choose a color palette
    unique_items = pivot_counts.columns.tolist()
    palette = sns.color_palette('tab10', n_colors=min(10, len(unique_items)))
    if len(unique_items) > 10:
        palette = sns.color_palette('tab20', n_colors=min(20, len(unique_items)))
        if len(unique_items) > 20:
            palette = sns.color_palette('husl', n_colors=len(unique_items))

    # Map item names to colors consistently
    color_map = {item: palette[i % len(palette)] for i, item in enumerate(unique_items)}

    # Expand horizontally: wider figure
    plt.figure(figsize=(16, 6))
    ax = pivot_counts.plot(kind='bar', stacked=True, color=[color_map[c] for c in pivot_counts.columns])

    # Titles and labels
    tf_title = "All Time" if str(time_frame).strip().lower() == "all" else f"Past {int(time_frame)} Days"
    ax.set_title(f'Item Count by Day of Week (colored by Item Name) — {tf_title}')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Count')

    # Rotate x ticks 45 degrees for readability
    plt.xticks(rotation=45, ha='right')

    # Remove vertical grid lines; keep optional subtle horizontal gridlines
    ax.grid(axis='x', linestyle='-', alpha=0.0)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # Place legend outside
    ax.legend(title='Item Name', bbox_to_anchor=(1.02, 1), loc='upper left')

    # Add value labels for total counts per day, ensuring they don't go over top of graph
    label_offset = 0
    total_counts_per_day = pivot_counts.sum(axis=1)
    ymax_needed = float(total_counts_per_day.max() + label_offset + 2) if len(total_counts_per_day) else 0
    current_ymax = ax.get_ylim()[1]
    if ymax_needed > current_ymax:
        ax.set_ylim(top=ymax_needed)

    for i, total in enumerate(total_counts_per_day):
        ax.text(i, total + label_offset, f'{int(total)}', ha='center', va='bottom', color='black', fontsize=9)

    # --- New: Annotate each stacked segment with its percent of the day's total ---
    # Only add percentages if there is more than one unique item (i.e., multiple stacked bars)
    if len(unique_items) >= 2:
        # Get the container list for bars (one container per item/column)
        bar_containers = ax.containers
        # Compute percentages per day
        totals = total_counts_per_day.values  # array aligned with x positions
        # Iterate over each container (each item) and its bars
        for container_idx, container in enumerate(bar_containers):
            # Determine which column this container corresponds to
            col_name = pivot_counts.columns[container_idx] if container_idx < len(pivot_counts.columns) else None
            # Fetch the counts for this item across days
            item_counts = pivot_counts[col_name].values if col_name is not None else None
            for rect_idx, rect in enumerate(container):
                height = rect.get_height()
                if totals[rect_idx] > 0 and height > 0:
                    pct = (height / totals[rect_idx]) * 100.0
                    # Position text centered within the segment
                    x = rect.get_x() + rect.get_width() / 2.0
                    y = rect.get_y() + height / 2.0
                    ax.text(x, y, f"{pct:.0f}%", ha='center', va='center', color='white', fontsize=7, fontweight='bold')

    plt.tight_layout()
    plt.show()

plot_specific_item_by_day

# #Input which months to analyze
# months_to_analyze = ['September', 'October', 'November']
# years_to_analyze = 2025
# sales_data = load_item_selection_data(months_to_analyze, years_to_analyze)

# # Extract the day of the week from the 'Time' column
# # Use dt.day_name() to get the full name of the day
# sales_data['Day_of_Week'] = sales_data['Time'].dt.day_name()

# # Define the desired order of the days of the week
# day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# # Convert 'Day_of_Week' to a categorical type with the specified order
# sales_data['Day_of_Week'] = pd.Categorical(sales_data['Day_of_Week'], categories=day_order, ordered=True)

# ## plot_category_sales_and_volume

# ### Plots Sales (after create_category_sales_df) by Category and Volume

def plot_category_sales_and_volume(df, money_column="Net Sales", plot_all=True):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    import seaborn as sns

    if money_column not in df.columns:
        raise ValueError(f"{money_column} not found in dataframe")

    category_sales = df.copy()

    # Remove any pre-existing Total rows
    category_sales = category_sales[category_sales['Sales Category'] != 'Total']

    # ---------- Compute total per month ----------
    total_per_month = category_sales.groupby('Month')[money_column].sum().reset_index()

    category_sales['Month'] = category_sales['Month'].astype(str)

    # ---------- Optional category filter ----------
    core_categories = ['Total', 'Food', 'Drinks', 'Retail']
    if not plot_all:
        category_sales = category_sales[
            category_sales['Sales Category'].astype(str).isin(core_categories)
        ]

    # ---------- Month order ----------
    calendar_months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    months_present = category_sales['Month'].unique().tolist()
    ordered_months = [m for m in calendar_months if m in months_present]
    month_order = (['Total'] if 'Total' in months_present else []) + ordered_months

    # ---------- Category order ----------
    main = ['Total','Food','Drinks','Retail']
    cats = category_sales['Sales Category'].astype(str).unique().tolist()

    if plot_all:
        category_order = [c for c in main if c in cats] + [c for c in cats if c not in main]
    else:
        category_order = [c for c in main if c in cats]

    category_sales['Month'] = pd.Categorical(category_sales['Month'], categories=month_order, ordered=True)
    category_sales['Sales Category'] = pd.Categorical(
        category_sales['Sales Category'],
        categories=category_order,
        ordered=True
    )

    category_sales = category_sales.sort_values(['Month','Sales Category'])
    category_sales = category_sales.dropna(subset=[money_column])

    # ---------- Plot ----------
    plt.figure(figsize=(16, 8))

    base_colors = {
        'Food':'red',
        'Drinks':'blue',
        'Retail':'green',
        'Total':'black'
    }

    missing = [c for c in category_order if c not in base_colors]
    if missing:
        extra = sns.color_palette('tab10', n_colors=len(missing))
        for c,col in zip(missing, extra):
            base_colors[c] = col

    ax = sns.barplot(
        x='Month',
        y=money_column,
        hue='Sales Category',
        data=category_sales,
        palette=base_colors,
        dodge=True,
        hue_order=category_order
    )
    y_max = ax.get_ylim()[1]

    ax.scatter(
            x=total_per_month['Month'],
            y=total_per_month[money_column],
            color='black',
            s=100,      # dot size
            zorder=5,   # ensures dots are on top
            label='Total'
        )
    
    # Annotate each dot with the total value
    for i, row in total_per_month.iterrows():
        ax.text(
            x=i,  # dot position
            y=row[money_column] + y_max*0.02,  # slightly above the dot
            s=f"${row[money_column]/1000:.1f}k",
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold',
            color='black'
        )
    
    plt.xlabel('Month', fontsize=18, labelpad = 14)
    plt.ylabel(money_column, fontsize=18, labelpad = 12)
    plt.title(f'{money_column} by Sales Category and Month', fontsize=20)
    ax.legend(title='Sales Category', fontsize=9, title_fontsize=10)

    ax.tick_params(axis='x', labelsize=14)  # x-axis tick labels
    ax.tick_params(axis='y', labelsize=14)  # y-axis tick labels

    formatter = mtick.FuncFormatter(lambda x, _: '${:,.0f}k'.format(x/1000))
    ax.yaxis.set_major_formatter(formatter)

    # ---------- Quantity lookup ----------
    if 'Quantity' in category_sales.columns:
        qty_table = category_sales.pivot(index="Month", columns="Sales Category", values="Quantity")
    else:
        qty_table = pd.DataFrame()

    def contrast(rgba):
        r,g,b = rgba[:3]
        return "black" if (0.299*r + 0.587*g + 0.114*b) > 0.6 else "white"

    # ---------- Dynamic text fit helper ----------
    def add_fitted_text(ax, patch, text, max_font=14, min_font=5):
        fig = ax.figure

        x = patch.get_x() + patch.get_width()/2
        y = patch.get_height() * 0.5

        txt = ax.text(
            x, y, text,
            ha="center",
            va="center",
            fontsize=max_font,
            fontweight="bold",
            color=contrast(patch.get_facecolor())
        )

        for fontsize in range(max_font, min_font-1, -1):
            txt.set_fontsize(fontsize)

            # force full draw so sizes are correct
            fig.canvas.draw()
            renderer = fig.canvas.get_renderer()

            text_box = txt.get_window_extent(renderer=renderer)
            bar_box = patch.get_window_extent(renderer=renderer)

            if (
                text_box.width <= bar_box.width * 0.9 and
                text_box.height <= bar_box.height * 0.9
            ):
                return

        txt.set_visible(False)

    # ensure renderer ready
    plt.gcf().canvas.draw()

    # ---------- Annotate bars ----------
    drawn_months = [m for m in month_order if m in category_sales['Month'].cat.categories]

    for container, category in zip(ax.containers, category_order):
        for patch, month in zip(container, drawn_months):
            height = patch.get_height()
            if height <= 0 or height < y_max * 0.03:
                continue

            if qty_table.empty:
                continue
            if month not in qty_table.index or category not in qty_table.columns:
                continue

            q = qty_table.loc[month, category]
            if pd.isna(q):
                continue

            label = f"{int(q)}" if q < 1000 else f"{q/1000:.1f}k \nSold"
            add_fitted_text(ax, patch, label)

    plt.tight_layout()
    plt.show()
plot_category_sales_and_volume

# ## plot_hourly_sales_by_day

# ### input: (item_selection df, day_of_week)
# 
# Output: total sales by time of day

def plot_hourly_sales_by_day(df, day_of_week="All"):
    """
    Plots the total sales by time of day for a specific day of the week or all days
    with a consistent x-axis showing hours from 7 to 17, including data outside this range.

    Args:
        df: A pandas DataFrame with 'Time', 'Price', and 'Day_of_Week' columns.
            'Time' should be in datetime format, and 'Day_of_Week' should contain day names.
        day_of_week: The name of the day to filter by (e.g., 'Monday', 'Tuesday').
                     Use "All" to include all days. Defaults to "All".
    """
    # Ensure 'Time' is in datetime format
    df['Time'] = pd.to_datetime(df['Time'])

    # Filter data based on the specified day of the week
    if day_of_week == "All":
        filtered_df = df.copy()
        title_suffix = " (All Days)"
    else:
        filtered_df = df[df['Day_of_Week'] == day_of_week].copy()
        title_suffix = f" ({day_of_week}s)"

    # Extract the hour from the 'Time' column
    filtered_df['Hour'] = filtered_df['Time'].dt.hour

    # Calculate total sales by hour
    hourly_sales = filtered_df.groupby('Hour')['Price'].sum().reset_index()

    # Create a DataFrame with all possible hours (0-23) and merge with hourly_sales
    # This ensures all hours are included in the data, even if no sales occurred,
    # before setting the displayed x-axis range.
    all_hours = pd.DataFrame({'Hour': range(0, 24)})
    hourly_sales = pd.merge(all_hours, hourly_sales, on='Hour', how='left').fillna(0)


    # Calculate the total sales across all hours for the filtered data (including hours with 0 sales)
    total_hourly_sales = hourly_sales['Price'].sum()

    # Plot sales by hour
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='Hour', y='Price', data=hourly_sales, palette='viridis', hue='Hour', legend=False)
    plt.title(f'Total Sales by Time of Day{title_suffix}')
    plt.xlabel('Hour of Day')
    plt.ylabel('Total Sales')

    # Set displayed x-axis limits to cover the range 7 to 17
    plt.xlim(6.5, 17.5) # Add some padding to the limits

    # Set x-ticks and labels explicitly for the range 7 to 17
    plt.xticks(range(7, 18))

    plt.grid(axis='y')

    # Add percentage annotations on top of each bar
    for p in ax.patches:
        height = p.get_height()
        # Find the corresponding hour for this patch based on its x-position
        # The x-position of the bar corresponds to the hour value when x is numerical
        hour = int(p.get_x() + p.get_width() / 2.)
        # Find the total sales for this hour from the hourly_sales DataFrame
        hourly_total = hourly_sales[hourly_sales['Hour'] == hour]['Price'].iloc[0]


        if total_hourly_sales > 0 and height > 0: # Only annotate bars with sales
            percentage = (height / total_hourly_sales) * 100
            ax.annotate(f'{percentage:.1f}%', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', xytext=(0, 3), textcoords='offset points')

    plt.show()

# Example usage:
# plot_hourly_sales_by_day(sales_data, "Monday") # Plot for Mondays
# plot_hourly_sales_by_day(sales_data, "Saturday") # Plot for Saturdays
# plot_hourly_sales_by_day(sales_data) # Plot for all days
plot_hourly_sales_by_day

# ## plot_top_bottom_revenue_items

# ### Input: (df, category, title_suffix, top_x)

def plot_top_bottom_revenue_items(df, category, title_suffix="", top_x=5):
    """
    Filters the input DataFrame by sales category, calculates total revenue and volume sold
    for each menu item, identifies the top X and bottom X items by revenue, and generates
    a combined bar chart with revenue on the y-axis and volume sold as annotations.

    Args:
        df: The input DataFrame (e.g., sales_data).
        category: A string representing the sales category to filter by (e.g., 'Drinks').
        title_suffix: An optional string for the plot title (e.g., ' (August & September)').
        top_x: The number of top and bottom items to display. Defaults to 5.
    """

    # Filter the input df to include only items where the 'Sales Category' column matches the provided category.
    filtered_category_items = df[df['Sales Category'] == category].copy()

    # Group the filtered data by 'Menu Item' and calculate aggregated metrics:
    # total_revenue: The sum of Price * Qty for each menu item.
    # volume_sold: The sum of Qty for each menu item.
    item_revenue_volume = filtered_category_items.groupby('Menu Item').apply(lambda x:
        pd.Series({
            'total_revenue': (x['Price'] * x['Qty']).sum(),
            'volume_sold': x['Qty'].sum()
        }), include_groups=False
    ).reset_index()

    # Identify the top X revenue-generating items
    top_items = item_revenue_volume.nlargest(top_x, 'total_revenue')

    # Identify the bottom X revenue-generating items
    # For this specific task, we'll assume bottom X can include low/zero revenue items if they exist.
    bottom_items = item_revenue_volume.nsmallest(top_x, 'total_revenue')

    # Concatenate the DataFrames for the top X and bottom X items into a single DataFrame.
    combined_items = pd.concat([top_items, bottom_items], ignore_index=True)

    # Sort for better visualization, perhaps by revenue
    combined_items = combined_items.sort_values(by='total_revenue', ascending=False)

    # Create a bar plot using seaborn.barplot
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x='Menu Item', y='total_revenue', data=combined_items, palette='viridis', hue='Menu Item', legend=False)

    # Set the plot title
    plt.title(f'Top and Bottom {top_x} {category} Items by Revenue{title_suffix}')
    plt.xlabel('Menu Item')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45, ha='right')

    # Format the y-axis labels as currency
    import matplotlib.ticker as mtick
    formatter = mtick.FuncFormatter(lambda x, _: '${:,.0f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)

    # Add annotations on top of each bar showing the 'volume_sold' for that item.
    for i, p in enumerate(ax.patches):
        x_center = p.get_x() + p.get_width() / 2.0
        y_pos = p.get_height()

        # Access the volume_sold from combined_items using the index 'i'
        volume_sold = combined_items.iloc[i]['volume_sold']

        ax.annotate(f'{int(volume_sold)} Sold', (x_center, y_pos),
                    ha='center', va='bottom', xytext=(0, 5), textcoords='offset points')

    plt.tight_layout()
    plt.show()
plot_top_bottom_revenue_items
