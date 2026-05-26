"""
Inventory
Inventory costs, recipes, and menu pricing.

Originally developed in Deepnote. Deepnote "module import" blocks are
marked with # DEEPNOTE MODULE IMPORT comments — replace with standard
Python imports in a local environment.
"""

# # This Notebook loads in Inventories, Recipes, Prices, Costs

# ## Libraries

import pandas as pd
import numpy as np
import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation

import zipfile
from datetime import datetime
import calendar
# %matplotlib inline  # Jupyter magic: run `matplotlib.use("Agg")` or remove in a script context

# ## Passwords

# [CREDENTIALS REDACTED — store securely in environment variables or a secrets manager]

# [CREDENTIALS REDACTED — store securely in environment variables or a secrets manager]

# [CREDENTIALS REDACTED — store securely in environment variables or a secrets manager]

# # Inventory Costs, Quantities, Recipes, etc.

# ## Purchased Inventory: Prices and Quantities

# ### Manual Entry Inventory Costs

## COFFEE ##

coffeeBag_size = 2268 #g
coffeeBag_price = 60

## PAPER ##

hot_cup_8oz_box_size = 1000 #units
hot_cup_8oz_box_price = 40

hot_cup_10oz_box_size = 1000 #units
hot_cup_10oz_box_price = 45

hot_cup_16oz_box_size = 1000 #units
hot_cup_16oz_box_price = 65

iced_cup_16oz_box_size = 1000 #units
iced_cup_16oz_box_price = 65

hot_lid_8oz_box_size = 1200 #units
hot_lid_8oz_box_price = 45

hot_lid_16oz_box_size = 1200 #units
hot_lid_16oz_box_price = 45

iced_lid_16oz_box_size = 1000 #units
iced_lid_16oz_box_price = 35

## Numbers are wrong ##
sleeve_box_size = 400 #units
sleeve_box_price = 15

## MILK/RETAIL DRINKS/SUGAR/SYRUPS ##

whole_milk_box_size = 4 #bags
whole_milk_box_price = 20
whole_milk_gallon_size = 128 #oz
whole_milk_gallon_price = whole_milk_box_price / whole_milk_box_size

## Add these to menuPrices ##

skim_milk_size = 64 #units
skim_milk_price = 2

twoPercent_milk_size = 64 #units
twoPercent_milk_price = 3

halfhalf_milk_size = 32 #units
halfhalf_milk_price = 3
# end add ##

## Oat numbers are wrong ##
oat_milk_box_size = 6 #bags
oat_milk_box_price = 20
oat_milk_carton_size = 32 #oz
oat_milk_carton_price = oat_milk_box_price / oat_milk_box_size

almond_milk_box_size = 6 #bags
almond_milk_box_price = 20
almond_milk_carton_size = 32 #oz
almond_milk_carton_price = almond_milk_box_price / almond_milk_box_size

sugar_bag_size = 1814.37 #g
sugar_bag_price = 5

#Add these to menu_PricesAndQuantities
still_water_box_size = 24 #bottles
still_water_box_price = 10
still_water_bottle_size = 16.9 #oz
still_water_bottle_price = still_water_box_price / still_water_box_size

sparkling_water_box_size = 24 #bottles
sparkling_water_box_price = 30
sparkling_water_bottle_size = 16.9 #oz
sparkling_water_bottle_price = sparkling_water_box_price / sparkling_water_box_size

orange_juice_box_size = 6 #bottles
orange_juice_box_price = 15
orange_juice_bottle_size = 12 #oz
orange_juice_bottle_price = orange_juice_box_price / orange_juice_box_size

lemonade_box_size = 6 #bottles
lemonade_box_price = 10
lemonade_bottle_size = 12 #oz
lemonade_bottle_price = lemonade_box_price / lemonade_box_size

apple_juice_box_size = 12 #bottles
apple_juice_box_price = 20
apple_juice_bottle_size = 8 #oz
apple_juice_bottle_price = apple_juice_box_price / apple_juice_box_size

## end add these ##

vanilla_syrup_bottle_size = 33.814 #oz
vanilla_syrup_bottle_price = 10

caramel_syrup_bottle_size = 33.814 #oz
caramel_syrup_bottle_price = 10

hazelnut_syrup_bottle_size = 33.814 #oz
hazelnut_syrup_bottle_price = 10

lavender_syrup_bottle_size = 33.814 #oz
lavender_syrup_bottle_price = 10

pistachio_syrup_bottle_size = 33.814 #oz
pistachio_syrup_bottle_price = 10

mocha_syrup_bottle_size = 64 #oz
mocha_syrup_bottle_price = 20

maple_syrup_bottle_size = 128 #oz
maple_syrup_bottle_price = 70

whipped_cream_bottle_size = 48 #oz
whipped_cream_bottle_price = 3

## numbers made up ##
chocolate_box_size = 300 #pieces
chocolate_box_price = 30

##numbers made up
coldbrew_carton_size = 32 #oz
coldbrew_carton_price = 10

chai_box_size = 20 #bags
chai_box_price = 20
chai_bag_size = 1 #bag
chai_bag_price = chai_box_price / chai_box_size

matcha_bag_size = 150 #g
matcha_bag_price = 15

earlGray_bag_size = 300 #g
earlGray_bag_price = 40

jasminePearls_bag_size = 300 #g
jasminePearls_bag_price = 40

whitePeach_bag_size = 300 #g
whitePeach_bag_price = 40

clarityMushroom_bag_size = 300 #g
clarityMushroom_bag_price = 40

upliftMushroom_bag_size = 300 #g
upliftMushroom_bag_price = 40

## AFFOGATO ##
affogato_carton_size = 64 #oz
affogato_carton_price = 20

## EL PRINCIPITO ##
cookie_cup_box_size = 24 #pieces
cookie_cup_box_price = 50

# ### Purchased Inventory: Into a Dataframe "inventory_QuantityAndCosts"

#Add 1 bag whole beans coffee
#set up inventory_QuantityAndCosts
coffeeBag_cost = {'Item': ['coffee_bag'],
               'Quantity': coffeeBag_size,
               'Unit': 'g',
               'Cost': coffeeBag_price}
inventory_QuantityAndCosts = pd.DataFrame(coffeeBag_cost)

#Add 1 gallon whole milk
new_item_data = {
    'Item': ['whole_milk_gallon'],
    'Quantity': whole_milk_gallon_size,
    'Unit': 'oz',
    'Cost': whole_milk_gallon_price}

