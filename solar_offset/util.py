import sqlite3

# Assume an average solar panel power of 350W
SOLAR_PANEL_POWER = 350 / 1000.0 # kW

# Assume that a solar panel emits about 45 grams of CO2 equivalent per kWh
solar_emissions = 45 / 1000.0 # kg


# TODO: Double check these calculations
def calc_carbon_offset(country: sqlite3.Row):
        mix_solar = country["electricity_mix_percentage"]
        mix_non_solar = 1.0 / mix_solar

        # Calculate how much energy (kWh) one solar panel is estimated to produce
        panel_energy_kWh = country["solar_hours"] * SOLAR_PANEL_POWER # kWh

        # Calculate how much energy non-solar energy has been used (kWh)
        country_non_solar_energy_kWh = country["electricty_consumption"] * mix_non_solar * (1000 * 1000 * 1000.0) # Convert to TWh to kWh

        # The fraction of energy that could be replaced through this one solar panel
        fraction_panel_energy = panel_energy_kWh / country_non_solar_energy_kWh

        # How many kg of CO2eq are produced by non-solar energy sources
        country_non_solar_emissions_kg = country["carbon_emissions"] * mix_non_solar * 1000.0 # Convert to kg

        # How many kg of CO2eq produced by non-solar energy are taken away by installing the solar panel
        panel_replaced_emissions_kg = fraction_panel_energy * country_non_solar_emissions_kg

        # How much kg CO2eq a typical solar panel emits (eg. through production)
        panel_emissions_kg = solar_emissions * panel_energy_kWh

        # kg CO2eq that is being offset through one solar panel
        carbon_offset_per_panel = panel_replaced_emissions_kg - panel_emissions_kg

        # How much a single solar panel costs based on the price per kW
        price_per_panel = SOLAR_PANEL_POWER * country["solar_panel_price"]

        # kg CO2 eq being offset by donating £1
        return (carbon_offset_per_panel / price_per_panel) * 1000 # Convert kg to g
        