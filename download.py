import requests

'''获取页面页面'''
def get_response(url):
    r = requests.get(url)
    return r
