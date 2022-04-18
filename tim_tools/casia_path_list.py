from os import listdir
path = "/home/trieber/Synthetic-SG2/generated/sg2_cond_idnet_resume"
with open("../image_path_list.txt", "w") as file:
    for i in range(0, 10572):
        images = [f for f in listdir(path + "/" + str(i))]  # "{:0>6d}".format(i))]
        for image in images:
            #file.write("{:0>6d}".format(i) + "/" + image)
            file.write(str(i) + "/" + image)
            file.write("\n")
file.close()
