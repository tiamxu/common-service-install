# 介绍
官网：https://www.elastic.co/docs
截止目前最新版本：8.15 
测试版本：6.8、7.15、8.14 
Elasticsearch8.14不需要手动开启认证，安装时候自动引导开启
# 目标
在k8s中部署 elasticsearch 集群，存储使用ceph 块存储。并配置
- 配置集群身份认证。
- 集群节点间通信加密。
- 配置使用https访问集群。
- 用户鉴权

# 配置
## 生成证书
```
./bin/elasticsearch-certutil ca  --out /tmp/elastic-stack-ca.p12 --pass ''
./bin/elasticsearch-certutil cert --ca /tmp/elastic-stack-ca.p12 --out /tmp/elastic-certificates.p12 --pass '' --ca-pass ''
sh init.sh
```

## 查看证书
```
openssl pkcs12 -info -nodes -in certs/elastic-stack-ca.p12
```
## 查看证书有效期
```
openssl pkcs12 -in certs/elastic-stack-ca.p12 -nodes -nokeys -clcerts | openssl x509 -enddate -noout
```
# 部署
```

kubectl create ns middleware
# 生成集群间通信证书
bash init.sh

#kubectl create cm es-cluster-cert --from-file=certs/elastic-certificates.p12 --from-file=certs/elastic-stack-ca.p12  -n middleware
kubectl create cm es-cluster-cert --from-file=certs/ -n middleware

kubectl apply -f es-cm.yaml
kubectl apply -f es-sts.yaml
kubectl apply -f es-svc.yaml
kubectl exec -it es-cluster-0 -n middleware -- sh
./bin/elasticsearch-setup-passwords interactive
```
# 配置文件说明
```
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate 
xpack.security.transport.ssl.client_authentication: required
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
```
verification_mode有3种模式： 
- full，其为默认值，除了验证证书的有效性外，还会检查节点的 hostname 或者 ip。
- certificate，持有有效证书的节点才能加入到集群，所以需要将生成的证书复制到所有的节点上。
- none，不需要认证就可以加入到集群中。一般在调试的时候使用，强烈建议不要在生产环境中使用
