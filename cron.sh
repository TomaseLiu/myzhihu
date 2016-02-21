#! /bin/sh

export PATH=$PATH:/usr/local/bin
#source ~/.profile
cd /home/xiangzi777/workspace/python/Scrapy/zhihu
#mv active_now.log active_pre.log
nohup scrapy crawl people >> people.log 2>&1
nohup python compare_active.py >> people.log 2>&1 &

