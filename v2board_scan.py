import asyncio
import aiohttp

proxies = "http://127.0.0.1:10809"
v2_data_clean = []


async def fetch_v2(url: str):
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.5005.63 Safari/537.36',
    }
    index1 = url.find('https://')
    index2 = url.find('http://')
    if index1 == -1 and index2 == -1:
        url = 'https://' + url
    if url[-1] == '\n':
        url = url[:-1]
    try:
        async with aiohttp.ClientSession() as session:
            print("开始访问：", url)
            async with session.get(url=url, proxy=proxies, headers=_headers, timeout=20) as r:
                if r.status == 200:
                    # print(r.headers)
                    # print(r.status)
                    data = await r.text()
                    index = data.find("version: '1.6.1.1665920414108'")
            if index > 0:
                async with session.get(url=url + '/admin', proxy=proxies, headers=_headers, timeout=20) as res1:
                    if res1.status == 200:
                        v2_data_clean.append(url)
                        print("已找到符合目标: ", url)
    except aiohttp.ClientConnectorError as e:
        print(str(e))
    except Exception as e:
        pass


async def main():
    urls = []
    with open(r"v2bfull_url.txt", 'r', encoding='utf-8') as fp:
        for f in fp:
            urls.append(f)
    tasks = [asyncio.create_task(fetch_v2(url)) for url in urls]
    async with asyncio.Semaphore(10):
        await asyncio.gather(*tasks)
    with open('./v2board_scan_clean_plus1.txt', 'a+', encoding='utf-8') as fp1:
        for v2 in v2_data_clean:
            fp1.write(v2 + '\n')


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
