proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "H1A59P91061009GD"
proxyPass = "4B3BED3EB512C474"

proxyMeta = f"http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}"

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
}
