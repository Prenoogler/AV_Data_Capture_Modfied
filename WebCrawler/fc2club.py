import sys
sys.path.append('../')
import re
import requests
from lxml import etree#need install
import json
import ADC_function
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)

def getTitle_fc2com(htmlcode): #获取厂商
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    result = html.xpath('/html/head/title/text()')[0].replace(' - FC2CLUB.COM','').split(' ',1)[1]
    return result
def getActor_fc2com(htmlcode):
    try:
        html = etree.fromstring(htmlcode, etree.HTMLParser())
        result = html.xpath('/html/body/div[2]/div/div[1]/h5[5]/a/text()')[0]
        return result
    except:
        return ''
def getStudio_fc2com(htmlcode): #获取厂商
    try:
        html = etree.fromstring(htmlcode, etree.HTMLParser())
        result = str(html.xpath('//*[@id="top"]/div[1]/section[1]/div/section/div[2]/ul/li[3]/a/text()')).strip(" ['']")
        return result
    except:
        return ''
def getNum_fc2com(htmlcode):     #获取番号
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[1]/span[2]/text()')).strip(" ['']")
    return result
def getRelease_fc2com(htmlcode2): #
    html=etree.fromstring(htmlcode2,etree.HTMLParser())
    result = str(html.xpath('//*[@id="top"]/div[1]/section[1]/div/section/div[2]/div[2]/p/text()')).strip(" ['販売日 : ']").replace('/','-')
    return result
def getCover_fc2com(htmlcode2): #获取厂商 #
    html = etree.fromstring(htmlcode2, etree.HTMLParser())
    result = str(html.xpath('//*[@id="slider"]/ul[1]/li[1]/img/@src')).strip(" ['']").replace('../','fc2club.net/')
    return 'https://' + result
# def getOutline_fc2com(htmlcode2):     #获取番号 #
#     xpath_html = etree.fromstring(htmlcode2, etree.HTMLParser())
#     path = str(xpath_html.xpath('//*[@id="top"]/div[1]/section[4]/iframe/@src')).strip(" ['']")
#     html = etree.fromstring(ADC_function.get_html('https://adult.contents.fc2.com/'+path), etree.HTMLParser())
#     print('https://adult.contents.fc2.com'+path)
#     print(ADC_function.get_html('https://adult.contents.fc2.com'+path,cookies={'wei6H':'1'}))
#     result = str(html.xpath('/html/body/div/text()')).strip(" ['']").replace("\\n",'',10000).replace("'",'',10000).replace(', ,','').strip('  ').replace('。,',',')
#     return result
def getTag_fc2com(htmlcode2):     #获取番号
    html = etree.fromstring(htmlcode2, etree.HTMLParser())
    keywords=str(html.xpath('/html/head/meta[3]/@content')).strip(" ['']")
    result=keywords.split(',')
    result.pop()
    return result
def getYear_fc2com(release):
    try:
        result = re.search('\d{4}',release).group()
        return result
    except:
        return ''

def main(number):
    try:
        number = number.replace('FC2-', '').replace('fc2-', '')
        kv={'user-agent':'Mozilla/5.0'}
        wangye=requests.get('https://fc2club.net/html/FC2-'+number+'.html',headers=kv)
        wangye.raise_for_status()
        wangye.encoding=wangye.apparent_encoding
        htmlcode2=wangye.text
        actor = getActor_fc2com(htmlcode2)
        if getActor_fc2com(htmlcode2) == '':
            actor = 'FC2系列'
        dic = {
            'title': getTitle_fc2com(htmlcode2),
            'studio': '',
            'year': '',
            'outline': '',  # getOutline_fc2com(htmlcode2),
            'runtime': '',
            'director': '',
            'actor': actor,
            'release': '',
            'number': 'FC2-' + number,
            'label': '',
            'cover': getCover_fc2com(htmlcode2),
            'imagecut': 2,
            'tag': getTag_fc2com(htmlcode2),
            'actor_photo': '',
            'website': 'https://fc2club.net/html/FC2-' + number + '.html',
            'source': 'https://fc2club.net/html/FC2-' + number + '.html',
            'series': '',
        }
    except Exception as e:
        # print(e)
        dic = {"title": ""}
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js

if __name__ == '__main__':
    print(main('778927'))
