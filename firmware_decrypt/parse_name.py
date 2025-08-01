import os
import subprocess

#path = '/home/ubuntu/FirmAE/firmwares/DJI/'
path = '/home/ubuntu/FirmAE/firmwares/'
file_list = os.listdir(path)

def unpack(file_list):
    for i in file_list:
    	full_path = path+i

        if os.path.isfile(full_path) == True:
            with open(path+i, 'rb+') as f:
                dji_magic = f.read(4)
                if dji_magic != "IM*H":
                    print ("Not Match!")
                    subprocess.call(["binwalk", "-e", full_path])
                    print("BINWALK Done!!!!")

                else:
                    print("Find the IM*H : "+full_path)
                    #sig_parse(path, i)


"""
def sig_parse(path, file_list):
    for i in file_list:
        full_path = path+i
        unpack_dir = path+"_"+i+".extracted"

        if os.path.isdir(unpack_dir) != False:
            print(unpack_dir+" : This Directory is Not Found!!!")
            return
            

        else:
            unpack_list = os.listdir(unpack_dir)
            print (unpack_dir)
"""     



def main():
    unpack(file_list)
    #sig_parse(path, file_list)

main()

