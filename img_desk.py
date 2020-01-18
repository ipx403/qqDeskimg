import requests
from lxml import etree
import time
import os


class Qqimg():

    def __init__(self, type):
        self.type = type

    def etre(self, url_t):
        url = 'http://www.qqbizhi.com'
        select = etree.HTML(url_t)
        url_m = select.xpath('//*[@id="main"]/div/div[2]/ul/li')
        z_url = []
        for i in url_m:
            m = i.xpath('a/@href')[0]
            zurl = url + m
            z_url.append(zurl)
        return z_url

    def etre1(self, rr):
        select = etree.HTML(rr.text)
        urllis2 = []
        zurl = select.xpath('//*[@id="main"]/div/div[2]/div/ul/li')
        for url in zurl:
            urlx = url.xpath('a/@href')[0]
            url = 'http://www.qqbizhi.com/desk/'+self.type+ '/' + urlx
            urllis2.append(url)
        return urllis2

    def etre2(self, rr):
        select = etree.HTML(rr.text)
        urllis2 = []
        zurl = select.xpath('//*[@id="main"]/div/div[2]/div/ul/li')
        for url in zurl:
            urlx = url.xpath('a/img/@href')[0]
            url = 'http://www.qqbizhi.com/desk/'+self.type +'/' + urlx
            urllis2.append(url)
        return urllis2

    def download(self, title, url):
        if os.path.exists(self.type):
            filename = title
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

            try:
                pic = requests.get(url, headers=headers)
                with open(self.type +'/'+ filename + '.jpg', 'wb') as fp:
                    fp.write(pic.content)
                print(title, 'Download ok !!')
            except Exception as e:
                print(e)
        else:
            os.mkdir(self.type)
            filename = title
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
            try:
                pic = requests.get(url, headers=headers)
                with open(self.type + '/' + filename + '.jpg', 'wb') as fp:
                    fp.write(pic.content)
                print(title, 'Download ok !!')
            except Exception as e:
                print(e)

    def main_img(self):
        for ui in range(1, 55):
            url = f'http://www.qqbizhi.com/desk/{self.type}/index_{ui}.html'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
            r = requests.get(url, headers=headers)
            lis_url = self.etre(r.text)
            for url1 in lis_url:
                rr = requests.get(url1, headers=headers)
                try:
                    for url2 in self.etre1(rr):
                        rrr = requests.get(url2, headers=headers)
                        rrr.encoding = 'cp936'
                        img = etree.HTML(rrr.text)
                        try:
                            img_url = img.xpath('//*[@id="main"]/div/div[2]/div[2]/p[1]/span[3]/a/@href')[0]
                            title = img.xpath('/html/body/div[2]/div/h1/text()')[0]
                            self.download(title, url=img_url)
                            # time.sleep(1)
                        except:
                            print(url2)
                except:
                    try:
                        rr.encoding = 'cp936'
                        sele = etree.HTML(rr.text)
                        img_url = sele.xpath('//*[@id="main"]/div/div[2]/div[2]/p[1]/span[3]/a/@href')[0]
                        title = sele.xpath('/html/body/div[2]/div/h1/text()')[0]
                        self.download(title, url=img_url)
                        # time.sleep(1)
                    except:
                        for url2 in self.etre2(rr):
                            rrr = requests.get(url2, headers=headers)
                            rrr.encoding = 'cp936'
                            img = etree.HTML(rrr.text)
                            img_url = img.xpath('//*[@id="main"]/div/div[2]/div[2]/p[1]/span[3]/a/@href')[0]
                            title = img.xpath('/html/body/div[2]/div/h1/text()')[0]
                            self.download(title, url=img_url)
                            # time.sleep(1)


if __name__ == '__main__':
    typ = ['dongman','weimei','keai','katong','qiche','youxi','shejichuangyi','qq','mingxing','3d','rili','dongwu','zhiwu','jianzhu','yingshi','tiyu','junshi','xitong','other']
    for type in typ:
        img = Qqimg(type)
        img.main_img()
