Файл task_anomaly_detection_dbscan_ip_info.ipynb содержит ноутбук с применением алг-ов dbscan, hdbscan, GaussianMixture, KMeans на оригинальном датафрейме.
Файл task_anomaly_detection_dbscan_ip_info.ipynb содержит ноутбук с применением алг-ов dbscan, hdbscan, GaussianMixture, KMeans на датафрейме с оригинальными признаками и дополнительными, которые содержат инф-ию ipv4 адресов: ['timezone', 'status', 'mobile', 'proxy', 'hosting'].
В целом, получила кол-во классов = 47 на dbscan, kmeans.
Файл part_10.csv - оригинальный датасет.
Файл VALID_IP_INFO.csv содержит доп инфу для валидных ipv4 адресов.
CLuster_label_dist.png, DBSCAN_47classes_ip_info.png, timezone_proxy_variable.png, timezone_useragent_responsecode.png - картинки с визуализацией работы DBSCAN
