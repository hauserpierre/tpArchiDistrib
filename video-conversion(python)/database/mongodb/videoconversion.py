import logging

import boto3
from botocore.exceptions import ClientError
import time
import os
import websocket
import json
import ssl

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)


#  ffmpeg -i Game.of.Thrones.S07E07.1080p.mkv -vcodec mpeg4 -b 4000k -acodec mp2 -ab 320k converted.avi


class VideoConversion(object):
    def __init__(self, _config_):
        dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
        self.table = dynamodb.Table("video_conversion")

    def find_one(self):
        conversion = self.video_conversion_collection.find_one()
        uri = conversion['originPath']
        id = conversion['_id']
        logging.info('id = %s, URI = %s', id, uri)
        #ff = ffmpy.FFmpeg(
        #    inputs={uri: None},
        #    outputs={'converted.avi': '-y -vcodec mpeg4 -b 4000k -acodec mp2 -ab 320k'}
        #)
        #logging.info("FFMPEG = %s", ff.cmd)
        # ff.run()
        self.video_conversion_collection.update({'_id': id}, {'$set': {'targetPath': 'converted.avi'}})
        self.video_conversion_collection.update({'_id': id}, {'$set': {'tstamp': time.time()}})

        # for d in self.video_conversion_collection.find():
        #    logging.info(d)

    def convert(self, _id_, _uri_):
        converted = _uri_.replace(".mkv", "-converted.avi")
        logging.info('ID = %s, URI = %s —› %s', _id_, _uri_, converted)
        #ff = ffmpy.FFmpeg(
        #    inputs={_uri_: None},
        #    outputs={converted: '-y -vcodec mpeg4 -b 4000k -acodec mp2 -ab 320k'}
        #)
        #logging.info("FFMPEG = %s", ff.cmd)
        #ff.run()

        self.update_item(_id_, 'TERMINE')

        payload = dict()
        payload["id"] = _id_;
        payload["status"] = 0;

        json_payload = json.dumps(payload)
        logging.info("payload = %s", json_payload)

        ws = websocket.create_connection(self.url)
        #        ws = websocket.create_connection(self.url)
        ws.send(json_payload);
        ws.close()

    def update_item(self, _id_, _status_):
        try:
            response = self.table.update_item(
                Key={'uuid': _id_},
                UpdateExpression='set video_status = :status',
                ExpressionAttributeValues={':status': _status_},
                ReturnValues="TERMINE"
            )
            logging.info(response)
        except ClientError as e:
            logging.error('Error when updating item: ', e)
        else:
            logging.info('Update item status succeeded: ')
            logging.info(json.dumps(response, indent=4))
