import platform
from datetime import datetime
from typing import Dict
import json

import psutil
from tabulate import tabulate


def get_size(byte_count, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if byte_count < factor:
            return f"{byte_count:.2f}{unit}{suffix}"
        byte_count /= factor
    return byte_count


class _ThermalInformation:
    @classmethod
    def get_current_fan_speed(cls):
        return psutil.sensors_fans()

    @classmethod
    def get_current_sensors_temperatures(cls):
        return psutil.sensors_temperatures(fahrenheit=False)

    def get_system_information(self):
        return {
            'fanSpeed': self.get_current_fan_speed(),
            'temperature': self.get_current_sensors_temperatures()
        }

    def __repr__(self):
        return tabulate([
            ['fan_speed', self.get_current_fan_speed()],
            ['temp_speed', self.get_current_sensors_temperatures()]
        ])


class _NetworkInformation:
    def __init__(self):
        pass

    @classmethod
    def get_interface_information(cls):
        interfaces = []
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            interface = {
                'interface_name': interface_name,
                'interface_address': interface_addresses
            }
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    interface['IP Address'] = address.address
                    interface['Netmask'] = address.netmask
                    interface['Broadcast IP'] = address.broadcast
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    interface['MAC Address'] = address.address
                    interface['Netmask'] = address.netmask
                    interface['Broadcast MAC'] = address.broadcast
            interfaces.append(interface)
        return interfaces

    @classmethod
    def get_bytes_sent(cls):
        net_io = psutil.net_io_counters()
        return get_size(net_io.bytes_sent)

    @classmethod
    def get_bytes_received(cls):
        net_io = psutil.net_io_counters()
        return get_size(net_io.bytes_recv)

    def __repr__(self):
        return tabulate([
            ['Interfaces', self.get_interface_information()],
            ['Bytes Sent', self.get_bytes_sent()],
            ['Bytes Received', self.get_bytes_received()]
        ])

    def get_system_information(self):
        return {
            'sent': self.get_bytes_sent(),
            'received': self.get_bytes_received(),
            'interfaces': self.get_interface_information()
        }


class _DiskInformation:
    # Disk Information
    def __init__(self):
        self.partitions = psutil.disk_partitions()

    @classmethod
    def get_total_read(cls):
        disk_io = psutil.disk_io_counters()
        return get_size(disk_io.read_bytes)

    @classmethod
    def get_total_write(cls):
        disk_io = psutil.disk_io_counters()
        return get_size(disk_io.write_bytes)

    def get_partition_information(self):
        partitions = []
        for partition in self.partitions:
            partition_info = {
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'file_system_type': partition.fstype
            }

            try:
                partition_usage = psutil.disk_usage(partition_info['mountpoint'])
            except PermissionError:
                continue

            partition_info['total_size'] = get_size(partition_usage.total)
            partition_info['used'] = get_size(partition_usage.used)
            partition_info['free'] = get_size(partition_usage.free)
            partition_info['percentage'] = partition_usage.percent

            partitions.append(partition_info)
        return partitions

    def __repr__(self):
        return tabulate([
            ['total_write', self.get_total_write()],
            ['total_read', self.get_total_read()],
            ['partitions_information', self.get_partition_information()]
        ])

    def get_system_information(self):
        return {
            'read': self.get_total_read(),
            'write': self.get_total_write(),
            'partitions': self.get_partition_information()
        }


class _MemoryInformation:
    def __init__(self):
        self.svmem = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
        self.total_svmem = self.svmem.total
        self.total_swap = self.swap.total

    def get_available_memory(self):
        return self.svmem.available

    def get_used_memory(self):
        return self.svmem.used

    def get_percentage_memory(self):
        return self.svmem.percent

    def get_available_swap(self):
        return self.swap.free

    def get_used_swap(self):
        return self.swap.used

    def get_percentage_swap(self):
        return self.swap.percent

    def get_system_information(self):
        return {
            'totalMemory': self.total_svmem,
            'availableMemory': self.get_available_memory(),
            'usedMemory': self.get_used_memory(),
            'percentageMemory': self.get_percentage_memory(),
            'totalSwap': self.total_swap,
            'availableSwap': self.get_available_swap(),
            'usedSwap': self.get_used_swap(),
            'percentageSwap': self.get_percentage_swap()
        }

    def __repr__(self):
        return tabulate([
            ['total_memory', get_size(self.total_svmem)],
            ['available_memory', get_size(self.get_available_memory())],
            ['used_memory', get_size(self.get_used_memory())],
            ['percentage_memory', self.get_percentage_memory()],
            ['total_swap', get_size(self.total_swap)],
            ['available_swap', get_size(self.get_available_swap())],
            ['used_swap', get_size(self.get_used_swap())],
            ['percentage_swap', self.get_percentage_swap()]
        ])


class _CPUInformation:
    def __init__(self):
        self.physical_cores = psutil.cpu_count(logical=False)
        self.total_cores = psutil.cpu_count(logical=True)
        self.cpu_frequency = psutil.cpu_freq()
        self.max_frequency = self.cpu_frequency.max
        self.min_frequency = self.cpu_frequency.min

    def get_current_frequency(self):
        return self.cpu_frequency.current

    @classmethod
    def get_total_cpu_usage(cls):
        return psutil.cpu_percent()

    @classmethod
    def get_per_core_usage(cls):
        core_usages = {}
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            core_usages[f"core_{i}"] = percentage
        return core_usages

    def get_system_information(self) -> Dict:
        return {
            "physical_cores": self.physical_cores,
            "total_cores": self.total_cores,
            "cpu_frequency": self.get_current_frequency(),
            "max_frequency": self.max_frequency,
            "min_frequency": self.min_frequency,
            "per_core_usage": self.get_per_core_usage(),
            "total_core_usage": self.get_total_cpu_usage()
        }

    def __repr__(self):
        info = []
        system_info = self.get_system_information()
        for key in system_info.keys():
            info.append([key, system_info[key]])
        return tabulate(info)


class _BootInformation:
    def __init__(self):
        self.boot_time_timestamp = psutil.boot_time()
        self.boot_time_datetime = datetime.fromtimestamp(self.boot_time_timestamp)

    def get_system_information(self):
        return {
            'bootTime': self._get_timestamp()
        }

    def _get_timestamp(self):
        return self.boot_time_datetime.strftime("%d/%m/%Y %H:%M:%S")

    def __repr__(self):
        return f"Boot Time: " + self._get_timestamp()


class _SystemInformation:
    uname = platform.uname()

    def __init__(self):
        self.system = self.uname.system
        self.node_name = self.uname.node
        self.release = self.uname.release
        self.version = self.uname.version
        self.machine = self.uname.machine
        self.processor = self.uname.processor

        self._system_information_lst = [
            ["System", self.system],
            ["Node Name", self.node_name],
            ["Release", self.release],
            ["Version", self.version],
            ["Machine", self.machine],
            ["Processor", self.processor]
        ]

    def get_system_information(self):
        """
        Function to get system information for the given machine
        :return: dictionary containing:
        """
        return {
            "System:": self.system,
            "Node Name:": self.node_name,
            "Release:": self.release,
            "Version:": self.version,
            "Machine:": self.machine,
            "Processor:": self.processor
        }

    def __repr__(self):
        return tabulate(self._system_information_lst)


class SystemMonitor:

    def __init__(self):
        self.system_informant = _SystemInformation()
        self.cpu_informant = _CPUInformation()
        self.memory_informant = _MemoryInformation()
        self.disk_informant = _DiskInformation()
        self.network_informant = _NetworkInformation()
        self.thermal_informant = _ThermalInformation()
        self.boot_informant = _BootInformation()

    def __repr__(self):
        return self.system_informant.__repr__() + '\n' + \
               self.boot_informant.__repr__() + '\n' + \
               self.cpu_informant.__repr__() + '\n' + \
               self.memory_informant.__repr__() + '\n' + \
               self.disk_informant.__repr__() + '\n' + \
               self.network_informant.__repr__() + '\n' + \
               self.thermal_informant.__repr__()

    def get_system_information(self):
        return {
            'systemInformation': self.system_informant.get_system_information(),
            'cpu': self.cpu_informant.get_system_information(),
            'memory': self.memory_informant.get_system_information(),
            'disk': self.disk_informant.get_system_information(),
            'network': self.network_informant.get_system_information(),
            'thermal': self.thermal_informant.get_system_information(),
            'boot': self.boot_informant.get_system_information()
        }


if __name__ == "__main__":
    print(json.dumps(SystemMonitor().get_system_information(), indent=4))
    # print(SystemMonitor().disk_informant.get_partition_information())