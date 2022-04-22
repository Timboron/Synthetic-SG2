from os import listdir
path = "/data/trieber/syn_datasets/sg2cond"
with open("/data/trieber/syn_datasets/image_path_list.txt", "w") as file:
    for i in range(0, 10572):
        images = [f for f in listdir(path + "/" + "{:0>6d}".format(i))]
        for image in images:
            file.write("{:0>6d}".format(i) + "/" + image)
            file.write("\n")
file.close()
