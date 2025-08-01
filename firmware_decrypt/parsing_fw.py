#!/usr/bin/python3

import sys
import subprocess
import os
from ctypes import Structure, c_char, c_uint, c_ubyte

def help():
	help_text = '''DJI mavic mini firmware unpack/parse/decrypt tool
	usage: ./parseing_fw.py [-option] firmware

	you need a "binwalk", "lzma".
	And also do "git clone https://github.com/fvantienen/dji_rev" first.

	[-option]
	-h : [help] : print this page
	-d : decrypt the encrypted firmware which have a .sig format
	-u : decrypt the firmware and get the uImage file
	-i : print the firmware's file header information
	-c : clean the files

	default : get the .cpio file(Root File System) from the firmware
	'''

	print(help_text)

def decrypt(firm_name):
	print("DECRYPTING "+firm_name + "\n. . . ")
	subprocess.call(["./image.py",firm_name])
	output = firm_name[:-4] + '_' + firm_name[6:10] + '.bin'
	print("CLEAR! FILE : "+output)
	return output

def uImage(firm_name):
	print("Extracting the "+firm_name)
	subprocess.call(["binwalk", "-e", decrypt(firm_name)])
	print("BINWALK DONE!")

	output = firm_name[:-4] + '_' + firm_name[6:10] + '.bin'
	return "_"+output+".extracted"

def get_cpio(firm_name):
	dir = uImage(firm_name)
	if not os.path.isdir(dir):
		print("THERE ARE NO UIMAGE")
		return 0

	file_list = os.listdir(dir)
	check = 0
	for i in file_list:
		if i[-2:] == "7z":
			check = 1
			lzma = i
			break
	if check == 0:
		print("THERE IS NO LZMA COMPREESED DATA_1")

	check_lzma = subprocess.check_output(["file","./"+dir+"/"+lzma]).split()
	check = 0

	for i in check_lzma:
		if i == b'LZMA':
			check = 1
			break

	if check == 0:
		print("THERE IS NO LZMA COMPREESED DATA_2")
		return 0

	lzma = "./"+dir+"/"+lzma
	print("\nlzma data : " + lzma)

	subprocess.call(["mv",lzma,"./"+dir+"/uImage.lzma"])
	subprocess.call(["lzma","-d","./"+dir+"/uImage.lzma"])

	subprocess.call(["binwalk", "-e", "./"+dir+"/uImage"])

	print("\n\n    ALL DONE! The CPIO FILE (ROOT FILE SYSTEM) is in the _uImage.extracted")
	print("    PLEASE RENAME THE _uImage.extracted FOLDER BEFORE EXCUTE ./parseing_fw.py -c firmware")


def clean(firm_name):
	print("START CLEARING!")
	output = firm_name[:-4] + '_' + firm_name[6:10] + '.bin'
	subprocess.call(["rm",output])
	subprocess.call(["rm","-r","_"+output+".extracted"])
	subprocess.call(["rm","-r","_uImage.extracted"])

	print("DONE!")


class header(Structure):
    _pack_ = 1
    _fields_ = [('magic', c_char * 4), ('header_version', c_uint), ('size', c_uint), ('reserved', c_char * 4), ('header_size', c_uint), ('signature_size', c_uint), ('payload_size', c_uint), ('target_size', c_uint), ('os', c_ubyte), ('arch', c_ubyte), ('compression', c_ubyte), ('anti_version', c_ubyte), ('auth_alg', c_uint), ('auth_key', c_char * 4), ('enc_key', c_char * 4), ('scram_key', c_ubyte * 16), ('name', c_char * 32), ('type', c_uint), ('version', c_uint), ('date', c_uint), ('reserved2', c_char * 20), ('userdata', c_char * 16), ('entry', c_char * 8), ('reserved3', c_char * 4), ('chunk_num', c_uint), ('sha256_payload', c_ubyte * 32)]

    def dict_export(self):
        d = dict()
        for (varkey, vartype) in self._fields_:
            if not varkey.startswith('unk'):
                d[varkey] = getattr(self, varkey)
        return d
    def __repr__(self):
        d = self.dict_export()
        from pprint import pformat
        return pformat(d, indent=4, width=1)


def print_informatinon(file):
	print("\n    header information")
	head = header()
	file.readinto(head)
	print(head)


def main():
	if len(sys.argv) == 3:
		option = sys.argv[1]
		firm_name = sys.argv[2]
	
	elif len(sys.argv) == 2:
		firm_name = sys.argv[1]
		option = ""
	
	else:
		help()
		return 0

	if sys.argv[1] == "-h":
		help()
		return 0

	file = open(firm_name,"rb")

	if option == "-i":
		print_informatinon(file)
		return 0
	
	if option == "-d":
		decrypt(firm_name)
		return 0

	if option == "-u":
		uImage(firm_name)
		return 0

	if option == "-c":
		clean(firm_name)
		return 0

	get_cpio(firm_name)
	return 0

main()