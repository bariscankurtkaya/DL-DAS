import os
import glob

xml_files = glob.glob("../Dataset/gece1.1/*.xml")
png_files = glob.glob("../Dataset/gece1.1/*.png")

if __name__ == "__main__":
    print(xml_files)
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
