#-*- coding:utf-8 -*-
'''
Created on 2018-06-27

@author: ranyixu
'''
from ipquery import IPQuery
import asyncio

ip_list = ("216.58.221.238", "132.232.11.22", 
           "118.24.116.236", "119.29.228.160",
           "140.205.230.3", "220.181.57.216",
           "47.95.164.112")

async def main():
    query =  IPQuery()
    result = await query.query_ip(ip_list)
    print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    