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

System administrators must ensure that the web application works as intended. They have the ability to modify accounts and upgrade users to staff accounts. Questions and issues can be reported to system administrators by other users that system administrators will resolve or answer.

## User Stories

## Architecture Technology Choices