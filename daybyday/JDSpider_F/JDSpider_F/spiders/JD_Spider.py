# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from JDSpider_F.items import JdspiderFItem
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup
import time
import requests
import re,json

class JdSpider(CrawlSpider):
    name = "JDSpider"
    redis_key = "JDSpider:start_urls"
    start_urls = [
        # "https://list.jd.com/list.html?cat=737,738,751",##电风扇

        'https://list.jd.com/list.html?cat=737,738,751'
     ]

    def parse(self, response):
        item = JdspiderFItem()
        selector = Selector(response)
        Products = selector.xpath('//*[@id="plist"]/ul/li')
        for each in Products:
            temphref = each.xpath('div/div[@class="p-img"]/a/@href').extract()
            temphref = str(temphref)
            ProductID = str(re.search('com/(.*?)\.html',temphref).group(1))
            # ProductID='1959718783'
            ##获取价格
            # json_url_p = 'http://p.3.cn/prices/mgets?skuIds=J_' + ProductID
            # try:
            #     data = requests.get(json_url_p,timeout = 1000).json()[0]
            #     price = data['m']
            #     PreferentialPrice = data['p']
            # except requests.exceptions.ConnectionError:  #requests.exceptions.ReadTimeout
            #     print('Timeout ConnectionError1:json_url_p')
            #     time.sleep(600)
            #     try:
            #         data = requests.get(json_url_p, timeout=1000).json()[0]
            #         price = data['m']
            #         PreferentialPrice = data['p']
            #     except requests.exceptions.ConnectionError:
            #         print('Timeout ConnectionError2:json_url_p')
            #         time.sleep(3600)
            #         data = requests.get(json_url_p, timeout=1000).json()[0]
            #         price = data['m']
            #         PreferentialPrice = data['p']
            #     except requests.exceptions.ReadTimeout:
            #         print('Timeout,ReadTimeout:',json_url_p)
            # except requests.exceptions.ReadTimeout:
            #     print('Timeout,ReadTimeout:',json_url_p)



            # ##获取评论总数
            # json_url_connent= 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=' + ProductID
            # try:
            #     data = requests.get(json_url_connent,timeout = 1000).json()
            #     data = data['CommentsCount'][0]
            #     CommentCount=data['CommentCount']
            #     GoodRateShow=data['GoodRateShow']
            #     GoodCount = data['GoodCount']
            #     GeneralCount=data['GeneralCount']
            #     PoorCount=data['PoorCount']
            # except json.decoder.JSONDecodeError or requests.exceptions.ConnectionError or requests.packages.urllib3.exceptions.MaxRetryError:
            #     print('Timeout ConnectionError1:json_url_connent')
            #     time.sleep(600)
            #     try:
            #         data = requests.get(json_url_connent,timeout = 1000).json()
            #         data = data['CommentsCount'][0]
            #         CommentCount = data['CommentCount']
            #         GoodRateShow = data['GoodRateShow']
            #         GoodCount = data['GoodCount']
            #         GeneralCount = data['GeneralCount']
            #         PoorCount = data['PoorCount']
            #     except json.decoder.JSONDecodeError or requests.exceptions.ConnectionError or requests.packages.urllib3.exceptions.MaxRetryError:
            #         print('Timeout ConnectionError2:json_url_connent')
            #         time.sleep(3600)
            #         data = requests.get(json_url_connent, timeout=1000).json()
            #         data = data['CommentsCount'][0]
            #         CommentCount = data['CommentCount']
            #         GoodRateShow = data['GoodRateShow']
            #         GoodCount = data['GoodCount']
            #         GeneralCount = data['GeneralCount']
            #         PoorCount = data['PoorCount']
            #     except requests.exceptions.ReadTimeout:
            #         print('Timeout,ReadTimeout:',json_url_connent)
            # except requests.exceptions.ReadTimeout:
            #     print('Timeout,ReadTimeout:',json_url_connent)

            # ##获取商品评论关键字
            # json_url_keyword= 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv79456&score=0&sortType=5&pageSize=10&isShadowSku=0&page=0&productId=' + ProductID
            #
            # try:
            #     r = requests.get(json_url_keyword,timeout = 1000)
            #     html = r.content.decode('gb2312', 'ignore')
            #     keywords = re.findall(r',"name":"(.*?)",', html)
            #     keyword = ' '.join(keywords)
            # except requests.exceptions.ConnectionError:  # this is important
            #     print('Timeout ConnectionError1:json_url_keyword')
            #     time.sleep(600)
            #     try:
            #         r = requests.get(json_url_keyword,timeout = 1000)
            #         html = r.content.decode('gb2312', 'ignore')
            #         keywords = re.findall(r',"name":"(.*?)",', html)
            #         keyword = ' '.join(keywords)
            #     except requests.exceptions.ConnectionError:  # this is important
            #         print('Timeout ConnectionError2:json_url_keyword')
            #         time.sleep(3600)
            #         r = requests.get(json_url_keyword,timeout = 1000)
            #         html = r.content.decode('gb2312', 'ignore')
            #         keywords = re.findall(r',"name":"(.*?)",', html)
            #         keyword = ' '.join(keywords)
            #     except requests.exceptions.ReadTimeout:
            #         print('Timeout,ReadTimeout:', json_url_keyword)
            # except requests.exceptions.ReadTimeout:
            #     print('Timeout,ReadTimeout:', json_url_keyword)

            ##获取商品参数 ()
            product_typ_url="https://item.jd.com/"+ ProductID+".html"
            try:
                r = requests.get(product_typ_url,timeout = 1000)
                time.sleep(3)
                soup = BeautifulSoup(r.text, 'lxml')
                time.sleep(3)
                ips1 = soup.find_all('ul', class_="parameter2 p-parameter-list")
                ips2 = soup.find_all('div', class_="detail-elevator-floor")
                ips = [ips1, ips2]
                for i in ips:
                    type = re.findall(r'<li title=".*?">.*?：(.*?)<', str(ips))
                    try:
                        X_name = re.findall(r'<li title=".*?">.*?商品名称：(.*?)<', str(ips))[0]
                    except IndexError:
                        try:
                            r = requests.get(product_typ_url, timeout=1000)
                            time.sleep(3)
                            soup = BeautifulSoup(r.text, 'lxml')
                            time.sleep(3)
                            ips1 = soup.find_all('ul', class_="parameter2 p-parameter-list")
                            ips2 = soup.find_all('div', class_="detail-elevator-floor")
                            ips = [ips1, ips2]
                            for i in ips:
                                type = re.findall(r'<li title=".*?">.*?：(.*?)<', str(ips))
                                X_name = re.findall(r'<li title=".*?">.*?商品名称：(.*?)<', str(ips))[0]
                        except IndexError:
                            X_name = None
                    try:
                        X_type = re.findall(r'<li title=".*?">类别：(.*?)<', str(ips))[0]
                    except IndexError:
                        try:
                            X_type = re.findall(r'<li title=".*?">类型：(.*?)<', str(ips))[0]
                        except IndexError:
                            X_type = re.findall(r'<li title=".*?">分类：(.*?)<', str(ips))[0]
                try:
                    shop_name = re.findall(r'<a clstag=".*?" href=".*?" target="_blank" title="(.*?)">', str(soup))[0]
                except IndexError:
                    shop_name = "none"
                try:
                    brand = soup.find_all('ul', id="parameter-brand")
                    brand = re.findall(r'<li title="(.*?)"', str(brand))[0]
                except IndexError:
                    brand = X_name
                else:
                    brand='None'


            except requests.exceptions.ConnectionError:  # this is important
                print('Timeout ConnectionError1:product_typ_url')
                time.sleep(600)
                try:
                    r = requests.get(product_typ_url,timeout = 1000)
                    time.sleep(3)
                    soup = BeautifulSoup(r.text, 'lxml')
                    time.sleep(3)
                    ips1 = soup.find_all('ul', class_="parameter2 p-parameter-list")
                    ips2 = soup.find_all('div', class_="detail-elevator-floor")
                    ips = [ips1, ips2]
                    for i in ips:
                        type = re.findall(r'<li title=".*?">.*?：(.*?)<', str(ips))
                        try:
                            X_name = re.findall(r'<li title=".*?">.*?商品名称：(.*?)<', str(ips))[0]
                        except IndexError:
                            try:
                                r = requests.get(product_typ_url, timeout=1000)
                                time.sleep(3)
                                soup = BeautifulSoup(r.text, 'lxml')
                                time.sleep(3)
                                ips1 = soup.find_all('ul', class_="parameter2 p-parameter-list")
                                ips2 = soup.find_all('div', class_="detail-elevator-floor")
                                ips = [ips1, ips2]
                                for i in ips:
                                    type = re.findall(r'<li title=".*?">.*?：(.*?)<', str(ips))
                                    X_name = re.findall(r'<li title=".*?">.*?商品名称：(.*?)<', str(ips))[0]
                            except IndexError:
                                X_name =None

                        try:
                            X_type = re.findall(r'<li title=".*?">类别：(.*?)<', str(ips))[0]
                        except IndexError:
                            try:
                                X_type = re.findall(r'<li title=".*?">类型：(.*?)<', str(ips))[0]
                            except IndexError:
                                X_type = re.findall(r'<li title=".*?">分类：(.*?)<', str(ips))[0]
                    try:
                        shop_name = re.findall(r'<a clstag=".*?" href=".*?" target="_blank" title="(.*?)">', str(soup))[0]
                    except IndexError:
                        shop_name = "none"
                    try:
                        brand = soup.find_all('ul', id="parameter-brand")
                        brand = re.findall(r'<li title="(.*?)"', str(brand))[0]
                    except IndexError:
                        brand = X_name
                    else:
                        brand = 'None'


                except requests.exceptions.ConnectionError:  # this is important
                    print('Timeout ConnectionError2:product_typ_url')
                    time.sleep(3600)
                    r = requests.get(product_typ_url,timeout = 1000)
                    time.sleep(3)
                    soup = BeautifulSoup(r.text, 'lxml')
                    time.sleep(3)
                    ips1 = soup.find_all('ul', class_="parameter2 p-parameter-list")
                    ips2 = soup.find_all('div', class_="detail-elevator-floor")
                    ips = [ips1, ips2]
                    for i in ips:
                        type = re.findall(r'<li title=".*?">.*?：(.*?)<', str(ips))
                        try:
                            X_name = re.findall(r'<li title=".*?">.*?商品名称：(.*?)<', str(ips))[0]
                        except IndexError:
                            try:
                                r = requests.get(product_typ_url, timeout=1000)
                                time.sleep(3)
                                soup = BeautifulSoup(r.text, 'lxml')
                                time.sleep(3)
                                ips1 = soup.find_all('ul', class_="parameter2 p-parameter-list")
                                ips2 = soup.find_all('div', class_="detail-elevator-floor")
                                ips = [ips1, ips2]
                                for i in ips:
                                    type = re.findall(r'<li title=".*?">.*?：(.*?)<', str(ips))
                                    X_name = re.findall(r'<li title=".*?">.*?商品名称：(.*?)<', str(ips))[0]
                            except IndexError:
                                X_name =None
                        try:
                            X_type = re.findall(r'<li title=".*?">类别：(.*?)<', str(ips))[0]
                        except IndexError:
                            try:
                                X_type = re.findall(r'<li title=".*?">类型：(.*?)<', str(ips))[0]
                            except IndexError:
                                X_type = re.findall(r'<li title=".*?">分类：(.*?)<', str(ips))[0]
                    try:
                        shop_name = re.findall(r'<a clstag=".*?" href=".*?" target="_blank" title="(.*?)">', str(soup))[
                            0]
                    except IndexError:
                        shop_name = "none"
                    try:
                        brand = soup.find_all('ul', id="parameter-brand")
                        brand = re.findall(r'<li title="(.*?)"', str(brand))[0]
                    except IndexError:
                        brand = X_name
                    else:
                        brand = 'None'

                except requests.exceptions.ReadTimeout:
                    print('Timeout,ReadTimeout:', product_typ_url)
            except requests.exceptions.ReadTimeout:
                print('Timeout,ReadTimeout:', product_typ_url)
            Name = each.xpath('div/div[@class="p-name"]/a/em/text()').extract()[0]
            p_Name=Name.strip()
            # print(p_Name)
            if p_Name=='':
                p_Name=X_name
            print(p_Name)
            # ##item
            item['p_Name'] = p_Name
            item['shop_name'] = shop_name
            item['ProductID'] = ProductID
            # item['price'] = price
            # item['PreferentialPrice'] = PreferentialPrice

            # item['CommentCount']=CommentCount
            # item['GoodRateShow']=GoodRateShow
            # item['GoodCount']=GoodCount
            # item['GeneralCount'] = GeneralCount
            # item['PoorCount'] = PoorCount
            # item['keyword'] = keyword

            item['brand'] = brand
            item['type'] = type
            item['X_type'] = X_type
            item['X_name'] = X_name
            yield item

        # donetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print("Sleep time start......")
        # time.sleep(5)
        # print("donetime is:", donetime)


        nextLink = selector.xpath('//*[@id="J_bottomPage"]/span[1]/a[10]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            yield Request('https://list.jd.com/'+nextLink,callback=self.parse)
