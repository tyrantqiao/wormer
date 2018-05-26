#!/usr/bin/python
# coding:utf-8
from scrapy import cmdline

# spilt() when is none, the whitespace string and empty string will be removed
cmdline.execute("scrapy crawl urls".split())
