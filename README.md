## 用途

基于S3上传事件调用Lambda对指定CloudFront PoP点进行预热

## 配置指引

1. Lambda环境变量
    * cloudfront_cname: xxxxx.cloudfront.net
    * alt_cname: 备用域名，比如static.example.com

1. Lambda内存、超时时间
    * 内存 128M
    * 超时时间 15min，测试数据20MB MP4，~2s

2. Lambda requests layer
    * `arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-requests:26`
    * https://github.com/keithrozario/Klayers

3. S3事件配置

## 验证方式

可使用如下curl命令验证预热结果
```
curl -H "host:vod.ensean.space" http://d3wov59arknox.ams50-c1.cloudfront.net/mp4/What-is-AWS.mp4 -v -o /dev/null
```

## Reference
[nwcd-samples cloudfront warmup](https://github.com/nwcd-samples/cloudfront-prewarm/)
