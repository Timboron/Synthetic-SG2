from os import listdir
path = "/data/fboutros/faces_webface_112x112"
with open("image_path_list.txt", "w") as file:
    for i in range(0, 10572):
        images = [f for f in listdir(path + "/" + "{:0>6d}".format(i))]
        for image in images:
            file.write("{:0>6d}".format(i) + "/" + image.split(".")[0])

file.close()