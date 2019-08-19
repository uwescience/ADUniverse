# This document contains constant values for use throughout the application

# The criteria for selecting subsample, change to 0 if full database
SQFTLOT = 10000

# Seattle coordinates, default for the application map
SEATTLE = (47.6062, -122.3321)

# Initial level for zoom parameter
INIT_ZOOM = 11

# Structural Parameter Assumptions
APR = 0.069  # annual interest rate
MONTHLY_APR = APR/12

MATURITY = 15  # loan MATURITY years
ANNUAL_MATURITY = 15*12

# Cost function constants
ADU_VAR = 125
AADU_SEWER = 6760
DADU_FIXED = 125000
DADU_SEWER = 11268
DESIGN_PERCENTAGE = 0.06
MULTIPLIER = 0.2
PERMIT_FIXED = 400
PERMIT_VAR = 3
PROPERTY_TAX = 0.01
SALES_TAX = 0.101
