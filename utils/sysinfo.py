import platform
import psutil
import subprocess
import distro


class SystemInfo:
    def __init__(self) -> None:
        self.platform = platform.system()
        self.distro_linux_name = distro.name()

    def _run_command(self, command) -> str:
        output = subprocess.check_output(command, shell=True).decode().strip()
        return output

    def _is_virtualized_linux(self) -> str:
        output = self._run_command("systemd-detect-virt")
        if output.strip() == "none":
            return "Não."
        return f"{output.strip().capitalize()}."

    @property
    def _used_ram(self) -> float:
        virtual_memory = psutil.virtual_memory()
        used_ram_gb = virtual_memory.used / (1024 ** 3)
        return float(f"{used_ram_gb:.2f}")
    
    @property
    def info_memory(self) -> str:
        if self.platform == "Linux":
            output = self._run_command("free -h")
            total_memory = output.splitlines()[1].split()
            total_memory_installed_gb = float(total_memory[1][:-2])
        return f"{self._used_ram} GB / {total_memory_installed_gb:.2f} GB | {((self._used_ram/total_memory_installed_gb)*100):.2f}%"
    
    @property
    def cpu_info(self) -> tuple:
        if self.platform == "Linux":
            output = self._run_command("lscpu")
            lines = output.split('\n')
            cpu_info = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':')
                    cpu_info[key.strip()] = value.strip()
            return (cpu_info.get('Architecture', ''), cpu_info.get('Model name', ''), cpu_info.get('CPU(s)', ''), cpu_info.get('Thread(s) per core', ''), self._is_virtualized_linux())

    @property
    def cpu_usage(self) -> str:
        cpu_usage = psutil.cpu_percent(interval=3)
        return f"{cpu_usage}%"
