-- Data to populate database during development for visualisation

INSERT INTO country (country_code, short_code, name, solar_hours, carbon_emissions, solar_panel_price, electricity_mix_percentage, electricty_consumption, description)
VALUES
    -- Hours of Sunlight average estimated from https://www.currentresults.com/Weather/Spain/annual-days-of-sunshine.php (2445.702 hours)
    -- Carbon Emissions for 2023 taken from https://app.electricitymaps.com/zone/ES (39.2 Megatons)
    -- Price for Solar Panel taken from https://murciatoday.com/how-much-does-it-cost-to-install-solar-panels-in-spain_1672684-a.html (2000€/kW ~= £1800/kW)
    ('ESP', 'ES', 'Spain', 2445, 39200000, 1800, 0.1617, 'Spain (España), or the Kingdom of Spain (Reino de España), is a country located in Southwestern Europe, with parts of its territory in the Atlantic Ocean, the Mediterranean Sea and Africa. It is the largest country in Southern Europe and the fourth-most populous European Union member state. [https://en.wikipedia.org/wiki/Spain]');


INSERT INTO projects (name, description, sites, status, country_code)
VALUES
    ('Solaris', 'A project to install a solar power plant in farmlands .', '348', 'Ongoing', 'ESP'),
    ('Rural Electrification Initiative', 'Electrification of remote villages using solar energy.', '54', 'Completed', 'ESP'),
    ('Sunflower Global Ltd', 'Solar panel installation to Govt housing colonies  ', '273', 'Completed', 'ESP');



INSERT INTO countryinfo (description,country_code)
VALUES
    ('Solar power in Spain has grown significantly due to favorable conditions and government support. Abundant sunshine, coupled with investments in solar technology, has led to increased capacity. There''s still potential for further growth, supported by ongoing advancements in technology and favorable policies aimed at increasing renewable energy usage.','ESP');