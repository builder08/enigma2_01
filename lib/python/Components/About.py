from __future__ import print_function
import sys, os, time
import re
from sys import modules, version as pyversion
from fcntl import ioctl
from struct import pack
from socket import socket, inet_ntoa, AF_INET, SOCK_DGRAM
from time import localtime, strftime
from os import stat
from Components.SystemInfo import SystemInfo
from boxbranding import getBoxType, getMachineBuild, getImageVersion
from Tools.Directories import fileReadLine, fileReadLines
from subprocess import PIPE, Popen

MODULE_NAME = __name__.split(".")[-1]

# def getImageVersionString():
# 	return getImageVersion()

def getImageVersionString():
	try:
		if os.path.isfile('/var/lib/opkg/status'):
			st = os.stat('/var/lib/opkg/status')
		tm = time.localtime(st.st_mtime)
		if tm.tm_year >= 2018:
			return time.strftime("%H:%M:%S %d.%m.%Y", tm)
	except:
		pass
	return _("unavailable")

def getVersionString():
	return getImageVersion()


def getFlashDateString():
	try:
		# return time.strftime(_("%Y-%m-%d %H:%M:%S"), time.localtime(os.stat("/etc/version").st_ctime))
		return time.strftime(_("%Y-%m-%d %H:%M:%S"), time.localtime(os.path.getatime("/bin")))
	except:
		return _("unknown")

def getEnigmaVersionString():
	import enigma
	enigma_version = enigma.getEnigmaVersionString()
	if '-(no branch)' in enigma_version:
		enigma_version = enigma_version [:-12]
	# return enigma_version	
	return "%s.%s.%s" % (enigma_version[8:10], enigma_version[5:7], enigma_version[:4])

def getGStreamerVersionString():
	try:
		from glob import glob
		gst = [x.split("Version: ") for x in open(glob("/var/lib/opkg/info/gstreamer[0-9].[0-9].control")[0], "r") if x.startswith("Version:")][0]
		return "%s" % gst[1].split("+")[0].replace("\n","")
	except:
		return _("Not Required") if cpu.upper().startswith('HI') else _("Not Installed")

def getFFmpegVersionString():
	try:
		from glob import glob
		ffmpeg = [x.split("Version: ") for x in open(glob("/var/lib/opkg/info/ffmpeg.control")[0], "r") if x.startswith("Version:")][0]
		version = ffmpeg[1].split("-")[0].replace("\n", "")
		return "%s" % version.split("+")[0]
	except:
		return _("unknown")

def getGlibcVersion():
	process = Popen(("/lib/libc.so.6"), stdout=PIPE, stderr=PIPE, universal_newlines=True)
	stdout, stderr = process.communicate()
	if process.returncode == 0:
		for line in stdout.split("\n"):
			if line.startswith("GNU C Library"):
				data = line.split()[-1]
				if data.endswith("."):
					data = data[0:-1]
				return data
	print("[About] Get glibc version failed.")
	return _("Unknown")


def getGccVersion():
	process = Popen(("/lib/libc.so.6"), stdout=PIPE, stderr=PIPE, universal_newlines=True)
	stdout, stderr = process.communicate()
	if process.returncode == 0:
		for line in stdout.split("\n"):
			if line.startswith("Compiled by GNU CC version"):
				data = line.split()[-1]
				if data.endswith("."):
					data = data[0:-1]
				return data
	print("[About] Get gcc version failed.")
	return _("Unknown")

def getKernelVersionString():
	try:
		f = open("/proc/version", "r")
		kernelversion = f.read().split(' ', 4)[2].split('-', 2)[0]
		f.close()
		return kernelversion
	except:
		return _("unknown")

def getDVBAPI():
	if SystemInfo["OLDE2API"]:
		return _("Old")
	else:
		return _("New")

def getModelString():
	model = getBoxType()
	return model


def getChipSetString():
	if getMachineBuild() in ('dm7080', 'dm820'):
		return "7435"
	elif getMachineBuild() in ('dm520', 'dm525'):
		return "73625"
	elif getMachineBuild() in ('dm900', 'dm920', 'et13000', 'sf5008'):
		return "7252S"
	elif getMachineBuild() in ('hd51', 'vs1500', 'h7'):
		return "7251S"
	elif getMachineBuild() in ('alien5',):
		return "S905D"
	else:
		try:
			f = open('/proc/stb/info/chipset', 'r')
			chipset = f.read()
			f.close()
			return str(chipset.lower().replace('\n', '').replace('bcm', '').replace('brcm', '').replace('sti', ''))
		except IOError:
			return "unavailable"


