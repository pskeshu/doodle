import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from skimage import measure


def draw_arrow(ax, posA, posB):
    arrow = ConnectionPatch(posA, posB, coordsA="data", coordsB="data", lw=1)
    return ax.add_artist(arrow)


def lineprofile(img):
    """
    Interactive line profile of an image.
    """
    def onclick(event):
        clicks.append([int(event.ydata), int(event.xdata)])

    def mouse_move(event):
        if len(clicks) == 0 or len(clicks) == 2:
            return

        if len(previous_line) == 0:
            line = draw_arrow(ax, clicks[0][::-1], [event.xdata, event.ydata])
            previous_line.append(line)

        if len(previous_line) == 1:
            last_arrow = previous_line.pop()
            last_arrow.remove()
            fig.canvas.draw_idle()

            line = draw_arrow(ax, clicks[0][::-1], [event.xdata, event.ydata])
            fig.canvas.draw_idle()

            previous_line.append(line)

    clicks = []
    currentline = []
    previous_line = []

    fig, ax = plt.subplots()

    ax.imshow(img)

    cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
    cid_hover = fig.canvas.mpl_connect('motion_notify_event', mouse_move)

    plt.show()

    return measure.profile_line(img, clicks[0], clicks[1]), clicks
