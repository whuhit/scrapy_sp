proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "H3KFV54K015071JD"
proxyPass = "73774F1F8042AD29"

proxyMeta = f"http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}"

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
}
