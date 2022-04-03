path = "" # "~/Synthetic-SG2/generated/sg2-casia-cond/"
with open("image_path_list.txt", "w") as file:
    for i in range(0, 10572):
        for j in range (1, 16):
            file.write("{:0>6d}".format(i) + "/" + "{:0>8d}".format(j) + ".jpg")
            file.write("\n")
file.close()