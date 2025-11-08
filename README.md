# ulearning-helper
Automatically check in without any assistance from your classmates.

QR-code check-in has not supported yet. (working...)
## Install
Python needs to be installed.
```bash
git clone https://github.com/Aestas16/ulearning-helper
cd ulearning-helper
pip install -r requirements.txt
```
## Configuration
Copy `config.yaml.example` to `config.yaml`.

```yaml
interval: 1000 # check-in detection polling interval (ms)
username: username
password: password 
location: 114.433000,30.613000 # the first is longitude, and the second is latitude
address: 武汉火车站 # location name
# If you don't understand the meaning of the following parameters, please do not modify them.
UA: App ulearning Android # User-Agent
logininfo:
  device: android
  appVersion: 20250903
  webEnv: 1
  registrationId: 0
```
## Usage
After installation and configuration, run
```bash
python main.py
```