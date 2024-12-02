# Create a virtual environment
python3 -m venv env
# Activate env
source env/bin/activate

#export MATCH_MANIFEST_VERSIONS=false
set MATCH_MANIFEST_VERSIONS=false

# Install libraries
pip install -r requirements.txt
# Move to the src folder
cd src
# Run the main.py
python3 main.py