"""
Report Runner
Report generation and ad-hoc analysis runner.

Originally developed in Deepnote. Deepnote "module import" blocks are
marked with # DEEPNOTE MODULE IMPORT comments — replace with standard
Python imports in a local environment.
"""

# # Library and data read-in

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

# # Module Read in

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
# In Deepnote, this block runs notebook 'Cleaning Data Pipeline' as a module,
# making its variables and functions available in this notebook.
# In standard Python, import the equivalent module:
#   from cleaning_data_pipeline import *
# or copy the relevant function definitions from that notebook.
# ============================================================

# ============================================================
# DEEPNOTE MODULE IMPORT
# In Deepnote, this block runs notebook 'Expense Read-in' as a module,
# making its variables and functions available in this notebook.
# In standard Python, import the equivalent module:
#   from expense_read-in import *
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

# # Set Months/Years to Analyze

#Input which months to analyze
months_to_analyze = ['September', 'October', 'November', 'December']
years_to_analyze = 2025

# ## Define Variables for DataFrames
# 
# Menu_data is grouped already
# Sales_data is messier, but has each sale recorded individually

# Costs, Menu Prices, Profit % of Menu Items
menu_ProfitAnalysis_df = menu_PricesandCosts.copy()

menu_data = load_ProductMix_MenuData(months_to_analyze, years_to_analyze)

sales_data = load_ItemSelectionDetails_SalesData(months_to_analyze, years_to_analyze)

# Cleaning Pipeline
menu_ProfitAnalysis_df = cleaning_pipeline(menu_ProfitAnalysis_df)
menu_data = cleaning_pipeline(menu_data)
sales_data = cleaning_pipeline(sales_data)

# Aggregations
sales_daily_agg = aggregate_sales_data(sales_data, time_period = "Day")
sales_monthly_agg = aggregate_sales_data(sales_data, time_period = "Month")

# Add profit
sales_with_profit_pct = add_profit_to_sales(sales_data, menu_ProfitAnalysis_df)
sales_daily_agg = add_profit_to_sales(sales_daily_agg, menu_ProfitAnalysis_df)
sales_monthly_agg = add_profit_to_sales(sales_monthly_agg, menu_ProfitAnalysis_df)


daily_profit_df = build_daily_profitability_with_expenses(
    sales_daily_agg,
    expenses_config_df
)

# # Sales/Profit to Date

# There are a significant (~380) items with quantities sold, but no profit/price

# I can probably save myself some headback by just using daily_profits
# Run the function on sales_with_profit_pct
#plot_daily_profit_and_revenue(sales_with_profit_pct)

ax, ax2, plot_df = plot_daily_and_cumulative_profit(daily_profit_df)

# The recreated graph uses daily_profit_df mapped to the expected columns and matches the earlier plot, confirming the aggregation worked as intended.

# # Sales by Month/Category

categorized_monthly_sales = categorize_group_sales(sales_monthly_agg)
categorized_monthly_sales.head()

plot_category_sales_and_volume(categorized_monthly_sales, "Net Sales", False)

plot_category_sales_and_volume(categorized_monthly_sales, "Net Sales", True)

plot_category_sales_and_volume(categorized_monthly_sales, "Profit", False)

plot_category_sales_and_volume(categorized_monthly_sales, "Profit", True)

# Menu data and sales data still don't fully align, but are close. Sales aggregated is generally a little lower, I think because I am dropping nan sales and items without profit i.e. "free coffee"

# # Top 10 Most Profitable Days so far

# using daily profit, plot the 10 most profitable days

import matplotlib.ticker as mtick

