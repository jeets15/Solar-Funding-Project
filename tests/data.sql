-- Data to add into separate test database for unit tests

-- Use werkzeug.security.generate_password_hash to generate hashes to insert
-- Don't forget to write down the plain text test passwords or the hashes are useless

INSERT INTO user (user_type, email_username, display_name, householder_carbon_footprint, id, password_hash)
VALUES
    -- Password = "h_test"
    ('h__', 'h_test', 'Test Householder', 14.72, '2c06f907-4ca3-42ab-9a3b-d3ccbf0326d3', 'scrypt:32768:8:1$FQygLjDw2iUhdRvF$194122453ce201239ad3c9d68a08881c2af31806aa7ab01443820f853b00e17306d191bcc785dd50d260a409be36a31214c109f245e731a100f81181dd32791c'),
    -- Password = "john!Smith977"
    ('h__', 'john.smith977@example.co.uk', 'John Smith', NULL, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e', 'scrypt:32768:8:1$mrhixSkl8zpgEzjw$1d0eb679f0627b2ad0aff80bae7f9b3b724519715da197de555c136b6f4a275510a31e8099ae5e7ed96c7f08e922fa75c56e4146294b8fcf45891bfa183c025e'),
    -- Password = "12Jane!DoeDoe"
    ('h__', 'jane.doe15@example.com', 'Jane Doe', NULL, '3d1886b7-abec-49b9-b849-99ceb616b127', 'scrypt:32768:8:1$NzKNPOundEOjypTn$dd9534ea0c7eae235f329d3c699c99963cb8186cb6fd6ea91b4509d84f6367aac3e45cf01b5381413b2024c76bdba1405d684d53a639b753165bfc0cb09ec3b4'),
    -- Password = "staff@29r83910"
    ('_s_', "staff3881@hhrs", NULL, NULL, 'ed8425f7-8313-4382-9d7d-2b061eb890c5', 'scrypt:32768:8:1$oXJ7HMTqbUOnRQ51$4f70127d583052d1195fed4d00a1ba879b44d4c203173d2fa890d1f2f217ad5abc398ff31dac9415d51c4beb5035a5ad8034fce57afb3820a0d28c71b0f89b51'),
    -- Password = "admin$219047"
    ('__a', 'admin1@12', NULL, NULL, '8b1a1136-0024-477f-9e29-cb7266cb46d6', 'scrypt:32768:8:1$FnYQbrFKnN0hzMVS$3bd8242911240ebfc967a338f3cb3e656ad2ff9d8f07ea14280a11aec492508bf191880c19fbcbdd8d3f644638f37415c53a61e7432ccbe6a3af011f18555e54'),
    -- Password = "staffmin12"
    ('_sa', 'staffmin12', 'Mark', NULL, '4912602e-457a-45fb-90f9-d334606ca434', 'scrypt:32768:8:1$qu3NWpxv1Iob8Vjj$fc897b83583c38c42c543b68671be107673c962842b6c3927c92ad9ccc10a5eabfdd3798b0ce1662f074f9cd3dea62c0f9e8b6212aec24e58d6402bf2035e970');


-- Country Codes taken from https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
-- country_code: ISO 3166-1 A-3 (3 Characters)
-- short_code:   ISO 3166-1 A-2 (2 Characters)
INSERT INTO country (country_code, short_code, name, solar_hours, carbon_emissions, solar_panel_price_per_kw, electricity_mix_percentage, electricty_consumption, population_size, description)
VALUES
    -- This is a dummy entry that does not reflect real-world data
    -- Hours of Sunshine simply set to 6 months (4380 hours)
    -- Carbon Emissions are basically 0 (there are only a couple of research centers)
    -- Set solar panel price to be relatively high due to shipping costs etc.
    -- Assume 50% renewable energies in research facilities
    -- Guess electricty consumption to be around 2TWh per year
    -- Antarctica's population size is between 1300 and 5100
    ('ATA', 'AQ', 'Antarctica', 4380, 100000, 8000, 0.5, 2, 3200,
        'This data does not reflect the reality. Antarctica is the continent surrounding the South-Pole. While Antarctica is not officially a country, it is often treated as one due to the fact that most inhabitants are members of research groups.'),
    -- Hours of Sunlight average estimated from https://www.currentresults.com/Weather/Spain/annual-days-of-sunshine.php (2445.702 hours)
    -- Carbon Emissions for 2023 taken from https://app.electricitymaps.com/zone/ES (39.2 Megatons)
    -- Price for Solar Panel taken from https://murciatoday.com/how-much-does-it-cost-to-install-solar-panels-in-spain_1672684-a.html (2000€/kW ~= £1800/kW)
    -- Spain Population https://en.wikipedia.org/wiki/Spain#cite_note-10
    ('ESP', 'ES', 'Spain', 2445, 39200000, 1800, 0.1617, 259, 48592909,
        'Spain (España), or the Kingdom of Spain (Reino de España), is a country located in Southwestern Europe, with parts of its territory in the Atlantic Ocean, the Mediterranean Sea and Africa. It is the largest country in Southern Europe and the fourth-most populous European Union member state. [https://en.wikipedia.org/wiki/Spain]
        \nSolar power in Spain has grown significantly due to favorable conditions and government support. Abundant sunshine, coupled with investments in solar technology, has led to increased capacity. There''s still potential for further growth, supported by ongoing advancements in technology and favorable policies aimed at increasing renewable energy usage.'),

    -- United of America
    ('USA', 'US', 'United States', 3000, 1600000000, 2500, 0.2, 4000, 334914895,
'The United States of America (USA), commonly known as the United States (U.S. or US) or America, is a country primarily located in North America. It consists of 50 states, a federal district, five major unincorporated territories, 326 Indian reservations, and some minor possessions. The United States is the world''s third-largest country by both land and population. [https://en.wikipedia.org/wiki/United_States]
\nThe United States has a diverse energy mix, with a significant reliance on fossil fuels like natural gas and coal, as well as growing renewable energy sources like solar and wind power. The country has made progress in increasing its renewable energy capacity, but there is still room for further growth and development in this area to reduce carbon emissions and address climate change concerns.'),

    -- South Africa
    ('ZAF', 'ZA', 'South Africa', 2800, 440000000, 1500, 0.1, 250, 60871900,
'South Africa is a country located at the southern tip of the African continent. It is known for its diverse landscapes, rich wildlife, and vibrant culture.
\nSouth Africa has made progress in expanding its renewable energy capacity, particularly in solar power, but fossil fuels still make up a significant portion of the country''s energy mix. The government has set targets to increase the share of renewable energy in the coming years.
\nAccording to the latest data, South Africa has an average of 2,800 hours of sunshine per year, which is favorable for solar power generation. The country''s carbon emissions are estimated at 440 million metric tons per year. The average cost of solar panels is around 1,500 ZAR/kW (approximately $100/kW). Renewable energy currently makes up around 10% of the country''s electricity generation, and the government aims to increase this to 20% by 2030.'),


-- Argentina
('ARG', 'AR', 'Argentina', 2800, 440000000, 1500, 0.1, 250, 46234830,
'Argentina is a country located in the southern part of South America. It is known for its diverse landscapes, rich culture, and vibrant economy.\nAccording to the data, Argentina has an average of 2,800 hours of sunshine per year, which is favorable for solar power generation. The country carbon emissions are estimated at 440 million metric tons per year. The average cost of solar panels is around 1,500 ARS/kW (approximately $100/kW). Renewable energy currently makes up around 10% of Argentina electricity generation. \nArgentina GDP per capital was $11,852 in 2022, according to World Bank data. The country has a population of around 46.2 million people. Argentina trade balance has fluctuated in recent years, with a trade deficit of $9.7 billion in 2018 and a trade surplus of $15.1 billion in 2021. The country inward foreign direct investment stock was $116.7 billion.'),

-- Australia
('AUS', 'AU', 'Australia', 3000, 180000000, 1500, 0.2, 250, 26636454,
'Australia is a country located in the Southern Hemisphere, comprising the mainland of the Australian continent, the island of Tasmania, and numerous smaller islands. It is the sixth-largest country by total area. Australia has a diverse climate ranging from tropical in the north to temperate in the south, with a generally hot and dry interior. [https://en.wikipedia.org/wiki/Australia]
\nAustralia has significant potential for solar power generation due to its abundant sunshine, particularly in the northern and central regions. The government has implemented policies to support the growth of renewable energy, including solar, leading to increased installation of solar panels across the country. However, there is still room for further expansion of solar power to reduce the country''s reliance on fossil fuels.'),

-- Brazil
('BRA', 'BR', 'Brazil', 2600, 65000000, 1500, 0.2, 500, 217341830,
'Brazil is the largest country in both South America and Latin America. It is the world''s fifth-largest country, both by geographical area and by population. Brazil''s economy is the world''s ninth-largest by nominal GDP and eighth-largest by purchasing power parity. [https://en.wikipedia.org/wiki/Brazil]
\nBrazil has significant potential for solar power generation due to its large land area and high levels of solar irradiation, especially in the northeast region. The country has seen rapid growth in solar capacity in recent years, driven by government incentives and falling technology costs. However, there is still room for further expansion of solar power to diversify Brazil''s energy mix, which has historically been dominated by hydroelectric and fossil fuel sources.'),

-- Canada
('CAN', 'CA', 'Canada', 2000, 530000000, 2500, 0.67, 600, 40528396,
'Canada is a country in North America. It is the worlds second-largest country by total area. Canadas climate varies widely, ranging from arctic weather in the north to hot summers in the south. While Canada has significant renewable energy resources, including hydroelectric, solar, and wind power, it still relies heavily on fossil fuels for its energy needs. The government has set targets to increase the share of renewable energy in the country electricity mix. [https://en.wikipedia.org/wiki/Canada]\nCanada has significant solar energy potential, especially in the southern regions, but the industry is still relatively small compared to other renewable sources like hydroelectric and wind power. The government has introduced various incentives and policies to support the growth of solar power, and there is potential for further expansion in the coming years as costs continue to decline and technology improves.'),

-- Iran
('IRN', 'IR', 'Iran', 3000, 600000000, 1500, 0.1, 300, 86500000,
'Iran, officially the Islamic Republic of Iran, is a country located in Western Asia. It is bordered by the Caspian Sea, the Persian Gulf, and the Gulf of Oman. Iran has a diverse climate, ranging from arid and semi-arid regions in the central and eastern parts to subtropical along the Caspian coast. The country experiences abundant sunshine, making it well-suited for solar power development. [https://en.wikipedia.org/wiki/Iran]
\nIran has been actively investing in solar energy in recent years, driven by its abundant solar resources and the government efforts to diversify the country energy mix and reduce reliance on fossil fuels. The country has set ambitious targets for renewable energy deployment, including plans to install 5 gigawatts (GW) of solar capacity by 2022. However, progress has been slower than expected due to various challenges, including economic sanctions and grid integration issues. Nevertheless, Iran solar potential remains significant, and continued policy support and technological advancements could unlock further growth in the sector.'),

-- Saudi Arabia
('SAU', 'SA', 'Saudi Arabia', 3285, 600000000, 2000, 0.0038, 300, 37473929,
'Saudi Arabia is a country located in Western Asia, bordering the Red Sea and the Persian Gulf. It is the largest country in the Middle East and the 13th-largest country in the world by land area. Saudi Arabia has a hot desert climate, with high temperatures and low rainfall throughout the year. [https://en.wikipedia.org/wiki/Saudi_Arabia]
\nSaudi Arabia has been investing heavily in renewable energy, particularly solar power, in recent years. The country has set ambitious targets to increase its renewable energy capacity, aiming to generate 50% of its electricity from renewables by 2030. This is driven by the country abundant solar resources and the desire to diversify its energy mix and reduce its reliance on oil and gas exports. However, the country still relies heavily on fossil fuels, and there is significant potential for further growth in renewable energy generation.');


INSERT INTO organization (name_slug, country_code, name, details_paypal, details_stripe, sites, status, description)
VALUES
    ('antarctica_solar_project', 'ATA', 'Antarctica Solar Project', NULL, NULL, NULL, NULL, 'This project is completely made up. Nobody lives in antarctica so why would you invest here?'),
    ('solaris', 'ESP', 'Solaris', NULL, NULL, '348', 'Ongoing', 'A project to install a solar power plant in farmlands .'),
    ('rural_electrification_initiative', 'ESP', 'Rural Electrification Initiative', NULL, NULL, '54', 'Completed', 'Electrification of remote villages using solar energy.'),
    ('sunflower_global_ltd', 'ESP', 'Sunflower Global Ltd', NULL, NULL, '273', 'Completed', 'Solar panel installation for Govt housing colonies.');


INSERT INTO donation (created, country_code, organization_slug, donation_amount, householder_id)
VALUES
    ('2024-01-12 01:15:38.587367', 'ATA', 'antarctica_solar_project', 2800, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2024-02-01 03:20:49.565309', 'ATA', 'antarctica_solar_project', 2800, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-03-25 04:01:21.346968', 'ATA', 'antarctica_solar_project', 2800, '3d1886b7-abec-49b9-b849-99ceb616b127'),
    ('2023-04-13 06:33:40.246119', 'ESP', 'solaris', 1260, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-05-19 08:42:16.262143', 'ESP', 'solaris', 630, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-06-08 10:19:39.237623', 'ESP', 'solaris', 1260, '3d1886b7-abec-49b9-b849-99ceb616b127'),
    ('2023-09-28 11:02:32.332768', 'ESP', 'rural_electrification_initiative', 630, '47fa9dc4-cb7a-44c0-ace2-a65d8705495e'),
    ('2023-11-03 18:52:04.351058', 'ESP', 'rural_electrification_initiative', 1260, '3d1886b7-abec-49b9-b849-99ceb616b127');
