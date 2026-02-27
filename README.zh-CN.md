# Polymarket Bot

<div align="center">

![Rust](https://img.shields.io/badge/python-3.12+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

[English](README.md) • [简体中文](#polymarket-bot)

</div>

别纠结过程，盯紧结果。

这是我做交易的方式，你呢？

我想你也是这么想的，那就跑起来吧。

## 重要说明

本软件是一个 **跟单机器人**，用于在 Polymarket 上复制指定钱包的持仓。当前版本（v1）不包含内置策略逻辑、风控或盈利保证。盈亏取决于跟单对象、你的仓位比例以及市场环境。你可以在现有代码基础上扩展或改写，加入自己的风控与策略。更新版本尚未公开；后续会持续提供更新与支持。

### 联系方式

- [讨论区](../../discussions)
- [WhatsApp](https://wa.me/16286666724?text=Hello%20there)
- [Telegram](https://t.me/angel_10_x)
- [Discord](https://discord.com/users/1114372741672488990)

## 为什么用 Python？

我至今还记得决定写这个 Polymarket 机器人的那一刻。

一开始，我站在每个开发者都再熟悉不过的岔路口——该把「快、稳、聪明」这件事交给哪门语言？TypeScript 用规整的生态和丰富的工具链在招手；别的语言也在强调性能或严格类型。但总觉得，没有哪一门像是这段旅程该用的那一个。

因为要做的不是又一个脚本。

而是一个会动的系统——能观察市场、解读信号、应对不确定性，在概率如潮水般变化的场域里精准执行。

所以我选了 Python。

Python 给的不仅是语法，更是 *节奏*。代码像是想法直接变成动作。当我开始把行情接入、事件解析和策略逻辑串在一起时，Python 让我能按着好奇心的速度推进：想法几分钟成原型，策略一夜之间迭代，重构像轻描淡写的修改，而不是大动干戈。

但更深一层的原因是「智能」。

做 Polymarket 机器人，不只是发交易，更是理解上下文——解析情绪、建模概率、快速试强化信号、验证假设。Python 的生态把一整间实验室摆在手边：数据分析、统计库、异步框架、机器学习，让项目从「交易机器人」变成可做实验的平台。

TypeScript 可以把 API 编排得很优雅。

Python 能帮我 *思考*。

还有一点是 Python 的可读性带来的安心。几周后策略叠了好几层、决策路径缠在一起，我还能打开文件就读懂当时的自己。代码读起来像对话笔记，而不是刻在石头上的指令。这种清晰让迭代敢放手做。

而在预测市场里，迭代就是生存。

Python 也成了研究和实盘之间的桥。我可以做策略模拟、可视化结果、调参数，再把结论立刻写回机器人的运行逻辑。实验和生产的边界被抹掉了。

最让我意外的是情绪那一面。

深夜调 WebSocket 流、看概率数字跳动、第一次看到自动成交——Python 让这些时刻更像在合作，而不是在和语言较劲。语言退到背景里，只剩下问题本身和好奇心。

这个 Polymarket 机器人后来不止是自动化。

它成了一连串决策、风险和认知演进的记录。

选 Python 不是要否定 TypeScript 或其他语言，而是选最贴合问题特质的媒介——动态、探索、数据驱动、能随时调整。

最后，Python 不止驱动了机器人。

它驱动了让这个机器人得以存在的那段探索过程。

## 安装与配置

1. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

2. **环境变量**

   将 `.env.example` 复制为 `.env`，并填写你的 Polymarket 凭证：

   ```
   POLYMARKET_PRIVATE_KEY=你的私钥
   POLYMARKET_PROXY_ADDRESS=你的代理钱包地址
   ```

3. **配置文件**

   在项目根目录创建或编辑 `config.json`：

   ```json
   {
       "wallets_to_track": ["0x..."],
       "copy_percentage": 1.0,
       "rate_limit": 25,
       "poll_interval": 0.5,
       "trading_enabled": true
   }
   ```

### 配置项说明

| 配置项               | 说明                                                                 |
|----------------------|----------------------------------------------------------------------|
| `wallets_to_track`   | 要跟单的钱包地址列表。                                               |
| `copy_percentage`    | 相对跟单对象的仓位比例（如 `1.0` = 100%，`0.5` = 50%）。            |
| `rate_limit`         | 每 10 秒内最大 API 请求数（默认 25）。                               |
| `poll_interval`      | 两次持仓检查的间隔秒数（默认 0.5；最小 0.3）。数值越小，发现变动越快。 |
| `trading_enabled`    | 为 `false` 时仅记录将要执行的操作，不实际下单（模拟运行）。           |

## 运行

在项目根目录执行：

```bash
python main.py
```

或以模块方式运行：

```bash
python -m polymarket_copy_trader
```

按 `Ctrl+C` 停止。

### 控制台界面

启动 Web 界面后可启停机器人并查看实时日志：

```bash
python -m uvicorn dashboard.app:app --reload --host 0.0.0.0 --port 8000
```

在浏览器打开 [http://localhost:8000](http://localhost:8000)。侧栏会列出所有机器人（跟单、套利、体育博彩、做市）。目前仅「跟单」可用；使用 **启动** / **停止** 和 **配置** 操作，日志会实时刷新。其他机器人显示「即将推出」。

## 许可证

见 [LICENSE](LICENSE)。
