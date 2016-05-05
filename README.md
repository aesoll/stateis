# stateis
A simple Python command line utility to check the status of your servers.

----
## Installation

    sudo apt-get install python-dev python-pip python-virtualenv
    cd [directory you want to house stateis]
    git clone https://github.com/aesoll/stateis.git
    cd stateis
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Read about Python virtual environments [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

----
## Usage
*Ensure your Python virtual environment has been activated before running Python commands in order to access the correct packages.*

    python stateis.py table

The above command will output the server information to a table in the terminal window.

    python stateis.py xml


The above command will output the server information to a properly formatted XML file.

    python stateis.py json

The above command will output the server information to a properly formatted JSON file. 
