# -*- coding: utf-8 -*-
import scrapy, time, json, re, math, execjs, datetime, pymongo
from Wenshu.items import WenshuCaseItem


class WenshuSpider(scrapy.Spider):
    name = 'wenshu'
    # allowed_domains = ['wenshu.court.gov.cn']
    start_urls = ['http://wenshu.court.gov.cn/list/list/?sorttype=1']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guid = 'aaaabbbb-aaaa-aaaabbbb-aaaabbbbcccc'
        with open('Wenshu\spiders\get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        with open('Wenshu\spiders\get_docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.js_2 = execjs.compile(jsdata_2)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['WenshuDB']
        self.mydocid = mydb['docid']        

    def parse(self, response):
        '''获取cookie'''
        try:
            vjkl5 = response.headers['Set-Cookie'].decode('utf-8')
            vjkl5 = vjkl5.split(';')[0].split('=')[1]
            url_num = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
            data = {
                'guid': self.guid
            }
            yield scrapy.FormRequest(url_num, formdata=data, meta={'vjkl5': vjkl5}, callback=self.get_count,
                                     dont_filter=True)
        except:
            yield scrapy.Request(WenshuSpider.start_urls, callback=self.parse, dont_filter=True)

    def get_count(self, response):
        '''获取案件数目,设置请求页数'''
        number = response.text
        vjkl5 = response.meta['vjkl5']
        vl5x = self.js_1.call('getvl5x', vjkl5)
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        start_day = "2016-01-01"
        end_day = "2016-12-31"
        end_date = datetime.datetime.strptime(end_day, '%Y-%m-%d')
        #court_name_list = ['重庆市江北区人民法院', '重庆市沙坪坝区人民法院', '重庆市北碚区人民法院', '重庆市大足区人民法院', '重庆市渝北区人民法院', '重庆市长寿区人民法院', '重庆市合川区人民法院', '重庆市璧山区人民法院', '重庆市铜梁区人民法院', '重庆市潼南区人民法院', '重庆市万州区人民法院', '重庆市梁平区人民法院', '城口县人民法院', '忠县人民法院', '重庆市开州区人民法院', '云阳县人民法院', '奉节县人民法院', '巫山县人民法院', '巫溪县人民法院', '重庆市涪陵区人民法院', '重庆市南川区人民法院', '丰都县人民法院', '垫江县人民法院', '重庆市武隆区人民法院', '重庆市黔江区人民法院', '石柱土家族自治县人民法院', '秀山土家族苗族自治县人民法院', '酉阳土家族苗族自治县人民法院', '彭水苗族土家族自治县人民法院', '重庆市渝中区人民法院', '重庆市大渡口区人民法院', '重庆市九龙坡区人民法院', '重庆市南岸区人民法院', '重庆市綦江区人民法院', '重庆市巴南区人民法院', '重庆市江津区人民法院', '重庆市永川区人民法院', '重庆市荣昌区人民法院', '重庆铁路运输法院']
        #for court_name in court_name_list:
        # region_list = ['北京市','天津市','河北省','山西省','内蒙古自治区',
        # '辽宁省','吉林省','黑龙江省','上海市','江苏省',
        # '浙江省','安徽省','福建省','江西省','山东省',
        # '河南省','湖北省','湖南省','广东省','广西壮族自治区',
        # ,'重庆市','四川省','贵州省','云南省', '陕西省','甘肃省',
        # '海南省', '西藏自治区', '青海省','宁夏回族自治区',  '新疆维吾尔自治区','新疆维吾尔自治区高级人民法院生产建设兵团分院']
        region_list1 = ['北京市','天津市','河北省','山西省','内蒙古自治区']
        region_list2 = ['辽宁省','吉林省','黑龙江省','上海市','江苏省']
        region_list3 = ['浙江省','安徽省','福建省','江西省','山东省']
        region_list4 = ['河南省','湖北省','湖南省','广东省','广西壮族自治区']
        region_list5 = ['重庆市','四川省','贵州省','云南省', '陕西省','甘肃省']
        region_list6 = ['海南省', '西藏自治区', '青海省','宁夏回族自治区',  '新疆维吾尔自治区','新疆维吾尔自治区高级人民法院生产建设兵团分院']
        case_date_list = ['2017-01-01 TO 2017-12-31']
        #                 '2016-01-01 TO 2016-01-31',
        #                 '2016-02-01 TO 2016-02-28',
        #                 '2016-03-01 TO 2016-03-31',
        #                 '2016-04-01 TO 2016-04-30',
        #                 '2016-05-01 TO 2016-05-31',
        #                 '2016-06-01 TO 2016-06-30',
        #                 '2016-07-01 TO 2016-07-31',
        #                 '2016-08-01 TO 2016-08-15',
        #                 '2016-08-16 TO 2016-08-31',
        #                 '2016-09-01 TO 2016-09-30',
        #                 '2016-10-01 TO 2016-10-31',
        #                 '2016-11-01 TO 2016-11-30',
        #                 '2016-12-01 TO 2016-12-31',
        # ]
        region_list = region_list5
        for region in region_list:
            print(region)
            start_date = datetime.datetime.strptime(start_day, '%Y-%m-%d')
            #while start_date < end_date:
            for case_date in case_date_list:
                        #upload_date = f"{start_date.year}-{start_date.month:02d}-{start_date.day:02d}"
                        #search_criteria = f"案件类型:刑事案件,基层法院:{court_name},文书类型:判决书,裁判日期:{start_date.year}-{start_date.month:02d}-{start_date.day:02d}"
                #search_criteria = f"案件类型:刑事案件,审判程序:一审,法院地域:{region},文书类型:判决书,四级案由:妨害公务,裁判日期:{start_date.year}-{start_date.month:02d}-{start_date.day:02d}"
                #search_criteria = f"案件类型:刑事案件,审判程序:一审,法院地域:{region},文书类型:判决书,四级案由:妨害公务,裁判日期:{case_date}"
                search_criteria = f"案件类型:刑事案件,审判程序:一审,法院地域:{region},文书类型:判决书,四级案由:妨害公务,裁判年份:2017"
                
                #search_criteria = f"案件类型:刑事案件,审判程序:一审,法院地域:{region},文书类型:判决书,四级案由:妨害公务,裁判年份:2016"
                         
                #search_criteria = f"案件类型:刑事案件,基层法院:{court_name},文书类型:判决书,上传日期:{upload_date} TO {upload_date}"
                start_date += datetime.timedelta(days=1)
                data = {
                        'Param': search_criteria,
                        'Index': '1',  # 页数
                        'Page': '0',  # 只为了获取案件数目,所有请求0条就行了
                        'Order': '裁判日期',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
                        'Direction': 'asc',  # 排序方式(1.asc:从小到大/2.desc:从大到小)
                        'vl5x': vl5x,
                        'number': number,
                        'guid': self.guid
                    }
                headers = {
                    'Cookie': 'vjkl5=' + response.meta['vjkl5'],  # 在这单独添加cookie,settings中就可以禁用cookie,防止跟踪被ban
                    'Host': 'wenshu.court.gov.cn',
                    'Origin': 'http://wenshu.court.gov.cn',
                }
                # print(response.request.headers.getlist('Cookie'))
                yield scrapy.FormRequest(url, formdata=data,
                                        meta={'vl5x': vl5x, 'vjkl5': vjkl5, 'number': number, 'search_criteria': search_criteria},
                                        callback=self.get_content, headers=headers, dont_filter=True)

    def get_content(self, response):
        '''获取每页的案件'''
        html = response.text
        result = eval(json.loads(html))
        count = result[0]['Count']
        print(f"******* {response.meta['search_criteria']}:该筛选条件下共有多少条数据:{count} ********")
        pages = math.ceil(int(count) / 10)  # 向上取整,每页10条
        #if pages <= 20:  # max:10*20=200 ; 20181005 -只能爬取20页,每页10条!!!
        if pages > 20:
            pages = 20
            for i in range(1, int(pages) + 1):
                url = 'http://wenshu.court.gov.cn/List/ListContent'
                data = {
                    'Param': response.meta['search_criteria'],
                    'Index': str(i),  # 页数
                    'Page': '10',  # 每页显示的条目数
                    'Order': '裁判日期',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
                    'Direction': 'asc',  # 排序方式(1.asc:从小到大/2.desc:从大到小)
                    'vl5x': response.meta['vl5x'],  # 保存1个小时
                    'number': response.meta['number'],  # 每次都要请求一次GetCode,获取number带入
                    'guid': self.guid
                }
                headers = {
                    'Cookie': 'vjkl5=' + response.meta['vjkl5'],
                    'Host': 'wenshu.court.gov.cn',
                    'Origin': 'http://wenshu.court.gov.cn',
                }
                yield scrapy.FormRequest(url, formdata=data, callback=self.get_docid, headers=headers, dont_filter=True)
        else:
            # TODO: Add it into scrapy log
            print(f"{response.meta['search_criteria']} has {pages}  pages of results.")


    def get_docid(self, response):
        '''计算出docid'''
        html = response.text
        result = eval(json.loads(html))
        runeval = result[0]['RunEval']
        content = result[1:]
        for i in content:
            casewenshuid = i.get('文书ID', '')
            casejudgedate = i.get('裁判日期', '')
            docid = self.js_2.call('getdocid', runeval, casewenshuid)
            if self.mydocid.find_one({"docid":docid}):
                continue
            if docid:
                url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(docid)
                yield scrapy.Request(url, callback=self.get_detail, meta={'casejudgedate':casejudgedate, 'docid':docid}, dont_filter=True)

    def get_detail(self, response):
        '''获取每条案件详情'''
        html = response.text
       
        try:
            content_1 = json.loads(re.search(r'JSON\.stringify\((.*?)\);\$\(document', html).group(1))  # 内容详情字典1
        except:
            #print(f"doc id is {response.meta['docid']}")
            print(f"Failed to get content_1 of {html}")
            #if "此篇文书不存在" in html:
            #    self.mydocid.insert_one({"docid": docid, "status"： "not exist"}):
            return None

        try:
            content_3 = re.search(r'"Html\\":\\"(.*?)\\"}"', html).group(1)  # 内容详情字典3(doc文档正文)
        except:
            #print(f"Failed to get content_3 {html}")
            return None

        reg = re.compile(r'<[^>]+>', re.S)
        # 存储到item
        item = WenshuCaseItem()
        item['court'] = {
            'id': content_1.get('法院ID', ''),
            'name': content_1.get('法院名称', ''),
            'province': content_1.get('法院省份', ''),
            'city': content_1.get('法院地市', ''),
            'district': content_1.get('法院区县', ''),
            'area': content_1.get('法院区域', ''),
        }
        item['content'] = {
            'base': content_1.get('案件基本情况段原文', ''),
            'add': content_1.get('附加原文', ''),
            'head': content_1.get('文本首部段落原文', ''),
            'main': content_1.get('裁判要旨段原文', ''),
            'corrections': content_1.get('补正文书', ''),
            'doc': content_1.get('DocContent', ''),
            'litigation': content_1.get('诉讼记录段原文', ''),
            'party': content_1.get('诉讼参与人信息部分原文', ''),
            'tail': content_1.get('文本尾部原文', ''),
            'result': content_1.get('判决结果段原文', ''),
            'str': reg.sub('', content_3),  # 去除html标签后的文书内容
        }
        item['type'] = content_1.get('案件类型', '')  # 案件类型
        item['judgedate'] = response.meta['casejudgedate']  # 裁判日期
        item['procedure'] = content_1.get('审判程序', '')
        item['number'] = content_1.get('案号', '')
        item['nopublicreason'] = content_1.get('不公开理由', '')
        item['casedocid'] = content_1.get('文书ID', '')
        item['name'] = content_1.get('案件名称', '')
        item['contenttype'] = content_1.get('文书全文类型', '')
        item['uploaddate'] = time.strftime("%Y-%m-%d",
                                               time.localtime(int(content_1['上传日期'][6:-5]))) if 'Date' in content_1[
            '上传日期'] else ''
        item['doctype'] = content_1.get('案件名称').split('书')[0][-2:] if '书' in content_1.get(
            '案件名称') else '令'  # 案件文书类型:判决或者裁定...还有令
        item['closemethod'] = content_1.get('结案方式', '')
        item['effectivelevel'] = content_1.get('效力层级', '')
        #print('*************案件名称:' + item['name'])
        yield item
