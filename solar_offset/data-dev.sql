-- Data to populate database during development for visualisation

INSERT INTO country (country_code, short_code, name, solar_hours, carbon_emissions, solar_panel_price, electricity_mix_percentage, electricty_consumption, description)
VALUES
    -- Hours of Sunlight average estimated from https://www.currentresults.com/Weather/Spain/annual-days-of-sunshine.php (2445.702 hours)
    -- Carbon Emissions for 2023 taken from https://app.electricitymaps.com/zone/ES (39.2 Megatons)
    -- Price for Solar Panel taken from https://murciatoday.com/how-much-does-it-cost-to-install-solar-panels-in-spain_1672684-a.html (2000€/kW ~= £1800/kW)
    ('ESP', 'ES', 'Spain', 2445, 39200000, 1800, 0.1617, 259,
     'Spain (España), or the Kingdom of Spain (Reino de España), is a country located in Southwestern Europe, with parts of its territory in the Atlantic Ocean, the Mediterranean Sea and Africa. It is the largest country in Southern Europe and the fourth-most populous European Union member state. [https://en.wikipedia.org/wiki/Spain]');

INSERT INTO user (id, email_username, password_hash, user_type)
VALUES ("8b1a1136-0024-477f-9e29-cb7266cb46d6", "admin1@12",
        "scrypt:32768:8:1$FnYQbrFKnN0hzMVS$3bd8242911240ebfc967a338f3cb3e656ad2ff9d8f07ea14280a11aec492508bf191880c19fbcbdd8d3f644638f37415c53a61e7432ccbe6a3af011f18555e54",
        "__a"); -- Password = "admin$219047"

INSERT INTO user (id, email_username, password_hash, user_type)
VALUES ("ed8425f7-8313-4382-9d7d-2b061eb890c5", "staff3881@hhrs",
        "scrypt:32768:8:1$oXJ7HMTqbUOnRQ51$4f70127d583052d1195fed4d00a1ba879b44d4c203173d2fa890d1f2f217ad5abc398ff31dac9415d51c4beb5035a5ad8034fce57afb3820a0d28c71b0f89b51",
        "_s_"); -- Password = "staff@29r83910"




/*INSERT INTO projects (name, description, sites, status, country_code)
VALUES
    ('Solaris', 'A project to install a solar power plant in farmlands .', '348', 'Ongoing', 'ESP'),
    ('Rural Electrification Initiative', 'Electrification of remote villages using solar energy.', '54', 'Completed', 'ESP'),
    ('Sunflower Global Ltd', 'Solar panel installation to Govt housing colonies  ', '273', 'Completed', 'ESP');



INSERT INTO countryinfo (description,country_code)
VALUES
    ('Solar power in Spain has grown significantly due to favorable conditions and government support. Abundant sunshine, coupled with investments in solar technology, has led to increased capacity. There''s still potential for further growth, supported by ongoing advancements in technology and favorable policies aimed at increasing renewable energy usage.','ESP');
*/





-- Inserting data for users
INSERT INTO user (id, email_username, password_hash, display_name, user_type)
VALUES 
    ('11111111-2222-3333-4444-555555555555', 'john@example.com', 'hashed_password_1', 'John Doe', '__a'),
    ('22222222-3333-4444-5555-666666666666', 'alice@example.com', 'hashed_password_2', 'Alice Smith', '_s_'),
    ('33333333-4444-5555-6666-777777777777', 'bob@example.com', 'hashed_password_3', 'Bob Johnson', 'h__');


-- Inserting data for countries
INSERT INTO country (country_code, short_code, name, description, solar_hours, carbon_emissions, solar_panel_price, electricity_mix_percentage, electricty_consumption) 
VALUES ('USA', 'US', 'United States', 'Description for United States', 2000, 50000, 5000, 10, 2000),
    ('UK', 'GB', 'United Kingdom', 'Description for United Kingdom', 1800, 30000, 6000, 15, 1500),
    ('CAN', 'CA', 'Canada', 'Description for Canada', 1900, 40000, 5500, 12, 1800);


-- Inserting data for organizations
INSERT INTO organization (name_slug, country_code, name, description, details_paypal, details_stripe) 
VALUES ('org1', 'USA', 'Organization 1', 'Description for Organization 1', 'paypal_details_1', 'stripe_details_1'),
    ('org2', 'UK', 'Organization 2', 'Description for Organization 2', 'paypal_details_2', 'stripe_details_2'),
    ('org3', 'CAN', 'Organization 3', 'Description for Organization 3', 'paypal_details_3', 'stripe_details_3');



-- Inserting data for donations
INSERT INTO donation (created, householder_id, country_code, organization_slug, donation_amount) 
VALUES ('2023-01-01 10:00:00', '11111111-2222-3333-4444-555555555555', 'USA', 'org1', 1000),
    ('2023-01-02 11:00:00', '2', 'UK', 'org2', 1500),
    ('2023-01-03 12:00:00', '3', 'CAN', 'org3', 2000);
