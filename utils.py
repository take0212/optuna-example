import os
import matplotlib.pyplot as plt


def make_dirs(dirpath):
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)


def add_suffix(file, suffix):
    root, ext = os.path.splitext(file)
    return root + suffix + ext


def write_image(ax, dirname, filename, suffix='_ply'):
    filename = add_suffix(filename, suffix)
    filepath = os.path.join(dirname, filename)
    ax.write_image(filepath)


def savefig(dirname, filename, suffix='_plt', dpi=100):
    filename = add_suffix(filename, suffix)
    filepath = os.path.join(dirname, filename)
    plt.savefig(filepath)
    plt.savefig(filepath, dpi=dpi)
