import hashlib
import json
import re
import time
import requests


# 获取核心参数signature
def get_signature(clienttime, keyword):
    return hashlib.md5(f"NVPh5oo715z5DIWAeQlhMDsWXXQV4hwtbitrate=0callback=callback123clienttime"
                       f"={clienttime}clientver=2000dfid=-inputtype=0iscorrection=1isfuzzy=0keyword={keyword}mid"
                       f"={clienttime}page=1pagesize=30platform=WebFilterprivilege_filter=0srcappid=2919tag=emuserid"
                       f"=0uuid={clienttime}NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt".encode()).hexdigest()


# 获取歌曲列表
def get_song_list(signature, clienttime, keyword):
    url = f"https://complexsearch.kugou.com/v2/search/song?callback=callback123&keyword={keyword}&page=1&pagesize=30" \
          "&bitrate=0&isfuzzy=0&tag=em&inputtype=0&platform=WebFilter&userid=0&clientver=2000&iscorrection=1" \
          f"&privilege_filter=0&srcappid=2919&clienttime={clienttime}&mid={clienttime}&uuid={clienttime}&dfid" \
          f"=-&signature={signature}"
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.55 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://www.kugou.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.request("GET", url, headers=headers)
    response = json.loads(response.text.replace("callback123(", "").replace("})", "}")).get('data').get('lists')
    return response


# 通过hash和album_id获取歌曲播放链接
def get_player_url(filehash, albumid, clienttime):
    url = f"https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={filehash}&mid" \
          f"=08ea0f85e7e7e866f4f33adb5e3bd40d&album_id={albumid}&_={clienttime}"
    headers = {
        'Host': 'wwwapi.kugou.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.55 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://www.kugou.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text).get('data').get('play_url')


if __name__ == '__main__':
    song_name = input('请输入歌曲名称，按回车键搜索：')
    millis = str(round(time.time() * 1000))
    song_list = get_song_list(get_signature(millis, song_name), millis, song_name)
    print('搜索结果如下：')
    for i, song in enumerate(song_list):
        r = re.compile(r'<[^>]+>', re.S)
        print(str(i+1) + "：" + r.sub('', song.get('FileName')))
        print(get_player_url(song.get('FileHash'), song.get('AlbumID'), millis))
