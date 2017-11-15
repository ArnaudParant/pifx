# External deps
import time
import logging
import lifxlan

# Internal deps
from pifx.utils import ApiException

class Group(lifxlan.group.Group):

    def __init__(self, lan, group_name):
        self.group_name = group_name
        self.group = lan.get_devices_by_group(group_name)
        super().__init__()

    @staticmethod
    def list_group(lan):
        groups = set()
        for device in lan.get_devices():
            groups.add(device.get_group())
        return list(groups)

    @staticmethod
    def stats_group(lan):
        stats = {}
        for device in lan.get_devices():
            group = device.get_group()
            if group is None:
                group = "Unassigned"
            if group not in stats:
                stats[group] = {"devices": []}
            stats[group]["devices"].append(device)

        for group, group_stats in stats.items():
            power = 0
            for device in group_stats["devices"]:
                power += device.get_power()
            group_stats["power"] = power / len(group_stats["devices"])
        return stats

    def get_name(self):
        return self.group_name

    def get_devices_label(self):
        return [d.get_label() for d in self.group.get_device_list()]

    def get_power(self):
        devices = self.group.get_device_list()
        total = len(devices)
        return sum([d.get_power() for d in devices]) / float(total) / 65535

    def power_on(self, hard=False):
        if hard is True:
            self.power_off(wait=True)
            power = 0
        else:
            power = self.get_power()
        if power < 1:
            self.group.set_power("on")
            self.group.set_brightness(0, 0)
            self.__log("Set Power", "on")

    def power_off(self, duration=0, wait=False):
        self.set_brightness(0, duration, wait=wait)
        self.group.set_power("off")
        self.__log("Set Power", "off")

    def set_power(self, power, duration=0, wait=False, hard=False):
        if power == "on":
            self.power_on(hard=hard)
        elif power == "off":
            self.power_off(duration=duration, wait=wait)
        else:
            raise ApiException("Invalid power value: %s" % power)

    def set_color(self, color, duration=0, wait=False):
        self.power_on()
        color[0] *= 65535
        color[1] *= 65535
        color[2] *= 65535
        color[3] *= 2500 + color[3] * 6500,
        self.group.set_color(color, duration * 1000)
        self.__log("Set Color", color, duration)
        self.__wait(wait, duration)

    def set_hue(self, hue, duration=0, wait=False):
        self.power_on()
        self.group.set_hue(hue * 65535, duration * 1000)
        self.__log("Set Hue", hue, duration)
        self.__wait(wait, duration)

    def set_brightness(self, brightness, duration=0, wait=False):
        self.power_on()
        self.group.set_brightness(brightness * 65535, duration * 1000)
        self.__log("Set Brightness", brightness, duration)
        self.__wait(wait, duration)

    def set_saturation(self, saturation, duration=0, wait=False):
        self.power_on()
        self.group.set_saturation(saturation * 65535, duration * 1000)
        self.__log("Set Saturation", saturation, duration)
        self.__wait(wait, duration)

    def set_colortemp(self, colortemp, duration=0, wait=False):
        self.power_on()
        self.group.set_colortemp(2500 + colortemp * 6500, duration * 1000)
        self.__log("Set Color Temperature", colortemp, duration)
        self.__wait(wait, duration)

    def set_infrared(self, infrared_brightness, duration=0, wait=False):
        self.power_on()
        self.group.set_infrared(infrared_brightness * 65535, duration * 1000)
        self.__log("Set Color Temperature", infrared_brightness, duration)
        self.__wait(wait, duration)

################################################################################
######### Utils
################################################################################

    def __wait(self, wait, duration):
        if wait and duration > 0:
            time.sleep(duration)

    def __log(self, action, value, duration=None):
        if duration:
            if duration < 1:
                str_duration = (" in %.0fms" % (duration * 1000))
            else:
                str_duration = (" in %.1fs" % duration)
        else:
            str_duration = ""
        logging.info("Group %s: %s: %s%s" % (self.get_name(), action,
                                             str(value), str_duration))