def plot_top_bottom_profit_days(daily_profit_df, which='Top', n=10, palette_name="tab10", show_legend=False):
    # Ensure required columns
    required_cols = ['Date', 'total_profit', 'day_of_the_week']
    missing = [c for c in required_cols if c not in daily_profit_df.columns]
    if missing:
        raise ValueError(f"daily_profit_df missing columns: {missing}")
        
    # Normalize which
    which_norm = which.strip().lower()
    if which_norm not in ('top', 'bottom'):
        raise ValueError("Parameter 'which' must be 'Top' or 'Bottom'.")

    # -----------------------------
    # For Bottom, keep only days with sales conducted
    # -----------------------------
    df = daily_profit_df.copy()
    if which_norm == 'bottom':
        df = df[df['total_sales'] > 0]

    ascending = True if which_norm == 'bottom' else False
    subset = df.sort_values('total_profit', ascending=ascending).head(n).copy()
    subset['Date'] = pd.to_datetime(subset['Date']).dt.date

    unique_days = list(subset['day_of_the_week'].unique())
    palette_to_use = sns.color_palette(palette_name, n_colors=len(unique_days))

    # Map day_of_the_week to color palette
    day_to_color = dict(zip(unique_days, palette_to_use))

    plt.figure(figsize=(14, 8))
    ax = sns.barplot(
        data=subset,
        x='Date',
        y='total_profit',
        hue='day_of_the_week',
        dodge=False,
        palette=day_to_color,
        legend = False
    )

    # Titles and labels
    title_prefix = 'Top' if which_norm == 'top' else 'Bottom'
    plt.title(f'{title_prefix} {n} Most {"Profitable" if which_norm=="top" else "Unprofitable"} Days', fontsize=16)
    plt.xlabel('Date', fontsize=14, labelpad=10)
    plt.ylabel('Total Profit', fontsize=14, labelpad=10)
    plt.xticks(rotation=45, ha='right')

    # Format y-axis
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: f'${x/1000:.0f}k'))

    # Annotate day-of-week above each bar
    # Get the x positions of the bars (centered on the tick)
    x_positions = ax.get_xticks()

    y_offset = subset['total_profit'].max() * 0.02

    for x_pos, (_, row) in zip(x_positions, subset.iterrows()):
        y = row['total_profit']
        
        if y >= 0:
            text_y = y + y_offset
            va = 'bottom'
        else:
            text_y = 0 + y_offset  # annotation above 0 line
            va = 'bottom'
        
        ax.text(
            x=x_pos,
            y=text_y,
            s=row['day_of_the_week'],
            ha='center',
            va=va,
            fontsize=10,
            fontweight='bold',
            color='black'
    )

    if show_legend:
        ax.legend(title='Day of Week', bbox_to_anchor=(1.02,1), loc='upper left')

    plt.subplots_adjust(bottom=0.2, top=0.9, right=0.8 if show_legend else 0.95)
    plt.show()

    return subset
plot_top_bottom_profit_days(daily_profit_df, which='Top', n=10)

# # Top 10 Least Profitable Days so far

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd

def plot_top_bottom_profit_days(daily_profit_df, which='Top', n=10, palette_name="tab10", show_legend=False):
    # Ensure required columns
    required_cols = ['Date', 'total_profit', 'day_of_the_week']
    missing = [c for c in required_cols if c not in daily_profit_df.columns]
    if missing:
        raise ValueError(f"daily_profit_df missing columns: {missing}")
        
    # Normalize which
    which_norm = which.strip().lower()
    if which_norm not in ('top', 'bottom'):
        raise ValueError("Parameter 'which' must be 'Top' or 'Bottom'.")

    # -----------------------------
    # For Bottom, keep only days with sales conducted
    # -----------------------------
    df = daily_profit_df.copy()
    if which_norm == 'bottom':
        df = df[df['total_sales'] > 0]

    ascending = True if which_norm == 'bottom' else False
    subset = df.sort_values('total_profit', ascending=ascending).head(n).copy()
    subset['Date'] = pd.to_datetime(subset['Date']).dt.date

    unique_days = list(subset['day_of_the_week'].unique())
    palette_to_use = sns.color_palette(palette_name, n_colors=len(unique_days))

    # Map day_of_the_week to color palette
    day_to_color = dict(zip(unique_days, palette_to_use))

    plt.figure(figsize=(14, 8))
    ax = sns.barplot(
        data=subset,
        x='Date',
        y='total_profit',
        hue='day_of_the_week',
        dodge=False,
        palette=day_to_color,
        legend = False
    )

    # Titles and labels
    title_prefix = 'Top' if which_norm == 'top' else 'Bottom'
    plt.title(f'{title_prefix} {n} Most {"Profitable" if which_norm=="top" else "Unprofitable"} Days', fontsize=16)
    plt.xlabel('Date', fontsize=14, labelpad=10)
    plt.ylabel('Total Profit', fontsize=14, labelpad=10)
    plt.xticks(rotation=45, ha='right')

    # Format y-axis
    def thousands_formatter(x, pos):
        if abs(x) >= 1000:
            return f'${x/1000:.1f}k'
        elif abs(x) >= 100:  # small values, show 1 decimal
            return f'${x/1000:.1f}k'
        else:  # really small numbers
            return f'${x:.0f}'

    ax.yaxis.set_major_formatter(mtick.FuncFormatter(thousands_formatter))

    # Annotate day-of-week above each bar
    # Get the x positions of the bars (centered on the tick)
    x_positions = ax.get_xticks()

    y_offset = subset['total_profit'].max() * 0.02

    for x_pos, (_, row) in zip(x_positions, subset.iterrows()):
        y = row['total_profit']
        
        if y >= 0:
            text_y = y + y_offset
            va = 'bottom'
        else:
            text_y = 0 + y_offset  # annotation above 0 line
            va = 'bottom'
        
        ax.text(
            x=x_pos,
            y=text_y,
            s=row['day_of_the_week'],
            ha='center',
            va=va,
            fontsize=10,
            fontweight='bold',
            color='black'
    )

    if show_legend:
        ax.legend(title='Day of Week', bbox_to_anchor=(1.02,1), loc='upper left')

    plt.subplots_adjust(bottom=0.2, top=0.9, right=0.8 if show_legend else 0.95)
    plt.show()

    return subset
