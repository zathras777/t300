#!/usr/bin/env python3

import minimalmodbus
import json

# Each setpoint we are interested in is listed below with a list containing
#  - register number
#  - code to use for retrieval
#  - type of variable FLOAT, INT, IDX, BOOL
#  - number of decimals in the number
#  - offset to apply or the dict of index values
setpoints:dict = {
    "A": [2, 3, "BOOL"],
    "B": [79, 4, "FLOAT", 1],
    "C": [1, 3, "BOOL"],
    "D01": [3, 3, "FLOAT", 1],
    "D02": [6, 3, "IDX", {0: "German", 1: "English"}],
    "D03": [9, 3, "INT"],
    "D04": [25, 3, "BOOL"],
    "D05": [10, 3, "BOOL"],
    "D07": [11, 3, "INT", -100],
    "D08": [12, 3, "BOOL"],
    "E14": [38, 4, "INT"],
    "E18": [22, 4, "INT"],
    "F01": [50, 3, "INT"],
    "F02": [24, 3, "INT"],
    "F03": [26, 3, "FLOAT", 1, -100],
    "F04": [27, 3, "BOOL"],
    "F05": [28, 3, "FLOAT", 1],
    "F06": [29, 3, "FLOAT", 1],
    "F07": [30, 3, "FLOAT", 1],
    "F08": [31, 3, "FLOAT", 1],
    "F09": [33, 3, "INT"],
    "F10": [34, 3, "INT"],
    "F11": [35, 3, "FLOAT", 1],
    "F12": [52, 3, "FLOAT", 1],
    "F13": [65, 3, "FLOAT", 1],
    "F14": [36, 3, "INT"],
    "F15": [37, 3, "IDX", {0: 9600, 1: 19200}],
    "F16": [38, 3, "IDX", {0: 'None', 1: 'Even', 2: 'Odd'}],
    "F17": [39, 3, "BOOL"],
    "F18": [81, 3, "BOOL"],
    "F19": [51, 3, "INT"],
    "F22": [88, 3, "IDX", {0: 'Off', 1: 'PV', 2: 'SG'}],
    "F23": [89, 3, "FLOAT", 1],
    "F24": [90, 3, "FLOAT", 1],
    "F25": [91, 3, "INT"],
    "F26": [92, 3, "BOOL"],
    "F27": [4, 3, "INT"],
    "F28": [5, 3, "INT"],
    "P14": [29, 4, "FLOAT", 1, -100],
    "P19": [19, 4, "FLOAT", 1],
    "R02": [24, 4, "BOOL"],
    "R03": [25, 4, "BOOL"],
    "R04": [26, 4, "BOOL"],
    "R05": [27, 4, "BOOL"],
    "R06": [28, 4, "BOOL"],
    "S06": [65, 4, "INT"],
    "T05": [11, 4, "FLOAT", 1, -100],
    "T06": [12, 4, "FLOAT", 1, -100],
    "T09": [17, 4, "FLOAT", 1, -100],
    "T11": [16, 4, "FLOAT", 1, -100],
    "T13": [15, 4, "FLOAT", 1, -100],
    "T14": [29, 4, "FLOAT", 1, -100],
    "T20": [13, 4, "FLOAT", 1, -100],
    "T21": [14, 4, "FLOAT", 1, -100],
}

setpoint_descriptions:dict = {
    "A": "Operation",
    "B": "Target Temperature",
    "C": "Heat rod/Boost",
    "D01": "Temperature Heat Rod",
    "D02": "Language",
    "D03": "Display Standby",
    "D04": "Legionella Function",
    "D05": "PV Function",
    "D07": "Heat rod on at temperature",
    "D08": "Only heat rod, no Heat Pump",
    "E14": "Fan Speed",
    "E18": "E-Valve",
    "F01": "Fan speed operation",
    "F02": "Filter change interval",
    "F03": "Cold operation temperature",
    "F04": "Auxillary function",
    "F05": "Floor heating enable temperature",
    "F06": "Floor heating setpoint",
    "F07": "Aux hysteresis",
    "F08": "Maximum temperature",
    "F09": "Defrosting start temperature",
    "F10": "Defrosting start temperature, 80%",
    "F11": "Defrosting stop",
    "F12": "Delta T Mid T Low",
    "F13": "Compressor off hysteresis",
    "F14": "ModBus Unit ID",
    "F15": "ModBus Baud Rate",
    "F16": "ModBus Parity",
    "F17": "Modbus Write Enabled",
    "F18": "USB Enabled",
    "F19": "Display Contrast",
    "F20": "Default Settings",
    "F21": "Service Mode",
    "F22": "PV Mode",
    "F23": "PV Heat Rod Voltage",
    "F24": "PV WP",
    "F25": "PV WP Time",
    "F26": "Enable Fan Speed 1 and 2",
    "F27": "Fan Speed 1",
    "F28": "Fan Speed 2",
    "P14": "E-Valve",
    "P19": "E-Valve",
    "R02": "Compressor",
    "R03": "Supplemental P",
    "R04": "Heat E",
    "R05": "Fan",
    "R06": "Defrost",
    "S06": "Defrost",
    "T05": "Temperature Before Evaporation",
    "T06": "Evaporation Temperature",
    "T09": "AUX Temperature",
    "T11": "Suction Temperature",
    "T13": "Compressor Temperature",
    "T14": "E-Valve Temperature",
    "T20": "Low Tank Temperature",
    "T21": "Mid Tank Temrpertaure",
}