def getCPUSpeedString():
	if getMachineBuild() in ('u41', 'u42', 'u43', 'u45'):
		return _("%s GHz") % "1,0"
	elif getMachineBuild() in ('dags72604', 'vusolo4k', 'vuultimo4k', 'vuzero4k', 'gb72604', 'vuduo4kse'):
		return _("%s GHz") % "1,5"
	elif getMachineBuild() in ('formuler1tc', 'formuler1', 'triplex', 'tiviaraplus'):
		return _("%s GHz") % "1,3"
	elif getMachineBuild() in ('dagsmv200', 'gbmv200', 'u51', 'u52', 'u53', 'u532', 'u533', 'u54', 'u55', 'u56', 'u57', 'u571', 'u5', 'u5pvr', 'h9', 'i55se', 'h9se', 'h9combose', 'h9combo', 'h10', 'h11', 'cc1', 'sf8008', 'sf8008m', 'sf8008opt', 'hd60', 'hd61', 'pulse4k', 'pulse4kmini', 'i55plus', 'ustym4kpro', 'beyonwizv2', 'viper4k', 'multibox', 'multiboxse'):
		return _("%s GHz") % "1,6"
	elif getMachineBuild() in ('vuuno4kse', 'vuuno4k', 'dm900', 'dm920', 'gb7252', 'dags7252', 'xc7439', '8100s'):
		return _("%s GHz") % "1,7"
	elif getMachineBuild() in ('alien5', 'hzero', 'h8'):
		return _("%s GHz") % "2,0"
	elif getMachineBuild() in ('vuduo4k',):
		return _("%s GHz") % "2,1"
	elif getMachineBuild() in ('hd51', 'hd52', 'sf4008', 'vs1500', 'et1x000', 'h7', 'et13000', 'sf5008', 'osmio4k', 'osmio4kplus', 'osmini4k'):
		try:
			from binascii import hexlify
			f = open('/sys/firmware/devicetree/base/cpus/cpu@0/clock-frequency', 'rb')
			clockfrequency = f.read()
			f.close()
			CPUSpeed_Int = round(int(hexlify(clockfrequency), 16) / 1000000, 1)
			if CPUSpeed_Int >= 1000:
				return _("%s GHz") % str(round(CPUSpeed_Int / 1000, 1))
			else:
				return _("%s MHz") % str(round(CPUSpeed_Int, 1))
		except:
			return _("%s GHz") % "1,7"
	else:
		try:
			file = open('/proc/cpuinfo', 'r')
			lines = file.readlines()
			for x in lines:
				splitted = x.split(': ')
				if len(splitted) > 1:
					splitted[1] = splitted[1].replace('\n', '')
					if splitted[0].startswith("cpu MHz"):
						mhz = float(splitted[1].split(' ')[0])
						if mhz and mhz >= 1000:
							mhz = _("%s GHz") % str(round(mhz / 1000, 1))
						else:
							mhz = _("%s MHz") % str(round(mhz, 1))
			file.close()
			return mhz
		except IOError:
			return "unavailable"

def getImageTypeString():
	try:
		image_type = open("/etc/issue").readlines()[-2].strip("openfix-")[:-6]
		return image_type.capitalize()
	except:
		return _("undefined")	

def getBuildDateString():
	try:
		if os.path.isfile('/etc/version'):
			version = open("/etc/version","r").read()
			return "%s.%s.%s" % (version[6:8], version[4:6], version[:4])
	except:
		pass
	return _("unknown")

