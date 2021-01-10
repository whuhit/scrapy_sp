proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "H73I853PG0X5191D"
proxyPass = "575793DC6FB278F2"

proxyMeta = f"http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}"

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
}
