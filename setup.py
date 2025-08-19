from setuptools import setup

setup(name='doodle',
      version='0.1',
      description='A library to segment objects in an image in a semi-automated fashion.',
      url='https://github.com/pskeshu/doodle',
      author='Kesavan Subburam',
      author_email='pskesavan@tifrh.res.in',
      license='MIT',
      packages=['doodle'],
      install_requires=['numpy>=1.13.3',
                        'scikit-image>=0.13.0', 
                        'matplotlib>=2.0.0'],
      zip_safe=False)
