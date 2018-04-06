import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, MultiCursor


def _make_2d(images, mode="max"):
    if images.ndim is 3:
        if mode is "max":
            images = np.max(images, axis=0)
        if mode is "min":
            images = np.min(images, axis=0)
        if mode is "mean":
            images = np.mean(images, axis=0)
        if mode is "median":
            images = np.median(images, axis=0)
    images = np.squeeze(images)
    return images


def dd(image, cmap=plt.cm.viridis, clim=[None, None], hold=False):
    """Visualize two-dimensional images.

    Parameters
    ----------
    image : (M, N) numpy array
        The image or any 2D array that is to be visualized.

    cmap : str or class, optional
        The colormap that will be applied to grayscale images. This is viridis
        by default.

    clim : list, optional
        List of two elements that defines the lower and upper bound for
        contrast enhancement.

    hold : bool, optional
        * If `True`, the image will not be displayed. This is useful when one
            needs to plot on top of the images - a scatter plot, for instance.
            This returns the `fig` object.

        * If `False`, the image will be displayed after calling this function.
            This is the default behaviour.

    Returns
    -------
        fig : if `hold` is True: `matplotlib` figure.
            Figure object of `matplotlib`.

    """
    if image.ndim is not 2:
        raise ValueError("Not a 2D image")

    fig, ax = plt.subplots()
    ax.imshow(image, clim=clim, cmap=cmap)
    ax.axis('off')
    if hold:
        return fig
    else:
        plt.show()
        plt.close()


def ddd(images):
    """Visualize three-dimensional images.

    Parameters
    ----------
    image : (T, M, N) numpy array
        The image or any 3D array that is to be visualized.
    """
    def _update_image(num):
        num = int(num)
        image = np.squeeze(images[num:num+1])
        image_ax.set_data(image)
        fig.canvas.draw_idle()

    if images.ndim is not 3:
        raise ValueError("Not a 3D image.")

    Z = images.shape[0]

    fig, ax = plt.subplots()
    image_ax = ax.imshow(np.squeeze(images[0]), cmap=plt.cm.gray)
    ax.axis("off")

    slider_ax = plt.axes([0.19, 0.05, 0.65, 0.03],
                         facecolor="lightgoldenrodyellow")
    image_slider = Slider(slider_ax, "Z", 0, Z-1,
                          valfmt='%d', valinit=0)
    image_slider.on_changed(_update_image)
    plt.show()


def side(image1, image2):
    """Side by side comparision of images with multiple cursors. Useful to
    compare images side-by-side.

    Parameters
    ----------
    image1 : (N, M) numpy array
        Image on the left.

    image2 : (N, M) numpy array
        Image on the right.
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.imshow(image1, cmap="jet", clim=[0.1, 0.2])

    ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)
    ax2.imshow(image2, cmap="jet")

    multi = MultiCursor(fig.canvas, (ax1, ax2), color='r', lw=1, horizOn=True)
    ax1.axis('off')
    ax2.axis('off')
    plt.tight_layout()
    plt.show()
