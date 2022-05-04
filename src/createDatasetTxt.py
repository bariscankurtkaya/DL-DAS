import os
import glob


file_direction = "../Dataset/gece1.1/*.xml"
xml_files = glob.glob("*.xml")
png_files = glob.glob("*.png")
txt_files = glob.glob("*.txt")

def create_file_for_train(files, name):
    with open(name, 'w') as f:
        for i in range(len(files)):
            print(files[i])
            f.write("data/gece1.1/" + files[i] + "\n")


def delete_xml_files(xml_files):
    for i in range(len(xml_files)):
        os.system("rm " + xlm_files[i])

if __name__ == "__main__":
    #print(xml_files)
    #delete_xml_files(xml_files)
    
    train_count = len(txt_files) * 0.8
    train_count = round(train_count)
    create_file_for_train(txt_files[:train_count], "train.txt")
    create_file_for_train(txt_files[train_count:], "test.txt")

    print("Success" , train_count)
    
    """
    for i in range(len(png_files)):
        for j in range(len(xml_files)):
            if png_files[i][:-3] == xml_files[j][:-3]:
                png_files[i] = 0
                break

    count = 0
    for i in range(len(png_files)):
        if png_files[i] != 0:
            count += 1
            os.system("rm " + png_files[i])

    print(len(png_files), count)
    """
