# three types of workout

# 1 time based
# max reps
# rep count

# the second two wait for the user to hit space before continuing, but the first will just tell you to stop

# default times for interval and rest are set in the config, but can also be overridden in each workout item

# need:
# text to speech that tells you what is going on
# open a new window with text updates in large font

import json

import time

from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

import sys

import os

import hashlib
import subprocess



class Workout:

    def __init__(self, config_name):

        with open(config_name) as file:
            self.config_data = json.load(file)

        self.config_name = config_name
    
        return 
    
    
    @staticmethod
    def print_speak(text, pause = False):

        hash = hashlib.sha256(text.encode()).hexdigest()
        fname = f'temp/output_{hash}.mp3'

        if not os.path.exists(fname):
            tts = gTTS(text=text, lang='en',tld = 'com.au')
            tts.save(fname)

        print(text)

        if pause:
            os.system(f'afplay {fname}')
        else:
            process = subprocess.Popen(['afplay',fname])

        return 
    
    @staticmethod
    def countdown(t):

        # wait until there are three seconds left
        time.sleep(t-3)

        for i in range(3):
            Workout.print_speak(f'{3-i}')
            time.sleep(1)

    
    def run_workout(self):


        print(f"Starting Workout {self.config_data['workout_name']}")

        for i in range(self.config_data['sets']):
            self.print_speak(f'Start Set {i+1}', True)

            for exercise in self.config_data['run_sheet']:
                self.print_speak(exercise['name'])

                if 'wait' in exercise.keys() and exercise['wait']:
                    # await spacebar
                    input('press ENTER when done ...')
                    
                elif 'interval' in exercise.keys():
                    self.countdown(exercise['interval'])
                else:
                    self.countdown(self.config_data['interval'])

                self.print_speak('Rest')
                if 'rest' in exercise.keys():
                    self.countdown(exercise['rest'])
                else:
                    self.countdown(self.config_data['rest'])
            
            if 'cooldown' in self.config_data.keys() and (i+1 != self.config_data['sets']):
                self.print_speak('Cool Down')
                self.countdown(self.config_data['cooldown'])
        
        self.print_speak('Workout Over! Good job!')



        return 
    


            
if __name__ == '__main__':


    wo = Workout(config_name = sys.argv[1])
    wo.run_workout()
                


            
        



