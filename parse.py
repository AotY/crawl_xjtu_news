from bs4 import BeautifulSoup
from urllib.request import urljoin
import jieba
import re

from common import SCHOOL_NAMES, KEYWORDS
from download import get_response


def init_jieba():
    jieba.add_word('十九大')
    jieba.add_word('党建')
    jieba.add_word('人才培养')
    jieba.add_word('双一流')

init_jieba()

number_re = re.compile('\d+')

'''解析列表'''
def parse_content_list(response, url_manager):

    content_list_result = {}
    soup = BeautifulSoup(response.content, 'lxml')

    # 新闻列表
    div_li_list = soup.findAll('div', {'class': 'l_li'})

    # 判断时间
    is_2017 = True
    for div_li in div_li_list:
        page_url = urljoin(response.url, div_li.a['href'])
        title = div_li.a.text
        date_time = div_li.cite.text[1:-1]

        print('page_url: {} \n title: {} \n date_time: {} \n'.format(page_url, title, date_time))

        # 判断时间 2017年
        year = int(date_time[:4])
        print('------- year ------- : {}'.format(year))
        if year < 2017:
            is_2017 = False
            url_manager.add_viewed(page_url)
            continue
        else:
            # 解析正文
            result = parse_page(title, page_url)
            if result is None:
                continue
            content, imgs_url, author = result

            url_manager.add_viewed(page_url)

            # 当前新闻编号
            page_number = number_re.match(page_url.split('/')[-1]).group(0)
            content_list_result[page_number] = {
                'title': title,
                'date_time': date_time,
                'author': author,
                'imgs_url': imgs_url,
                'content': content
            }

    if is_2017:
        '''获取下一页url'''
        next_url = urljoin(response.url, soup.findAll('a', {'class': 'Next'})[0]['href'])
    else:
        next_url = None
    return content_list_result, next_url

'''解析page'''
def parse_page(title, page_url):
    response = get_response(page_url)
    soup = BeautifulSoup(response.content, 'lxml')

    # 判断是否是电信学院的相关报道
    title_tokens = jieba.cut(title)
    is_school_relative = is_relative(SCHOOL_NAMES, title_tokens)
    is_keyword_relative = is_relative(KEYWORDS, title_tokens)

    # 判断标题和正文是否包含关键字
    content = soup.find('div', {'id': 'lmz_content'}).text

    # 如果标题没有相关内容，则判断正文
    if not is_school_relative or not is_keyword_relative:
        content_tokens = jieba.cut(content)
        is_school_relative = is_relative(SCHOOL_NAMES, content_tokens)
        is_keyword_relative = is_relative(KEYWORDS, content_tokens)

    # 如果还没有则跳过
    if not is_school_relative or not is_keyword_relative:
        return None

    # 图片
    imgs_url = []
    imgs = soup.find('div', {'id': 'lmz_content'}).findAll('img')
    if imgs is not None:
        for img in imgs:
            img_url = urljoin(response.url, img['src'])
            imgs_url.append(img_url)

    # 作者
    author = ''
    author_div_list = soup.findAll('div', {'class': 'd_write2'})
    for div in author_div_list:
        author += div.text + '\n'

    print('---- author ---- : {}'.format(author))

    return content, imgs_url, author


def is_relative(keywords, tokens):
    for keyword in keywords:
        if keyword in tokens:
            return True
    return False