def getCPUString():
	if getMachineBuild() in ('vuduo4k', 'vuduo4kse', 'osmio4k', 'osmio4kplus', 'osmini4k', 'dags72604', 'vuuno4kse', 'vuuno4k', 'vuultimo4k', 'vusolo4k', 'vuzero4k', 'hd51', 'hd52', 'sf4008', 'dm900', 'dm920', 'gb7252', 'gb72604', 'dags7252', 'vs1500', 'et1x000', 'xc7439', 'h7', '8100s', 'et13000', 'sf5008'):
		return "Broadcom"
	elif getMachineBuild() in ('dagsmv200', 'gbmv200', 'u41', 'u42', 'u43', 'u45', 'u51', 'u52', 'u53', 'u532', 'u533', 'u54', 'u55', 'u56', 'u57', 'u571', 'u5', 'u5pvr', 'h9', 'i55se', 'h9se', 'h9combose', 'h9combo', 'h10', 'h11', 'cc1', 'sf8008', 'sf8008m', 'sf8008opt', 'hd60', 'hd61', 'pulse4k', 'pulse4kmini', 'i55plus', 'ustym4kpro', 'beyonwizv2', 'viper4k', 'multibox', 'multiboxse', 'hzero', 'h8'):
		return "Hisilicon"
	elif getMachineBuild() in ('alien5',):
		return "AMlogic"
	else:
		try:
			system = "unknown"
			file = open('/proc/cpuinfo', 'r')
			lines = file.readlines()
			for x in lines:
				splitted = x.split(': ')
				if len(splitted) > 1:
					splitted[1] = splitted[1].replace('\n', '')
					if splitted[0].startswith("system type"):
						system = splitted[1].split(' ')[0]
					elif splitted[0].startswith("Processor"):
						system = splitted[1].split(' ')[0]
			file.close()
			return system
		except IOError:
			return "unavailable"

def getCPUSerial():
	with open('/proc/cpuinfo', 'r') as f:
		for line in f:
			if line[0:6] == 'Serial':
				return line[10:26]
		return "0000000000000000"
		
def getCPUArch():
	if SystemInfo["ArchIsARM64"]:
		return _("ARM64")
	elif SystemInfo["ArchIsARM"]:
		return _("ARM")
	else:
		return _("Mipsel")	
		
