import requests
import sys
sys.path.append('../')
import json
from bs4 import BeautifulSoup
from lxml import html
from ADC_function import *
from WebCrawler import airav,airavcc


suren=['luxu','mium','sim','simm','gana','maan','heyzo','ore',
       'oretd','orec','mmgh','msfh','reg','ntk','ara','dcv','kwp']

def main(number: str) -> json:
    fanhaozimu=''.join(x for x in number if x.isalpha())
    airnumber=airavnumbermod(number,fanhaozimu)
    
    result = requests.post(url="https://www.jav321.com/search", data={"sn": number})
    
    if fanhaozimu.lower() in suren:
        imagecutswitch=3
    else:
        imagecutswitch=1
    soup = BeautifulSoup(result.text, "html.parser")
    lx = html.fromstring(str(soup))

    if "/video/" in result.url:
        data = parse_info(soup)
        dic = {
            "title": get_title(lx,airnumber),
            "year": get_year(data),
            "outline": get_outline(lx,airnumber),
            "director": "",
            "cover": get_cover(lx),
            "imagecut": imagecutswitch,
            "actor_photo": "",
            "website": result.url,
            "source": "jav321.py",
            "cover_small":get_cover_small(lx),
            **data,
        }
    else:
        dic = {}
    return json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))

def airavnumbermod(number,fanhaozimu):
    group={'luxu':'259luxu','mium':'300mium','gana':'200gana','maan':'300maan',
           'ntk':'300ntk','dcv':'277dcv'}
    if fanhaozimu.lower() in group.keys():
        number=number.replace(fanhaozimu,group[fanhaozimu.lower()])
        return number
    else:
        return number

def airavcctitle(airnumber):
 
    try:
        search=requests.get('https://linesearch.airav.cc/ajax/data.php?act=s&w='+airnumber)
        searchjson=json.loads(search.text)
        link=searchjson['msgs'][1]['link']
        htmlcode=get_html(link)
        airavcctitle=airavcc.getTitle(htmlcode)
        if airavcctitle!='':
            return airavcctitle
    except:
        return 'error'

def airavtitle(airnumber):

    try:
        htmlcode=get_html('https://cn.airav.wiki/video/' + airnumber)
        airavtitle=airav.getTitle(htmlcode)
        if airavtitle!='':
            return airavtitle
    except:
        return 'error'

def get_title(lx: html.HtmlElement,airnumber) -> str:
    
    if airavtitle(airnumber) not in ['','error',None]:
        print('[+]正在从airav.wiki获取中文信息')
        return airavtitle(airnumber)
    else:
        return lx.xpath("/html/body/div[2]/div[1]/div[1]/div[1]/h3/text()")[0].strip()

'''
#airav正常访问时禁用airavcc,因为cc可能会识别错误
    elif airavcctitle(airnumber) not in ['','error',None]:
        print('[+]正在从airav.cc获取中文信息')
        return airavcctitle(airnumber)
'''
        


def parse_info(soup: BeautifulSoup) -> dict:
    data = soup.select_one("div.row > div.col-md-9")

    if data:
        dd = str(data).split("<br/>")
        data_dic = {}
        for d in dd:
            data_dic[get_bold_text(h=d)] = d

        return {
            "actor": get_actor(data_dic),
            "label": get_label(data_dic),
            "studio": get_studio(data_dic),
            "tag": get_tag(data_dic),
            "number": get_number(data_dic),
            "release": get_release(data_dic),
            "runtime": get_runtime(data_dic),
            "series": get_series(data_dic),
        }
    else:
        return {}


def get_bold_text(h: str) -> str:
    soup = BeautifulSoup(h, "html.parser")
    if soup.b:
        return soup.b.text
    else:
        return "UNKNOWN_TAG"


def get_anchor_info(h: str) -> str:
    result = []

    data = BeautifulSoup(h, "html.parser").find_all("a", href=True)
    for d in data:
        result.append(d.text)

    return ",".join(result)


def get_text_info(h: str) -> str:
    return h.split(": ")[1]


def get_cover(lx: html.HtmlElement) -> str:
    return lx.xpath("/html/body/div[2]/div[2]/div[1]/p/a/img/@src")[0]
    
def get_cover_small(lx: html.HtmlElement) -> str:
    smallcoveradd=lx.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/img/@src')[0]
    if 'pf_o1' in smallcoveradd:
        smallcoveradd=smallcoveradd.replace('pf_o1','pf_e')
    return smallcoveradd

def airavccoutline(airnumber):
 
    try:
        search=requests.get('https://linesearch.airav.cc/ajax/data.php?act=s&w='+airnumber)
        searchjson=json.loads(search.text)
        link=searchjson['msgs'][1]['link']
        htmlcode=get_html(link)
        airavccoutline=airavcc.getOutline(htmlcode)
        if airavccoutline!='':
            return airavccoutline
    except:
        return 'error'

def airavoutline(airnumber):

    try:
        htmlcode=get_html('https://cn.airav.wiki/video/' + airnumber)
        airavoutline=airav.getOutline(htmlcode)
        if airavoutline!='':
            return airavoutline
    except:
        return 'error'



def get_outline(lx: html.HtmlElement,airnumber) -> str:

    if airavoutline(airnumber) not in ['','error',None]:
        return airavoutline(airnumber)
    else:
        try:
            return lx.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/text()")[0]
        except:
            return ''
'''
#与TITLE原因相同，避免识别错误
    elif airavccoutline(airnumber) not in ['','error',None]:
        return airavccoutline(airnumber)
'''


def get_series2(lx: html.HtmlElement) -> str:
    return lx.xpath("/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/a[11]/text()")[0]


def get_actor(data: hash) -> str:
    if "女优" in data:
        return get_anchor_info(data["女优"])
    else:
        return ""


def get_label(data: hash) -> str:
    if "片商" in data:
        return get_anchor_info(data["片商"])
    else:
        return ""


def get_tag(data: hash) -> str:
    if "标签" in data:
        return get_anchor_info(data["标签"])
    else:
        return ""


def get_studio(data: hash) -> str:
    if "片商" in data:
        return get_anchor_info(data["片商"])
    else:
        return ""


def get_number(data: hash) -> str:
    if "番号" in data:
        return get_text_info(data["番号"])
    else:
        return ""


def get_release(data: hash) -> str:
    if "发行日期" in data:
        return get_text_info(data["发行日期"])
    else:
        return ""


def get_runtime(data: hash) -> str:
    if "播放时长" in data:
        return get_text_info(data["播放时长"])
    else:
        return ""


def get_year(data: hash) -> str:
    if "release" in data:
        return data["release"][:4]
    else:
        return ""


def get_series(data: hash) -> str:
    if "系列" in data:
        return get_anchor_info(data["系列"])
    else:
        return ""


if __name__ == "__main__":
    print(main("sdsi-019"))
