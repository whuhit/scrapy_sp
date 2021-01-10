for i in range(1,500):
    url = f"https://order.mi.com/api/getSaleStore.php?city_id={i}&jsonpcallback=jQuery1113011367795492988364_1610176062889&_={int(time.time()*1000)}"
    r = requests.get(url,headers=headers, proxies=proxies)
    if r.status_code == 200:
        with open(f"data/{i}.json", 'w') as f:
            f.write(r.text)
print(r)