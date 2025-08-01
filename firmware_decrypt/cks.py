import os
import subprocess

#path = '/home/sane/ADD/FirmAE/firmwares/DJI/'
#path = '/home/sane/ADD/FirmAE/firmwares/'
path = './V02.00.0810_P4_dji_system/' # 디렉토리 경로 환경에 맞게 설정 필요
file_list = os.listdir(path)

# decryption option dictionary
options = {
    b"PRAK" : "PRAK-2017-01",
    b"SLAK" : "SLAK",
    b"GFAK" : "GFAK",
    b"RRAK" : "RRAK",
    b"SLEK" : "SLEK",
    b"UFIE" : "UFIE-2021-06",
    b"TRIE" : "TRIE-2021-06",
    b"PUEK" : "PUEK-2017-07",
    b"SAAK" : "SAAK",
    b"DRAK" : "DRAK",
    b"RUEK" : "RUEK",
    b"RIEK" : "RIEK-2017-01",
    b"RREK" : "RREK-2017-01",
    b"IAEK" : "RIEK-2017-01"
}

def unpack(file_list):
    output_file_list = list()
    for i in file_list:
        full_path = path+i
        if i.endswith(".sig"):
            if os.path.isfile(full_path) == True:
                with open(full_path, 'rb+') as f:
                    dji_magic = f.read(4)
                    if dji_magic == b"IM*H":
                        # for debugging
                        #print("Find the IM*H : " + full_path)
                        output_file_list.append(full_path)
                    # for debugging
                    #else:
                        #print ("Not Match!")
        # for debugging
        #else:
            #print(i+"is not ended with .sig")
    return output_file_list

def check_enc_method(file_list):
    output_list = list()
    for file in file_list:
        with open(file, 'rb+') as f:
            full_binary = f.read(48)
            enc_method = full_binary[40:48] # left = full_binary[40:44], right = full_binary[44:48]
            output_list.append(enc_method)
    return output_list

def check_bin(filename):
    new_file_list = os.listdir(path)
    newfilename = filename[0:len(filename)-4] + ".bin"
    if newfilename in new_file_list:
        return 1
    else:
        return 2

def decryption_sig(file, option):
    # output(1): decryption clear, output(2): decryption failed
    # input: filepath, decrypt option
    option1 = options[option[0:4]]
    option2 = options[option[4:8]]
    decryptor = ["python", "./dji-firmware-tools/dji_imah_fwsig.py", "-vv", "-k", option1, "-k", option2, "-u", "-i ", "\"" + file + "\""]
    #print(decryptor)
    subprocess.run(decryptor) # 문제 발생 시 Python 3.5 이상의 버전 설치(개발 환경: Windows Python 3.10.7 64-bit)
    is_clear = check_bin(file)
    if is_clear == 1:
        print(file + " is successfully decrypted")
    elif is_clear == 2:
        print(file + " is not decrypted")
    return is_clear


def main():
    sig_file_list = unpack(file_list)
    enc_chek_list = check_enc_method(sig_file_list)

    # for debugging
    #for i in range(len(sig_file_list)):
    #    print(sig_file_list[i]) # 파일 전체목록 출력(.sig 확장자가 아닌 파일은 제외)
    #    print(enc_chek_list[i]) # 각 파일의 암호화 방식 출력(.sig 확장자가 아닌 파일은 제외)

    for fileindex in range(len(sig_file_list)):
        filename = sig_file_list[fileindex]
        option = enc_chek_list[fileindex]
        result = decryption_sig(filename, option)
        
        with open("dec_log.txt", "a") as dl:
            if result == 1:
                dl.write(filename + " is successfully decrypted\n")
            elif result == 2:
                dl.write(filename + " is not decrypted\n")
            else:
                print("Unknown error occured while decrypting " + filename)
                exit(1)
            dl.close()

main()