---
qno: 19
title: "最新のVSCodeはGitHub Copilot Chatが標準でついてくるが、Devinもそうなる？"
category: 05-ide-cli
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/collaborate-with-devin/vscode-profiles
related: []
estimated: true
---

# Q19. 最新のVSCodeはGitHub Copilot Chatが標準でついてくるが、Devinもそうなる？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: IDE・エディタ・CLI](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/collaborate-with-devin/vscode-profiles ｜ 推定あり

### 結論: **ならない見込み（少なくとも近い将来は）**。理由は **(1) DevinのIDEはMicrosoftブランドのVSCodeではなくOSS版ベース** **(2) Copilotは Devinの直接競合** **(3) Devinセッション自体が既にAIエージェント**

### 背景: VSCodeとCopilot Chatの現状

- 2025年、GitHub Copilot Chatの**VSCode拡張ソースがOSS化**
- 最新のMicrosoftブランドVSCodeには**Copilot Chat拡張が標準で同梱**（無料枠も提供）

→ これは**Microsoftブランドの公式VSCodeに限る**話。

### DevinのIDEは「OSS版VSCode」

DevinのIDEが使っているのはOSSベース:
- **code-server**（Coder社）
- **VSCodium**
- **独自のVSCode派生**

#### OSS版VSCodeとMicrosoftブランド版の違い

| 観点 | **Microsoftブランド VSCode** | **OSS版 VSCode** |
|---|---|---|
| **Copilot Chat 同梱** | ✅（2025〜） | ❌ |
| Microsoft Marketplace アクセス | ✅ | ❌（Open VSX Registry経由） |
| Pylance / Remote / C++ 等の独占拡張 | ✅ | ❌ |
| GitHub 統合（MS認証） | 深い | 限定的 |
| テレメトリ | あり | なし/抑制 |
| ライセンス | プロプライエタリ | MIT |

→ **DevinのIDEは構造的に「Copilot Chat込み」のMS VSCodeと違うビルド**。

### DevinがCopilotを公式に入れる可能性は低い

理由:
1. **Copilotは競合製品**（Cognition vs GitHub/Microsoft）
2. **Devinセッション自体がAIエージェント** → IDE内AIは多重化
3. **課金の衝突** → Copilotサブスクの別途管理負荷
4. **安全性・秘密情報** → Copilotへの送信プライバシー問題
5. **製品戦略** → 独自AI機能を強化する方向

### ユーザ視点の整理

| 役割 | 提供元 |
|---|---|
| **コード生成の主役** | **Devinエージェント本体** |
| IDE内のインライン補完 | 基本なし |
| チャット形式のAI | Devinセッションのメッセージ欄 |
| エディタ上でのLLM編集 | なし |

### Copilotが使いたいならどうする？

1. **ローカルVSCodeで作業 → Devin APIにタスク発注**
2. **Cursor / Windsurfで作業 → MCP経由でDevin呼び出し**
3. **Devinを「非IDE補完」として割り切って使う**

### 将来可能性

| シナリオ | 可能性 |
|---|---|
| 現行維持（Copilot統合なし） | **最も高い** |
| ユーザのCopilot BYO | 中程度 |
| 競合との統合 | 低 |
| Devin独自のinline AI | 中長期で**あり得る** |

### まとめ

| 観点 | 結論 |
|---|---|
| DevinにCopilot Chat同梱？ | **ならない見込み** |
| 理由 | OSS版VSCodeベース / Copilotは競合 / Devin自体がエージェント |
| MSブランドVSCodeの標準同梱は関係するか | 構造的に別ビルドなので**波及しない** |
| Copilot使いたいユーザへの対処 | **ローカルVSCodeで自分のCopilot** + **Devinはタスク発注** |
| 将来可能性 | **Devin自前のinline AI**機能が出る可能性の方が高い |

**核心**: DevinのIDEは**OSS版VSCode**を使っているため、**MSブランドVSCodeの「Copilot同梱」とは無縁**。Copilotは競合製品なので公式に入る可能性は限りなく低い。

---

[← Q18. DevinのIDEはWindsurf？VSCode？](q18-windsurf-vs-vscode.md) ｜ [Q20. GitHub Copilotと併用すべき？フルスクラッチでの役割分担は？ →](q20-copilot-coexistence.md)
