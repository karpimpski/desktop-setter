"""Finds URL of the image with closest aspect ratio to desktop."""

import curses
import json
import requests
SCR = curses.initscr()
SCR_HEIGHT, SCR_WIDTH = SCR.getmaxyx()
SCREEN_RESOLUTION_RATIO = SCR_WIDTH/SCR_HEIGHT


def get_image_url():
    """Finds image with closest ratio to desktop and returns its URL."""
    imgs = sorted(_get_images(), key=_image_ratio)
    most_compatible = imgs[0]
    for img in imgs:
        if (img['data']['preview']['images'][0]['source']['width'] > SCR_WIDTH and
                img['data']['preview']['images'][0]['source']['height'] > SCR_HEIGHT):
            ratio_difference = abs(_image_ratio(img) - SCREEN_RESOLUTION_RATIO)
            if ratio_difference < abs(_image_ratio(most_compatible) - SCREEN_RESOLUTION_RATIO):
                most_compatible = img

    url = most_compatible['data']['url']

    return url


def _image_ratio(img):
    """Finds width/height ratio of given image."""
    width = img['data']['preview']['images'][0]['source']['width']
    height = img['data']['preview']['images'][0]['source']['height']
    return width/height


def _get_images():
    """Fetches a list of recent images from r/EarthPorn."""
    request_url = 'https://www.reddit.com/r/EarthPorn/top/.json?limit=20'
    result = requests.get(request_url, headers={'User-agent': 'nature-dt'})
    response = json.loads(result.text)

    if "error" in response:
        print('Error ' + str(response["error"]) + '. ' + response["message"])
        return 1
    return response["data"]["children"]
