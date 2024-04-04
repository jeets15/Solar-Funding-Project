-- Data to populate database during development for visualisation

INSERT INTO country (country_code, short_code, name, solar_hours, carbon_emissions, solar_panel_price_per_kw, electricity_mix_percentage, electricty_consumption, description)
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
INSERT INTO donation (created, country_code, organization_slug, donation_amount, householder_id)
VALUES
    ('2024-01-12 01:15:38.587367', 'ATA', 'antarctica_solar_project', 10, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2024-02-01 03:20:49.565309', 'ATA', 'antarctica_solar_project', 5, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-03-25 04:01:21.346968', 'ATA', 'antarctica_solar_project', 35, '3d1886b7-abec-49b9-b849-99ceb616b127'),
    ('2023-04-13 06:33:40.246119', 'ESP', 'solaris', 50, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-05-19 08:42:16.262143', 'ESP', 'solaris', 10, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-06-08 10:19:39.237623', 'ESP', 'solaris', 103, '3d1886b7-abec-49b9-b849-99ceb616b127'),
    ('2023-09-28 11:02:32.332768', 'ESP', 'rural_electrification_initiative', 13, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-11-03 18:52:04.351058', 'ESP', 'rural_electrification_initiative', 107, '3d1886b7-abec-49b9-b849-99ceb616b127');



