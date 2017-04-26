doodle
======

A library to segment objects in an image in a semi-automated fashion.

As of now, the library can segment objects manually. If you are using `skimage`,
you can find a similar function in the `future` module in the developmental
version.

Semi-automated approaches to segmentation will be available soon.

Installation
------------

Using `pip`:
	
	$ pip install doodle

For the developmental version:
	
	$ git clone https://github.com/pskeshu/doodle.git
	$ pip install -e .

Example
-------

	>>> import doodle
	>>> from skimage import data, io
	>>> camera = data.camera()
	>>> seg = doodle.manual(camera)
	>>> io.imshow(seg)
	>>> io.show()
