# API Structure

Cash is a way to add and keep track of expenses, revenues and money for a specific user. This should be filterable on categories (that can be created by users), as well as time periods and prices. It should also aggregate data to highlight general spending.

To handle the above, the following backend structure is needed.

## Database

The database needs to keep track of a few different things:

1. Users - these should be creatable using email and password. Users will be linked to most other tables.
2. Categories - these are created by users and consist of a name. They can then be linked to revenue and expenses.
3. Revenue - Incoming money for a user. Contains the amount, time, categories as well as a description.
4. Expense - Outgoing money for a user. Contains the amount, time, categories as well as a description.

## API

The Cash backend will be a REST API. It will allow for CRUD methods on the various database models (except users). Revenue and expenses can be fetches using filters that include categories (on comma separated ID lists), time periods and prices. Category filters should use OR logic (i.e. if a user filters on "CAR" and "TECH" categories, all items of either "CAR", "TECH" or _both_ should show up), whereas using multiple filters should use AND logic.
