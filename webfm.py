# Get all brains and electrode positions

import base64
import tempfile
import urllib.request
import json
import os

import imageio

def get_geometry( subject,
                  webfm_location = 'http://cerebro.neuro.jhu.edu:8080' ):

    subject_geometry = None

    webfm_geometry_url = '{0}/api/geometry/{1}'.format( webfm_location, subject )

    try:
        with urllib.request.urlopen( webfm_geometry_url ) as contents:
            contents_data = contents.read()
            subject_geometry = json.loads( contents_data.decode( 'utf-8' ) )

    except:
        print( 'Could not extract geometry for subject {0} at {1}'.format( subject, webfm_geometry_url ) )
        return None

    return subject_geometry

def get_brain( subject,
               webfm_location = 'http://cerebro.neuro.jhu.edu:8080' ):

    subject_brain = None

    webfm_image_url = '{0}/api/brain/{1}'.format( webfm_location, subject )

    try:
        with urllib.request.urlopen( webfm_image_url ) as contents:
            brain_raw_data = contents.read()
    except:
        print( 'Could not extract brain for subject {0} at {1}'.format( subject, webfm_image_url ) )
        return None

    # Identify which image format we're using
    brain_format = brain_raw_data.split( b'/.' )[1].split( b';' )[0]
    brain_data = brain_raw_data.split( b',' )[1]

    with tempfile.TemporaryDirectory() as brain_dir:
        brain_filename = 'brain_{0}.{1}'.format( subject, brain_format )
        brain_path = os.path.join( brain_dir, brain_filename )

        with open( brain_path, 'wb' ) as brain_file:
            brain_file.write( base64.decodebytes( brain_data ) )

        subject_brain = imageio.imread( brain_path )

    return subject_brain

def get_record(subject,
                task,
                webfm_location = 'http://cerebro.neuro.jhu.edu:8080'):

    webfm_record_url = '{0}/api/data/{1}/{2}'.format(webfm_location,subject,task)    
    
    numChannels = len(urllib.request.urlopen(webfm_record_url).read().split(b'{')[3].split(b'"'))-7

    channelArray=[]
    dataArray=[]
    for i in range(1,numChannels):
        if(i%2==1):
            channelArray.append(urllib.request.urlopen(webfm_record_url).read().split(b'{')[3].split(b'"')[i].decode("utf-8"))
            print(channelArray)
        elif(i%2==0):
            splitString = urllib.request.urlopen(webfm_record_url).read().split(b'{')[3].split(b'"')[i].split(b':')[1].decode("utf-8").replace('[',"")
            print(splitString)
            if(splitString[len(splitString)-2] =="}"):
                finalString = splitString.replace(']},',"").split(',')
            else:
                finalString = splitString.replace('],',"").split(',')

            results = list(map(float, finalString))
            print(results)
            dataArray.append(results)
            
    return dataArray,channelArray
    
    