# rpicamera
Exercises with Raspberry Pi libcamera package

- libcamera-hello
- libcamera-jpeg
- libcamera-still
- libcamera-vid
- libav integration with libcamera-vid
- libcamera-raw
- libcamera-detect 

## libcamera-hello

## libcamera-jpeg

## libcamera-still
Permits files to be saved in a variety of popular formats. The encoding option (-e or --encoding) must be explicitly specified since the file format is not dependent on the filetype name.

### Example
`
  $ libcamera-still -o hello.jpg -e png -n -r --metering average -v 0 --roi 0.25, 0.25, 0.75, 0.75
`
where
| Parameter | Value | Default | Notes |
|-----------|-------|---------|-------|
| -o, --output | _filename_ | none | output filename |
| -e, --encoding | _type_ | none | _type_= png, jpg, bmp, rgb, yuv420 |
| -n, --nopreview |  |  | do not show preview |
| -r, --raw | | | capture RAW data too |
| --metering | average | centre | set the metering mode (_centre_, spot, average, custom) |
| -v | 0 | 1 |  Set verbosity level, 0 is no output |
| --roi | 0.2,0,25,0.9,0.5 | 0,0,1,1 | select a crop (region of interest) from the camera <x,y,w,h> |

## libcamera-vid

## libav integration with libcamera-vid

## libcamera-raw

## libcamera-detect 

## References
[Raspberry Pi Documentation - libcamera](https://www.raspberrypi.com/documentation/computers/camera_software.html#libcamera-still)
[The Picamera2 Library](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
