# cfsb-noclist

## Docker Setup (Recommended - especially for non-MacOS users)

### Requirements
- docker

### docker-compose
Note: This will pull/build and start up docker contianers for both `adhocteam/noclist` and the app in this repo 
(`src/app.py`).  The app, will run and output will be listed among the stdout of the docker container.

Run the following:
```shell script
cd <this_project_path>
docker-compose up
```

### docker run
Note: This process will first pull and run a container for `adhocteam/noclist`, the build and image and run a container 
for the app in this repo (`src/app.py`).  The app, will run and output will be listed among the stdout of the 
docker container.

Run the following:
```shell script
cd <this_project_path>
docker run --rm -p 8888:8888 adhocteam/noclist
docker build -t cfsd-noclist_image .
docker run --rm --name cfsd-noclist_container cfsd-noclist_image
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
- Mac
```shell script
brew install pyenv (Follow post installation steps)
pip install virtualenv
``` 
- Linux
```shell script
git clone https://github.com/pyenv/pyenv.git ~/.pyenv (Follow post installation steps)
pip install virtualenv
```
- Windows
    - Follow steps in - https://github.com/pyenv-win/pyenv-win
    - Then run the following:
```shell script
cd <this_project_path>
pyenv install 3.9.1
pyenv local 3.9.1
pip install virtualenv
```


### Mac/Linux - Run App
- Run the following
```shell script
cd <this_project_path>
./local-install.sh
```

### Windows - Run App
- Run the following
```shell script
cd <this_project_path>
virtualenv --python=$(pyenv which python) "<this_project_path>/venv"
source venv\bin\activate
pip install -r requirements
python src\app.py
```
