# import base64
# import tempfile
import urllib.request
# import json
# import os
import argparse

# import imageio


def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument( 'subject', default = 'PY17N009' )
    parser.add_argument( 'task', default = 'FingerMovements_Day1_all' )

    return parser





def main():

    args = get_parser().parse_args()

    webfm_record_url = '{0}/api/data/{1}/{2}'.format('http://cerebro.neuro.jhu.edu:8080',args.subject,args.task)

    raw_data = urllib.request.urlopen(webfm_record_url).read()

    print(raw_data)

    return 0


if __name__ == '__main__':
    main()
