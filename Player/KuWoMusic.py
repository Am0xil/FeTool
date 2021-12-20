import json
import uuid

import requests


# 获取歌曲列表
def get_song_list(keyword, uuid1):
    url = f"http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={keyword}&pn=1&rn=30&httpsStatus=1&reqId" \
          f"={uuid1}"
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'csrf': 'IUL870T3M6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.55 Safari/537.36',
        'Referer': 'http://www.kuwo.cn/search/list',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1638317015; '
                  'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1638317015; _ga=GA1.2.486756032.1638317016; '
                  '_gid=GA1.2.2129255142.1638317016; _gat=1; kw_token=IUL870T3M6; kw_token=0ZHQWR81QPYP '
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text).get('data').get('list')


# 获取歌曲播放链接
def get_player_url(mid, uuid1):
    url = f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={mid}&type=music&httpsStatus=1&reqId={uuid1}"
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.55 Safari/537.36',
        'Referer': 'http://www.kuwo.cn/search/list',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text).get('data').get('url')


if __name__ == '__main__':
    song_name = input('请输入歌曲名称，按回车键搜索：')
    id1 = uuid.uuid1()
    song_list = get_song_list(song_name, id1)
    print('搜索结果如下：')
    for i, song in enumerate(song_list):
        print(str(i + 1) + "：" + song.get('artist') + '—————' + song.get('name'))
        try:
            print(get_player_url(song.get('rid'), id1))
        except Exception as e:
            print("该歌曲为付费内容，请下载酷我音乐客户端后付费收听")