plot_top_bottom_profit_days(daily_profit_df, which='Bottom', n=10)

# Need to move this function to Functions

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as mtick


def plot_top_seller_by_category(
    df,
    n=10,
    value_column='Quantity',
    sales_category=None,
    palette_name='tab10',
    which='Top',
    min_quantity=1
):
    """
    Plot the top or bottom n items by a specified value column (Quantity, Profit, or Profit %).

    Parameters:
    - df: pd.DataFrame containing item-level aggregated data. Expected columns include:
        ['Item Name', 'Sales Category', 'Quantity', 'Profit', 'Profit %'] (at minimum, depending on value_column)
    - n: int, number of items to display.
    - value_column: str, which column to sort/plot by. Options: 'Quantity', 'Profit', or 'Profit %'.
    - sales_category: None, str, or list-like. If provided, filter df to these Sales Category values.
    - palette_name: str, seaborn palette name for coloring bars. (Ignored for category colors; retained for API compatibility.)
    - which: 'Top' or 'Bottom'. If 'Bottom', items are filtered to those with Quantity > min_quantity.
    - min_quantity: numeric; when which='Bottom', require items to have strictly more than this quantity.

    Returns:
    - subset: pd.DataFrame of the selected n items used in the plot.
    """
    # Validate inputs
    if not isinstance(df, pd.DataFrame):
        raise ValueError('df must be a pandas DataFrame')

    # Validate value_column
    valid_value_cols = {'Quantity', 'Profit', 'Profit %'}
    if value_column not in valid_value_cols:
        raise ValueError(f"value_column must be one of {valid_value_cols}, got '{value_column}'")

    # Normalize which parameter
    which_norm = str(which).strip().lower()
    if which_norm not in ('top', 'bottom'):
        raise ValueError("Parameter 'which' must be 'Top' or 'Bottom'.")

    # Required columns check
    base_required = {'Item Name', 'Sales Category', 'Quantity'}
    if value_column == 'Profit':
        required_cols = base_required | {'Profit'}
    elif value_column == 'Profit %':
        required_cols = base_required | {'Profit %'}
    else:
        required_cols = base_required

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")

    plot_df = df.copy()

    # Filter by sales category if provided
    if sales_category is not None:
        if isinstance(sales_category, (list, set, tuple)):
            plot_df = plot_df[plot_df['Sales Category'].isin(sales_category)]
        else:
            plot_df = plot_df[plot_df['Sales Category'] == sales_category]

    # Keep numeric rows for selected value_column
    plot_df = plot_df[pd.to_numeric(plot_df[value_column], errors='coerce').notna()]

    if plot_df.empty:
        raise ValueError('No data available to plot after filtering.')

    # Aggregate at item level in case df is transaction-level
    agg_dict = {'Quantity': 'sum'}
    # For Profit % we will use mean by item (more sensible than sum). Others sum.
    if value_column == 'Profit %':
        agg_dict[value_column] = 'mean'
    else:
        agg_dict[value_column] = 'sum'

    agg_df = (
        plot_df.groupby(['Item Name', 'Sales Category'], dropna=False)
               .agg(agg_dict)
               .reset_index()
    )

    # If bottom: filter out items with low quantity according to min_quantity
    if which_norm == 'bottom':
        agg_df = agg_df[agg_df['Quantity'] > min_quantity]

    if agg_df.empty:
        raise ValueError('No items available after applying bottom/quantity filters.')

    # Sort by value_column and take n based on which
    ascending = True if which_norm == 'bottom' else False
    subset = agg_df.sort_values(value_column, ascending=ascending).head(n).copy()

    # Force colors by Sales Category mapping
    # Drinks -> blue, Food -> red, Retail -> green; handle case-insensitively
    # Use a default gray for any unexpected categories to avoid errors.
    category_color_map = {
        'drinks': '#1f77b4',  # blue
        'drink': '#1f77b4',   # alias safeguard
        'beverages': '#1f77b4',
        'food': '#d62728',    # red
        'retail': '#2ca02c'   # green
    }

    # Build palette only for categories that appear in subset
    unique_cats = list(subset['Sales Category'].astype(str).unique())
    cat_to_color = {}
    for cat in unique_cats:
        key = str(cat).strip().lower()
        cat_to_color[cat] = category_color_map.get(key, '#7f7f7f')  # fallback gray

    # Plot
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(
        data=subset,
        x='Item Name',
        y=value_column,
        hue='Sales Category',
        palette=cat_to_color,
        dodge=False
    )

    # Titles and labels
    title_cat = ''
    if sales_category is not None:
        if isinstance(sales_category, (list, set, tuple)):
            title_cat = f" for Categories: {', '.join(map(str, sales_category))}"
        else:
            title_cat = f" for Category: {sales_category}"
    title_prefix = 'Top' if which_norm == 'top' else 'Bottom'
    plt.title(f"{title_prefix} {n} Items by {value_column}{title_cat}", fontsize=16)
    plt.xlabel('Item Name', fontsize=14, labelpad=10)

    # Y-axis label and formatter based on value_column
    if value_column == 'Profit':
        plt.ylabel('Profit', fontsize=14, labelpad=10)
        def thousands_formatter(x, pos):
            if abs(x) >= 1000:
                return f'${x/1000:.0f}k'
            else:
                return f'${x:,.0f}'
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(thousands_formatter))
    elif value_column == 'Profit %':
        plt.ylabel('Profit %', fontsize=14, labelpad=10)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0)) if subset[value_column].max() <= 1.0 else ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:.0f}%'))
    else:
        plt.ylabel('Quantity', fontsize=14, labelpad=10)
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

    plt.xticks(rotation=45, ha='right')

    # Hide legend if only one category
    if len(unique_cats) <= 1:
        if ax.get_legend() is not None:
            ax.legend_.remove()

    plt.tight_layout()
    plt.show()

    return subset

