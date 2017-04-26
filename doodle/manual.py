"""Copyright (C) 2011, the scikit-image team All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
    Neither the name of skimage nor the names of its contributors may be used
        to endorse or promote products derived from this software without
        specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED 
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from functools import reduce
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from skimage.draw import polygon


LEFT_CLICK = 1
RIGHT_CLICK = 3

# Borrowed from skimage.future


def _mask_from_vertices(vertices, shape, label):
    mask = np.zeros(shape, dtype=int)
    pr = [y for x, y in vertices]
    pc = [x for x, y in vertices]
    rr, cc = polygon(pr, pc, shape)
    mask[rr, cc] = label
    return mask


def _draw_polygon(ax, vertices, alpha=0.4):
    polygon = Polygon(vertices, closed=True)
    p = PatchCollection([polygon], match_original=True, alpha=alpha)
    polygon_object = ax.add_collection(p)
    plt.draw()
    return polygon_object


def manual(image, alpha=0.4, return_all=False):
    """Return a label image based on freeform selections made with the mouse.

    Parameters
    ----------
    image : (M, N[, 3]) array
        Grayscale or RGB image.

    alpha : float, optional
        Transparency value for polygons drawn over the image.

    return_all : bool, optional
        If True, an array containing each separate polygon drawn is returned.
        (The polygons may overlap.) If False (default), latter polygons
        "overwrite" earlier ones where they overlap.

    Returns
    -------
    labels : array of int, shape ([Q, ]M, N)
        The segmented regions. If mode is `'separate'`, the leading dimension
        of the array corresponds to the number of regions that the user drew.

    Notes
    -----
    Press and hold the left mouse button to draw around each object.

    Examples
    --------
    >>> from skimage import data, future, io
    >>> camera = data.camera()
    >>> mask = future.manual_lasso_segmentation(camera)
    >>> io.imshow(mask)
    >>> io.show()
    """
    list_of_vertex_lists = []
    polygons_drawn = []

    if image.ndim not in (2, 3):
        raise ValueError('Only 2D grayscale or RGB images are supported.')

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.imshow(image, cmap="gray")
    ax.set_axis_off()

    def _undo(*args, **kwargs):
        if list_of_vertex_lists:
            list_of_vertex_lists.pop()
            # Remove last polygon from list of polygons...
            last_poly = polygons_drawn.pop()
            # ... then from the plot
            last_poly.remove()
            fig.canvas.draw_idle()

    undo_pos = fig.add_axes([0.85, 0.05, 0.075, 0.075])
    undo_button = matplotlib.widgets.Button(undo_pos, u'\u27F2')
    undo_button.on_clicked(_undo)

    def _on_lasso_selection(vertices):
        if len(vertices) < 3:
            return
        list_of_vertex_lists.append(vertices)
        polygon_object = _draw_polygon(ax, vertices, alpha=alpha)
        polygons_drawn.append(polygon_object)
        plt.draw()

    lasso = matplotlib.widgets.LassoSelector(ax, _on_lasso_selection)

    plt.show(block=True)

    labels = (_mask_from_vertices(vertices, image.shape[:2], i)
              for i, vertices in enumerate(list_of_vertex_lists, start=1))
    if return_all:
        return np.stack(labels)
    else:
        return reduce(np.maximum, labels, np.broadcast_to(0, image.shape[:2]))
