from skimage import filters, morphology, segmentation
import scipy.ndimage as ndi
import numpy as np


def otsu(image, offset=0):
    """Function that calculates Otsu's threshold for a given image
    and returns a binary image after applying the threshold.

    Parameters
    ----------
    image : (N, M) numpy array
        Image for which the threshold has to be calculated.

    offset : int or float, optional
        The offset value that will be added to the calculated threshold.

    Returns
    -------
    image : (N, M) bool numpy array
        A binary image that has been thresholded.
    """
    threshold = filters.threshold_otsu(image) + offset
    return image > threshold


def median(image, size=2):
    """Function to apply a median filter to the image.

    Parameters
    ----------
    image : (N, M) numpy array
        Image for which the median filter has to be applied.

    size : int, optional
        The size of the median filter.

    Returns
    -------
    image : (N, M) bool numpy array
        The image with median filter applied.
    """
    return ndi.median_filter(image, size)


def remove_small(image, min_size=5, connectivity=1):
    """Function to remove small connected objects from a binary image.

    Parameters
    ----------
    image : (N, M) bool numpy array
        Binary image in which small connected objects are to be removed.

    min_size : int, optional
        The minimum size (area) of an object that will be removed from the
        final image.

    connectivity : int
        The connectivity defining the neighbourhood of the object.

    Returns
    -------
    image : (N, M) bool numpy array
        A binary image without objects that are smaller than `min_size`.

    """
    out = image

    if out.dtype == bool:
        selem = ndi.generate_binary_structure(image.ndim, connectivity)
        ccs = np.zeros_like(image, dtype=np.int32)
        ndi.label(image, selem, output=ccs)
    else:
        ccs = out

    component_sizes = np.bincount(ccs.ravel())
    too_small = component_sizes < min_size
    too_small_mask = too_small[ccs]
    out[too_small_mask] = 0

    return out


def clear(image):
    """Clear objects that are touching the image boundary.

    Parameters
    ----------
    image : (N, M) bool numpy array
        Binary image where the objects touching the borders have to be
        removed.

    Returns
    -------
    image : (N, M) bool numpy array
        Binary image with the objects toucing the borders removed.
    """
    return segmentation.clear_border(image)


def fill_holes(image):
    """Fill the holes in binary, connected objects.

    Parameters
    ----------
    image : (N, M) bool numpy array
        Binary image where objects with holes have to be filled.

    Returns
    -------
    image : (N, M) bool numpy array
        Binary image with filled holes in the connected objects.

    """
    return ndi.binary_fill_holes(image)
