# ipquery
> 基于淘宝IP归属地查询的API(http://ip.taobao.com/service/getIpInfo.php)的python封装, 异步网络, 支持批量执行与迭代.
> 支持的python版本: python>=3.5.

## install
> **python3 setup.py**

## usage
### `ipquery.IPQuery`

> #### `def __init__(self, concurrent_limit = 0)`
>
> 参数:
> * concurrent_limit: 表示IPQuery对象的查询并发限制, 即这个IPQuery对象能同时进行的ip查询请求数量的限制, 默认为0, 表示没有限制.


> #### `async def query_ip(self, ip, batch_count = 3)`
>
> 查询ip的归属地.
>
> 参数:
> * ip: 查询的ip, 可以是一个ip字符串, 也可以是一个包含ip字符串的可迭代对象.
> * batch_count: 批量查询ip的值, 意为在此次调用中, 能同时进行的ip查询请求量, 对于单个ip无效.
>
> 返回值:
> * 如果传入的ip是ip字符串, 则返回`(ip, result)`, ip表示传入的ip值, result可能为一个`Exception`对象, 也可能是查询到的结果.
> * 如果传入的是可迭代对象, 则返回一个字典, key为每一个ip, value可能为一个`Exception`对象, 也可能是查询到的结果.

> #### `def iter(self, ip, batch_count = 3)`
> 
> 以`async for`的方式调用.
> 参数: 同`query_ip`.

### 使用示例
#### 普通调用
```python
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
```

#### `async for`
```python
import asyncio

from ipquery import IPQuery


ip_list = ("216.58.221.238", "132.232.11.22", 
           "118.24.116.236", "119.29.228.160",
           "140.205.230.3", "220.181.57.216",
           "47.95.164.112")

async def main():
    query =  IPQuery(10)
    async for ip,ip_info in query.iter(ip_list, 5):
        print(ip, ip_info)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```

