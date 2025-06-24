# Prompt Engineering with DeepSeek API

## 概述
本项目旨在利用 DeepSeek API，基于 CRISPE（能力、角色、洞察、陈述、个性、实验）框架生成响应，并增添了“内容”与“要求”。

## 特性
- **CRISPE 框架**：使用 CRISPE 框架构建详细的提示，从而能够向 DeepSeek API 发起高度定制化和有针对性的请求。
- **API 集成**：与 DeepSeek API 无缝集成，以获取符合指定参数的响应。
- **性能监控**：测量每次 API 调用生成响应所需的时间，为系统性能提供洞察。

## 前提条件
- Python 3.x
- 所需的 Python 包：`os`、`json`、`requests`、`dotenv`、`PIL`、`io`、`time`
- 有效的 DeepSeek API 密钥，应在 `.env` 文件中设置为 `DEEPSEEK_API_KEY=your_api_key`

## 配置
在项目的根目录下有 `.env` 文件，需要添加你的 DeepSeek API 密钥：
```plaintext
DEEPSEEK_API_KEY=sk-d7204degb5f46f3cab6730c1108e2defa
```

## 使用方法
1. 打开 `ori.py` 文件。
2. 你可以修改 `architecture_params` 字典，根据需要更改 CRISPE 参数。例如，你可以更改 `capacity`（能力）、`role`（角色）、`statement`（陈述）等。
3. 运行脚本：
```bash
python ori.py
```
脚本将打印 CRISPE 参数、模型的响应以及生成过程所花费的时间。

## 代码结构
- `ori.py`：主 Python 脚本，包含 `DeepSeekCRISPEGenerator` 类。该类有使用 CRISPE 框架生成响应并打印结果的方法。
- `.env`：用于存储环境变量的文件，特别是 DeepSeek API 密钥。

## 未来新增功能
预计先增加创建图片、生成流程图的功能。


## 贡献
如果你想为这个项目做出贡献，请分叉仓库并提交包含你更改的拉取请求。

## 许可证
本项目根据 [MIT 许可证](https://opensource.org/licenses/MIT) 授权。

## 联系
如果你有任何问题或建议，请随时通过 2981130749@qq.com 联系项目维护者。 