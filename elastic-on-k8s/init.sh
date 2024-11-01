#!/bin/bash
basepath=$(cd `dirname $0`;pwd)
cd $basepath
echo "########## `date '+%F %T'` ##############"
certs="/srv/certs"
image="harbor.xx.com/library/elasticsearch:6.8.5"
name="elastic"
if [ ! -d "$certs" ];then
  mkdir $certs && echo "$certs 创建成功." 
else
  echo "$certs 目录已存在."
fi
echo "######### 启动容器 ########"
docker run -itd --rm --name ${name} -v ${certs}:/srv ${image} sh
[ -f ${certs}/elastic-stack-ca.p12 ] && rm -f ${certs}/elastic-stack-ca.p12
[ -f ${certs}/elastic-certificates.p12 ] && rm -f ${certs}/elastic-certificates.p12
echo "####### 生成证书 #######"
docker exec -it ${name} ./bin/elasticsearch-certutil ca  --out /srv/elastic-stack-ca.p12 --pass '' 
docker exec -it ${name} ./bin/elasticsearch-certutil cert --ca /srv/elastic-stack-ca.p12 --out /srv/elastic-certificates.p12 --pass '' --ca-pass ''
docker stop ${name} && echo "已删除容器成功"
