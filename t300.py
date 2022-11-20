#!/usr/bin/env python3

import minimalmodbus

# Each setpoint we are interested in is listed below with a list containing
#  - register number
#  - code to use for retrieval
#  - type of variable FLOAT, INT, IDX, BOOL
#  - number of decimals in the number
#  - offset to apply or the dict of index values
setpoints:dict = {
    "D01": [3, 3, "FLOAT", 1],
    "D07": [11, 3, "INT", -100],
    "F03": [26, 3, "FLOAT", 1, -100],
    "F04": [27, 3, "BOOL"],
    "F05": [28, 3, "FLOAT", 1],
    "F06": [29, 3, "FLOAT", 1],
    "F07": [30, 3, "FLOAT", 1],
    "F08": [31, 3, "FLOAT", 1],
    "F09": [33, 3, "INT"],
    "F14": [36, 3, "INT"],
    "F15": [37, 3, "IDX", {0: 9600, 1: 19200}],
    "F16": [38, 3, "IDX", {0: 'None', 1: 'Even', 2: 'Odd'}],
    "F27": [4, 3, "INT"],
    "F28": [5, 3, "INT"],
}

setpoint_descriptions:dict = {
    "F14": "ModBus Unit ID",
    "F15": "ModBus Baud Rate",
    "F16": "ModBus Parity",
}

setpoint_units:dict = {
    "D01": "C",
    "D07": "C",
    "F03": "C",
    "F05": "C",
    "F06": "C",
    "F08": "C",
    "F09": "Pa",
    "F10": "Pa",
    "F27": "%",
    "F28": "%"
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


class HPW300:
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
        print(self.ranges)

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
        print("HPW 300 Information:")
        print(f"  Date/Time Reported:  {tm['Weekday']} {tm['Day']}/{tm['Month']}/{tm['Year']} @ {tm['Hour']}:{tm['Mins']} ")
        print("  Setpoints:")
        prev = ''
        for key in sorted(self.values):
            if prev != '' and key[0] != prev:
                print()
            desc = setpoint_descriptions.get(key, "")
            units = setpoint_units.get(key, "")
            print(f"    {key: >3}  {desc: <30}  {self.values[key]} {units}")
            prev = key[0]

h = HPW300("/dev/ttyUSB0")
h.dump()
