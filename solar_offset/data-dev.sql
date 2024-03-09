-- Data to populate database during development for visualisation

INSERT INTO country (country_code, short_code, name, solar_hours, carbon_emissions, solar_panel_price,
                     electricity_mix_percentage, description)
VALUES
    -- Hours of Sunlight average estimated from https://www.currentresults.com/Weather/Spain/annual-days-of-sunshine.php (2445.702 hours)
    -- Carbon Emissions for 2023 taken from https://app.electricitymaps.com/zone/ES (39.2 Megatons)
    -- Price for Solar Panel taken from https://murciatoday.com/how-much-does-it-cost-to-install-solar-panels-in-spain_1672684-a.html (2000€/kW ~= £1800/kW)
    ('ESP', 'ES', 'Spain', 2445, 39200000, 1800, 0.1617,
     'Spain (España), or the Kingdom of Spain (Reino de España), is a country located in Southwestern Europe, with parts of its territory in the Atlantic Ocean, the Mediterranean Sea and Africa. It is the largest country in Southern Europe and the fourth-most populous European Union member state. [https://en.wikipedia.org/wiki/Spain]');

INSERT INTO user (id, email_username, password_hash, user_type)
VALUES ("8b1a1136-0024-477f-9e29-cb7266cb46d6", "admin1@12",
        "scrypt:32768:8:1$FnYQbrFKnN0hzMVS$3bd8242911240ebfc967a338f3cb3e656ad2ff9d8f07ea14280a11aec492508bf191880c19fbcbdd8d3f644638f37415c53a61e7432ccbe6a3af011f18555e54",
        "admin"); -- Password = "admin$219047"

INSERT INTO user (id, email_username, password_hash, user_type)
VALUES ("ed8425f7-8313-4382-9d7d-2b061eb890c5", "staff3881@hhrs",
        "scrypt:32768:8:1$oXJ7HMTqbUOnRQ51$4f70127d583052d1195fed4d00a1ba879b44d4c203173d2fa890d1f2f217ad5abc398ff31dac9415d51c4beb5035a5ad8034fce57afb3820a0d28c71b0f89b51",
        "staff"); -- Password = "staff@29r83910"