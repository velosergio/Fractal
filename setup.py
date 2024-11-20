from setuptools import setup

setup(
    name="fractal",
    version="1.0.0",
    py_modules=['fractal'],
    install_requires=[
        'pygame==2.5.2',
        'opencv-python==4.9.0.80',
        'mediapipe==0.10.11',
        'numpy<2.0.0'
    ],
) 