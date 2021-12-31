
# Tracert (Traceroute)

> Finds the route from you to the given IP address by sending ICMP pings.

## How to run (Linux)

1) Clone the repo

```shell
git clone https://github.com/Furetur/tracert-python.git
cd tracert-python
```

2) Install the dependencies

```shell
pip3 install -r requirements.txt

# or with virtual env
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

3) Run with root privileges

```shell
sudo python3 main.py 8.8.8.8

# or with virtual env
sudo ./venv/bin/python3 main.py 8.8.8.8
```


