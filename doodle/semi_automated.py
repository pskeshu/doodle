from .manual import manual
from skimage import filters, measure, morphology


def manual_otsu(image, min_size=64):
    mask = manual(image)
    _image = mask * (image)
    thres = filters.threshold_otsu(_image)
    otsu_mask = _image > thres
    otsu_mask = morphology.remove_small_objects(otsu_mask, min_size)
    return measure.label(otsu_mask)
