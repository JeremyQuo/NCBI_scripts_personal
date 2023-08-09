import requests
from bs4 import BeautifulSoup
import argparse
# Created by GUO ZHIHAO
# E-mail: zhihaguo-c@my.cityu.edu.hk
# Create in 2023-08
def generate_url_list(input_string):
    # input_string='GCA_020872695.1'
    input_string = input_string.replace("\n", "")
    input_string_template=input_string[:3]+'/'+input_string[4:7]+'/'+input_string[7:10]+'/'+input_string[10:13]+'/'
    url = 'https://ftp.ncbi.nlm.nih.gov/genomes/all/'+input_string_template

    response = requests.get(url)
    content = response.text

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(content, 'html.parser')

    # 提取<a>标签中的链接
    links = soup.find_all('a')
    result_list=[]
    # 打印提取到的链接
    for link in links:
        if input_string in link.text:
            href = link.get('href')
            response = requests.get(url+href)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            # 提取<a>标签中的链接
            new_links = soup.find_all('a')
            for temp in new_links:
                if temp.text[-6:] == 'fna.gz' or temp.text[-6:] == 'fa.gz':
                    whole_url=url+href+temp.text
                    result_list.append(whole_url)
            if result_list is None or len(result_list)==0:
                Warning(input_string+" is lost")
            return result_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', default="assemble.txt")
    parser.add_argument('-o','--output', default="result.txt")
    args = parser.parse_args()
    f = open(args.input, 'r')
    f_out = open(args.output, 'w+')
    for line in f:
        new_line_list = generate_url_list(line)
        if new_line_list is not None:
            for item in new_line_list:
                f_out.write(item + '\n')
    f_out.close()
    # global npd_file
