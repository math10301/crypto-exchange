# Crypto Exchange API Documentation

## Endpoints

### Authentication

- `POST /api/register`
  - Registers a new user.
  - Request Body: `{ "username": "string", "email": "string", "password": "string" }`

- `POST /api/login`
  - Logs in a user.
  - Request Body: `{ "username": "string", "password": "string" }`

### Account Management

- `GET /api/account/{user_id}`
  - Retrieves the account balance of a user.
  - Path Parameter: `user_id`

- `POST /api/transfer`
  - Transfers funds between accounts.
  - Request Body: `{ "from_account_id": "int", "to_account_id": "int", "amount": "float" }`

### Currency Exchange

- `POST /api/exchange`
  - Exchanges currency for a user.
  - Request Body: `{ "user_id": "int", "from_currency": "string", "to_currency": "string", "amount": "float" }`

### Charts

- `GET /api/chart/{currency}`
  - Retrieves the price chart of a currency.
  - Path Parameter: `currency`

### Admin

- `POST /api/admin/update_balance`
  - Updates the balance of a user.
  - Request Body: `{ "user_id": "int", "fiat_balance": "float", "crypto_balance": "float" }`

- `DELETE /api/admin/delete_user/{user_id}`
  - Deletes a user.
  - Path Parameter: `user_id`

### Integration

- `POST /api/external/deposit`
  - Deposits funds from an external service.
  - Request Body: `{ "user_id": "int", "amount": "float", "currency": "string" }`

- `POST /api/external/withdraw`
  - Withdraws funds to an external service.
  - Request Body: `{ "user_id": "int", "amount": "float", "currency": "string" }`