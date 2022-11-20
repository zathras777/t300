# t300

Access internal data from a Proxon T-300 Water Heater using modbus

We use a [Proxon T-300 Water Heater](https://www.zimmermann-lueftung.de/komforttechnik/die-proxon-geraete/proxon-t300-trinkwasserwaermepumpe) for our domestic hot water, but we don't have the other parts of the Proxon system that normally provide the information and control aspects for the system as detailed in various other Github Projects,

- [m4dmin/proxon-control](https://github.com/m4dmin/proxon-control)
- [jgralfs/Proxon-FWT-modbus-connector](https://github.com/jgralfs/Proxon-FWT-modbus-connector)

Following some research it transpires that the T-300 communicates with the control module via a standard modbus connection. Connecting directly to the T-300 system is possible and the data can be read, but I have been unable to find any details of the registers online. This project details an effort to figure the various registers needed to extract useful information from the system.

The intent is to create a way to provide the system information to an external home automation system either via a simple JSON REST interface or MQTT.

## Physical Connection

The modbus connector is X17 on the logic board. The pins are A, B and GND.

## Modbus Setup

The configuration turned out to be the same as for the main Proxon module

- 19200 Baud Rate
- 8 bits
- Even Parity
- 1 stop bit

## Setpoints & Registers

Data was available on

- input registers 1-119, 200-206 and 300-315 (code #3)
- holding registers 1-119 (code #4)

As with other projects I have found that negative temperature values are stored by adding 100 to the value, i.e. -15 is stored as 85.
Where a value has a decimal place, the value is stored multiplied to give a integer, i.e. 7.0 is stored as 70.

I plan on creating a PDF with the details of the registers and setpoints they relate to and uploading it.

## Time / Date

The currently configured date & time are available on register 200-206.

## t300.py

The python script presently queries for known setpoints and the date/time and dumps the data to the terminal. It is a work in progress :-)

## Future Plans

I am hoping to resolve more of the registers and add them to the script.
