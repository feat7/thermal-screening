# Thermal Screening using Computer Vision

This repository is code for the blog:

# Dataset

The video data is taken from [http://csr.bu.edu/BU-TIV/BUTIV.html](http://csr.bu.edu/BU-TIV/BUTIV.html)

# Installation

1. Create new virtual environment and activate it.

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run demo

```bash
python thermal_screening.py
```

# Command line options

```
usage: thermal_screening.py [-h] [-t THRESHOLD_TEMPERATURE]
                            [-b BINARY_THRESHOLD] [-c CONVERSION_FACTOR]
                            [-a MIN_AREA] [-i INPUT_VIDEO] [-o OUTPUT_VIDEO]
                            [-f FPS]

Thermal screening demo by Codevector Labs (support [at] codevector [dot] in).

optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLD_TEMPERATURE, --threshold_temperature THRESHOLD_TEMPERATURE
                        Threshold temperature in Farenheit (float)
  -b BINARY_THRESHOLD, --binary_threshold BINARY_THRESHOLD
                        Threshold pixel value for binary threshold (between
                        0-255)
  -c CONVERSION_FACTOR, --conversion_factor CONVERSION_FACTOR
                        Conversion factor to convert pixel value to
                        temperature (float)
  -a MIN_AREA, --min_area MIN_AREA
                        Minimum area of the rectangle to consider for further
                        porcessing (int)
  -i INPUT_VIDEO, --input_video INPUT_VIDEO
                        Input video file path (string)
  -o OUTPUT_VIDEO, --output_video OUTPUT_VIDEO
                        Output video file path (string)
  -f FPS, --fps FPS     FPS of output video (int)
```

# License

`Apache 2.0`

Check LICENSE File for more details.
