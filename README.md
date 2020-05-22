# TECHFLIX - Restructured
## Status: Functional, the flagship implementation
Currently hosted on: http://techflix-env.eba-egeycdfq.ap-south-1.elasticbeanstalk.com/

*Requirements:*
- Python 3.6+
- Just create a python environment and run `pip install -r requirements.txt`

Setup for running the app:
- Copy `setup/config.py` to `instance/config.py`
- Run with `python application.py`

### create_user.py
`testing/create_user.py` is a click tool to create a user with chosen story_id.
Run `python3 testing/create_user.py --help`