def getCPUInfoString():
	try:
		cpu_count = 0
		cpu_speed = 0
		processor = ""
		for line in open("/proc/cpuinfo").readlines():
			line = [x.strip() for x in line.strip().split(":")]
			if not processor and line[0] in ("system type", "model name", "Processor"):
				processor = line[1].split()[0]
			elif not cpu_speed and line[0] == "cpu MHz":
				cpu_speed = "%1.0f" % float(line[1])
			elif line[0] == "processor":
				cpu_count += 1

		if processor.startswith("ARM") and os.path.isfile("/proc/stb/info/chipset"):
			processor = "%s (%s)" % (open("/proc/stb/info/chipset").readline().strip().upper(), processor)

		if not cpu_speed:
			try:
				cpu_speed = int(open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq").read()) / 1000
			except:
				try:
					import binascii
					cpu_speed = int(int(binascii.hexlify(open('/sys/firmware/devicetree/base/cpus/cpu@0/clock-frequency', 'rb').read()), 16) / 100000000) * 100
				except:
					cpu_speed = "-"

		temperature = None
		if os.path.isfile('/proc/stb/fp/temp_sensor_avs'):
			temperature = open("/proc/stb/fp/temp_sensor_avs").readline().replace('\n', '')
		elif os.path.isfile('/proc/stb/power/avs'):
			temperature = open("/proc/stb/power/avs").readline().replace('\n', '')
		elif os.path.isfile('/proc/stb/fp/temp_sensor'):
			temperature = open("/proc/stb/fp/temp_sensor").readline().replace('\n', '')
		elif os.path.isfile('/proc/stb/sensors/temp0/value'):
			temperature = open("/proc/stb/sensors/temp0/value").readline().replace('\n', '')
		elif os.path.isfile('/proc/stb/sensors/temp/value'):
			temperature = open("/proc/stb/sensors/temp/value").readline().replace('\n', '')
		elif os.path.isfile("/sys/devices/virtual/thermal/thermal_zone0/temp"):
			try:
				temperature = int(open("/sys/devices/virtual/thermal/thermal_zone0/temp").read().strip()) / 1000
			except:
				pass
		elif os.path.isfile("/proc/hisi/msp/pm_cpu"):
			try:
				temperature = re.search('temperature = (\d+) degree', open("/proc/hisi/msp/pm_cpu").read()).group(1)
			except:
				pass
		if temperature:
			# return "%s %s MHz (%s) %s\xb0C" % (processor, cpu_speed, ngettext("%d core", "%d cores", cpu_count) % cpu_count, temperature)
			return "%s\xb0C" % (temperature)
		# return "%s %s MHz (%s)" % (processor, cpu_speed, ngettext("%d core", "%d cores", cpu_count) % cpu_count)
	except:
		return _("undefined")			

def getCpuCoresString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n', '')
				if splitted[0].startswith("processor"):
					if getMachineBuild() in ('dagsmv200', 'gbmv200', 'u51', 'u52', 'u53', 'u532', 'u533', 'u54', 'u55', 'u56', 'u57', 'u571', 'vuultimo4k', 'u5', 'u5pvr', 'h9', 'i55se', 'h9se', 'h9combose', 'h9combo', 'h10', 'h11', 'alien5', 'cc1', 'sf8008', 'sf8008m', 'sf8008opt', 'hd60', 'hd61', 'pulse4k', 'pulse4kmini', 'i55plus', 'ustym4kpro', 'beyonwizv2', 'viper4k', 'vuduo4k', 'vuduo4kse', 'multibox', 'multiboxse'):
						cores = 4
					elif getMachineBuild() in ('u41', 'u42', 'u43', 'u45'):
						cores = 1
					elif int(splitted[1]) > 0:
						cores = 2
					else:
						cores = 1
		file.close()
		return cores
	except IOError:
		return "unavailable"


def _ifinfo(sock, addr, ifname):
	iface = pack('256s', bytes(ifname[:15], 'utf-8'))
	info = ioctl(sock.fileno(), addr, iface)
	if addr == 0x8927:
		return ''.join(['%02x:' % ord(chr(char)) for char in info[18:24]])[:-1].upper()
	else:
		return inet_ntoa(info[20:24])


def getIfConfig(ifname):
	ifreq = {'ifname': ifname}
	infos = {}
	sock = socket(AF_INET, SOCK_DGRAM)
	# offsets defined in /usr/include/linux/sockios.h on linux 2.6
	infos['addr'] = 0x8915 # SIOCGIFADDR
	infos['brdaddr'] = 0x8919 # SIOCGIFBRDADDR
	infos['hwaddr'] = 0x8927 # SIOCSIFHWADDR
	infos['netmask'] = 0x891b # SIOCGIFNETMASK
	try:
		for k, v in list(infos.items()):
			ifreq[k] = _ifinfo(sock, v, ifname)
	except Exception as ex:
		print("[About] getIfConfig Ex:", ex)
		pass
	sock.close()
	return ifreq


def getIfTransferredData(ifname):
	f = open('/proc/net/dev', 'r')
	for line in f:
		if ifname in line:
			data = line.split('%s:' % ifname)[1].split()
			rx_bytes, tx_bytes = (data[0], data[8])
			f.close()
			return rx_bytes, tx_bytes


def getPythonVersionString():
	try:
		return pyversion.split(' ')[0]
	except:
		return _("unknown")


def getBoxUptime():
	upTime = fileReadLine("/proc/uptime", source=MODULE_NAME)
	if upTime is None:
		return "-"
	secs = int(upTime.split(".")[0])
	times = []
	if secs > 86400:
		days = secs // 86400
		secs = secs % 86400
		times.append(ngettext("%d day", "%d days", days) % days)
	h = secs // 3600
	m = (secs % 3600) // 60
	times.append(ngettext("%d hour", "%d hours", h) % h)
	times.append(ngettext("%d minute", "%d minutes", m) % m)
	return " ".join(times)

def getIdea():
	return _("BlackFish")

def getEmail():
	return _("blackfish.3654@gmail.com")
		
def getBrand():
	return _("octagon")			

def getDonate():
	return _("Z541154775569, R610636086219")
		
def getThanks():
	return _("gisclub.tv, opena.tv, ShadowA, moskvish")

def getopensslVersionString():
	lines = fileReadLines("/var/lib/opkg/info/openssl.control", source=MODULE_NAME)
	if lines:
		for line in lines:
			if line[0:8] == "Version:":
				return line[9:].split("+")[0]
	return _("Not Installed")


# For modules that do "from About import about"
about = modules[__name__]