new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'oat_milk_carton'
new_item_data = {
    'Item': ['oat_milk_carton'],
    'Quantity': [oat_milk_carton_size],
    'Unit': ['oz'],
    'Cost': [oat_milk_carton_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'almond_milk_carton'
new_item_data = {
    'Item': ['almond_milk_carton'],
    'Quantity': [almond_milk_carton_size],
    'Unit': ['oz'],
    'Cost': [almond_milk_carton_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'hot_cup_8oz_box'
new_item_data = {
    'Item': ['hot_cup_8oz_box'],
    'Quantity': [hot_cup_8oz_box_size],
    'Unit': ['ea'],
    'Cost': [hot_cup_8oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'hot_cup_10oz_box'
new_item_data = {
    'Item': ['hot_cup_10oz_box'],
    'Quantity': [hot_cup_10oz_box_size],
    'Unit': ['ea'],
    'Cost': [hot_cup_10oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'hot_cup_16oz_box'
new_item_data = {
    'Item': ['hot_cup_16oz_box'],
    'Quantity': [hot_cup_16oz_box_size],
    'Unit': ['ea'],
    'Cost': [hot_cup_16oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'iced_cup_16oz_box'
new_item_data = {
    'Item': ['iced_cup_16oz_box'],
    'Quantity': [iced_cup_16oz_box_size],
    'Unit': ['ea'],
    'Cost': [iced_cup_16oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'hot_lid_8oz_box'
new_item_data = {
    'Item': ['hot_lid_8oz_box'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_lid_8oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add '16oz_hot_lid_box'
new_item_data = {
    'Item': ['hot_lid_16oz_box'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_lid_16oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add '16oz_iced_lid_box'
new_item_data = {
    'Item': ['iced_lid_16oz_box'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [iced_lid_16oz_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'sleeve box'
new_item_data = {
    'Item': ['sleeve_box'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [sleeve_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)


# Add 'vanilla_syrup_bottle'
new_item_data = {
    'Item': ['vanilla_syrup_bottle'],
    'Quantity': [vanilla_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [vanilla_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)


# Add 'caramel_syrup_bottle'
new_item_data = {
    'Item': ['caramel_syrup_bottle'],
    'Quantity': [caramel_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [caramel_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'hazelnut_syrup_bottle'
new_item_data = {
    'Item': ['hazelnut_syrup_bottle'],
    'Quantity': [hazelnut_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [hazelnut_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'lavender_syrup_bottle'
new_item_data = {
    'Item': ['lavender_syrup_bottle'],
    'Quantity': [lavender_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [lavender_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'pistachio_syrup_bottle'
new_item_data = {
    'Item': ['pistachio_syrup_bottle'],
    'Quantity': [pistachio_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [pistachio_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'mocha_syrup_bottle'
new_item_data = {
    'Item': ['mocha_syrup_bottle'],
    'Quantity': [mocha_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [mocha_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'maple_syrup_bottle'
new_item_data = {
    'Item': ['maple_syrup_bottle'],
    'Quantity': [maple_syrup_bottle_size],
    'Unit': ['oz'],
    'Cost': [maple_syrup_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'whipped_cream_bottle'
new_item_data = {
    'Item': ['whipped_cream_bottle'],
    'Quantity': [whipped_cream_bottle_size],
    'Unit': ['oz'],
    'Cost': [whipped_cream_bottle_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'chocolate_box'
new_item_data = {
    'Item': ['chocolate_box'],
    'Quantity': [chocolate_box_size],
    'Unit': ['sticks'],
    'Cost': [chocolate_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'coldbrew_carton'
new_item_data = {
    'Item': ['coldbrew_carton'],
    'Quantity': [coldbrew_carton_size],
    'Unit': ['oz'],
    'Cost': [coldbrew_carton_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'matcha_bag'
new_item_data = {
    'Item': ['matcha_bag'],
    'Quantity': [matcha_bag_size],
    'Unit': ['g'],
    'Cost': [matcha_bag_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'chai_box'
new_item_data = {
    'Item': ['chai_box'],
    'Quantity': [chai_box_size],
    'Unit': ['ea'],
    'Cost': [chai_box_price]
 }
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'chai_bag'
new_item_data = {
    'Item': ['chai_bag'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [chai_bag_price]
 }
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'sugar_bag'
new_item_data = {
    'Item': ['sugar_bag'],
    'Quantity': [sugar_bag_size],
    'Unit': ['g'],
    'Cost': [sugar_bag_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'Affogato' carton
new_item_data = {
    'Item': ['affogato_carton'],
    'Quantity': [affogato_carton_size],
    'Unit': ['g'],
    'Cost': [affogato_carton_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'cookie cup box' 
new_item_data = {
    'Item': ['cookie_cup_box'],
    'Quantity': [cookie_cup_box_size],
    'Unit': ['g'],
    'Cost': [cookie_cup_box_price]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# ## Purchased Inventory: Derived Prices

### COFFEES ###

coffee_1g_cost = coffeeBag_price / coffeeBag_size
# Calculate cost of 1oz drip coffee
#235 grams whole batch makes 3.79L/128.1551oz
coffee_batch_quantity = 128.1551 #oz
coffee_batch_grams = 235 #g
drip_coffee_1oz_cost = coffee_batch_grams * coffee_1g_cost / coffee_batch_quantity
# Add 'drip_coffee_1oz'
new_item_data = {
    'Item': ['drip_coffee_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [drip_coffee_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of espresso shot from bag of coffee
esp_shot_cost_var = 18 * coffee_1g_cost
#Add espresso_shot
new_item_data = {'Item': ['espresso_shot'],
               'Quantity': 18,
               'Unit': 'g',
               'Cost': esp_shot_cost_var}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

### MILKS ###

# Calculate cost of 1oz whole milk
whole_milk_1oz_cost = whole_milk_gallon_price / whole_milk_gallon_size
#add 1oz whole milk
new_item_data = {
    'Item': ['whole_milk_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [whole_milk_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz oat milk
oat_milk_1oz_cost = oat_milk_carton_price / oat_milk_carton_size
# Add 'oat_milk_1oz'
new_item_data = {
    'Item': ['oat_milk_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [oat_milk_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz almond milk
almond_milk_1oz_cost = almond_milk_carton_price / almond_milk_carton_size
# Add 'almond_milk_1oz'
new_item_data = {
    'Item': ['almond_milk_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [almond_milk_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

### CUPS + LIDS ###

# Calculate cost of 8oz hot cup from box
hot_cup_8oz_price_var = hot_cup_8oz_box_price / hot_cup_8oz_box_size
# Add 'hot_cup_8oz'
new_item_data = {
    'Item': ['hot_cup_8oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_cup_8oz_price_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 10oz hot cup from box
hot_cup_10oz_price_var = hot_cup_10oz_box_price / hot_cup_10oz_box_size
# Add 'hot_cup_10oz'
new_item_data = {
    'Item': ['hot_cup_10oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_cup_10oz_price_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 16oz hot cup from box
hot_cup_16oz_price_var = hot_cup_16oz_box_price / hot_cup_16oz_box_size
# Add 'hot_cup_16oz'
new_item_data = {
    'Item': ['hot_cup_16oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_cup_16oz_price_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 16oz iced cup from box
iced_cup_16oz_price_var = iced_cup_16oz_box_price / iced_cup_16oz_box_size
# Add 'iced_cup_16oz'
new_item_data = {
    'Item': ['iced_cup_16oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [iced_cup_16oz_price_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 8oz hot lid from box
hot_lid_8oz_var = hot_lid_8oz_box_price / hot_lid_8oz_box_size
# Add 'iced_cup_16oz'
new_item_data = {
    'Item': ['hot_lid_8oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_lid_8oz_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 16oz hot lid from box
hot_lid_16oz_var = hot_lid_16oz_box_price / hot_lid_16oz_box_size
# Add 'iced_cup_16oz'
new_item_data = {
    'Item': ['hot_lid_16oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [hot_lid_16oz_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 16oz iced lid from box
iced_lid_16oz_var = iced_lid_16oz_box_price / iced_lid_16oz_box_size
# Add 'iced_cup_16oz'
new_item_data = {
    'Item': ['iced_lid_16oz'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [iced_lid_16oz_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of sleeve from box
sleeve_var = sleeve_box_price / sleeve_box_size
# Add 'sleeve'
new_item_data = {
    'Item': ['sleeve'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [sleeve_var]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

### SYRUPS + SUGAR + CHOCOLATE ###

# Calculate cost of 1g sugar
sugar_1g_cost = sugar_bag_price / sugar_bag_size
# Add 'sugar_1g'
new_item_data = {
    'Item': ['sugar_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [sugar_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of a chocolate stick
chocolate_stick_cost = chocolate_box_price / chocolate_box_size
# Add 'chocolate_stick'
new_item_data = {
    'Item': ['chocolate_stick'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [chocolate_stick_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz vanilla syrup
vanilla_syrup_1oz_cost = vanilla_syrup_bottle_price / vanilla_syrup_bottle_size
# Add 'vanilla_syrup_1oz'
new_item_data = {
    'Item': ['vanilla_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [vanilla_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz caramel syrup
caramel_syrup_1oz_cost = caramel_syrup_bottle_price / caramel_syrup_bottle_size
# Add 'caramel_syrup_1oz'
new_item_data = {
    'Item': ['caramel_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [caramel_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz hazelnut syrup
hazelnut_syrup_1oz_cost = hazelnut_syrup_bottle_price / hazelnut_syrup_bottle_size
# Add 'hazelnut_syrup_1oz'
new_item_data = {
    'Item': ['hazelnut_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [hazelnut_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz lavender syrup
lavender_syrup_1oz_cost = lavender_syrup_bottle_price / lavender_syrup_bottle_size
# Add 'lavender_syrup_1oz'
new_item_data = {
    'Item': ['lavender_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [lavender_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)


# Calculate cost of 1oz pistachio syrup
pistachio_syrup_1oz_cost = pistachio_syrup_bottle_price / pistachio_syrup_bottle_size
# Add 'pistachio_syrup_1oz'
new_item_data = {
    'Item': ['pistachio_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [pistachio_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)


# Calculate cost of 1oz maple syrup
maple_syrup_1oz_cost = maple_syrup_bottle_price / maple_syrup_bottle_size
# Add 'maple_syrup_1oz'
new_item_data = {
    'Item': ['maple_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [maple_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz of whipped cream
#whipped cream is 1:1 ratio of heavy cream to sugar
whipped_cream_1oz_cost = whipped_cream_bottle_price / whipped_cream_bottle_size
# Add 'whipped_cream_1oz'
new_item_data = {
    'Item': ['whipped_cream_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [whipped_cream_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz mocha syrup
mocha_syrup_1oz_cost = mocha_syrup_bottle_price / mocha_syrup_bottle_size
# Add 'mocha_syrup_1oz'
new_item_data = {
    'Item': ['mocha_syrup_1oz'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [mocha_syrup_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)


### COLD BREW + CHAI + MATCHA ###

# Calculate cost of 1oz cold brew
#Cold brew is made in 3:1 water:cold brew ratio. So 1oz concentrate gives 4oz final product
coldbrew_1oz_cost = coldbrew_carton_price / coldbrew_carton_size
coldbrew_1oz_cost = coldbrew_1oz_cost / 4
# Add 'coldbrew_1oz'
new_item_data = {
    'Item': ['coldbrew_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [coldbrew_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1g matcha
matcha_1g_cost = matcha_bag_price / matcha_bag_size
# Add 'matcha_1g'
new_item_data = {
    'Item': ['matcha_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [matcha_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz matcha
#matcha_recipe: 40g Matcha + 96oz?
matcha_1oz_cost = 40 * matcha_1g_cost / 96
#Add 'matcha_1oz'
new_item_data = {
    'Item': ['matcha_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [matcha_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1oz nitro matcha
#nitro matcha recipe: 32oz + 6.765oz = 38.765oz oat + 40g matcha + 110gr vanilla + 400ml water
#assuming 1 33.8oz bottle is ~1770grams
nitro_matcha_vanilla_quantity = (110/1770) * vanilla_syrup_bottle_size #oz
nitro_matcha_water_quantity = 13.526 #oz
nitro_matcha_oat_quantity = 38.765 #oz
nitro_matcha_batch_quantity = nitro_matcha_vanilla_quantity + nitro_matcha_water_quantity + nitro_matcha_oat_quantity
nitro_matcha_batch_cost = (nitro_matcha_vanilla_quantity * vanilla_syrup_1oz_cost) + (nitro_matcha_oat_quantity * oat_milk_1oz_cost)
nitro_matcha_1oz_cost = nitro_matcha_batch_cost / nitro_matcha_batch_quantity
# Add 'nitro_matcha_1oz'
new_item_data = {
    'Item': ['nitro_matcha_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [nitro_matcha_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1g chai
chai_1g_cost = chai_bag_price / chai_bag_size
# Add 'chai_1g'
new_item_data = {
    'Item': ['chai_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [chai_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Add 'chai_1oz' (cost to be calculated later)
#chai recipe: 1 bag + 1/2cup/100g sugar with 2.36L/79.8oz water
chai_1oz_cost = (1 * chai_bag_price + 100 * sugar_1g_cost) / 79.8
# Add 'chai_1oz'
new_item_data = {
    'Item': ['chai_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [chai_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

### TEAS ###

# Calculate cost of 1g Organic Earl Gray
earlGray_1g_cost = earlGray_bag_price / earlGray_bag_size
# Add 'earlGray_1g'
new_item_data = {
    'Item': ['earlGray_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [earlGray_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1g Jasmine Pearls
jasminePearls_1g_cost = jasminePearls_bag_price / jasminePearls_bag_size
# Add 'jasminePearls_1g'
new_item_data = {
    'Item': ['jasminePearls_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [jasminePearls_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1g White Peach
whitePeach_1g_cost = whitePeach_bag_price / whitePeach_bag_size
# Add 'whitePeach_1g'
new_item_data = {
    'Item': ['whitePeach_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [whitePeach_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1g Clarity Mushroom
clarityMushroom_1g_cost = clarityMushroom_bag_price / clarityMushroom_bag_size
# Add 'clarityMushroom_1g'
new_item_data = {
    'Item': ['clarityMushroom_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [clarityMushroom_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# Calculate cost of 1g Uplift Mushroom
upliftMushroom_1g_cost = upliftMushroom_bag_price / upliftMushroom_bag_size
# Add 'upliftMushroom_1g'
new_item_data = {
    'Item': ['upliftMushroom_1g'],
    'Quantity': [1],
    'Unit': ['g'],
    'Cost': [upliftMushroom_1g_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)
## AFFOGATO ##

# Calculate cost of 1oz Affogato
affogato_1oz_cost = affogato_carton_price / affogato_carton_size
# Add 'affogato_1oz'
new_item_data = {
    'Item': ['affogato_1oz'],
    'Quantity': [1],
    'Unit': ['oz'],
    'Cost': [affogato_1oz_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

## COOKIE CUP ##
# Calculate cost of a cookie cup
cookie_cup_cost = cookie_cup_box_price / cookie_cup_box_size
# Add 'cookie_cup'
new_item_data = {
    'Item': ['cookie_cup'],
    'Quantity': [1],
    'Unit': ['ea'],
    'Cost': [cookie_cup_cost]
}
new_item_df = pd.DataFrame(new_item_data)
inventory_QuantityAndCosts = pd.concat([inventory_QuantityAndCosts, new_item_df], ignore_index=True)

# ## Clean inventory_QuantityAndCosts

#drop duplicates
inventory_QuantityAndCosts = inventory_QuantityAndCosts.drop_duplicates(subset='Item', keep='first')
#make into alphabetical order
inventory_QuantityAndCosts = inventory_QuantityAndCosts.sort_values(by='Item')
#reset index
inventory_QuantityAndCosts.reset_index(inplace = True, drop = True)
#display
#display(inventory_QuantityAndCosts.head())


# ### Module Export "inventory_QuantityAndCosts"

inventory_QuantityAndCosts

# # Recipes

# ## Drink Recipes, in "all_recipes_df"

#Create cost recipes for all items
all_recipes = {}

## LATTES ##

#16oz latte recipe
latte_milk_16oz_quant = 12
latte_16oz_recipe = {'hot_cup_16oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'espresso_shot': 1,
                     'whole_milk_1oz': latte_milk_16oz_quant}
all_recipes['16oz Latte'] = latte_16oz_recipe

#10oz latte recipe
latte_milk_10oz_quant = 7
latte_10oz_recipe = {'hot_cup_10oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'espresso_shot': 1,
                     'whole_milk_1oz': latte_milk_10oz_quant}
all_recipes['10oz Latte'] = latte_10oz_recipe

#Dine-in latte recipe
latte_milk_dine_quant = 7
latte_dine_recipe = {'espresso_shot': 1,
                     'whole_milk_1oz': latte_milk_dine_quant}
all_recipes['Dine-in Latte'] = latte_dine_recipe

#Iced latte recipe
latte_milk_cold_quant = 7
latte_16oz_cold_recipe = {'iced_cup_16oz': 1,
                     'iced_lid_16oz': 1,
                     'sleeve': 1,
                     'espresso_shot': 1,
                     'whole_milk_1oz': latte_milk_cold_quant}
all_recipes['Iced Latte'] = latte_16oz_cold_recipe

## CAPPUCCINO ##

#10oz cappuccino recipe
cappuccino_milk_10oz_quant = 6
cappuccino_10oz_recipe = {'hot_cup_10oz': 1,
                          'hot_lid_16oz': 1,
                          'sleeve': 1,
                          'espresso_shot': 1,
                          'whole_milk_1oz': cappuccino_milk_10oz_quant}
all_recipes['10oz Cappuccino'] = cappuccino_10oz_recipe

#Dine-in cappuccino recipe
cappuccino_dine_quant = 5
cappuccino_dine_recipe = {'espresso_shot': 1,
                          'whole_milk_1oz': cappuccino_dine_quant}
all_recipes['Dine-in Cappuccino'] = cappuccino_dine_recipe

## FLAT WHITE ##

#8oz flat white recipe
flat_white_milk_8oz_quant = 7
flat_white_8oz_recipe = {'hot_cup_8oz': 1,
                         'hot_lid_8oz': 1,
                         'sleeve': 1,
                         'espresso_shot': 1,
                         'whole_milk_1oz': flat_white_milk_8oz_quant}
all_recipes['8oz Flat White'] = flat_white_8oz_recipe

#Dine-in flat white recipe
flat_white_milk_dine_quant = 7
flat_white_dine_recipe = {'espresso_shot': 1,
                          'whole_milk_1oz': flat_white_milk_dine_quant}
all_recipes['Dine-in Flat White'] = flat_white_dine_recipe

# New recipe definitions

## AMERICANO ##

#16oz americano recipe
americano_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'espresso_shot': 2}
all_recipes['16oz Americano'] = americano_16oz_recipe

#10oz americano recipe
americano_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'espresso_shot': 1}
all_recipes['10oz Americano'] = americano_10oz_recipe

#Dine-in americano recipe
americano_dine_recipe = {'espresso_shot': 1}
all_recipes['Dine-in Americano'] = americano_dine_recipe

#Iced americano recipe
americano_iced_recipe = {'iced_cup_16oz': 1,
                         'iced_lid_16oz': 1,
                         'sleeve': 1,
                         'espresso_shot': 1}
all_recipes['Iced Americano'] = americano_iced_recipe

## CORTADO ##

#8oz cortado recipe
cortado_milk_8oz_quant = 4
cortado_8oz_recipe = {'hot_cup_8oz': 1,
                      'hot_lid_8oz': 1,
                      'sleeve': 1,
                      'espresso_shot': 1,
                      'whole_milk_1oz': cortado_milk_8oz_quant}
all_recipes['8oz Cortado'] = cortado_8oz_recipe

#Dine-in cortado recipe
cortado_milk_dine_quant = 4
cortado_dine_recipe = {'espresso_shot': 2,
                      'whole_milk_1oz': cortado_milk_dine_quant}
all_recipes['Dine-in Cortado'] = cortado_dine_recipe

## MACCHIATO ##

#8oz macchiato recipe
macchiato_milk_8oz_quant = 4
macchiato_8oz_recipe = {'hot_cup_8oz': 1,
                        'hot_lid_8oz': 1,
                        'sleeve': 1,
                        'espresso_shot': 1,
                        'whole_milk_1oz': macchiato_milk_8oz_quant}
all_recipes['8oz Macchiato'] = macchiato_8oz_recipe

#Dine-in macchiato recipe
macchiato_milk_dine_quant = 4
macchiato_dine_recipe = {'espresso_shot': 1,
                        'whole_milk_1oz': macchiato_milk_dine_quant}
all_recipes['Dine-in Macchiato'] = macchiato_dine_recipe

## DRIP COFFEE ##

#16oz drip recipe
drip_16oz_recipe = {'hot_cup_16oz': 1,
                    'hot_lid_16oz': 1,
                    'sleeve': 1,
                    'drip_coffee_1oz': 16}
all_recipes['16oz Drip Coffee'] = drip_16oz_recipe

#10oz drip recipe
drip_10oz_recipe = {'hot_cup_10oz': 1,
                    'hot_lid_16oz': 1,
                    'sleeve': 1,
                    'drip_coffee_1oz': 10}
all_recipes['10oz Drip Coffee'] = drip_10oz_recipe

#Dine-in drip recipe
drip_dine_recipe = {'drip_coffee_1oz': 12}
all_recipes['Dine-in Drip Coffee'] = drip_dine_recipe

## CAFE AU LAIT ##

#16oz cafeAuLait recipe
cafeAuLait_milk_16oz_quant = 6
cafeAuLait_coffee_16oz_quant = 10
cafeAuLait_16oz_recipe = {'hot_cup_16oz': 1,
                          'hot_lid_16oz': 1,
                          'sleeve': 1,
                          'drip_coffee_1oz': cafeAuLait_coffee_16oz_quant,
                          'whole_milk_1oz': cafeAuLait_milk_16oz_quant}
all_recipes['16oz Cafe Au Lait'] = cafeAuLait_16oz_recipe

#10oz cafeAuLait recipe
cafeAuLait_milk_10oz_quant = 4
cafeAuLait_coffee_10oz_quant = 6
cafeAuLait_10oz_recipe = {'hot_cup_10oz': 1,
                          'hot_lid_16oz': 1,
                          'sleeve': 1,
                          'drip_coffee_1oz': cafeAuLait_coffee_10oz_quant,
                          'whole_milk_1oz': cafeAuLait_milk_10oz_quant}
all_recipes['10oz Cafe Au Lait'] = cafeAuLait_10oz_recipe

#Dine-in cafeAuLait recipe
cafeAuLait_dine_quant = 4
cafeAuLait_coffee_dine_quant = 6
cafeAuLait_dine_recipe = {'drip_coffee_1oz': cafeAuLait_coffee_dine_quant,
                          'whole_milk_1oz': cafeAuLait_dine_quant}
all_recipes['Dine-in Cafe Au Lait'] = cafeAuLait_dine_recipe

## ESPRESSO ##

#8oz espresso recipe
espresso_8oz_recipe = {'hot_cup_8oz': 1,
                        'hot_lid_8oz': 1,
                        'sleeve': 1,
                        'espresso_shot': 1}
all_recipes['8oz Espresso'] = espresso_8oz_recipe

#Dine-in espresso recipe
espresso_dine_recipe = {'espresso_shot': 1}
all_recipes['Dine-in Espresso'] = espresso_dine_recipe

## BABYCCINO ##

#8oz babyccino recipe
babyccino_8oz_recipe = {'hot_cup_8oz': 1,
                        'hot_lid_8oz': 1,
                        'sleeve': 1,
                        'mocha_syrup_1oz': 1.5,
                        'whole_milk_1oz': 6}
all_recipes['8oz Babyccino'] = babyccino_8oz_recipe

## COLD BREW ##

#Iced cold_brew recipe
coldbrew_iced_recipe = {'iced_cup_16oz': 1,
                         'iced_lid_16oz': 1,
                         'sleeve': 1,
                         'coldbrew_1oz': 8}
all_recipes['16oz Iced Cold Brew'] = coldbrew_iced_recipe

#Iced nitro cold_brew recipe
nitro_coldbrew_iced_recipe = {'iced_cup_16oz': 1,
                         'iced_lid_16oz': 1,
                         'sleeve': 1,
                         'coldbrew_1oz': 8}
all_recipes['16oz Iced Nitro Cold Brew'] = nitro_coldbrew_iced_recipe

## CHAI ##

#16oz chai recipe
chai_milk_16oz_quant = 7
chai_tea_16oz_quant = 7
chai_16oz_recipe = {'hot_cup_16oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': chai_milk_16oz_quant,
                     'chai_1oz': chai_tea_16oz_quant}
all_recipes['16oz Chai Latte'] = chai_16oz_recipe

#10oz chai recipe
chai_milk_10oz_quant = 4
chai_tea_10oz_quant = 4
chai_10oz_recipe = {'hot_cup_10oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': chai_milk_10oz_quant,
                     'chai_1oz': chai_tea_10oz_quant}
all_recipes['10oz Chai Latte'] = chai_10oz_recipe

#Dine-in chai recipe
chai_milk_dine_quant = 5
chai_tea_dine_quant = 5
chai_dine_recipe = {'whole_milk_1oz': chai_milk_dine_quant,
                     'chai_1oz': chai_tea_dine_quant}
all_recipes['Dine-in Chai Latte'] = chai_dine_recipe

#Iced chai recipe
chai_milk_cold_quant = 5
chai_tea_cold_quant = 5
chai_16oz_cold_recipe = {'iced_cup_16oz': 1,
                     'iced_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': chai_milk_cold_quant,
                     'chai_1oz': chai_tea_cold_quant}
all_recipes['Iced Chai Latte'] = chai_16oz_cold_recipe

## MATCHA ##

#16oz matcha recipe
matcha_milk_16oz_quant = 13
matcha_tea_16oz_quant = 1.5
matcha_16oz_recipe = {'hot_cup_16oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': matcha_milk_16oz_quant,
                     'matcha_1oz': matcha_tea_16oz_quant}
all_recipes['16oz Matcha Latte'] = matcha_16oz_recipe

#10oz matcha recipe
matcha_milk_10oz_quant = 7
matcha_tea_10oz_quant = 1
matcha_10oz_recipe = {'hot_cup_10oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': matcha_milk_10oz_quant,
                     'matcha_1oz': matcha_tea_10oz_quant}
all_recipes['10oz Matcha Latte'] = matcha_10oz_recipe

#Dine-in matcha recipe
matcha_milk_dine_quant = 8
matcha_tea_dine_quant = 1
matcha_dine_recipe = {'whole_milk_1oz': matcha_milk_dine_quant,
                     'matcha_1oz': matcha_tea_dine_quant}
all_recipes['Dine-in Matcha Latte'] = matcha_dine_recipe

#Iced matcha recipe
matcha_milk_cold_quant = 7
matcha_tea_cold_quant = 1
matcha_16oz_cold_recipe = {'iced_cup_16oz': 1,
                     'iced_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': matcha_milk_cold_quant,
                     'matcha_1oz': matcha_tea_cold_quant}
all_recipes['Iced Matcha Latte'] = matcha_16oz_cold_recipe

#Nitro Vanilla Matcha recipe
nitro_matcha_16oz_cold_recipe = {'iced_cup_16oz': 1,
                     'iced_lid_16oz': 1,
                     'sleeve': 1,
                     'nitro_matcha_1oz': 10}
all_recipes['16oz Iced Nitro Vanilla Matcha'] = nitro_matcha_16oz_cold_recipe


## SUBMARINO ##

#16oz submarino recipe
submarino_milk_16oz_quant = 14
submarino_chocolate_16oz_quant = 6
submarino_16oz_recipe = {'hot_cup_16oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': submarino_milk_16oz_quant,
                     'chocolate_stick': submarino_chocolate_16oz_quant,
                     'vanilla_syrup_1oz': 1}
all_recipes['16oz Submarino'] = submarino_16oz_recipe

#10oz submarino recipe
submarino_milk_10oz_quant = 8
submarino_chocolate_10oz_quant = 4
submarino_10oz_recipe = {'hot_cup_10oz': 1,
                     'hot_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': submarino_milk_10oz_quant,
                     'chocolate_stick': submarino_chocolate_10oz_quant,
                     'vanilla_syrup_1oz': .5}
all_recipes['10oz Submarino'] = submarino_10oz_recipe

# Dine in submarino recipe
submarino_dine_recipe = {'whole_milk_1oz': submarino_milk_10oz_quant,
                     'chocolate_stick': submarino_chocolate_10oz_quant,
                     'vanilla_syrup_1oz': .5}
all_recipes['Dine-in Submarino'] = submarino_dine_recipe

## TEAS ##

tea_gram_quantity_10oz = 1.3
tea_gram_quantity_16oz = 2

#  16oz Earl Gray
earlGray_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'earlGray_1g': tea_gram_quantity_16oz}
all_recipes['16oz Organic Earl Gray Tea'] = earlGray_16oz_recipe

#  10oz Earl Gray
earlGray_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'earlGray_1g': tea_gram_quantity_10oz}
all_recipes['10oz Organic Earl Gray Tea'] = earlGray_10oz_recipe

# Dine Earl Gray
earlGray_dine_recipe = {'earlGray_1g': tea_gram_quantity_10oz}
all_recipes['Dine-in Organic Earl Gray Tea'] = earlGray_dine_recipe

# 16oz Jasmine Pearls
jasminePearls_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'jasminePearls_1g': tea_gram_quantity_16oz}
all_recipes['16oz Jasmine Pearls Tea'] = jasminePearls_16oz_recipe

# 10oz Jasmine Pearls
jasminePearls_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'jasminePearls_1g': tea_gram_quantity_10oz}
all_recipes['10oz Jasmine Pearls Tea'] = jasminePearls_10oz_recipe

# Dine Jasmine Pearls
jasminePearls_dine_recipe = {'jasminePearls_1g': tea_gram_quantity_10oz}
all_recipes['Dine-in Jasmine Pearls Tea'] = jasminePearls_dine_recipe

# 16oz White Peach
whitePeach_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'whitePeach_1g': tea_gram_quantity_16oz}
all_recipes['16oz White Peach Tea'] = whitePeach_16oz_recipe

# 10oz White Peach
whitePeach_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'whitePeach_1g': tea_gram_quantity_10oz}
all_recipes['10oz White Peach Tea'] = whitePeach_10oz_recipe

# Dine White Peach
whitePeach_dine_recipe = {'whitePeach_1g': tea_gram_quantity_10oz}
all_recipes['Dine-in White Peach Tea'] = whitePeach_dine_recipe

# 16oz Clarity Mushroom
clarityMushroom_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'clarityMushroom_1g': tea_gram_quantity_16oz}
all_recipes['16oz Clarity Mushroom Tea'] = clarityMushroom_16oz_recipe

# 10oz Clarity Mushroom
clarityMushroom_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'clarityMushroom_1g': tea_gram_quantity_10oz}
all_recipes['10oz Clarity Mushroom Tea'] = clarityMushroom_10oz_recipe

# Dine Clarity Mushroom
clarityMushroom_dine_recipe = {'clarityMushroom_1g': tea_gram_quantity_10oz}
all_recipes['Dine-in Clarity Mushroom Tea'] = clarityMushroom_dine_recipe

# 16oz Uplift Mushroom
upliftMushroom_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'upliftMushroom_1g': tea_gram_quantity_16oz}
all_recipes['16oz Uplift Mushroom Tea'] = upliftMushroom_16oz_recipe

# 10oz Uplift Mushroom
upliftMushroom_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'upliftMushroom_1g': tea_gram_quantity_10oz}
all_recipes['10oz Uplift Mushroom Tea'] = upliftMushroom_10oz_recipe

# Dine Uplift Mushroom
upliftMushroom_dine_recipe = {'upliftMushroom_1g': tea_gram_quantity_10oz}
all_recipes['Dine-in Uplift Mushroom Tea'] = upliftMushroom_dine_recipe

# 16oz London Fog
#London Fog 16oz Recipe: 1oz Vanilla, 1.3g Earl Gray, 6oz milk
londonFog_milk_16oz_quant = 6
londonFog_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'whole_milk_1oz': londonFog_milk_16oz_quant,
                         'vanilla_syrup_1oz': 1,
                         'earlGray_1g': tea_gram_quantity_16oz / 2}
all_recipes['16oz London Fog'] = londonFog_16oz_recipe

# 10oz London Fog
#London Fog Recipe: .5oz Vanilla, .7g Earl Gray, 4oz milk
londonFog_milk_10oz_quant = 4
londonFog_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'whole_milk_1oz': londonFog_milk_10oz_quant,
                         'vanilla_syrup_1oz': .5,
                         'earlGray_1g': tea_gram_quantity_10oz / 2}
all_recipes['10oz London Fog'] = londonFog_10oz_recipe

# Dine London Fog
londonFog_dine_recipe = {'whole_milk_1oz': londonFog_milk_10oz_quant,
                         'vanilla_syrup_1oz': .5,
                         'earlGray_1g': tea_gram_quantity_10oz / 2}
all_recipes['Dine-in London Fog'] = londonFog_dine_recipe

# Iced londonFog recipe
londonFog_milk_cold_quant = 4
londonFog_16oz_cold_recipe = {'iced_cup_16oz': 1,
                     'iced_lid_16oz': 1,
                     'sleeve': 1,
                     'whole_milk_1oz': londonFog_milk_cold_quant,
                     'vanilla_syrup_1oz': .5,
                     'earlGray_1g': tea_gram_quantity_10oz / 2}
all_recipes['Iced London Fog'] = londonFog_16oz_cold_recipe

# 16oz Generic Tea. Using price of White Peach as filler
looseLeaf_16oz_recipe = {'hot_cup_16oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'whitePeach_1g': tea_gram_quantity_16oz}
all_recipes['16oz Loose Leaf Tea'] = looseLeaf_16oz_recipe

# 10oz Generic Tea. Using price of White Peach as filler
looseLeaf_10oz_recipe = {'hot_cup_10oz': 1,
                         'hot_lid_16oz': 1,
                         'sleeve': 1,
                         'whitePeach_1g': tea_gram_quantity_10oz}
all_recipes['10oz Loose Leaf Tea'] = looseLeaf_10oz_recipe

# Dine Generic Tea. Using price of White Peach as filler
looseLeaf_dine_recipe = {'whitePeach_1g': tea_gram_quantity_10oz}
all_recipes['Dine-in Loose Leaf Tea'] = looseLeaf_dine_recipe

# Iced Generic Tea recipe
looseLeaf_16oz_cold_recipe = {'iced_cup_16oz': 1,
                     'iced_lid_16oz': 1,
                     'sleeve': 1,
                     'whitePeach_1g': tea_gram_quantity_16oz}
all_recipes['Iced Loose Leaf Tea'] = looseLeaf_16oz_cold_recipe

## AFFOGATO ##

#8oz macchiato recipe
affogato_8oz_recipe = {'hot_cup_8oz': 1,
                        'sleeve': 1,
                        'espresso_shot': 1,
                        'affogato_1oz': 6}
all_recipes['8oz Affogato'] = affogato_8oz_recipe

#Dine-in affogato recipe
affogato_dine_recipe = {'espresso_shot': 1,
                        'affogato_1oz': 6}
all_recipes['Dine-in Affogato'] = affogato_dine_recipe


## EL PRINCIPITO ##
#SignaturePastry recipe
el_principito_whipped_cream_quant = 1.5
el_principito_recipe = {'cookie_cup': 1,
                     'espresso_shot': 1,
                     'whipped_cream_1oz': el_principito_whipped_cream_quant}
all_recipes['Dine-in SignaturePastry'] = el_principito_recipe


# Make all_recipes into dataframe
all_recipes_df = pd.DataFrame(all_recipes.items(), columns=['Item', 'Recipe'])
all_recipes_df.sort_values(by='Item', inplace=True)
display(all_recipes_df.head())

# ### Module Export "all_recipes_df"

all_recipes_df

# # Menu Prices

# ## Menu prices stored in "menuPrices_df"

menuPrices = {}

# Prices for all recipes

## ESPRESSO ##
_8oz_espresso_menuprice = 4.1
menuPrices['8oz Espresso'] = _8oz_espresso_menuprice

_dine_in_espresso_menuprice = 4.1
menuPrices['Dine-in Espresso'] = _dine_in_espresso_menuprice

el_principito_menuprice = 9.35
menuPrices['Dine-in SignaturePastry'] = el_principito_menuprice

## LATTE ##
_16oz_latte_menuprice = 5.65
menuPrices['16oz Latte'] = _16oz_latte_menuprice

_10oz_latte_menuprice = 5.25
menuPrices['10oz Latte'] = _10oz_latte_menuprice

_dine_in_latte_menuprice = 5.50
menuPrices['Dine-in Latte'] = _dine_in_latte_menuprice

_iced_latte_menuprice = 5.65
menuPrices['Iced Latte'] = _iced_latte_menuprice

## CAPPUCCINO ##
_10oz_cappuccino_menuprice = 5
menuPrices['10oz Cappuccino'] = _10oz_cappuccino_menuprice

_dine_in_cappuccino_menuprice = 5
menuPrices['Dine-in Cappuccino'] = _dine_in_cappuccino_menuprice

## FLAT WHITE ##
_8oz_flat_white_menuprice = 5
menuPrices['8oz Flat White'] = _8oz_flat_white_menuprice

_dine_in_flat_white_menuprice = 5
menuPrices['Dine-in Flat White'] = _dine_in_flat_white_menuprice

## MACCHIATO ##
_8oz_macchiato_menuprice = 4.25
menuPrices['8oz Macchiato'] = _8oz_macchiato_menuprice

_dine_in_macchiato_menuprice = 4.25
menuPrices['Dine-in Macchiato'] = _dine_in_macchiato_menuprice

## AMERICANO ##
_16oz_americano_menuprice = 6.75
menuPrices['16oz Americano'] = _16oz_americano_menuprice

_10oz_americano_menuprice = 4.5
menuPrices['10oz Americano'] = _10oz_americano_menuprice

_dine_in_americano_menuprice = 4.5
menuPrices['Dine-in Americano'] = _dine_in_americano_menuprice

_iced_americano_menuprice = 4.5
menuPrices['Iced Americano'] = _iced_americano_menuprice

## CORTADO ##
_8oz_cortado_menuprice = 4.25
menuPrices['8oz Cortado'] = _8oz_cortado_menuprice

_dine_in_cortado_menuprice = 4.25
menuPrices['Dine-in Cortado'] = _dine_in_cortado_menuprice

## DRIP ##
_16oz_drip_menuprice = 3.75
menuPrices['16oz Drip Coffee'] = _16oz_drip_menuprice

_10oz_drip_menuprice = 3.5
menuPrices['10oz Drip Coffee'] = _10oz_drip_menuprice

_dine_in_drip_menuprice = 3.5
menuPrices['Dine-in Drip Coffee'] = _dine_in_drip_menuprice

## CAFE AU LAIT
_16oz_cafe_au_lait_menuprice = 5.25
menuPrices['16oz Cafe Au Lait'] = _16oz_cafe_au_lait_menuprice

_10oz_cafe_au_lait_menuprice = 4.85
menuPrices['10oz Cafe Au Lait'] = _10oz_cafe_au_lait_menuprice

_dine_in_cafe_au_lait_menuprice = 4.85
menuPrices['Dine-in Cafe Au Lait'] = _dine_in_cafe_au_lait_menuprice

## BABYCCINO ##
_8oz_babyccino_menuprice = 3.05
menuPrices['8oz Babyccino'] = _8oz_babyccino_menuprice

## SUBMARINO ##
_16oz_submarino_menuprice = 7.25
menuPrices['16oz Submarino'] = _16oz_submarino_menuprice

_10oz_submarino_menuprice = 5.5
menuPrices['10oz Submarino'] = _10oz_submarino_menuprice

_dine_in_submarino_menuprice = 5.5
menuPrices['Dine-in Submarino'] = _dine_in_submarino_menuprice

## COLD BREW ##
_16oz_cold_brew_menuprice = 6.5
menuPrices['16oz Iced Cold Brew'] = _16oz_cold_brew_menuprice

_16oz_nitro_cold_brew_menuprice = 7.1
menuPrices['16oz Iced Nitro Cold Brew'] = _16oz_nitro_cold_brew_menuprice

## CHAI ##
_16oz_chai_menuprice = 6.75
menuPrices['16oz Chai Latte'] = _16oz_chai_menuprice

_10oz_chai_menuprice = 5.6
menuPrices['10oz Chai Latte'] = _10oz_chai_menuprice

_dine_in_chai_menuprice = 5.6
menuPrices['Dine-in Chai Latte'] = _dine_in_chai_menuprice

_iced_chai_menuprice = 6.75
menuPrices['Iced Chai Latte'] = _iced_chai_menuprice

## MATCHA ##
_16oz_matcha_menuprice = 6.75
menuPrices['16oz Matcha Latte'] = _16oz_matcha_menuprice

_10oz_matcha_menuprice = 6
menuPrices['10oz Matcha Latte'] = _10oz_matcha_menuprice

_dine_in_matcha_menuprice = 6.75
menuPrices['Dine-in Matcha Latte'] = _dine_in_matcha_menuprice

_iced_matcha_menuprice = 6.75
menuPrices['Iced Matcha Latte'] = _iced_matcha_menuprice

_nitro_vanilla_matcha_menuprice = 8.75
menuPrices['16oz Iced Nitro Vanilla Matcha'] = _nitro_vanilla_matcha_menuprice

## TEAS ##
_10oz_tea_standard_price = 4
_16oz_tea_standard_price = 7

menuPrices['10oz Organic Earl Gray Tea'] = _10oz_tea_standard_price
menuPrices['16oz Organic Earl Gray Tea'] = _16oz_tea_standard_price
menuPrices['Dine-in Organic Earl Gray Tea'] = _10oz_tea_standard_price

menuPrices['10oz Jasmine Pearls Tea'] = _10oz_tea_standard_price
menuPrices['16oz Jasmine Pearls Tea'] = _16oz_tea_standard_price
menuPrices['Dine-in Jasmine Pearls Tea'] = _10oz_tea_standard_price


menuPrices['10oz White Peach Tea'] = _10oz_tea_standard_price
menuPrices['16oz White Peach Tea'] = _16oz_tea_standard_price
menuPrices['Dine-in White Peach Tea'] = _10oz_tea_standard_price


menuPrices['10oz Clarity Mushroom Tea'] = _10oz_tea_standard_price
menuPrices['16oz Clarity Mushroom Tea'] = _16oz_tea_standard_price
menuPrices['Dine-in Clarity Mushroom Tea'] = _10oz_tea_standard_price

menuPrices['10oz Uplift Mushroom Tea'] = _10oz_tea_standard_price
menuPrices['16oz Uplift Mushroom Tea'] = _16oz_tea_standard_price
menuPrices['Dine-in Uplift Mushroom Tea'] = _10oz_tea_standard_price

_10oz_londonFog_menuprice = 4.75
_16oz_londonFog_menuprice = 7.25

menuPrices['10oz London Fog'] = _10oz_londonFog_menuprice
menuPrices['16oz London Fog'] = _16oz_londonFog_menuprice
menuPrices['Iced London Fog'] = _10oz_londonFog_menuprice
menuPrices['Dine-in London Fog'] = _10oz_londonFog_menuprice

menuPrices['10oz Loose Leaf Tea'] = _10oz_tea_standard_price
menuPrices['16oz Loose Leaf Tea'] = _16oz_tea_standard_price
menuPrices['Iced Loose Leaf Tea'] = _10oz_tea_standard_price
menuPrices['Dine-in Loose Leaf Tea'] = _10oz_tea_standard_price

## AFFOGATO ##

_8oz_affogato_menuprice = 9.35
menuPrices['8oz Affogato'] = _8oz_affogato_menuprice

_dine_in_affogato_menuprice = 9.35
menuPrices['Dine-in Affogato'] = _dine_in_affogato_menuprice

# Make menuPrices into dataframe
menuPrices_df = pd.DataFrame(menuPrices.items(), columns=['Item', 'Menu Price'])
menuPrices_df.sort_values(by='Item', inplace=True)

display(menuPrices_df.head())

# ### Module Export "menuPrices_df"

menuPrices_df

# # Recipe Costs

# ## Calculate cost of inventory items, in "recipe_costs"

# ### Function: calculate_recipe_cost

def calculate_recipe_cost(recipe, ingredient_df):
    """
    Calculates the total cost of a recipe based on ingredient costs.

    Args:
        recipe (dict): A dictionary where keys are ingredient names and values are their quantities.
        ingredient_df (pd.DataFrame): A DataFrame containing 'Item' and 'Cost' columns for ingredients.

    Returns:
        float: The total cost of the recipe.
    """
    total_cost = 0
    for ingredient, quantity in recipe.items():
        try:
            ingredient_cost = ingredient_df[ingredient_df['Item'] == ingredient]['Cost'].iloc[0]
            total_cost += ingredient_cost * quantity
        except IndexError:
            print(f"Warning: Ingredient '{ingredient}' not found in inventory_QuantityAndCosts. Skipping.")
    return total_cost

print("Function 'calculate_recipe_cost' defined.")
calculate_recipe_cost

recipe_costs = {}
for index, row in all_recipes_df.iterrows():
    recipe_name = row['Item']
    recipe_details = row['Recipe']
    cost = calculate_recipe_cost(recipe_details, inventory_QuantityAndCosts)
    recipe_costs[recipe_name] = cost

# ### Module Export "recipe_costs"

recipe_costs

# ## Combine Menu Prices and Costs, in "menu_PricesandCosts"

# Make recipe_costs into a pandas dataframe
menu_PricesandCosts = pd.DataFrame(recipe_costs.items(), columns=['Item', 'Cost'])

# Create a temporary lowercase 'Item' column for case-insensitive merge
menu_PricesandCosts['item_lower'] = menu_PricesandCosts['Item'].str.lower()
menuPrices_df['item_lower'] = menuPrices_df['Item'].str.lower()

# Merge with menuPrices_df to add the 'Menu Price' column on the lowercase item column
# Keep the original 'Item' column from menu_PricesandCosts (left_on='item_lower', right_on='item_lower')
menu_PricesandCosts = pd.merge(menu_PricesandCosts, menuPrices_df[['item_lower', 'Menu Price']], on='item_lower', how='left')

# Drop the temporary lowercase item column
menu_PricesandCosts = menu_PricesandCosts.drop(columns=['item_lower'])
menuPrices_df = menuPrices_df.drop(columns=['item_lower'])

#Add profit ratio
profit_ratio_hold = []
for index, row in menu_PricesandCosts.iterrows():
    profit_ratio = ((row['Menu Price'] - row['Cost']) / row['Menu Price'] ) * 100
    profit_ratio_hold.append(profit_ratio)
menu_PricesandCosts['Profit %'] = profit_ratio_hold
menu_PricesandCosts.sort_values(by='Profit %', ascending=False, inplace=True)

menu_PricesandCosts.rename(columns = {"Item": "Item Name"}, inplace = True)
menu_PricesandCosts

# ### Module Export "menu_PricesandCosts"

menu_PricesandCosts

# ## Data Quality Sanity Check

## SANITY DATA CHECK - ALL ITEMS IN BOTH DATAFRAMES ##

# Check for items in menu_PricesandCosts that are not in menuPrices_df
items_only_in_costs = set(menu_PricesandCosts['Item Name']) - set(menuPrices_df['Item'])
if items_only_in_costs:
    print(f"Warning: The following items have calculated costs but no menu price: {', '.join(items_only_in_costs)}")

# Check for items in menuPrices_df that are not in menu_PricesandCosts
# Note: menu_PricesandCosts is created from recipe_costs, so this checks if a menu price exists for which no recipe cost was calculated
items_only_in_prices = set(menuPrices_df['Item']) - set(menu_PricesandCosts['Item Name'])
if items_only_in_prices:
    print(f"Warning: The following items have a menu price but no calculated cost: {', '.join(items_only_in_prices)}")

if not items_only_in_costs and not items_only_in_prices:
    print("All items in recipe_costs and menuPrices_df match.")

# Correcting the unterminated string literal error by properly closing the string
print("The dataframe variables created in this module are: `all_recipes_df', `inventory_QuantityAndCosts`, `menuPrices_df`, `recipe_costs`, and `menu_PricesandCosts`.")

import pandas as pd
expenses_config_df = pd.DataFrame({

    "category": [
        "Monthly Fixed","Monthly Fixed","Monthly Fixed","Monthly Fixed",
        "Monthly Fixed","Monthly Fixed","Monthly Fixed",

        "Labor Assumptions","Labor Assumptions","Labor Assumptions",

        "General Assumptions"
    ],

    "item": [
        "Rent",
        "Utilities",
        "Insurance",
        "Employee Benefits",
        "Payroll Taxes",
        "Marketing",
        "Miscellaneous",

        "Weekday Staff Hours",
        "Weekend Staff Hours",
        "Hourly Wage",

        "Slippage Rate"
    ],

    "amount": [
        13500,
        1500,
        1000,
        0,
        2000,
        500,
        500,

        36,
        72,
        18,

        0.10
    ],

    "notes": [
        "Monthly lease",
        "",
        "",
        "",
        "",
        "",
        "",

        "Total staff hours per weekday",
        "Total staff hours per weekend day",
        "Average hourly wage",

        "Buffer for unexpected costs"
    ]
})

expenses_config_df

# ## Enhanced unit parsing and correct file loading

# This block loads the Excel file named Recipes and Costs Excel.xlsx from the project root, implements a more robust and safe unit parsing function to convert various imperial and metric units to total ounces, and computes unit costs with safeguards. It keeps an unrounded Unit Cost (raw), a rounded Unit Cost, prints a brief summary and a preview, and saves both Excel and CSV outputs.

# ## Consolidate side-by-side tables into a unified dataset and compute unit costs

# This code reads the COSTOS sheet using the correct header row, extracts both the left and right tables into a consistent schema, concatenates them, removes sub-header rows, and then applies the previously defined unit parsing functions and conversions to compute Total_Oz and unit costs. It preserves DESCRIPCION DE PRODUCTO and PROVEEDOR so you can see items and providers in the output. It also saves the results to both Excel and CSV. If the right-side columns are missing, the code will gracefully proceed with only the left-side table.

# Note: The diagnostic block that lists sheet names and columns remains available above for troubleshooting and validation.

import pandas as pd
import numpy as np
import re
import math
from typing import Optional

# --- Unit normalization and conversion setup ---
# Canonical unit keys we will use: lb, oz, gal, fl oz, g, kg, ml, l
UNIT_ALIASES = {
    'lb': 'lb', 'lbs': 'lb', 'pound': 'lb', 'pounds': 'lb',
    'oz': 'oz', 'ounce': 'oz', 'ounces': 'oz', 'floz': 'fl oz', 'fl oz': 'fl oz', 'fl. oz': 'fl oz',
    'gal': 'gal', 'gallon': 'gal', 'gallons': 'gal', "gl": 'gal',
    'g': 'g', 'gram': 'g', 'grams': 'g',
    'qt': 'qt', 'qts': 'qt', 'quart': 'qt', 'quarts': 'qt',
    'pt': 'pt', 'pts': 'pt', 'pint': 'pt', 'pints': 'pt',
    'kg': 'kg', 'kilogram': 'kg', 'kilograms': 'kg',
    'l': 'l', 'liter': 'l', 'liters': 'l', 'litre': 'l', 'litres': 'l', 'lts': 'l',
    'ml': 'ml', 'milliliter': 'ml', 'milliliters': 'ml', 'millilitre': 'ml', 'millilitres': 'ml',
    'taza': 'cup', 'tazas': 'cup', 'cup': 'cup', 'cups': 'cup',
    'cdita': 'tsp', 'tsp': 'tsp', 'teaspoon': 'tsp', 'teaspoons': 'tsp',
    'cda': 'tbsp', 'cdas': 'tbsp', 'tbsp': 'tbsp', 'tablespoon': 'tbsp', 'tablespoons': 'tbsp',
    'ct': 'ea', 'count': 'ea', 'ea': 'ea', 'each': 'ea', 'pc': 'ea', 'pcs': 'ea', 'piece': 'ea', 'pieces': 'ea',
}

# Conversion factors to ounces (by weight) or fluid ounces for volume
UNIT_CONVERSION = {
    'lb': 16.0,
    'oz': 1.0,
    'gal': 128.0,          # US gallon to fluid ounces
    'fl oz': 1.0,          # already in fluid ounces
    'pt': 16.0,   # 1 US pint = 16 fluid ounces
    'qt': 32.0,   # 1 US quart = 32 fluid ounces
    'g': 0.0352739619,     # grams to ounces
    'kg': 35.2739619,      # kilograms to ounces
    'ml': 1.0 / 29.5735296,  # milliliters to fluid ounces
    'l': 33.8140227,       # liters to fluid ounces
    'ea': 1.0,   # 1 each = 1 unit (count-based, not weight/volume)
    'cup': 8.0,    # 1 cup = 8 fl oz
    'tsp': 0.1667, # 1 tsp = 1/6 fl oz
    'tbsp': 0.5,   # 1 tbsp = 1/2 fl oz
}

# Precompiled regex patterns
RE_PACK = re.compile(r"^(?:(?:\d+(?:\.\d+)?)\s*(?:pk|pack)\s*)?(\d+(?:\.\d+)?)\s*[x\u00D7]\s*([\d.]+)\s*([a-z\.\s]+)$")
RE_SINGLE = re.compile(r"^([\d.]+)\s*([a-z\.\s]+)$")
RE_FINDALL = re.compile(r"([\d.]+)\s*([a-z\.\s]{1,15})")

# Helpers
def normalize_text(s: str) -> str:
    s = (s or '')
    s = s.lower()
    s = s.replace(',', ' ')
    s = s.replace('-', ' ')
    s = s.replace('\u00A0', ' ')
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def normalize_unit_token(token: str) -> Optional[str]:
    if token is None:
        return None
    t = normalize_text(token)
    t = re.sub(r"[^a-z\.\s]", "", t)
    t = t.replace('.', '')
    t = re.sub(r"\s+", " ", t).strip()
    if t == 'fl oz' or t == 'fl  oz':
        t = 'fl oz'
    if t == 'fl':
        t = 'fl oz'
    if t in UNIT_ALIASES:
        return UNIT_ALIASES[t]
    t_nospace = t.replace(' ', '')
    if t_nospace in UNIT_ALIASES:
        return UNIT_ALIASES[t_nospace]
    return UNIT_ALIASES.get(t)

def to_ounces(qty: float, unit_text: str) -> float:
    canon = normalize_unit_token(unit_text)
    if canon is None:
        return np.nan
    factor = UNIT_CONVERSION.get(canon)
    if factor is None:
        return np.nan
    try:
        return float(qty) * float(factor)
    except Exception:
        return np.nan

# Main parser
def parse_spec(spec) -> float:
    s = normalize_text(str(spec))
    if not s:
        return np.nan

    m = RE_PACK.match(s)
    if m:
        count_str, size_str, unit_str = m.group(1), m.group(2), m.group(3)
        try:
            count = float(count_str)
            size = float(size_str)
        except Exception:
            count, size = np.nan, np.nan
        conv = to_ounces(size, unit_str)
        if not np.isnan(count) and not np.isnan(conv):
            return count * conv

    m = RE_SINGLE.match(s)
    if m:
        size_str, unit_str = m.group(1), m.group(2)
        try:
            size = float(size_str)
        except Exception:
            size = np.nan
        conv = to_ounces(size, unit_str)
        if not np.isnan(conv):
            return conv

    candidates = []
    for size_str, unit_str in RE_FINDALL.findall(s):
        try:
            size = float(size_str)
        except Exception:
            continue
        conv = to_ounces(size, unit_str)
        if not np.isnan(conv):
            candidates.append(conv)
    if candidates:
        return max(candidates)

    try:
        num = float(s)
        return num if num > 0 else np.nan
    except Exception:
        return np.nan



def read_recipes_costs_excel(file_path: str) -> pd.DataFrame:
    """Reads the COSTOS sheet and returns a consolidated, renamed DataFrame."""
    col_names = ['Item', 'Provider', 'Quantity', 'Cost', 'Unit Cost', 'Unit']

    left = pd.read_excel(file_path, sheet_name='COSTOS', header=1, usecols='A:F')
    left.columns = col_names
    right = pd.read_excel(file_path, sheet_name='COSTOS', header=1, usecols='G:L')
    right.columns = col_names

    costs = pd.concat([left, right], ignore_index=True)
    costs = costs.dropna(subset=['Item'])
    costs = costs[costs['Quantity'].notna()]
    costs = costs.iloc[1:]

    # Fix rows where Provider is missing and columns are shifted left
    shifted_mask = (
        costs['Provider'].isna() &
        pd.to_numeric(costs['Quantity'], errors='coerce').notna() &
        costs['Cost'].apply(lambda x: isinstance(x, str) and bool(re.search(r'[a-zA-Z]', str(x))))
    )
    costs.loc[shifted_mask, 'Unit'] = costs.loc[shifted_mask, 'Cost']
    costs.loc[shifted_mask, 'Unit Cost'] = costs.loc[shifted_mask, 'Quantity']
    costs.loc[shifted_mask, 'Quantity'] = (
        costs.loc[shifted_mask, 'Quantity'].astype(str) + ' ' +
        costs.loc[shifted_mask, 'Cost']
    )
    costs.loc[shifted_mask, 'Cost'] = np.nan

    # If Quantity is purely numeric, assume oz and backfill Cost and Unit Cost
    numeric_qty_mask = costs['Quantity'].apply(
        lambda x: bool(re.match(r"^\s*[\d.]+\s*$", str(x)))
    )
    costs.loc[numeric_qty_mask, 'Cost'] = pd.to_numeric(
        costs.loc[numeric_qty_mask, 'Quantity'], errors='coerce'
    )
    costs.loc[numeric_qty_mask, 'Unit Cost'] = pd.to_numeric(
        costs.loc[numeric_qty_mask, 'Quantity'], errors='coerce'
    )
    costs.loc[numeric_qty_mask, 'Quantity'] = (
        costs.loc[numeric_qty_mask, 'Quantity'].astype(str) + ' oz'
    )

    return costs


def compute_unit_costs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parses Quantity into a standardized oz/fl oz amount, computes Unit Cost,
    and updates the Unit column to reflect the standard unit used.
    """
    df = df.copy()

    # Coerce Cost to numeric
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

    # Parse Quantity into standard oz (or fl oz) via parse_spec
    df['Quantity_standard'] = df['Quantity'].apply(parse_spec)
    df.loc[~(df['Quantity_standard'] > 0), 'Quantity_standard'] = np.nan

    def get_standard_unit(quantity_str) -> str:
        s = normalize_text(str(quantity_str))
        # Count-based units
        for token in ['ct', 'count', 'ea', 'each', 'pc', 'pcs', 'piece', 'pieces']:
            if re.search(rf'\b{token}\b', s):
                return 'ea'
        # Volume units -> fl oz
        for token in ['gal', 'gallon', 'gallons', 'gl', 'l', 'liter', 'liters',
                    'lts', 'lt', 'ml', 'milliliter', 'fl oz', 'fl', 'qt',
                    'quart', 'pt', 'pint']:
            if re.search(rf'\b{token}\b', s):
                return 'fl oz'
        return 'oz'

    df['Unit'] = df['Quantity'].apply(get_standard_unit)

    # Recompute Unit Cost = Cost / Quantity_standard
    valid_mask = (
        df['Cost'].notna() &
        df['Quantity_standard'].notna() &
        (df['Quantity_standard'] > 0)
    )
    df['Unit Cost'] = np.where(
        valid_mask,
        (df['Cost'] / df['Quantity_standard']).round(2),
        np.nan
    )
    #Drop anything left with na in unit cost and cost
    df = df.dropna(subset=['Unit Cost', 'Cost'])
    
    return df
# --- Load data ---
file_path = 'Recipes and Costs Excel.xlsx'
excel_costs = read_recipes_costs_excel(file_path)
excel_costs = excel_costs.dropna(how='all')
excel_costs = compute_unit_costs(excel_costs)

# Summary stats
total_rows = len(excel_costs)
valid_oz = excel_costs['Quantity_standard'].notna().sum()
unit_cost_nan = excel_costs['Unit Cost'].isna().sum()
percent_valid = (valid_oz / total_rows * 100.0) if total_rows else 0.0
print(f"Rows: {total_rows}; Valid Quantity_standard: {valid_oz} ({percent_valid:.1f}%) ; Unit Cost NaN: {unit_cost_nan}")

# Save outputs
excel_out = 'recipes_with_unit_cost.xlsx'
csv_out = 'recipes_with_unit_cost.csv'
try:
    excel_costs.to_excel(excel_out, index=False)
except Exception as e:
    print(f"Warning: could not save Excel file due to: {e}")
try:
    excel_costs.to_csv(csv_out, index=False)
except Exception as e:
    print(f"Warning: could not save CSV file due to: {e}")
excel_costs

# need pint calculation, and inclusion of "ct" and "ea". Then drop na for Unit Costs. Need to calculate unit cost

def parse_quantity_str(qty_str: str):
    """
    Parses a quantity string like '1/2', '1.5', '2', '1/4' into a float.
    Also handles mixed like '1 1/2'.
    """
    s = str(qty_str).strip()
    # Handle fractions like 1/2
    frac_match = re.match(r'^(\d+)/(\d+)$', s)
    if frac_match:
        return float(frac_match.group(1)) / float(frac_match.group(2))
    # Handle mixed like "1 1/2"
    mixed_match = re.match(r'^(\d+)\s+(\d+)/(\d+)$', s)
    if mixed_match:
        return float(mixed_match.group(1)) + float(mixed_match.group(2)) / float(mixed_match.group(3))
    try:
        return float(s)
    except Exception:
        return np.nan


def parse_recipe_quantity(raw: str):
    """
    Given a raw quantity string like '1/2 taza', '150 gr', '1.2 oz (2 cdas)',
    returns (quantity_standard, unit_standard) where quantity_standard is in
    the canonical unit (oz, fl oz, g, ea, etc.)
    """
    s = normalize_text(str(raw))
    # Strip parenthetical notes e.g. "1.2 oz (2 cdas)" -> "1.2 oz"
    s = re.sub(r'\(.*?\)', '', s).strip()

    # Try to extract number + unit
    m = re.match(r'^([\d/\s\.]+)\s+([a-z]+)$', s)
    if m:
        qty = parse_quantity_str(m.group(1).strip())
        unit_raw = m.group(2).strip()
        canon = normalize_unit_token(unit_raw)
        if canon and not np.isnan(qty):
            factor = UNIT_CONVERSION.get(canon)
            if factor:
                return qty * factor, canon
    return np.nan, None


def read_recipe_sheet(file_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Reads a recipe sheet and returns a DataFrame with columns:
    [Recipe, Ingredient, Quantity_raw, Quantity_standard, Unit_standard]
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Get recipe name from row 1, col 1
    recipe_name = df.iloc[1, 1] if pd.notna(df.iloc[1, 1]) else sheet_name

    # Get yield: find the row with 'YIELD'
    yield_oz = np.nan
    for _, row in df.iterrows():
        for i, cell in enumerate(row):
            if str(cell).strip().upper() == 'YIELD':
                raw_yield = row.iloc[i + 1]
                yield_qty, yield_unit = parse_recipe_quantity(str(raw_yield))
                yield_oz = yield_qty
                break

    # Find ingredient rows: between INGREDIENTES and PROCEDIMIENTO/blank section
    ingredient_start = None
    for idx, row in df.iterrows():
        if str(row.iloc[0]).strip().upper() == 'INGREDIENTES':
            ingredient_start = idx + 1
            break

    rows = []
    if ingredient_start is not None:
        for idx in range(ingredient_start, len(df)):
            row = df.iloc[idx]
            qty_raw = row.iloc[0]
            ingredient = row.iloc[1]
            if pd.isna(qty_raw) or pd.isna(ingredient):
                break
            qty_std, unit_std = parse_recipe_quantity(str(qty_raw))
            rows.append({
                'Recipe': recipe_name,
                'Ingredient': str(ingredient).strip(),
                'Quantity_raw': str(qty_raw).strip(),
                'Quantity_standard': qty_std,
                'Unit_standard': unit_std,
                'Recipe_Yield_oz': yield_oz,
            })

    return pd.DataFrame(rows)


def cost_recipe(recipe_df: pd.DataFrame, costs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Matches each ingredient to excel_costs and calculates ingredient cost.
    Appends summary rows for total recipe cost and cost per oz.
    """
    recipe_df = recipe_df.copy()

    def match_cost(ingredient: str, qty_std: float, unit_std: str):
        """Fuzzy match ingredient name to costs_df and return line cost."""
        if pd.isna(qty_std) or not unit_std:
            return np.nan
        # Simple case-insensitive substring match
        mask = costs_df['Item'].str.contains(ingredient, case=False, na=False)
        matches = costs_df[mask]
        if matches.empty:
            # Try matching on first word of ingredient
            first_word = ingredient.split()[0]
            mask = costs_df['Item'].str.contains(first_word, case=False, na=False)
            matches = costs_df[mask]
        if matches.empty:
            return np.nan
        unit_cost = matches.iloc[0]['Unit Cost']
        if pd.isna(unit_cost):
            return np.nan
        return round(qty_std * unit_cost, 4)

    recipe_df['Ingredient_Cost'] = recipe_df.apply(
        lambda r: match_cost(r['Ingredient'], r['Quantity_standard'], r['Unit_standard']), axis=1
    )

    total_cost = recipe_df['Ingredient_Cost'].sum()
    yield_oz = recipe_df['Recipe_Yield_oz'].iloc[0]
    cost_per_oz = round(total_cost / yield_oz, 4) if yield_oz and yield_oz > 0 else np.nan
    recipe_name = recipe_df['Recipe'].iloc[0]

    summary = pd.DataFrame([
        {
            'Recipe': recipe_name,
            'Ingredient': '** TOTAL RECIPE COST **',
            'Quantity_raw': '',
            'Quantity_standard': yield_oz,
            'Unit_standard': 'oz',
            'Recipe_Yield_oz': yield_oz,
            'Ingredient_Cost': round(total_cost, 2),
        },
        {
            'Recipe': recipe_name,
            'Ingredient': '** COST PER OZ **',
            'Quantity_raw': '',
            'Quantity_standard': 1,
            'Unit_standard': 'oz',
            'Recipe_Yield_oz': yield_oz,
            'Ingredient_Cost': cost_per_oz,
        }
    ])

    return pd.concat([recipe_df, summary], ignore_index=True)


# --- Usage ---
recipe_sheets = ['PESTO', 'HOUSE DRESSING', 'MISO CAESAR', 'KIMCHI MAYO', 'BLT MAYO', 'GUACAMOLE']

all_recipes = []
for sheet in recipe_sheets:
    recipe_df = read_recipe_sheet(file_path, sheet)
    costed_df = cost_recipe(recipe_df, excel_costs)
    all_recipes.append(costed_df)

all_recipes_df = pd.concat(all_recipes, ignore_index=True)
all_recipes_df.to_excel('recipes_costed.xlsx', index=False)
all_recipes_df

# talk to Marco if he wants to modify the excel sheet, or try and make a bunch of exceptions
