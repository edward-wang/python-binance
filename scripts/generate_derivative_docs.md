## generate_derivative_docs.py 使用说明

### 作用
`generate_derivative_docs.py` 解析 `binance/client.py` 与 `binance/async_client.py` 中 `Client`、`AsyncClient` 的公开方法，根据方法名前缀自动归类（UM 合约、CM 合约、组合保证金、杠杆等），并生成对应分类的 Markdown 文档（位于 `api_index/*.md`），输出函数签名、核心参数、返回值等摘要。

### 依赖
- Python 3.9+
- 项目依赖已通过 `pip install -r requirements.txt` 安装
- 运行时需能够读取/写入 `api_index` 目录下的 Markdown 文件

### 使用
```bash
cd /Users/Long/Documents/quant/project/python-binance
python3 scripts/generate_derivative_docs.py
```
执行后脚本会读取客户端源码、更新各分类文档，并在控制台输出每个分类文档更新条数。

### 输出文件
- `api_index/derivative-um-futures.md`
- `api_index/derivative-cm-futures.md`
- `api_index/derivative-portfolio-margin.md`
- `api_index/margin-trading.md`

### 注意事项
- 仅处理函数名不以下划线开头的方法；若新增 API，需要在客户端类中补充 docstring，脚本才会解析参数描述。
- 判定函数所属分类依赖函数名和源码片段中的关键字，若命名不符合约定，需扩展 `determine_category`。
- Markdown 文档将保留标题以上的原有内容，其余内容会被重新生成，必要时请先备份或在版本控制中检视差异。

