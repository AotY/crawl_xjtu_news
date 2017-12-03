from parse import parse_content_list
from save import save_2_file
from url import UrlManager
from download import get_response

home_urls = [
    # 'http://news.xjtu.edu.cn/zyxw.htm', # 主页新闻
    'http://news.xjtu.edu.cn/zhxw.htm', # 综合新闻
    'http://news.xjtu.edu.cn/jyjx.htm', # 教育教学
    'http://news.xjtu.edu.cn/kydt.htm', # 科研动态
    'http://news.xjtu.edu.cn/ybdt.htm', # 院部动态
    'http://news.xjtu.edu.cn/xysh.htm', # 校园生活
    'http://news.xjtu.edu.cn/syjt.htm', # 思源讲堂
    'http://news.xjtu.edu.cn/rwfc.htm', # 人物风采
    'http://news.xjtu.edu.cn/mtjd.htm', # 媒体交大

]


for home_url in home_urls:
    # 首页
    print('------ home_url: {}'.format(home_url))

    # 每个类别使用一个url manager
    url_manager = UrlManager()

    # 加入每个类别首页
    url_manager.add_url(home_url)

    # 遍历
    while not url_manager.is_empty():
        cur_url = url_manager.get_url()
        print('cur_url: {}'.format(cur_url))

        if url_manager.is_viewed(cur_url):
            continue

        # 获取当前页面新闻列表 (列表页）
        response = get_response(cur_url)

        # 解析内容并保存 content_list_result返回的是列表页所有的page内容
        content_list_result, next_url = parse_content_list(response, url_manager)

        print('next_url： {}'.format(next_url))
        if next_url is not None:
            url_manager.add_url(next_url)

        # 保存
        save_2_file(content_list_result)

        # 标记已访问
        url_manager.add_viewed(cur_url)