from sightengine.client import SightengineClient
import requests
import os

def check_sightengine_properties(path):
    """
    Check some image properties offered by the sigthengine API
    (https://sightengine.com/) including:
    - Nudity Detection
    - Weapons, Alcohol, Drug detection
    - Offensive Signs an Gesture detection
    - Minors detection
    - Image Quality detection
    - Sunglasses detection
    """

    client = SightengineClient('1519637001','knEJCk3vyKorBydqMPek')
    output = client.check('nudity','wad','properties','offensive','scam','text-content','face-attributes','text').set_file(os.path.abspath(path))
    
    # Adjust the dictionary to our requirements
    del output['status']
    del output['request']
    del output['colors']
    del output['media']
    del output['text']

    # 0 = Low, 1 = High
    output['scam'] = 1 if output['scam']['prob'] > 0.75 else 0
    output['nudity'] = 1 if output['nudity']['raw'] > 0.85 else 0
    output['minor'] = 1 if output['faces'][0]['attributes']['minor'] > 0.75 else 0
    output['sunglasses'] = 1 if output['faces'][0]['attributes']['sunglasses'] > 0.75 else 0
    output['offensive'] = 1 if output['offensive']['prob'] > 0.75 else 0
    output['sharpness'] = 1 if output['sharpness'] > 0.75 else 0
    output['weapon'] = 1 if output['weapon'] > 0.75 else 0
    output['alcohol'] = 1 if output['alcohol'] > 0.75 else 0
    output['drugs'] = 1 if output['drugs'] > 0.75 else 0

    # 0 = OK, 1 = High, 2 = Low
    output['contrast'] = 1 if output['contrast'] > 0.85 else 2 if output['contrast'] < 0.15 else 0
    output['brightness'] = 1 if output['brightness'] > 0.85 else 2 if output['brightness'] < 0.2 else 0
    del output['faces']
    
    return output

