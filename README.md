## 1. 简介
thsauto是一款同花顺自动下单工具，通过提供一系列的接口，可以方便地实现如查询资金账户、持仓情况、下单操作、撤单以及客户端相关控制（关闭、重启等）功能。以下是具体的接口说明及使用示例。

## 2. 启动服务示例
在命令行中可以通过以下方式启动服务：
```
python .\server.py  192.168.0.116 5000 C:\Users\match\Desktop\THS\xiadan.exe
```

其中参数依次为服务运行的主机地址、端口号以及同花顺客户端的可执行文件路径（可根据实际情况进行调整）。



## 3. 接口列表及说明
### 3.1 查询资金账户
| 说明 | value |
| --- | ---|
|接口地址：|http://<host>:<port>/balance（host和port为服务启动时指定的主机地址和端口号，以下同）|
|请求方法：|GET|
|接口说明：|用于获取资金账户相关信息|
|请求示例：|http://192.168.0.116:5000/balance|
|响应示例：|以json格式返回资金账户相关的数据，例如：|
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 具体资金账户相关字段及值
    }
}
### 3.2 查询持仓
接口地址：http://<host>:<port>/position
请求方法：GET
接口说明：查询当前持仓情况。
请求示例：http://192.168.0.116:5000/position
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 持仓相关信息字段及值
    }
}
### 3.3 买入下单
接口地址：http://<host>:<port>/buy
请求方法：GET
接口说明：进行股票买入操作，需要传入股票代码、购买数量，价格可选传（不传则按默认策略处理）。
请求参数：
stock_no：股票代码，如600000。
amount：购买数量，如100。
price：购买价格，可选，如10.00（不传时按相关业务逻辑处理）。
请求示例：http://192.168.0.116:5000/buy?stock_no=600000&price=10.00&amount=100
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 下单操作后的相关反馈信息
    }
}
### 3.4 卖出下单
接口地址：http://<host>:<port>/sell
请求方法：GET
接口说明：执行股票卖出操作，同样需传入股票代码、卖出数量，价格可选传。
请求参数：
stock_no：股票代码，例如600000。
amount：卖出数量，比如100。
price：卖出价格，可选，像10.00（不传时按对应逻辑处理）。
请求示例：http://192.168.0.116:5000/sell?stock_no=600000&price=10.00&amount=100
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 卖出操作后的相关反馈信息
    }
}
### 3.5 科创板买入下单
接口地址：http://<host>:<port>/buy/kc
请求方法：GET
接口说明：针对科创板股票进行买入下单操作，参数要求同普通买入下单类似。
请求参数：
stock_no：科创板股票代码，如688819。
amount：购买数量，如200。
price：购买价格，可选，如40.00。
请求示例：http://192.168.0.116:5000/buy/kc?stock_no=688819&price=40.00&amount=200
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 科创板买入操作反馈信息
    }
}
### 3.6 科创板卖出下单
接口地址：http://<host>:<port>/sell/kc
请求方法：GET
接口说明：用于科创板股票的卖出操作，参数设置与其他卖出接口类似。
请求参数：
stock_no：科创板股票代码，比如688819。
amount：卖出数量，例如200。
price：卖出价格，可选，像40.00。
请求示例：http://192.168.0.116:5000/sell/kc?stock_no=688819&price=40.00&amount=200
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 科创板卖出操作反馈信息
    }
}
### 3.7查询已成订单
接口地址：http://<host>:<port>/filled_orders
请求方法：GET
接口说明：获取已经成交的订单相关信息。
请求示例：http://192.168.0.116:5000/filled_orders
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 已成订单相关详细信息
    }
}
### 3.9 查询未成订单
接口地址：http://<host>:<port>/success_orders
请求方法：GET
接口说明：查询尚未成交的订单情况。
请求示例：http://192.168.0.116:5000/success_orders
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 未成订单相关信息
    }
}
### 3.10 撤单
接口地址：http://<host>:<port>/cancel_entrust
请求方法：GET
接口说明：根据委托单号进行撤单操作，需要传入委托单号。
请求参数：
entrust_no：委托单号，例如2060704404。
请求示例：http://192.168.0.116:5000/cancel_entrust?entrust_no=2060704404
响应示例：
json
{
    "code": 0,
    "status": "success",
    "data": {
        // 撤单操作后的反馈信息
    }
}
### 3.11 关闭同花顺客户端
接口地址：http://<host>:<port>/client_exit
请求方法：GET
接口说明：关闭正在运行的同花顺客户端。
请求示例：http://192.168.0.116:5000/client_exit
响应示例：
json
{
    "code": 0,
    "status": "succeed"
}
### 3.12 重启同花顺客户端
接口地址：http://<host>:<port>/client_restart
请求方法：GET
接口说明：先关闭同花顺客户端，然后重新启动它。
请求示例：http://192.168.0.116:5000/client_restart
响应示例：
json
{
    "code": 0,
    "status": "succeed"
}
### 3.13 测试接口
接口地址：http://<host>:<port>/thsauto/test
请求方法：GET
接口说明：用于执行相关测试操作（具体测试内容由auto.test()方法内部逻辑决定）。
请求示例：http://192.168.0.116:5000/thsauto/test
响应示例：
json
{}
## 4 注意事项
所有接口都需要在请求头中传入正确的 Authorization 信息，格式为 Bearer <VALID_TOKEN>，其中 <VALID_TOKEN> 的值为 DSTdqw3Poq1mBzjY8OEUv6Zjl1JAHYoc，否则会返回 401 未授权的错误。
接口调用存在一定的时间间隔限制（通过 interval 等相关机制控制），避免频繁请求导致异常情况发生。
接口传入的参数需按照要求的格式和数据类型进行传入，确保操作能正常执行。