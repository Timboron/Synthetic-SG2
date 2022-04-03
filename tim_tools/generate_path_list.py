path = "" # "~/Synthetic-SG2/generated/sg2-casia-cond/"
with open("../image_path_list.txt", "w") as file:

    for i in range(0, 10572):
        for seed in ["0020", "0085", "0100", "0130", "0200", "0400", "0501", "0732", "0991", "0992"]:
            file.write(path + str(i) + "/seed" + seed + ".png")
            file.write("\n")
file.close()