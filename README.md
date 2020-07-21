Aliasmanager
============

To install:

  1. `git clone https://github.com/xoraxax/aliasmanager`
  2. `cd aliasmanager`
  3. `virtualenv -p python3 env`
  4. `. env/bin/activate`
  5. `pip install flask bcrypt`
  6. Set the `USERS_FILE` variable in `aliasmanager.py` to a preferred location.
  7. `sh set-password.sh admin foo`

To run:

  1. Ensure you are in the `aliasmanager` folder.
  2. `sh run.sh`
