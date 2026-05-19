# TODO - Cobra Kai Banking

## Banking Features
- Let users choose an account type during account creation.
- Add multiple accounts per user, such as checking and savings.
- Add transfer support between a user's own accounts.
- Automate interest calculation on a schedule.

## Security
- Replace `ALLOWED_HOSTS = ["*"]` with environment-specific host values before production deployment.
- Move all production secrets into environment variables.
- Add rate limiting or lockout behavior for repeated failed logins.

## User Experience
- Improve dashboard layout for transaction history and account actions.
- Add clearer form validation messages for invalid deposit and withdrawal amounts.
- Add confirmation messaging for account creation and withdrawals.

## Code
- Add forms for deposits, withdrawals, and account creation instead of reading raw POST values.
- Add model tests for deposit, withdrawal, insufficient balance, and withdrawal limits.
- Add view tests for authenticated and unauthenticated dashboard access.

## Deployment
- Add a `requirements.txt` if this repository does not already include one.
- Document the Render/Railway environment variables needed for deployment.
- Add a production database option such as PostgreSQL.

