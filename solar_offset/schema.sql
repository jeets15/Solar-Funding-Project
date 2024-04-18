DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS organization;
DROP TABLE IF EXISTS donation;

CREATE TABLE user
(
    -- id: A unique id for each user; this value should only be used in the back-end or as a session cookie
    -- Users should normally not have access to this id
    -- Entries to the id column will be generated using
    --   uuid.uuid4(), a random 36 character string
    id             CHAR(36) CHECK ( LENGTH(id) == 36 ) PRIMARY KEY,
    -- email_username: The e-mail address of a registered householder
    -- internal account types like admin and staff will usually have a username instead of an e-mail
    -- this column must be unique as users will use e-mail/username to log in to solar offset
    -- 70 as an upper limit is already very long
    email_username VARCHAR(70) CHECK ( LENGTH(id) <= 70 ) UNIQUE NOT NULL,
    -- password_hash: The hashed password that the login will be compared against
    -- Password hashes will be generated using werkzeug.security.generate_password_hash
    --   and checked with werkzeug.security.check_password_hash
    password_hash  TEXT                                          NOT NULL,
    -- display_name: optional entry that will be shown on personalised pages
    -- usually only used for the householder user type
    display_name   VARCHAR(70) CHECK ( LENGTH(id) <= 70 ),
    -- user_type: defines which type of user this entry belongs to
    -- h ~ householder, s ~ staff, a ~ admin
    -- if a user is a householder, they can't have any other roles
    -- a user can be admin, staff, or both at the same time
    user_type      CHAR(3) CHECK ( user_type IN ('h__', '__a', '_s_', '_sa') ),

    -- If user is suspended set column to a string containing the "suspension message"
    -- set to NULL otherwise
    status_suspend TEXT DEFAULT NULL,

    -- Householder Only
    --   Carbon footprint of householder in Tons (t)
    householder_carbon_footprint REAL DEFAULT NULL CHECK ( householder_carbon_footprint > 0 )
);

CREATE TABLE country
(
    country_code               CHAR(3) PRIMARY KEY, -- This column will store the ISO 3166-1 A-3 Country code (https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
    short_code                 CHAR(2) UNIQUE,      -- The two-character country code, useful for various API's
    name                       TEXT NOT NULL,       -- Country Name as displayed to the user
    description                TEXT,                -- long-ish description about country in relation to solar offset
    solar_hours                INTEGER,             -- hours of sunlight per year (estimate)
    carbon_emissions           INTEGER,             -- Yearly carbon emissions (from electricity production ideally) in Tons of CO2
    solar_panel_price_per_kw          INTEGER,             -- Price for constructing a solar panel in (£ / kW)
    electricity_mix_percentage DOUBLE,              -- What percentage of the electricity mix is generated from solar energy
    electricty_consumption     INTEGER,             -- Electric Energy being used in the Country (TWh)
    population_size            INTEGER NOT NULL DEFAULT 0 CHECK( population_size >= 0 ) -- Population size of the given country
);

CREATE TABLE organization
(
    name_slug      TEXT,          -- "slug" of the organization name (all lowercase, remove special character, hyphens and spaces to underscore)
    country_code   CHAR(3),       -- Foreign key to reference country in which organization acts
    name           TEXT NOT NULL, -- Organization name (what the slug is generated from)
    description    TEXT,          -- Optional organization description
    details_paypal TEXT,          -- Optional payment details for paypal
    details_stripe TEXT,          -- Optional payment details for stripe
    sites          TEXT,          -- #TODO what is the purpose of this column?
    status         TEXT,          -- #TODO what is the purpose of this column?
    PRIMARY KEY (name_slug, country_code),
    FOREIGN KEY (country_code) REFERENCES country (country_code)
);

CREATE TABLE donation
(
    created           TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Time at which donation was made
    householder_id    CHAR(36),                            -- id of householder that made this donation
    country_code      CHAR(3),                             -- Foreign key composite with organization slug
    organization_slug TEXT,                                -- Foreign key composite with country code
    donation_amount   INTEGER,                             -- Set the rule that only whole numbers are allowed as donations
    PRIMARY KEY (created, householder_id, country_code, organization_slug),
    FOREIGN KEY (householder_id) REFERENCES user (id),
    FOREIGN KEY (country_code) REFERENCES organization (country_code),
    FOREIGN KEY (organization_slug) REFERENCES organization (name_slug)
);