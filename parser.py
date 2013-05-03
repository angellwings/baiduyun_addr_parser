#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re, json, sys

def genDirUrl(path, uk, shareid):
    return 'http://pan.baidu.com/share/list?clienttype=0&web=1&num=100&page=1&dir={0}&uk={1}&shareid={2}'.format(path, uk, shareid)
    
def parser(url):
    jsonPattern = '{[^{}]*?fs_id[^{}]+}'
    uk, shareid = re.search('uk=(\d+).*shareid=(\d+)', url).group(1, 2)
    r = requests.get(url)
    dataList = re.findall(jsonPattern, r.content)
    for data in dataList:
        data = json.loads(data.decode("string-escape"))
        if data['isdir'] == '1':
            print 'dir\t{0}:'.format(data['server_filename'].encode('utf-8'))
            dirUrl = genDirUrl(data['path'].encode('utf-8'), uk, shareid)
            r = requests.get(dirUrl)
            subDataList = re.findall(jsonPattern, r.content)
            for subData in subDataList:
                subData = json.loads(subData.replace('\\', ''))
                print subData['dlink']
        else:
            print 'file\t{0}:\n{1}'.format(data['server_filename'].encode('utf-8'), data['dlink'])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print """
        usage: parser.py 'url'
        url must be quoted
        result will be sent to stdout
        """
        exit(1)
    
    parser(sys.argv[1])
    