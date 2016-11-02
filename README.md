- At the moment the information below is as is. Some updates need to be done to finalize it -

# wiolink2graphite
wio2graphite has been written to be able to extract data gathered by a WioLink and push the data to graphite.
This has been created to run on a RasberryPi, together with a graphite and a grafana installation.

## Modules currently supported by the script:
* Grove - Temp&Humi Sensor
* Grove - Digital Light Sensor
* Grove - Air quality sensor v1.3

# included
The environment directory contains the following files.
* wiolink2graphite.py
* parameters.py

# setup
* install graphite and grafana (could be done as described on https://markinbristol.wordpress.com/2015/09/20/setting-up-graphite-api-grafana-on-a-raspberry-pi/)
** Don't forget the graphite api: http://graphite-api.readthedocs.io/en/latest/installation.html#python-package
* Deploy a Local Lean Data Exchange Server as described at https://github.com/Seeed-Studio/Wio_Link/wiki/Server%20Deployment%20Guide
* configure the Wiolink to send it's data to the local Wiolink server vi the iOS app
* configure wiolink2graphite to get the data from the lean server

# More information
https://www.seeedstudio.com/s/WioLink.html
https://github.com/Seeed-Studio/Wio_Link
http://seeed-studio.github.io/Wio_Link/
