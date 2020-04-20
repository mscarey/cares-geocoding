# Geocoding.py

This script uses place names and addresses from a CSV to call the MapQuest API, and compares the coordinates of the result data to the existing data in the CSV. If the coordinates in the API response are different from those in the input CSV (and if the location found by the API is in the correct ZIP code), the script saves an update to a new CSV called `updates.csv`.

This process might be useful in correcting coordinates that may be wrong because the source data used nonstandard addresses or other ways of describing locations of apartment buildings. However, the addresses and coordinates in `updates.csv` are unverified and can also be wrong.

To run the script, obtain a free MapQuest API key, and create a file in this folder called `.env` containing text like `MAPQUEST_KEY="your-key-here"`. Activate a virtual environment if desired, and install the dependencies using `pip install -r requirements.txt` Then use Python to run the file with the command `python3 -m geocoding`.
