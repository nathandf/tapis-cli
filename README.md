# TapisV3 CLI

TapisV3 CLI is a command line interface tool written in python that wraps the tapipy library to enable user to make fast and efficient calls to tapisv3 APIs.

## Getting Started
tapis-cli can be set up and run in 2 ways; Locally, and in a Docker container.

### Local setup
**Clone the repo**\
`git clone https://github.com/nathandf/tapis-cli.git`

**Navigate to the root directory of the project where tapis.sh is found**\
`cd ./tapis-cli>`

**Initialze a virtual env**\
`pipenv shell`

**Install Tapipy**\
`pip install tapipy`

**Add the following line in your .bashrc file**\
`alias tapis="<path/to/tapis_cli_project>/tapis.sh"`

### Container setup

## Running Commands
### General Usage
$`tapis [category] [command] [action] [args]`

