#!/bin/bash
#30 0 * * * sh /root/vector/es_index.sh 2>&1 > /root/vector/es_index.log
ES_USER="elastic"
ES_PASS="test@123,"
suffix_day=`date -d "2 days ago" +%Y-%m-%d`
prefix_index=(applogs test-applogs ingress-logs)
es_url="https://es-dev.xxx.net"
echo "#########`date`###########"
for index in ${prefix_index[@]};do
   curl -u ${ES_USER}:${ES_PASS} -XDELETE --header 'Content-Type: application/json' ${es_url}/${index}-${suffix_day} 2>1 /dev/null
   echo -n "\n"
   echo -n "`date` ${index}-${suffix_day} delete success...\n"
#curl -u ${ES_USER}:${ES_PASS} -XGET --header 'Content-Type: application/json' http://10.11.3.205:9200/_cat/health?v
done

