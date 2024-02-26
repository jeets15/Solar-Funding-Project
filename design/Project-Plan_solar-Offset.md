# Project Planning - solar Offset

## Project Requirements

Requirements taken from the Client Brief.

- Standard account registration and login
- Allowing householders to compare carbon benefits for different countries, e.g. against the current carbon production for electricity
- May also be used to compare electricity availability, e.g. power grid/network availability
- Shows householders current solar funding with electricity generated and carbon footprint savings
- Shows total cost of installation for solar panels by country - typically only a couple of countries would be initially available since this data can be hard to come by
- Should also allow households to compare countries by their potential solar power generation as well as other aspects such as the population and the benefit to the communities
- The countries available should be included with (realistic) descriptions that would allow a household to fund with more knowledge and confidence
- Admin accounts and likely staff accounts for non user management processes
- Admin role can upgrade accounts for staff
- Payments should be via paypal and stripe (sandbox only)
- An Admin dashboard will need to be available for managing users accounts
Relevant reports should be available for staff, e.g. countries chosen, panels bought, totals for carbon offset, etc.
- Optionally allow householders to identify their household current carbon footprint, preferably through a third party, by age of property, insulation, electricity usage (by yearly or monthly adjusted for time year)

> Open Questions
> - How many donations options per country? One? How will they be decided?
> - What if householders want a refund? Does the webapp handle this? Does it go through paypal?
> - How should the country descriptions look? Pasted from Wikipedia?

## User Types

### Householder

A single person or a household of people that lives in the UK. A householder wishes to offset their carbon footprint by donating money to solar panel projects in other countries. They want to be able to calculate their own carbon footprint and by how much their solar funding could offset this footprint.

> Open Questions
> - Will the web application only be restricted to users in the UK? (GDPR, Data Protection Act, Cookies, etc...)
> - Will there be a single account for a household of 4? Or can many users form a household?
> - What information will be collected on this user? Will information be stored for statistical analysis?
> - Storing personal data requires compliance with GDPR
> - Will the footprint reduction be publicly visible? Will it be private?

### System Administrator

System administrators must ensure that the web application works as intended. They have the ability to modify accounts and upgrade users to staff accounts through a dashboard. Questions and issues can be reported to system administrators by other users that system administrators will resolve or answer.

### Staff

Staff accounts can help system administrators with keeping the information on the web application up to date, and can add more countries / opportunities for funding. Staff will be able to view generated reports on statistics of funding by country and carbon offset.

> Open Questions
> - Will staff changes / edits have to be approved by a system administrator?
> - What specifically should staff be able to do?
> - Are staff accounts allowed to donate money? Do they have to use a separate account?

## User Stories

| Priority | System Administrator User Story |
| :-: | :-- |
| Must<br> Have | As a system administrator, I want to use a dashboard to view a list of users that are registered for solar Offset and their role (householder or staff). I want to be able to delete a certain user account, so that I can comply with deletion requests and remove users that have been abusive or otherwise disruptive. |
| Should<br>Have | EITHER:<br>As a system administrator, I want to be able to create staff accounts, so that I can designate users for non user-management processes<br>OR:<br>As a system administrator, I want to be able to change a householder user account to a staff user account, so that this user can support solar Offset in non user-management processes.<br>( or staff accounts will be created manually on the database ) |
| Could<br>Have | As a system administrator, I want to be able to suspend user accounts (which is reversible), adding a message about why the account was suspended, so that I can take action against abusive or otherwise disruptive users without having to delete their account permanently. |

| Priority | Staff User Story |
| :-: | :-- |
| Should<br>Have | As staff, I want to view automatically generated reports on a dashboard showing statistics about donations per country, solar panels built, and offset carbon emissions, so that I can get better insights into the preferences of householders. |
| Would<br>Have | As staff, I want to be able to converse with householders over an interactive chat so that householder questions or issues can be resolved nearly instantaneously. |

| Priority | Householder User Story |
| :-: | :-- |
| Must<br>Have | As a householder, I want to be able to register for a Solar Offset account, so that I can keep a record of my donations and my carbon offset. |
| Must<br>Have | As a householder, I want to be able to view a list of countries (along with relevant data) with solar projects that I can donate towards via Solar Offset, so that I can fund solar electricity generation in other countries and offset my own carbon footprint.<br>Relevant data includes: yearly sun hours, yearly CO2 emissions, average cost of installing a solar panel, fraction of solar energy in country's electricity mix, number of donations made, amount of funds raised, and the potential carbon offset per unit of currency donated. |
| Must<br>Have | As a householder, I want to be able to donate to an available project of my choice choice on Solar Offset via paypal, so that I can contribute towards offsetting my carbon footprint and I can let Solar Offset keep track of my donations for me. |
| Should<br>Have | As a householder that is interested in using Solar Offset and visiting the home page, I want to be informed about what Solar Offset does and want to see statistics about how other householders have contributed towards funding solar projects in various countries across the world, so that I feel motivated to register for Solar Offset and donate towards solar projects.<br>Potential Statistics include: World map with highlighted countries that can be donated to, number of donations made through Solar Offset, funds collected, number of other householders that have joined Solar Offset, ... |
| Should<br>Have | As a householder that is interested in using Solar Offset, I want to be able to calculate an estimate of how much I can offset my carbon footprint based on a given amount of money on the Solar Offset homepage, so that I can be motivated to join Solar Offset and donate towards solar projects. |
| Should<br>Have | As a householder, I want to view my previous donations and other statistics on a dashboard, and compare carbon offsets from donating to different countries and projects to my own carbon footprint, so that I can track my contributions to renewable energy and monitor my environmental impact. |
| Should<br>Have | As a householder, I want to be pointed towards a service to calculate my carbon footprint easily and free of charge on my profile, so that I can compare my footprint against my carbon offsets through donations. |
| Could<br>Have | As a householder, I want to use SSO (Google/Facebook/Github) to register and login for Solar Offset without having to create a separate account. |
| Could<br>Have | As a householder, I want to be able to refer friends and family to Solar Offset so that I can spread awareness about offsetting carbon emissions by donating towards solar panel projects in other countries. (Referral) |
| Would<br>Have | As a householder, I want to receive achievement badges for certain amounts of donations or for donating towards several different projects, so that I can feel accomplished in offseting my carbon footprint and can share my achievements with others. |



## Architecture Technology Choices

- Front-end
  - HTML5,CSS3, Bootstrap, JS
- Back-end
  - Python Flask
- Database
  - SQL
