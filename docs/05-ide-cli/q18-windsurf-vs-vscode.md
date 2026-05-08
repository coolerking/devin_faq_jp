---
qno: 18
title: "DevinのIDEはWindsurf？VSCode？"
category: 05-ide-cli
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/work-with-devin/devin-session-tools
related: []
estimated: true
---

# Q18. DevinのIDEはWindsurf？VSCode？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: IDE・エディタ・CLI](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/work-with-devin/devin-session-tools ｜ 推定あり

### 結論: **VSCode**（正確には「VSCodeベースの組み込みIDE」）。**Windsurfではない**（ただし2025年7月〜WindsurfはCognition傘下の兄弟製品）

Windsurfは**2025年7月にCognition社が買収した**AI IDEで、Devinと同じ会社の**兄弟製品**（元はCodeium社が開発）。ただし、**DevinのセッションIDEそのものはWindsurfではなくVSCodeベース**で、VSCodeをDevinのVM上で動かしてブラウザ/Desktop経由で開く仕組み。将来的にはDevin×Windsurfの統合が進む見込み（公式発表: https://cognition.ai/blog/windsurf ）。

参考:
- https://docs.devin.ai/work-with-devin/devin-session-tools
- https://docs.devin.ai/collaborate-with-devin/vscode-profiles

### Devin IDEの仕様
- **VSCode ベースのエディタ**（OSS 版 `code-server` / `VSCodium` 系と推定。Cognition 公式は基盤実装の詳細を明示していない）が Devin の VM 内で動作
- ブラウザからアクセス or Desktop連携でローカルVSCodeと接続可能
- Devinが操作しているrepoを**一緒に見られる・編集できる**
- 拡張機能・テーマ・キーバインド等、**個人のVSCodeプロファイルを読み込める**

### Devin IDEとよく混同されるツール

| ツール | 提供元 | Devinとの関係 |
|---|---|---|
| **VSCode** | Microsoft | **DevinのIDEはこれがベース** |
| **Windsurf** | **Cognition**（2025/7買収、元Codeium） | **同社の兄弟AI IDE製品**、Devinセッション内のIDE本体ではない |
| **Cursor** | Anysphere | **別製品（競合のAI IDE）**、Devinとは無関係 |
| **Claude Code** | Anthropic | **別製品（競合のCLI型AI）** |
| **Devin's Browser** | Cognition | Devinの中のChromeブラウザ（IDEではない） |
| **Devin's Shell** | Cognition | Devinの中のターミナル（IDEではない） |

→ **Windsurf / Cursorは「ユーザが操作するAI IDE」であってDevinセッション内蔵のIDEではない**（WindsurfはCognition傘下なので将来的な統合は期待される）。

### Devin IDEの開き方

#### ブラウザから
1. DevinセッションのUIで **「IDE」タブ** / **「Open in VSCode」ボタン**
2. 新しいタブに**VSCodeの画面**が開く
3. Devinが作業中のワークスペースをそのまま見る

#### ローカルVSCodeから
1. Devin公式の**VSCode拡張機能**をインストール
2. ローカルVSCodeから**リモートでDevin VMに接続**
3. ローカルのキーバインド・拡張機能で作業可能

### VSCode Profileのアップロード

1. ローカルVSCodeで`Profiles > Export`
2. Devin Webappの **Settings > VSCode Profiles** からアップロード
3. Devinセッションを開くと**自動で読み込まれる**

参考: https://docs.devin.ai/collaborate-with-devin/vscode-profiles

### VSCodeベースゆえの制限

- **Microsoft独自拡張の一部**（Pylance等、ライセンス制約）は動かない
- **GitHub Copilot**（他社競合のため動作しない）

これは**VSCode公式ではなくOSS版（code-server / VSCodium系）**を使っているため。Pylance等が必要なら代替（basedpyright等）を使う。

### Devin × 外部AI IDEの併用

| 外部IDE | Devinとの連携方法 |
|---|---|
| **Windsurf**（Cognition傘下） | MCPでDevinを呼び出し可能。将来は深い統合が計画されている |
| **Cursor** | MCPでDevinを呼び出し可能 |
| **Claude Desktop** | Devin MCPで連携 |
| **ローカルVSCode** | Devin公式拡張 + プロファイル同期 |
| **JetBrains** | 直接統合は弱い、外部からDevin APIを叩く |

### まとめ

| 観点 | 結論 |
|---|---|
| DevinのIDE | **VSCode**（OSS版ベース）、ブラウザ or ローカル拡張で開く |
| Windsurfとの関係 | **同社兄弟製品**（2025/7にCognitionが買収）。ただしDevinセッション内蔵IDEはVSCodeベースで、Windsurfそのものではない |
| Cursorとの関係 | 無関係（別製品）、ただしMCP経由でDevin呼び出しは可能 |
| プロファイル | **自分のVSCode設定をアップロード可能** |
| 制限 | MS独自拡張（Pylance / Copilot等）は動かないことあり |
| 本質 | Devinは**標準的なVSCodeを提供**、ユーザ側の好みのIDEは自由 |

**核心**: DevinのセッションIDE = **VSCode**ベース。Windsurfは**2025年7月にCognitionが買収**した兄弟製品（AI IDE）、CursorはAnysphere社の競合製品。いずれもDevinセッション内蔵IDEそのものではないが、**MCP経由で併用可能**（Windsurfは将来の統合計画あり）。

---

[← Q17. DevinにKanban相当の機能はある？](../04-github-scm/q17-kanban.md) ｜ [Q19. 最新のVSCodeはGitHub Copilot Chatが標準でついてくるが、Devinもそうなる？ →](q19-vscode-copilot-bundled.md)
