# cfsb-noclist

This is a project used to return a list of user ids from a noclist api.  The noclist api is generated via a docker 
image tagged as `adhocteam/noclist`.  This app, contained in `src/app.py` can be used to auth against this api, and 
then return a list of relevant user is from it's endpoints. 

## Environment
Set the following variables in your environment if you need something other than these defaults to run.  You can 
update these values in app-variable.env, the docker commands should automatically pull them in.  Also, use one of the 
`DOMAIN` vars since they will otherwise overwrite each other.

- (for docker) NOCLIST_DOMAIN=http://host.docker.internal:8888
- (for local) NOCLIST_DOMAIN=http://localhost:8888
- NOCLIST_AUTH_REQUEST_PATH=/auth
- NOCLIST_USERS_REQUEST_PATH=/users
- REQUEST_RETRY_THRESHOLD=3

## Docker Setup (Recommended - especially for non-MacOS users)

### Requirements
- docker

### docker-compose
Note: This will pull/build and start up docker contianers for both `adhocteam/noclist` and the app in this repo 
(`src/app.py`).  The app, will run and output will be listed among the stdout of the docker container.

Optional Pre-requisite:
- Update the environment variables in `app-variables.env`

Run the following:
```shell script
cd <this_project_path>
docker-compose build
docker-compose up
```

### docker run
Note: This process will first pull and run a container for `adhocteam/noclist`, the build and image and run a container 
for the app in this repo (`src/app.py`).  The app, will run and output will be listed among the stdout of the 
docker container.

Optional Pre-requisite:
- Update the environment variables in `app-variables.env`

Run the following:
```shell script
cd <this_project_path>
docker run --rm -p 8888:8888 adhocteam/noclist
docker build -t cfsd-noclist_image .
docker run --rm --name cfsd-noclist_container --env-file app-variables.env cfsd-noclist_image
```


## Native Setup
You can use these steps to set this up locally, and run on your machine's "bare metal".  This process is really 
only hardened for mac users but if you're on Windows or Linux and committed, here are some tips to where I 
would start.

### Requirements
- `pyenv` - https://github.com/pyenv/pyenv
    - `pyenv-win` for Windows - https://github.com/pyenv-win/pyenv-win
- `virtualenv` - https://virtualenv.pypa.io/en/latest/index.html

Optional:
- Mac - `homebrew`

Note: This is where I would start for these OS, but other methods can be found here:
```
Pyenv - git clone https://github.com/pyenv/pyenv.git ~/.pyenv
Pyenv-win - git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
virtualenv - pip install virtualenv
```
### Mac
```shell script
brew install pyenv (Follow post installation steps)
pip install virtualenv
``` 
### Linux
```shell script
git clone https://github.com/pyenv/pyenv.git ~/.pyenv (Follow post installation steps)
pip install virtualenv
```
### Windows
- Follow steps in - https://github.com/pyenv-win/pyenv-win
- Then run the following:
```shell script
cd <this_project_path>
pyenv install 3.9.1
pyenv local 3.9.1
pip install virtualenv
```

## To Run
Set relevant environment variables in your environment from Environment section above.

### Mac/Linux
```shell script
cd <this_project_path>
./local-install.sh
```

### Windows
```shell script
cd <this_project_path>
virtualenv --python=$(pyenv which python) "<this_project_path>/venv"
source venv\bin\activate
pip install -r requirements
python src\app.py
```

## Tests
This project is set up to use pytest as its test runner.  To run the tests with that, use the command below.

Note: Building the docker image automatically runs the tests as well.  The build will fail if all the tests don't pass.
```shell script
pytest tests/unit/
```