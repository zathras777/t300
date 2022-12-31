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

The T300 uses an identifier of 20.

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

``` shell
$ python3 ./t300.py
T-300 Information:
  Date/Time Reported:  Thurs 24/11/2022 @ 21:38 
  Setpoints:
      A  Operation                            On 

      B  Target Temperature                   49.0 C

      C  Heat rod/Boost                       On 

    D01  Temperature Heat Rod                 44.0 C
    D02  Language                             English 
    D03  Display Standby                      12 Mins
    D04  Legionella Function                  On 
    D05  PV Function                          Off 
    D07  Heat rod on at temperature           -1 C
    D08  Only heat rod, no Heat Pump          Off 

    E14  Fan Speed                            30 %
    E18  E-Valve                              24 

    F01  Fan speed operation                  30 %
    F02  Filter change interval               0 Months
    F03  Cold operation temperature           -15.0 C
    F04  Auxillary function                   Off 
    F05  Floor heating enable temperature     35.0 C
    F06  Floor heating setpoint               21.0 C
    F07  Aux hysteresis                       5.0 
    F08  Maximum temperature                  60.0 C
    F09  Defrosting start temperature         40 Pa
    F10  Defrosting start temperature, 80%    50 Pa
    F11  Defrosting stop                      7.0 
    F12  Delta T Mid T Low                    5.0 
    F13  Compressor off hysteresis            5.0 
    F14  ModBus Unit ID                       20 
    F15  ModBus Baud Rate                     19200 
    F16  ModBus Parity                        Even 
    F17  Modbus Write Enabled                 Off 
    F18  USB Enabled                          Off 
    F19  Display Contrast                     5 
    F22  PV Mode                              SG 
    F23  PV Heat Rod Voltage                  5.0 V
    F24  PV WP                                5.0 V
    F25  PV WP Time                           13 mins
    F26  Enable Fan Speed 1 and 2             Off 
    F27  Fan Speed 1                          30 %
    F28  Fan Speed 2                          100 %

    P14  E-Valve                              -6.900000000000006 B
    P19  E-Valve                              80.7 P

    R02  Compressor                           Off 
    R03  Supplemental P                       Off 
    R04  Heat E                               On 
    R05  Fan                                  Off 
    R06  Defrost                              On 

    S06  Defrost                              550 

    T05  Temperature Before Evaporation       5.5 
    T06  Evaporation Temperature              3.200000000000003 
    T09  AUX Temperature                      156.89999999999998 
    T11  Suction Temperature                  6.5 
    T13  Compressor Temperature               39.599999999999994 
    T14  E-Valve Temperature                  -6.900000000000006 
    T20  Low Tank Temperature                 32.599999999999994 
    T21  Mid Tank Temrpertaure                32.69999999999999
```

## Future Plans

I am hoping to resolve more of the registers and add them to the script.
