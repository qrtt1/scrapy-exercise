
fetch from pttweb

```
scrapy crawl pttweb -a board=Soft_Job -a max_fetch=2
```

set the local storage path

```
scrapy crawl pttweb -a board=Soft_Job -a max_fetch=1 -a local_storage_path=/tmp/pttweb
```
