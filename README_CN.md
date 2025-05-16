# go-zero 签名框架的 Python 实现

这是一个实现了与 go-zero 框架兼容的签名机制的 Python 包。该包允许 Python 应用程序生成可以被 go-zero 服务验证的安全签名。

## 特性

- 🔐 与 go-zero 框架的签名机制兼容
- 🔑 生成 HMAC-SHA256 签名
- 🔒 使用 RSA 公钥加密内容
- 📝 计算 MD5 指纹
- 🛡️ 支持与 go-zero 相同的安全头部格式
- 🚀 易于与现有 Python 应用程序集成

## 要求

- Python 3.6+
- pycryptodome

## 安装

您可以使用 pip 安装该包：

```bash
# 从 PyPI 安装
pip install gozero-signature-python

# 或从源码安装
git clone https://github.com/yourusername/gozero-signature-python.git
cd gozero-signature-python
pip install -r requirements.txt
pip install -e .
```

## 快速开始

以下是使用该包的简单示例：

```python
from gozero_signature import GoZeroSigner

# 您的 RSA 公钥
public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyeDYV2ieOtNDi6tuNtAbmUjN9
pTHluAU5yiKEz8826QohcxqUKP3hybZBcm60p+rUxMAJFBJ8Dt+UJ6sEMzrf1rOF
YOImVvORkXjpFU7sCJkhnLMs/kxtRzcZJG6ADUlG4GDCNcZpY/qELEvwgm2kCcHi
tGC2mO8opFFFHTR0aQIDAQAB
-----END PUBLIC KEY-----"""

# 您的密钥（可以是纯文本或 base64 编码）
key = "1234567890"

# 创建签名器实例
signer = GoZeroSigner(public_key, key)

# 要签名的数据
payload = {"msg": "hello world!"}

# 生成 POST 签名头部
signature = signer.generate_post_signature(
    method="POST",
    url="http://example.com/api/endpoint",
    payload=payload
)

# 在请求中使用签名
headers = {
    "Content-Type": "application/json",
    "X-Content-Security": signature
}

# 使用 requests 或其他 HTTP 库发送 API 请求
# requests.post("http://example.com/api/endpoint", json=payload, headers=headers)
```

## 高级用法

### 自定义头部

您可以自定义安全头部名称：

```python
signature = signer.generate_post_signature(
    method="POST",
    url="http://example.com/api/endpoint",
    payload=payload,
    header_name="X-Custom-Security"  # 可选：自定义头部名称
)
```

### 错误处理

该包包含对无效密钥和格式错误的请求的适当错误处理：

```python
try:
    signature = signer.generate_post_signature(...)
except ValueError as e:
    print(f"无效输入: {e}")
except Exception as e:
    print(f"意外错误: {e}")
```

## 测试

运行测试套件：

```bash
python -m unittest test_gozero_signature.py
```

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 关于 go-zero

go-zero 是一个具有许多内置工程实践的 Web 和 RPC 框架。本包实现了 go-zero 中用于保护 API 请求的签名功能，但适用于需要与 go-zero 服务通信的 Python 应用程序。

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。
