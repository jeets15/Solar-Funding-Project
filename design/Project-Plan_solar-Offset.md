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
| Must<br>Have | As a system administrator, I want to use a dashboard to be able to manage, modify, and delete user accounts that have registered for solar Offset so that I can udpate potentially incorrect information and take action against abusive or otherwise disruptive users. |
| Must<br>Have | As a system administrator, I want to be able to upgrade householder user accounts to staff accounts and be able to downgrade them so that I can designate users that can help with the upkeep of solar Offset, but be able to take away their priviliges if necessary. |

| Priority | Staff User Story |
| :-: | :-- |
| Must<br>Have | As staff, I want to add a new country to the listing where I can add current carbon emissions for electricity, electricity availablility, cost of solar panels, potential solar energy generation, population size, benefit to the communities, and a realistic textual description of the country, so that householders can make informed decisions about where they want to donate to solar energy. |
| Must<br>Have | As staff, I want to be able to modify existing country listings so that I can keep them accurate and up to date. |
| Must<br>Have | As staff, I want to add, update, and delete payment details for donation recepients within a country listing. |
| Should<br>Have | As staff I want to view automatically generated reports showing statistics about donations per country, solar panels built, and offset carbon emissions, so that I can get better insights into the preferences of householders. |
| Could Have | As staff, I want to be able to see which country listings were updated least recently so that I can check if there is any updated information available. |

| Priority | Household Owner User Story |
| :-: | :-- |
| Must<br>Be | Able to login in case of a returning user or register himself in case of a new user. For registration, we can make use of SSO(Google, Facebook, Github) |
| Must<br>Be | As a household owner, he/she must be able to compare carbon benefits for different countries available against his/her own country's carbon footprint |
| Must<br>Have | As a household owner, I want to view my current solar funding and carbon savings,So that I can track my contributions to renewable energy and monitor my environmental impact. |
| Must<br>Have | As a household owner, I want to fund solar power for my country,So that I can reduce my carbon footprint and contribute to renewable energy initiatives. |
| Could<br>Have | As a household owner, I want to be able to refer friends and family to make contributions towards solar power projects. (Referal) |



## Architecture Technology Choices

- Front-end
  - HTML5,CSS3, Bootstrap, JS
- Back-end
  - Python Flask
- Database
  - SQL