# # Top 10 Products by Quantity

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Quantity', sales_category=None)

# medialuna needs to be renamed to argentinian medialuna

# ## Top 10 Products by Sales: Food

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Quantity', sales_category='Food')

# ## Top 10 Products by Sales: Drinks

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Quantity', sales_category='Drinks')

# ## Top 10 Products by Sales: Retail

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Quantity', sales_category='Retail')

# # Top 10 Products by Profit

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit')

# # Top 10 Products by Profit: Food

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit', sales_category = 'Food')

# # Top 10 Products by Profit: Drinks

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit', sales_category = 'Drinks')

# # Top 10 Products by Profit: Retail

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit', sales_category = 'Retail')

# # Top 10 Profit % Items

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit %', sales_category=None)

# # Top 10 Profit % Items: Food

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit %', sales_category='Food')

# # Top 10 Profit % Items: Drinks

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit %', sales_category='Drinks')

# # Top 10 Profit % Items: Retail

plot_top_seller_by_category(sales_with_profit_pct, n=10, value_column='Profit %', sales_category='Retail')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as mtick


def plot_specific_item_by_day(df, item_selection="", time_frame="all"):
    # Validate/prepare time frame filter
    filtered_df = df.copy()
    if time_frame is not None and str(time_frame).strip().lower() != "all":
        try:
            days = int(time_frame)
        except (ValueError, TypeError):
            raise ValueError("time_frame must be 'all' or an integer number of days, e.g., 7")
        if 'Time' not in filtered_df.columns:
            raise ValueError("DataFrame must contain a 'Time' datetime column to use time_frame filtering")
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

    # Create a pivot for stacked bars
    pivot_counts = counts.pivot(index='Day_of_Week', columns='Item Name', values='count').fillna(0)
    if 'day_order' in globals():
        pivot_counts = pivot_counts.reindex(day_order)

    # Choose a color palette
    unique_items = pivot_counts.columns.tolist()
    palette = sns.color_palette('tab10', n_colors=min(10, len(unique_items)))
    if len(unique_items) > 10:
        palette = sns.color_palette('tab20', n_colors=min(20, len(unique_items)))
        if len(unique_items) > 20:
            palette = sns.color_palette('husl', n_colors=len(unique_items))

    color_map = {item: palette[i % len(palette)] for i, item in enumerate(unique_items)}

    plt.figure(figsize=(16, 6))
    ax = pivot_counts.plot(kind='bar', stacked=True, color=[color_map[c] for c in pivot_counts.columns])

    tf_title = "All Time" if str(time_frame).strip().lower() == "all" else f"Past {int(time_frame)} Days"
    ax.set_title(f'Item Count by Day of Week (colored by Item Name) — {tf_title}')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Count')

    plt.xticks(rotation=45, ha='right')
    ax.grid(axis='x', linestyle='-', alpha=0.0)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(title='Item Name', bbox_to_anchor=(1.02, 1), loc='upper left')

    label_offset = 0
    total_counts_per_day = pivot_counts.sum(axis=1)
    ymax_needed = float(total_counts_per_day.max() + label_offset + 2) if len(total_counts_per_day) else 0
    current_ymax = ax.get_ylim()[1]
    if ymax_needed > current_ymax:
        ax.set_ylim(top=ymax_needed)

    for i, total in enumerate(total_counts_per_day):
        ax.text(i, total + label_offset, f'{int(total)}', ha='center', va='bottom', color='black', fontsize=9)

    if len(unique_items) >= 2:
        bar_containers = ax.containers
        totals = total_counts_per_day.values
        for container_idx, container in enumerate(bar_containers):
            col_name = pivot_counts.columns[container_idx] if container_idx < len(pivot_counts.columns) else None
            for rect_idx, rect in enumerate(container):
                height = rect.get_height()
                if totals[rect_idx] > 0 and height > 0:
                    pct = (height / totals[rect_idx]) * 100.0
                    x = rect.get_x() + rect.get_width() / 2.0
                    y = rect.get_y() + height / 2.0
                    ax.text(x, y, f"{pct:.0f}%", ha='center', va='center', color='white', fontsize=7, fontweight='bold')

    plt.tight_layout()
    plt.show()

    # --- Print average sold per item per day ---
    # Determine how many of each day appear in the filtered data to compute a true average
    # Count the number of distinct weeks (occurrences) per day to divide by
    if 'Time' in filtered_df.columns:
        filtered_df['Time'] = pd.to_datetime(filtered_df['Time'])
        # Count how many times each day of week appears (i.e., how many Mondays, Tuesdays, etc.)
        day_occurrence_counts = filtered_df.drop_duplicates(subset='Time').groupby(
            filtered_df['Time'].dt.date
        ).first().reset_index(drop=True)
        # Simpler: count distinct dates per day of week
        filtered_df['_date'] = filtered_df['Time'].dt.date
        distinct_days = filtered_df.drop_duplicates(subset='_date')[['_date', 'Day_of_Week']]
        day_occurrences = distinct_days.groupby('Day_of_Week', observed = False).size()
    else:
        day_occurrences = None

    print("\n--- Average Items Sold Per Day ---\n")
    for item in unique_items:
        if item not in pivot_counts.columns:
            continue
        print(f"{item} sold an average of:")
        for day in pivot_counts.index:
            total_sold = pivot_counts.loc[day, item]
            if day_occurrences is not None and day in day_occurrences.index and day_occurrences[day] > 0:
                avg = total_sold / day_occurrences[day]
            else:
                # Fall back to raw count if no date info available
                avg = total_sold
            print(f"  {avg:.1f} on {day},")
        print()

