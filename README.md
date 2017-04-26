doodle
======

A library to segment objects in an image in a semi-automated fashion.

Installation
------------

Using pip::
	
	$ pip install doodle

For the developmental version::
	
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
