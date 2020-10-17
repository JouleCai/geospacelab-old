import matplotlib
import matplotlib.pyplot as plt


def set_figsize(size=None, unit='centimeters', fig=None):
    if fig is None:
        fig = plt.gcf()
    if unit == 'centimeters':
        size[0] = size[0] / 2.54
        size[1] = size[1] / 2.54
    fig.set_size_inches(size[0], size[1], forward=True)
    return


def move_figure(pos, fig=None):
    """Move figure's upper left corner to pixel (x, y)"""
    x = pos[0]
    y = pos[1]
    if fig is None:
        fig = plt.gcf()
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        fig.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        fig.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        fig.canvas.manager.window.move(x, y)


if __name__ == "__main__":
    myfig = plt.figure()
    move_figure((500, 50))
    set_figsize([15, 15])
    plt.show()