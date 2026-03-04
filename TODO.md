# TODO: Fix Blockchain Connection Error

## Problem
The blockchain connection check in `blockchain/utils.py` runs at import time, causing Django to fail to start when Ganache is not running.

## Solution
Make the blockchain connection lazy - only connect when the function is actually called, not at import time.

## Tasks Completed
- [x] Modify `blockchain/utils.py` to make blockchain connection lazy
  - Remove module-level connection check
  - Add helper function to get web3 connection
  - Update functions to check connection before executing

## Additional Fixes
- [x] Fixed user dashboard certificate upload
  - Added JavaScript to make upload area clickable in `templates/users/user_dashboard.html`
  - Updated `accounts/views.py` to include certificate verification logic in user_dashboard view
- [x] Added better error handling for blockchain connection errors
  - Shows friendly message when Ganache is not running: "⚠️ Blockchain not connected. Please start Ganache to verify certificates."

## Important Note
To verify certificates, Ganache must be running on port 7545. The application will work without Ganache, but certificate verification will show a friendly error message.
