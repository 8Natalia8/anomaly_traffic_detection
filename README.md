1. Файл **task_anomaly_detection_dbscan_orig.ipynb** содержит ноутбук с применением алг-ов _dbscan, hdbscan, KMeans_ на оригинальном датафрейме.
2. Файл **task_anomaly_detection_dbscan_ip_info.ipynb** содержит ноутбук с применением алг-ов _dbscan, hdbscan, GaussianMixture, KMeans_ на датафрейме с оригинальными признаками и дополнительными, которые содержат доп инф-ию для ipv4 адресов: ['timezone', 'status', 'mobile', 'proxy', 'hosting'].
3. Файл **part_10.csv** - оригинальный датасет.
4. Файл **VALID_IP_INFO.csv** содержит доп инфу для валидных ipv4 адресов.
5. Файл **Test_original_result.csv** содержит итоговый результат для входного набора данных,исключая только полностью пустые строки.
6. В  целом, получила **кол-во классов = _48 (для метода без исп. доп признаков, файл под п.1.) и 47/48_ (для метода с доп. признаками, файл под п.2.)** на dbscan, kmeans.
7. **docker container** лежит здесь: https://hub.docker.com/r/5849/pt_task