plot_specific_item_by_day(sales_data, 'hand cut steak empanada, pulled bbq pork empanada, ham & cheese empanada, chicken empanada, capresse empanada', 60)

sales_data[sales_data['Menu Group'] == 'Pastry']['Item Name'].unique()

plot_specific_item_by_day(sales_data, 'croissant, almond croissant, cookie, chocolate croissant, brioche fruits, palmier, muffin', 60)

sales_data

import pandas as pd
import numpy as np
import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation

import zipfile
from datetime import datetime
import calendar
# %matplotlib inline  # Jupyter magic: run `matplotlib.use("Agg")` or remove in a script context

# ============================================================
# DEEPNOTE MODULE IMPORT
# In Deepnote, this block runs notebook 'Functions Read-in' as a module,
# making its variables and functions available in this notebook.
# In standard Python, import the equivalent module:
#   from functions_read-in import *
# or copy the relevant function definitions from that notebook.
# ============================================================

#Input which months to analyze
months_to_analyze = ['September', 'October', 'November', 'December']
years_to_analyze = 2025
sales_data = load_ItemSelectionDetails_SalesData(months_to_analyze, years_to_analyze)
sales_data = add_day_of_week(sales_data);

menu_data = load_ProductMix_MenuData(months_to_analyze, years_to_analyze);

