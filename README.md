# CDP/LLDP Network Discovery Crawler for Cisco networks

## Todo
- Add Serial Number collection
- Dedup devices on Serial Number
- Generate Graphviz Output
- Collect platform version and ios image

## Fork information
This has been forked to be able to accomodate the needs of Craig Armstrong
Commits will be as detailed as possible, code maintenance may die as quickly as this repo was forked

This is experimental at the moment. Uses netmiko and some seed devices to scrape
your network and output CSV files of all neighbor topology data, as well as a
device list file. Uses threaded connections at each iteration, moving out from
seed devices to next level of devices until all devices are discovered.

Uses a BFS algorithm with netmiko, and calculates distances from seed devices.
Currently only works with SSH access to Cisco IOS and NXOS devices, but other
devices could be added easily. Will gather all neighbors and devices found, but
can only scrape cisco devices to discover next level devices at the moment.

## Usage Example: Scrape network starting with the core devices

* Note: The initial devices should have the same device ID in the cdp neighbors
  to avoid duplicate device entries and proper distance calculations

```./ndcrawl.py -seed core1.domain.com,core2.domain.com --user yantisj -nei_file nd.csv -dev_file devices.csv --debug 1```

```
usage: ndcrawl.py [-h] [-seed switch1[,switch2]] [-nei_file file]
                  [-dev_file file] [-gv_file file] [-ng_file file] [--quiet]
                  [--seed_os cisco_nxos] [--seed_file file] [--user username]
                  [--max_crawl int] [--conf file] [--debug DEBUG] [-v]
                  [--en secret]

Discover Network Topology via CDP/LLDP

optional arguments:
  -h, --help            show this help message and exit
  -seed switch1[,switch2]
                        Seed devices to start crawl
  -nei_file file        Output Neighbors to File
  -dev_file file        Output Devices to File
  -gv_file file         Output GraphViz Topology File
  -ng_file file         Output NetGrph Topology File
  --quiet               Quiet output, log to file only
  --seed_os cisco_nxos  Netmiko OS type for seed devices
  --seed_file file      Seed devices from a file, one per line
  --user username       Username to execute as
  --max_crawl int       Max devices to crawl (default 10000)
  --conf file           Alternate Config File
  --debug DEBUG         Set debugging level
  -v                    Verbose Output
  --en secret           Activate privilege level 15
 ```
## Config File Notes

Copy the ndcrawl-sample.ini to ndcrawl.ini and edit options. All CLI options can be specified
from the config file for daemonizing the script. CLI options always override the config file.

## Neighbor List Output Example
```
local_device_id,distance,remote_device_id,platform,local_int,remote_int,ipv4,os
core1.domain.com,0,mdcoobsw1.domain.com,WS-C4948,mgmt0,GigabitEthernet1/1,10.25.9.1,cisco_ios
core1.domain.com,0,servchas1.domain.com,WS-C6504-E,Ethernet7/25,TenGigabitEthernet3/1,10.24.70.51,cisco_ios
core1.domain.com,0,core2.domain.com,N7K-C7010,Ethernet7/26,Ethernet8/26,10.25.156.103,cisco_nxos
core1.domain.com,0,artmdf1.domain.com,N7K-C7010,Ethernet7/27,Ethernet2/26,10.25.80.103,cisco_nxos
```

## Device List Output Example
```
device_id,ipv4,platform,os
core1.domain.com,10.25.9.103,N7K-C7010,cisco_nxos
cnew1.domain.com,10.25.9.10,N9K-C93180YC-EX,cisco_nxos
```
