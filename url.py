from pybloom import BloomFilter


# 管理url列表
class UrlManager(object):
    def __init__(self):
        self.urls = []
        self.url_bloom_filter = BloomFilter(capacity=500000, error_rate=0.001)

    def add_url(self, url):
        # if url not in self.url_bloom_filter:
        self.urls.append(url)
            # self.url_bloom_filter.add(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    def is_empty(self):
        return len(self.urls) == 0

    def get_url(self):
        return self.urls.pop(0)

    def get_len(self):
        return len(self.urls)

    def is_viewed(self, url):
        return url in self.url_bloom_filter

    def add_viewed(self, url):
        self.url_bloom_filter.add(url)