libcamera-vid -t 0 --inline --framerate 30 -o - | gst-launch-1.0 fdsrc ! h264parse ! rtph264pay ! udpsink host=192.168.1.21 port=567
