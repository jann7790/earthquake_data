# Earthquake Data 
## Overview
從 https://scweb.cwa.gov.tw/zh-tw/earthquake/data
下載台北、台南、新竹、台中顯著有感地震和小區域有感地震。

![](image.png)


1. 局發地震(local earthquake)：最大有感半徑小於100公里。

2. 小區域地震(small-felt-area earthquake)：最大有感半徑從100公里到200公里。

3. 稍顯著地震(moderate earthquake)：最大有感半徑從 200公里到300公里。

4. 顯著地震(remarkable earthquake)：最大有感半徑300公里及以上。
## File Structure


小區域有感地震，官方未提供詳細 txt 檔案，從網頁 extract 出來的資料，下載後轉換成json格式，並存放在`earthquake_reginal_data/`資料夾中。

    url = f"https://scweb.cwa.gov.tw/zh-tw/earthquake/details/{YYYYMMDDHHMMSS}{magnitude}"

顯著有感地震，官方提供txt檔案，下載後轉換成json格式，並存放在`earthquake_data/json/`資料夾中。

    url = f"https://scweb.cwa.gov.tw/zh-tw/earthquake/download?file=%2FdrawTrace%2Foutcome%2F{year}%2F{year}{earthquake_id}.txt"