# Fix grouping of misc_sales to aggregate across months per Item Name with specified aggregations
# Preserve existing variables and logic structure

# Filter menu_data to misc categories
misc_sales = menu_data[menu_data['Sales Category'].isin(['Books', 'Candles', 'Kinto'])]

# Group by Item Name while keeping other categorical columns consistent using first (they should be identical per item)
# Aggregate: Quantity sum, Avg Price mean, Net Sales sum
agg_spec = {
    'Sales Category': 'first',
    'Menu Group': 'first',
    'Month': lambda x: ', '.join(sorted(set(x))),  # list months present for the item
    'Avg Price': 'mean',
    'Quantity': 'sum',
    'Net Sales': 'sum',
    'Year': 'first'
}

misc_sales_grouped = (
    misc_sales
    .groupby('Item Name', as_index=False)
    .agg(agg_spec)
    .sort_values(by='Quantity', ascending=False)
)

# Display the grouped DataFrame
misc_sales_grouped

sales_data[sales_data['Sales Category'].isin(['Books', 'Candles', 'Kinto'])]

sales_data2[sales_data2['Item Name'] == "Hand Cut Steak Empanada"]

import pandas as pd

# Mapping dictionary for correcting Item Names with NaN Sales Category
# Keys are the incorrect/misc names, values are the canonical Item Name to look up
# Use None to indicate rows that should be dropped entirely during cleaning.
ITEM_NAME_CORRECTION_MAP = {
    # Existing examples provided by user
    'Carne Normal': 'Hand Cut Steak Empanada',
    'Steak Empanada': 'Hand Cut Steak Empanada',
    'Carne Picante': 'Hand Cut Steak Empanada',
    'Carne Picante Empanada': 'Hand Cut Steak Empanada',
    'Carne Empanada': 'Hand Cut Steak Empanada',
    'Empanada de Carne': 'Hand Cut Steak Empanada',
    'Fugazzeta': 'Fugazette Empanada',
    'Fugazzeta Empanada': 'Fugazette Empanada',  # normalize spelling to canonical
    'Hand cut steak empanadas': 'Hand Cut Steak Empanada',  # plural to singular canonical
    'Fugazzet': 'Fugazette Empanada',  # misspelling to canonical
    '2 Carne Picante': 'Hand Cut Steak Empanada',
    'Fugazzeta Y Carne Spicy': 'Fugazette Empanada',
    'Cheese And Onion Empanada': 'Fugazette Empanada',
    'Empanada Fugazzeta': 'Fugazette Empanada',
    'Fugazzeta Empanada': 'Fugazette Empanada',
    'Fugazette': 'Fugazette Empanada',
    # Drop cases
    'Dulce De Leche': None,  # indicate drop
}


