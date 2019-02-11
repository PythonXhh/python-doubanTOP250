import requests
import lxml.html
import csv

douban_url = 'https://movie.douban.com/top250?start={}&filter='

#定义一个函数，目的：获取网页中我们需要的数据
def get_source(url):
    response = requests.get(url)

    response.encoding = 'utf-8'

    return response.content

#定义第二个函数，目的：从这些数据中获取每一个电影相关信息
def get_every_item(source):
    selector = lxml.html.document_fromstring(source)
    #// 是可以提取某个标签所有的信息  @ 是选取属性
    movie_item_list = selector.xpath('//div[@class="info"]')
    #定义个空列表来展示信息：电影标题  国家  评分   引言
    movie_list = []
    for each_movie in movie_item_list:
        movie_dict = {}  #目的：保存电影信息，列表展示信息。如[{},{},....]
        title = each_movie.xpath('div[@class="hd"]/a/span[1][@class="title"]/text()')[0]#标题
        country = each_movie.xpath('div[@class="bd"]/p/text()')#国家
        star = each_movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]#评分
        quote = each_movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()') #引言（名句）
        if quote:
            quote = quote[0]
        else:
            quote = ''


        #保存到字典当中
        movie_dict['电影名'] = title
        movie_dict['国家'] = country
        movie_dict['评分'] = star
        movie_dict['名句'] = quote
        print(movie_dict)
        movie_list.append(movie_dict)
    return movie_list

#下载目标网页的数据
#定义第三个函数：写数据
def write_data(movie_list):
    with open('Movie_douban.csv','w',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=['电影名','评分','国家','名句'])
        writer.writeheader()#写入表头

        for each in movie_list:
            #每行来写入数据
            writer.writerow(each)

if __name__ == '__main__':

    movie_list = []

    for i in range(10):

        #获取url
        page_link = douban_url.format(i * 25)
        print(page_link)
        #有了url需要获取网页的数据-->调用获取网页数据的函数
        source = get_source(page_link)
        #有了整个网页的数据可以获取需要爬取的数据-->调用get_every_item
        movie_list += get_every_item(source)

    print(movie_list[:10])
    #写入数据
    write_data(movie_list)


