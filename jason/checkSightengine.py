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
    output['scam'] = output['scam']['prob']
    output['nudity'] = output['nudity']['raw']
    output['minor'] = output['faces'][0]['attributes']['minor']
    output['sunglasses'] = output['faces'][0]['attributes']['sunglasses']
    del output['faces']
    del output['colors']
    output['offensive'] = output['offensive']['prob']
    del output['media']
    del output['text']

    return output