setpoint_units:dict = {
    "B": "C",
    "D01": "C",
    "D03": "Mins",
    "D07": "C",
    "E14": "%",
    "F01": "%",
    "F02": "Months",
    "F03": "C",
    "F05": "C",
    "F06": "C",
    "F08": "C",
    "F09": "Pa",
    "F10": "Pa",
    "F23": "V",
    "F24": "V",
    "F25": "mins",
    "F27": "%",
    "F28": "%",
    "P14": "B",
    "P19": "P",
}

class RegisterRange:
    def __init__(self, start:int, code:int, key:str):
        self.start:int = start
        self.stop:int = start
        self.code:int = code
        self.keys:list = [key]

    def __repr__(self) -> str:
        return f"RegisterRange: {self.start} - {self.stop} : {', '.join(self.keys)}"

    @property
    def register_count(self) -> int:
        return self.stop - self.start + 1

    def add_or_stop(self, reg:int, code:int, key: str) -> bool:
        if reg != self.stop + 1 or code != self.code:
            return False
        self.stop = reg
        self.keys.append(key)
        return True

    def get_values(self, instrument:minimalmodbus.Instrument) -> list:
        regs = instrument.read_registers(self.start, self.register_count, self.code)
        return list(zip(self.keys, regs))


class T300:
    def __init__(self, dev_name: str):
        self.instrument = minimalmodbus.Instrument(dev_name, 20)
        self.instrument.serial.baudrate = 19200
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 0.05
        self.values = {}
        self.ranges = []
        self.build_ranges()
        self.update_values()

    def build_ranges(self):
        r = None
        for reg in sorted(setpoints.items(), key=lambda kv: (kv[1][0], kv[1][1])):
            if r is None:
                r = RegisterRange(reg[1][0], reg[1][1], reg[0])
                continue
            if r.add_or_stop(reg[1][0], reg[1][1], reg[0]):
                continue
            self.ranges.append(r)
            r = RegisterRange(reg[1][0], reg[1][1], reg[0])
        if r is not None:
            self.ranges.append(r)

    def update_values(self):
        for rr in self.ranges:
            raw = rr.get_values(self.instrument)
            for (id, raw_val) in raw:
                reg_info = setpoints[id]
                if reg_info[2] == "FLOAT":
                    raw_val /= reg_info[3] * 10
                    if len(reg_info) > 4:
                        raw_val += reg_info[4]
                elif reg_info[2] == "INT" and len(reg_info) > 3:
                    raw_val += reg_info[3]
                elif reg_info[2] == "BOOL":
                    raw_val = "On" if raw_val == 1 else "Off"
                elif reg_info[2] == "IDX":
                    raw_val = reg_info[3][raw_val]
                self.values[id] = raw_val

    def get_time(self) -> dict:
        regs = self.instrument.read_registers(200, 7)
        tm = {}
        tm['Hour'] = regs[0]
        tm['Mins'] = regs[1]
        tm['Weekday'] = {1: 'Monday', 2: 'Tuesday', 3: 'Weds', 4: 'Thurs', 5: 'Fri', 6: 'Sat', 7: 'Sun'}[regs[2]]
        tm['Day'] = regs[3]
        tm['Month'] = regs[4]
        tm['Year'] = 2000 + regs[5]
        tm['Format'] = {0: "12 Hour", 1: "24 Hour"}[regs[6]]
        return tm

    def dump(self):
        self.update_values()
        tm = self.get_time()
        print("T-300 Information:")
        print(f"  Date/Time Reported:  {tm['Weekday']} {tm['Day']}/{tm['Month']}/{tm['Year']} @ {tm['Hour']}:{tm['Mins']:02d} ")
        print("  Setpoints:")
        prev = ''
        for key in sorted(self.values):
            if prev != '' and key[0] != prev:
                print()
            desc = setpoint_descriptions.get(key, "")
            units = setpoint_units.get(key, "")
            print(f"    {key: >3}  {desc: <35}  {self.values[key]} {units}")
            prev = key[0]

    def as_json(self) -> bytes:
        return json.dumps(self.values).encode()

    @classmethod
    def dump_registers(__cls__):
        """ Used to dump the settings data into a format suitable for
            generation of the PDF.
        """
        regs = {3: {}, 4: {}}
        for k,v in setpoints.items():
            offs = 3 if v[2] != "FLOAT" else 4
            regs[v[1]][v[0]] = [k, setpoint_descriptions[k], v[offs:]]

        print("Register;Access;Setpoint;Description;Additional Information")
        for code in sorted(regs.keys()):
            for reg in sorted(regs[code].keys()):
                print(f"{reg};{code};{regs[code][reg][0]};{regs[code][reg][1]};{regs[code][reg][2]}")


# Included for development only.
if __name__ == '__main__':
    T300.dump_registers()

    t = T300("/dev/ttyUSB0")
    t.dump()
