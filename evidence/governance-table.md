# Governance and Credential-Handling Table (ADI501 only, 3 points)

One or two sentences per row, specific to **your** tool. Replace the example column with your own text.

| Row | Your answer | Example (Idea 2 appointments) |
|---|---|---|
| Data | | *Fifty made-up clients with invented names and phone numbers; no real person appears.* |
| Credentials | | *None in use. The agent was never given a key; `grep -rniE "key\|token\|password" . --exclude-dir=.git` finds only template wording, no real key.* |
| External step | | *Reminders are appended to `reminders.log`; no email or text is sent.* |
| Who can do what | | *Only front desk moves `booked` to `confirmed`; the test `client_cannot_confirm` proves a client cannot.* |
| Agent access | | *The agent ran only inside the project folder; I rejected a command that wrote to my home folder.* |
| If it goes wrong | | *If a key leaked I would stop, tell the instructor, and rotate the key; no key exists today.* |
