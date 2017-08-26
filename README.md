# pi_garden
script for my Raspberry Pi to turn on a pump every now and then

Start with the GPIO pin number as a command line parameter.

This script has both a watcher and a worker subprocess. The watcher checks if the process is alive every second. I don't want my plants to die while I'm on a vacation because of a stupid error, do I?

Overwatering (flooding) scenarios have to be considered better.

## Future improvements

0. Stability, testing.
1. Get weather info from somewhere (either Google's demo BigQuery dataset from NOAA, for exact measurements, or some forecast service), and based on that, modify the needed quantity.
2. Enable manual control by enabling querying a server for manual input. Also needs that server.
3. If I want to spend more, maybe get soil moisture sensors.
4. Better soldering so that birds don't try to get funny with my wires.
