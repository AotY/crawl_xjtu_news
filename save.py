import shutil

import requests
import os

'''
content_list_result:
{'800':{
        'content': ...
    }
}
'''

base_path = './data'
texts_path = os.path.join(base_path, 'texts')
images_path = os.path.join(base_path, 'images')

print('texts_path: {}'.format(texts_path))
print('images_path: {}'.format(images_path))


def save_2_file(content_list_result):
    for number, item in content_list_result.items():
        # 保存文本

        f = open(os.path.join(texts_path, number+'.txt'), 'w')
        f.write(item['title'] + '\n')
        f.write(item['date_time'] + '\n')
        f.write(item['author'] + '\n')
        f.write(item['content'])
        f.close()

        # 保存图片，对应一个文件夹
        imgs_dir = os.path.join(images_path, number)
        if not os.path.exists(imgs_dir):
            os.mkdir(imgs_dir)

        for i, img_url in enumerate(item['imgs_url']):
            print('download img : {}'.format(img_url))

            r = requests.get(img_url, stream=True)
            if r.status_code == 200:
                name = str(i) + '.' + img_url.split('.')[-1]
                with open(os.path.join(imgs_dir, name), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)