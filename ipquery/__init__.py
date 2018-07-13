import aiohttp
import json
import asyncio
from asyncio import FIRST_COMPLETED, Semaphore

class _FinishException(Exception):
    pass

class _IPQueryIterable(object):
    def __init__(self, query, ip_list, batch_count):
        self.ip_list = ip_list
        self._batch_count = batch_count
        self._query = query
        self._futs = set()
        self._started = False
        self._stopped = False
        self._done_fut_gen = None
        self._stop_ip_gen = False
    
    def _ip_generator(self):
            yield from self.ip_list
    
    def _done_fu_generator(self, done_futs):
        yield from done_futs
    
    def _fill_future(self):
        try:
            while len(self._futs) < self._batch_count:
                ip = self._ip_gen.send(None)
                fut = asyncio.ensure_future(self._query._query_one(ip))
                self._futs.add(fut)
        except StopIteration:
            self._stop_ip_gen = True
            
    def _get_result(self):
        fu = self._done_fut_gen.send(None)
        exception = fu.exception()
        return exception if exception is not None else fu.result()

    async def __aiter__(self):
        return self
    
    async def __anext__(self):
        try:
            return await self._once()
        except _FinishException:
            raise StopAsyncIteration()
    
    async def _once(self):
        if not self._started:
            self._started = True
            self._ip_gen = self._ip_generator()
            self._fill_future()
        elif self._done_fut_gen:
            try:
                return self._get_result()
            except:
                self._done_fut_gen = None
                if self._stopped:
                    raise _FinishException()
        done, pending = await asyncio.wait(self._futs, return_when = FIRST_COMPLETED)
        self._done_fut_gen = self._done_fu_generator(done)
        if not pending and self._stop_ip_gen:
            self._stopped = True
        else:
            self._futs = pending
        if not self._stop_ip_gen:
            self._fill_future()
            if not self._futs and not pending:
                self._stopped = True
        return self._get_result()
        
class IPQuery(object):
    
    def __init__(self, concurrent_limit = 0):
        self._futs = set()
        self.smaphore = Semaphore(concurrent_limit) if concurrent_limit > 0 else None
    
    async def query_ip(self, ip, batch_count = 3):
        if isinstance(ip, str):
            return await self._query_one(ip)
        else:
            rtn = dict()
            query_iterable = _IPQueryIterable(self, ip, batch_count)
            try:
                while True:
                    finished_ip, ip_info = await query_iterable._once()
                    rtn[finished_ip] = ip_info
            except _FinishException:
                pass
            return rtn

    def iter(self, ip, batch_count = 3):
        if isinstance(ip, str):
            ip = (ip, )
        return _IPQueryIterable(self, ip, batch_count)
    
    async def _query_one(self, ip):
        if self.smaphore:
            await self.smaphore.acquire()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://ip.taobao.com/service/getIpInfo.php", params = {"ip": ip}) as resp:
                    rtn_data = json.loads(await resp.text())
                    if rtn_data["code"] == 0:
                        return ip, rtn_data['data']
        except asyncio.CancelledError:
            raise
        except Exception as e:
            return ip, e
        finally:
            if self.smaphore:
                self.smaphore.release()
        