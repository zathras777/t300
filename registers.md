# Registers

The following are the registers I have managed to verify and may not be correct.

### Register Notes
- The register numbers shown are "human readable", i.e. the first register is shown as 1. 
- When querying the device the register numbers must be zero-referenced.
- Holding registers are generally read/write, Input registers are Read Only.

## Settings

| Register | Register Type | Purpose | Notes |
|----------|---------------|---------|-------|
| 1 | Holding | Target Temperature | Temperature |
| 2 | Holding | Heat Rod/Boost ||
| 3 | Holding | System Operation ||Boolean
| 4 | Holding | Temperature Heat Rod | Temperature | 
| 5 | Holding | Fan Speed 1 |
| 6 | Holding | Fan Speed 2 |
| 7 | Holding | Language | 0: German 1: English |
| 10 | Holding | Display Standby Time| Seconds |
| 11 | Holding | PV Function | Boolean |
| 12 | Holding | Temperature for Heat Rod On | Negative temperature (Small) |
| 13 | Holding | Heat Rod Only? | Boolean |
| 25 | Holding | Filter Change Interval |
| 26 | Holding | Legionella Function | Boolean |
| 27 | Holding | Cold Operation Temperature | Temperature |
| 28 | Holding | Auxillary Function | Boolean |

## Information
| Register | Register Type | Purpose | Notes |
|----------|---------------|---------|-------|
| 12 | Input | Temperature before evaporation | Negative temperature (Large) |
| 13 | Input | Evaporation temperature | Negative temperature (Large) |
| 14 | Input | Low Tank Temperature | Negative temperature (Large) |
| 15 | Input | Mid Tank Temperature | Negative temperature (Large) |
| 16 | Input | Compressor Temperature | Negative temperature (Large) |
| 17 | Input | Suction Temperature | Negative temperature (Large) |
| 18 | Input | AUX temperature |  Negative temperature (Large) |
| 23 | Input | Supplemental P | Negative temperature |
| 24 | Input | Heat E | Negative temperature |
| 25 | Input | Compressor Running | Boolean |
| 26 | Input | Supplemental E Operating | Boolean |
| 27 | Input | Heat E Operating | Boolean |
| 28 | Input | Fan Running | Boolean |
| 29 | Input | Defrost Active | Boolean |
| 39 | Input | Current Fan Speed |
| 60 | Input | Seconds since Legionella Cycle | See note below |
| 61 | Input | 2 hour blocks since Legionella Cycle | See note below |


## Notes

### Temperature Encoding
Most temperatures are recorded to 1 decimal and stored as tenths.
```
  Temperature = 10.1
  Value stored = 101
```

### Negative Temperatures
Recorded in tenths, but offset by 100 for a small number or 1000 for a larger number.
```
  Small Number
    Value stored = 99
    Adjusted value = 99 - 100 = -1
    Temperature =  -1 / 10 = -0.1
  Large Number
    Value stored = 1514
    Adjusted Value = 1514 - 1000 = 514
    Temperature = 514 / 10 = 51.4
    
    Value stored = 984
    Adjusted value = 984 - 1000 = -16
    Tempearture = -16 / 10 = -1.6
```

### Time Since Legionella Cycle 
Thanks to Heiko, it seems the time since the last cycle attained the 70C temperature is recorded in registers 60 and 61. The methodology is a little strange as register 60 shows a simple counter of seconds from 0 to 7199 (7200 seconds, 2 hours) and then resets to 0. Each time it resets the value in register 61 is incremented.
```
 Register 60 = 922
 Register 61 = 24
 
 Seconds since 70C attained = 922 + (24 * 7200)
 Time since 70C attained = 2d 0h 15m 22s
```

Discussion details here - https://community.home-assistant.io/t/proxon-t300-water-heater-modbus-hi-lo-word/878647/9?utm_source=chatgpt.com

