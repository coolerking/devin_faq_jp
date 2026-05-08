---
qno: 23
title: "Devinのスキルは他ツールと同じ作成方法？独自機能は？"
category: 06-commands-skills
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/product-guides/skills
related: []
estimated: true
---

# Q23. Devinのスキルは他ツールと同じ作成方法？独自機能は？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: コマンド・スキル](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/product-guides/skills ｜ 推定あり

### 結論: **基本は業界標準（Agent Skills仕様）と同じ**。Claude Code / Cursor / Codex CLIと同形式のSKILL.mdが使える。その上にDevin独自の便利機能が載る構造

参考: https://docs.devin.ai/product-guides/skills

### 他ツールと共通（Agent Skills標準）

Devin Skillsは [Agent Skills specification](https://agentskills.io/specification)というオープンスタンダードに準拠:
- ファイル名: `SKILL.md`
- 配置: `<skills-root>/<skill-name>/SKILL.md`
- 形式: YAMLフロントマター + Markdown本文
- 標準フィールド: `name`, `description`, `allowed-tools`

### Devinが**他ツールのskillsディレクトリも読む**

Devin公式ドキュメント [Skills > Supported Skill File Locations](https://docs.devin.ai/product-guides/skills#supported-skill-file-locations) により、Devinは以下**7パス全てを各リポジトリで自動スキャン**する（原文: _"All seven paths are scanned in every repo."_）：

| パス | 想定ツール |
|---|---|
| `.agents/skills/<name>/SKILL.md` | **推奨（標準）** |
| `.github/skills/<name>/SKILL.md` | GitHub系 |
| `.claude/skills/<name>/SKILL.md` | Claude Code |
| `.cursor/skills/<name>/SKILL.md` | Cursor |
| `.codex/skills/<name>/SKILL.md` | Codex CLI |
| `.cognition/skills/<name>/SKILL.md` | Cognition（Devin） |
| `.windsurf/skills/<name>/SKILL.md` | Windsurf |

**Claude Codeで作ったskillをDevinでもそのまま使える** → ツール乗り換えコスト実質ゼロ。

### Devin独自の拡張

**独自フィールド**（標準仕様にないもの）:

| フィールド | 用途 |
|---|---|
| `argument-hint` | skill名と一緒に表示される引数ヒント |
| `triggers` | `["user", "model"]` がデフォルト。`["user"]`にするとDevinは自動起動しない |

**動的コンテンツ機能（Devin独自）**:

1. **`$ARGUMENTS` / `$0`, `$1`, ...**（引数展開）
   ```markdown
   ---
   name: deploy
   argument-hint: <environment>
   ---
   ## Deploy
   1. Run `./scripts/deploy.sh $0`
   2. Curl `https://$0.example.com/health`
   ```
   → `@skills:deploy staging` で呼ぶと `$0`が `staging` に置換

2. **`` !`command` ``**（シェル実行結果の埋め込み）
   ```markdown
   - Branch: !`git branch --show-current`
   - Last commit: !`git log --oneline -1`
   ```
   → skill起動時に実際の値が埋め込まれる

### Skillの作成方法（4つ）

**方法1: 手書き**（Claude Code等と同じ）
- `.agents/skills/<name>/SKILL.md` を自分で書いてコミット

**方法2: Devinに作ってもらう**
- セッション内で「〜のskillを作って」と指示
- DevinがSKILL.mdを書いてPR化

**方法3: 🆕 Skill Suggestions（Devin独自の目玉機能）**
- Devinがテスト中・作業中に得た学びを**自動でSKILL.md化して提案**
- セッションタイムラインに「Create PR」ボタン付きで表示
- ユーザが承認するとrepoにPR作成される
- 参考: https://docs.devin.ai/work-with-devin/testing-and-recordings#skill-suggestions

**方法4: Test Mode経由**
- `test this app` のような指示でテストモードに入る
- テストで得た知見を自動でskill化して提案

### Skill発見の仕組み（二重スキャン）

| 経路 | タイミング | 用途 |
|---|---|---|
| **Indexed repos**（バックエンドで事前インデックス） | セッション開始前 | repo clone前から参照可能 |
| **Cloned repos**（ディスク上のファイルをスキャン） | clone完了時 | 最新ブランチの内容が反映 |

ディスク上の内容がインデックスを上書きするので、ブランチ切替時の事故なし。

### 他ツールとの違い早見表

| 観点 | Claude Code | Cursor | Codex CLI | **Devin** |
|---|---|---|---|---|
| SKILL.md形式（Agent Skills準拠） | ✅ | ✅ | ✅ | ✅ |
| 他ツールのskillsディレクトリも読む | ❌ | ❌ | ❌ | ✅ **7パス全スキャン** |
| `$ARGUMENTS` 引数展開 | △ | △ | △ | ✅ |
| `` !`command` `` 実行結果埋込 | ❌ | ❌ | ❌ | ✅ |
| `triggers` フィールド | △ | △ | △ | ✅ |
| **自動スキル提案（Suggest + PR化）** | ❌ | ❌ | ❌ | ✅ **目玉機能** |
| Test Modeからの自動生成 | ❌ | ❌ | ❌ | ✅ |

### まとめ

- **基本は業界標準（Agent Skills仕様）** → Claude Code等と互換
- Devinは**7パス全スキャン**で他ツールのskillsも流用可
- **動的コンテンツ機能**（`$ARGUMENTS`, `` !`command` ``）が独自
- **Skill Suggestions + Create PRボタン**がDevin最大の独自機能
- Test Modeからの自動skill化も独自
- 「他ツールと同じ作り方で書ける」+「Devinだけの便利機能もある」の両取り

**核心**: **Skillは「トリガー条件 + 実行手順」を Markdownで書くだけ**。repo 内に置けばチーム全員と Devinで共有される。

---

[← Q22. Devinにスキル機能はある？（Claude Code / Codex CLI相当）](q22-skills-existence.md) ｜ [Q24. Devinにスラッシュコマンドはあるか？Ask/Sessionで違いはあるか？ →](q24-slash-commands.md)