def clean_na_sales(df: pd.DataFrame, name_map: dict = None) -> pd.DataFrame:
    """Clean rows where Sales Category is NaN by mapping Item Name to a canonical item
    and filling Menu Group, Menu, and Sales Category from canonical rows in the same df.

    Parameters
    - df: sales_data DataFrame containing columns ['Item Name', 'Menu Group', 'Menu', 'Sales Category']
    - name_map: optional dict mapping problematic Item Name -> canonical Item Name (string), or None to drop.
                If None, uses ITEM_NAME_CORRECTION_MAP.

    Returns
    - A copy of df with NaN Sales Category rows fixed where possible. Rows mapped to None are dropped.
    """
    if name_map is None:
        name_map = ITEM_NAME_CORRECTION_MAP

    required_cols = ['Item Name', 'Menu Group', 'Menu', 'Sales Category']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"DataFrame missing required column: {col}")

    out = df.copy()

    # Identify rows needing fix (Sales Category NaN and present in map)
    needs_fix = out['Sales Category'].isna() & out['Item Name'].isin(name_map.keys())
    if not needs_fix.any():
        return out

    # Map each problematic Item Name to its canonical name (or None for drop)
    mapped = out.loc[needs_fix, 'Item Name'].map(name_map)

    # Handle drop cases: rows where mapped canonical is None are removed
    drop_mask = mapped.isna()
    if drop_mask.any():
        # Explicitly drop these rows
        to_drop_idx = mapped[drop_mask].index
        out = out.drop(index=to_drop_idx)
        # Recompute needs_fix on the updated DataFrame
        needs_fix = out['Sales Category'].isna() & out['Item Name'].isin(name_map.keys())
        mapped = out.loc[needs_fix, 'Item Name'].map(name_map)

    if not needs_fix.any():
        return out

    # Build a lookup from canonical item name to the canonical attributes
    # Prefer rows where Sales Category is not NaN, and take the most frequent non-null values
    canonical_names = set(mapped.dropna().unique())
    canon_rows = out[out['Sales Category'].notna() & out['Item Name'].isin(canonical_names)]

    if canon_rows.empty and len(canonical_names) > 0:
        # No canonical rows found — nothing to fill, return current out
        return out

    # Aggregate canonical info per canonical item
    def mode_nonnull(series):
        s = series.dropna()
        if s.empty:
            return pd.NA
        return s.mode().iloc[0]

    canon_info = (
        canon_rows
        .groupby('Item Name', as_index=True)
        .agg({
            'Menu Group': mode_nonnull,
            'Menu': mode_nonnull,
            'Sales Category': mode_nonnull
        })
    )

    # Join to canonical info
    filled = mapped.to_frame(name='Canonical Name').join(canon_info, on='Canonical Name')

    # Assign back where we have available canonical data
    for col in ['Menu Group', 'Menu', 'Sales Category']:
        out.loc[needs_fix, col] = filled[col].values

    # Normalize Item Name itself to canonical
    out.loc[needs_fix, 'Item Name'] = filled.index.map(lambda idx: mapped.loc[idx])

    return out

# Apply cleaning to current sales_data if present
try:
    sales_data2 = clean_na_sales(sales_data)
except Exception as e:
    print(f"clean_na_sales could not be applied: {e}")

# ## Update item name correction map and cleaning function to handle drop cases

# get sales data where sales category is nan
sales_data2[sales_data2['Sales Category'].isna()]

# NOTE: item name correction map (assign to dict for use)
# item_name_corrections = {
#     "Fugacetta Empanada": "Fugazzeta Empanada",
#     "Huevos Scrambled. Mezclado": None
#     "Breakfast Sandwich": "Breakfast Sandwich",
#     "Huevos Revuektod 2 Huevos": None,
#     "Almond Milk": None,
#     "E-Gift Card": None, #Look into adding items
#     "Huevos Revueltos 2 Huevos": None,
#     "Dos De Fugazzeta": "Fugazzeta Empanada",
#     "Yogurt Con Fresas Para AcA": "Parfait Bowl",
#     "Dirty Chai": 
# }


sales_data2[sales_data2['Item Name'] == 'Fugazzeta Empanada']

# Re-apply cleaning explicitly and verify
sales_data2 = clean_na_sales(sales_data)

# Simple checks
print('Remaining NaN Sales Category rows:', sales_data2['Sales Category'].isna().sum())

# Confirm that known drop item is gone
print('Contains Dulce De Leche after cleaning:', ('Dulce De Leche' in sales_data2['Item Name'].unique()))

# Show a few rows for items corrected to Fugazette Empanada and Hand Cut Steak Empanada
mask_examples = sales_data2['Item Name'].isin(['Fugazette Empanada', 'Hand Cut Steak Empanada'])
sales_data2[mask_examples].sort_values('Time').head(20)

sorted(menu_data['Item Name'].unique())

sales_data['Sales Category'].unique()
