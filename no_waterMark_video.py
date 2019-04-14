import requests
import configparser
import os


from requests.packages import urllib3
urllib3.disable_warnings()

def getHeaders( filename, key ):
    conf = configparser.ConfigParser()
    conf.read( filename );
    confDict = dict(conf._sections);
    headers = dict(confDict[key]);
    return headers;

def parseUrl( url, headers ):    
    res = requests.get( url, headers=headers, verify=False );    
    res.encoding = 'utf-8'
    
    data = res.text
    cover = data.split("cover: \"")[1].split("\"")[0]
    playAddr = data.split("playAddr: \"")[1].split("\",")[0]
    videoId = playAddr.split("video_id=")[1].split("&")[0]
    videoAddr = playAddr.replace("/playwm/","/play/");
    print (videoAddr)
    return
    return {
        "cover": cover,
        "playAddr": playAddr,
        "addr": videoAddr,
        "id": videoId
    }

def downVideo( parseDouyin, headers ):
   
    videoBin = requests.get( parseDouyin['addr'], headers=headers, verify=False );
    _filename = parseDouyin['id'] + ".mp4";
    with open( _filename, "wb") as f:
            f.write(videoBin.content)
            f.close()
    return _filename;




#主函数
if __name__ == '__main__':
    print("点击转发抖音视频时，可通过选择复制链接来获取视频链接\n")
    url = input("请输入抖音视频url：");

    headers = getHeaders( "config.ini", "headers" );
    arduinoHeaders = getHeaders( "config.ini", "arduino-headers" );

    parseUrl( url, headers);
    parseData = parseUrl( url, headers);
    print( "视频源地址为：" + parseData['addr'] );
    #下载视频
    filename = downVideo( parseData, arduinoHeaders );
    print( "视频下载完成，", "视频Id为：",parseData['id'], "\n" );
    print( "视频保存在当前同级目录下，格式为mp4\n" );
    
