1. Файл **task_anomaly_detection_dbscan_orig.ipynb** содержит ноутбук с применением алг-ов _dbscan, hdbscan, GaussianMixture, KMeans_ на оригинальном датафрейме.
2. Файл **task_anomaly_detection_dbscan_ip_info.ipynb** содержит ноутбук с применением алг-ов _dbscan, hdbscan, GaussianMixture, KMeans_ на датафрейме с оригинальными признаками и дополнительными, которые содержат инф-ию ipv4 адресов: ['timezone', 'status', 'mobile', 'proxy', 'hosting'].
3. Файл **part_10.csv** - оригинальный датасет.
4. Файл **VALID_IP_INFO.csv** содержит доп инфу для валидных ipv4 адресов.
5. **CLuster_label_dist.png**, **DBSCAN_47classes_ip_info.png**, **timezone_proxy_variable.png**, **timezone_useragent_responsecode.png** - картинки с визуализацией работы DBSCAN.
6. В целом, получила **кол-во классов = _46 (для метода без исп. доп признаков, файл под п.1.) и 47/48_(включая тот, лэйбл которого=-1) (для метода с доп. признаками, файл под п.2.)** на dbscan, kmeans.
