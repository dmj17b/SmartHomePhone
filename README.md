# SmartHomePhone
Apps and software to run on a raspberry pi built into an old landline phone.

No idea why the app scaling works differently on the pi, but just roll with it.
Will probably always need to adjust/test on the pi before the scaling is perfect but window should get you close.

Main file to run is app.py. Everything else is development or packaging code for the app (in applib)

# Python packages to install:

pip install tkinter ttkbootstrap
pip install openai
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install pyaudio setuptools SpeechRecognition

# OpenAI stuff:
Need to put in your own key. Include nothing but the key in a file named "openaikey.txt"