# Midterm project contract

This repository is a local-only, single-user demonstration of a salon appointment workflow.

## Contract expectations

1. Keep all data fictional and local.
2. Do not use real accounts, API keys, or external sends.
3. Use a SQLite database for persistence.
4. Put the business rules in the code and test them with known-answer cases.
5. Freeze expected results before implementing the final app logic.
6. Run the known-answer suite after each build slice.

## Core workflow

- Customer submits a fictional request for a service and provider.
- The app checks provider conflicts and business hours.
- Front desk confirms or moves the booking.
- Provider views their own schedule.
- Reminder entries are logged locally without sending anything to the outside world.

## Safety and audit

- No real health, contact, or payment data is allowed.
- Action records are written to SQLite audit/reminder tables only.
- The app behaves like a demo and must not be used as a production booking system.
