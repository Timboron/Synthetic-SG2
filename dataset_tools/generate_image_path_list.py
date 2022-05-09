from os import listdir
import click

@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
@click.option('--file', 'filename', required=True)
def generate_ipl(ctx: click.Context, pathname: str, filename: str):
    with open(filename + ".txt", "w") as file:
        for i in range(0, 10572):
            images = [f for f in listdir(pathname + "/" + "{:0>6d}".format(i))]
            for image in images:
                file.write("{:0>6d}".format(i) + "/" + image)
                file.write("\n")
    file.close()


if __name__ == "__main__":
    generate_ipl()