
-- Drop all tables to reset DB
DROP TABLE IF EXISTS householder;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS administrator;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS organization;
DROP TABLE IF EXISTS donation;


CREATE TABLE householder (
    id CHAR(36) PRIMARY KEY, -- Entries to the id column will be generated using uuid.uuid4(), a random 36 character string
    email VARCHAR(70) UNIQUE NOT NULL, -- 70 as an upper limit for e-mail length is already very long
    display_name VARCHAR(70) NOT NULL, -- Display name is how the householder will be adressed
    password_hash TEXT NOT NULL -- Password hashes will be generated using werkzeug.security.generate_password_hash and checked with werkzeug.security.check_password_hash
);

CREATE TABLE staff (
     id CHAR(36) PRIMARY KEY, -- Entries to the id column will be generated using uuid.uuid4(), a random 36 character string
     username VARCHAR(70) UNIQUE NOT NULL, -- Unique username that staff will use to log in
     password_hash TEXT NOT NULL -- Password hashes will be generated using werkzeug.security.generate_password_hash and checked with werkzeug.security.check_password_hash
);

CREATE TABLE administrator (
     id CHAR(36) PRIMARY KEY, -- Entries to the id column will be generated using uuid.uuid4(), a random 36 character string
     username VARCHAR(70) UNIQUE NOT NULL, -- Unique username that administrators will use to log in
     password_hash TEXT NOT NULL -- Password hashes will be generated using werkzeug.security.generate_password_hash and checked with werkzeug.security.check_password_hash
);

CREATE TABLE country (
    country_code CHAR(3) PRIMARY KEY, -- This column will store the ISO 3166-1 A-3 Country code (https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
    short_code CHAR(2) UNIQUE, -- The two-character country code, useful for various API's
    name TEXT NOT NULL, -- Country Name as displayed to the user
    description TEXT, -- long-ish description about country in relation to solar offset
    solar_hours INTEGER, -- hours of sunlight per year (estimate)
    carbon_emissions INTEGER, -- Yearly carbon emissions (from electricity production ideally) in Tons of CO2
    solar_panel_price DOUBLE, -- Price for constructing a solar panel in (£ / kW)
    electricity_mix_percentage DOUBLE, -- What percentage of the electricity mix is generated from solar energy
    electricty_consumption INTEGER -- Electric Energy being used in the Country (TWh)
);

CREATE TABLE organization (
    name_slug TEXT, -- "slug" of the organization name (all lowercase, remove special character, hyphens and spaces to underscore)
    country_code CHAR(3), -- Foreign key to reference country in which organization acts
    name TEXT NOT NULL, -- Organization name (what the slug is generated from)
    description TEXT, -- Optional organization description
    details_paypal TEXT, -- Optional payment details for paypal
    details_stripe TEXT, -- Optional payment details for stripe
    PRIMARY KEY (name_slug, country_code),
    FOREIGN KEY (country_code) REFERENCES country (country_code)
);

CREATE TABLE donation (
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Time at which donation was made
    householder_id CHAR(36), -- id of householder that made this donation
    country_code CHAR(3), -- Foreign key composite with organization slug
    organization_slug TEXT, -- Foreign key composite with country code
    donation_amount INTEGER, -- Set the rule that only whole numbers are allowed as donations
    PRIMARY KEY (created, householder_id, country_code, organization_slug),
    FOREIGN KEY (householder_id) REFERENCES householder (id),
    FOREIGN KEY (country_code) REFERENCES organization (country_code),
    FOREIGN KEY (organization_slug) REFERENCES organization (name_slug)
);
