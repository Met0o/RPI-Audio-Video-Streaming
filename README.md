# RPI-Audio-Video-Streaming

This project enables audio and video streaming from a Raspberry Pi 4 to a web application using a USB sound card and a HQ Pi camera module.

## Prerequisites

- Raspberry Pi 4
- Waveshare USB sound card
- High-quality Pi camera module
- Python 3.9

## Dependencies

- Flask
- Flask-SocketIO
- OpenCV
- PyAudio

Install the dependencies using the following command:

```bash
sudo apt-get install portaudio19-dev
pip install Flask Flask-SocketIO opencv-python-headless pyaudio

Access the web application from a browser by navigating to http://<raspberry_pi_ip_address>:8000.
