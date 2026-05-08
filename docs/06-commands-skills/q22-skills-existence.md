---
qno: 22
title: "Devinにスキル機能はある？（Claude Code / Codex CLI相当）"
category: 06-commands-skills
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/product-guides/skills
  - https://docs.devin.ai/product-guides/knowledge
related: []
estimated: false
---

# Q22. Devinにスキル機能はある？（Claude Code / Codex CLI相当）

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: コマンド・スキル](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/product-guides/skills / https://docs.devin.ai/product-guides/knowledge ｜ 推定なし

### 結論: **ある**。Devinには **Skills** 機能が正式に存在し、Claude Codeの `.claude/skills/` やCodex CLIのskillsと**ほぼ同じ思想**で作られている。さらに **Knowledge** と **Playbooks** が併存するので、実質3階層で記憶/ノウハウを管理できる

参考: https://docs.devin.ai/product-guides/skills

### Devinの「記憶・ノウハウ管理」機能の全体像

| 機能 | 保存場所 | 主な用途 | Claude Codeでの対応 |
|---|---|---|---|
| **Skills** | repo内の `.agents/skills/SKILL.md` | **手順書・操作方法** | `.claude/skills/` |
| **Knowledge** | Devin Web 側（repo外・組織横断） | **事実・背景情報** | （repo内の `CLAUDE.md` とは別レイヤ。repo内ガイドは後述の `AGENTS.md`） |
| **Playbooks** | Devin側（repo外） | **再利用可能なワークフロー** | カスタムコマンド |

### 1. Skills（スキル機能）

**ファイル構造**:
```
repo-root/
├── .agents/
│   └── skills/
│       ├── testing-app/
│       │   └── SKILL.md         ← このアプリの起動・テスト手順
│       ├── deploy-to-prod/
│       │   └── SKILL.md         ← 本番デプロイの手順
│       └── run-migrations/
│           ├── SKILL.md         ← マイグレーション手順
│           └── script.sh        ← 補助スクリプト
```

**SKILL.mdの中身（YAMLフロントマター + Markdown本文）**:
```markdown
---
name: testing-app
description: このアプリをローカルで起動してE2Eテストを実行する手順
triggers:
  - when the user asks to test the app
  - when verifying a new feature works
---

# Testing the App

## セットアップ
1. `pnpm install`
2. `.env.local.example` をコピーして `.env.local` を作る
3. `docker compose up -d postgres`

## テスト実行
- ユニットテスト: `pnpm test`
- E2Eテスト: `pnpm test:e2e`
```

**特徴**:
- repo内にコミット → チーム全員が共有・git履歴管理できる
- Devinがセッション開始時に自動で読み込む
- `@skill-name` メンションで明示的に呼べる

### Claude Code / Codex CLIとの違い

| 観点 | Claude Code | Codex CLI | **Devin Skills** |
|---|---|---|---|
| ディレクトリ | `.claude/skills/` | プロジェクト内で柔軟 | **`.agents/skills/`** |
| ファイル名 | `SKILL.md` | skill files | **`SKILL.md`** |
| フロントマター | YAML | YAML | **YAML** |
| 自動発見 | ◎ | ◎ | **◎** |
| トリガー（いつ呼ばれるか） | ◎ | ◎ | **◎**（`triggers:` フィールド） |
| チーム共有（git管理） | ◎ | ◎ | **◎**（repoにコミット） |
| Skillの自動提案 | △ | △ | **◎**（使える）|

### Devinならではの特長: Skill Suggestions（自動提案）

Devinは**テスト中に得た学びを自動でSKILL.md化して提案**してくれる。

- 例: Devinがアプリをテストして「dev serverは`pnpm dev`で起動、ポート3000」と学習
- → セッション終了時に「このSKILL.mdを `.agents/skills/testing-app/` に作成する？」とPRを提案
- ユーザが承認すればrepoに取り込まれる
- 参考: https://docs.devin.ai/work-with-devin/testing-and-recordings#skill-suggestions

Claude Code / Codex CLIにはないDevin独自の機能。

### 2. Knowledge（補助機能）

- Devin Webapp側に保存される（repoの外）
- 「事実・背景情報」を蓄積するのに向く
- 自動トリガーで関連セッションに注入される

**SkillsとKnowledgeの使い分け**:

| 種類 | 使う場面 | 例 |
|---|---|---|
| **Skills** | **手順・操作方法**（How） | 「アプリの起動手順」「デプロイ手順」 |
| **Knowledge** | **背景情報・ルール**（What/Why） | 「このrepoではTypeScript strict」「PRは必ずSquash merge」 |

迷ったら:
- 再現可能な手順 → Skill
- 判断基準・事実 → Knowledge

### 3. Playbooks（上位概念）

- 複数のSkill/Knowledge + 手順 + 入出力仕様を組み合わせた上位テンプレート
- 「この作業はこのPlaybookでやって」と指示するだけで全体を実行
- Webapp UIで作成・管理（`.devin.md`形式でrepo管理も可能）

**SkillsとPlaybooksの違い**:

| 観点 | Skills | Playbooks |
|---|---|---|
| 粒度 | 細かい（単一の手順書） | 大きい（タスク全体のワークフロー） |
| 発見方法 | 自動（triggers）+ @mention | ユーザが明示的に選択 |
| 保存場所 | repo内（.agents/skills/） | Devin側（or .devin.md） |
| 例 | 「テスト実行」「DBマイグレーション」 | 「新しいAPIエンドポイントを追加する一連の作業」 |

### Claude Code / Codex CLIユーザが移行する場合の対応表

| Claude Code / Codex CLI | Devinでの対応 |
|---|---|
| `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` **同じ形式** |
| `CLAUDE.md`（repo全体ガイド、Claude Code 向け） | `AGENTS.md`（**repo 内ガイド**の業界標準規格・Devin 公式サポート） |
| `CLAUDE.md`（モジュール固有） | `AGENTS.md` を各ディレクトリに配置 |

> **対応関係の整理（この FAQ の定義）**:
> - **Knowledge** … Devin Web 側（repo 外・組織横断）で保持される事実ノート。`CLAUDE.md` とは別レイヤ。
> - **AGENTS.md** … repo 内に置く Devin／他 AI エージェント向け共通ガイド。Claude Code の `CLAUDE.md` に相当する「repo 内ガイド」の Devin 公式サポート形式。
> - **SKILL.md**（`.agents/skills/<name>/SKILL.md`） … repo 内に置く**再利用可能な手順書**。Claude Code の `.claude/skills/` と同形式。
| カスタムスラッシュコマンド | Playbooks |
| 組み込みツール / プラグイン | Integrations（Linear, Jira, Slack等） |

**特に: AGENTS.md**
- repoルートやサブディレクトリに配置
- Markdownで repoのコンテキスト・規約を書く
- Cursor / Claude Code / Codex CLIも同形式をサポート（業界標準）
- 参考: https://docs.devin.ai/onboard-devin/agents-md
- **1つの `AGENTS.md` で複数のAIエージェントに同じコンテキストを渡せる**

### 推奨セットアップ（フルスクラッチ初期）

```
repo-root/
├── AGENTS.md                    ← 共通: repo全体のコンテキスト
├── .agents/
│   └── skills/
│       ├── dev-setup/SKILL.md   ← 開発環境セットアップ手順
│       ├── testing-app/SKILL.md ← テスト実行手順
│       └── deploy/SKILL.md      ← デプロイ手順
├── src/
│   └── api/
│       └── AGENTS.md            ← APIディレクトリ固有のルール
```

Devin側では:
- Knowledge: アーキテクチャ概要、使用技術、チーム規約
- Playbooks: 「新機能追加」「バグ修正」などのワークフロー

### まとめ

- ✅ Devinには **Skills機能あり**（`.agents/skills/SKILL.md`）
- ✅ Claude Code / Codex CLI のskillsと**ほぼ同じ思想・形式**
- ✅ さらに **Knowledge** と **Playbooks** があり、**3層構造**で記憶を管理できる
- ✅ **AGENTS.md** により他のAIエージェントとスキルを共有可能
- ✅ Devin独自の **Skill Suggestions** が強力
- 既存のClaude Codeプロジェクトからの移行コストは低い

**核心**: **Devin の Skill は Claude Code / Codex CLI 相当の拡張機構**。`AGENTS.md` と `.agents/skills/` で repoに永続化できる。

---

[← Q21. Devin + Copilot併用は初心者向きではない？](../05-ide-cli/q21-beginner-fitness.md) ｜ [Q23. Devinのスキルは他ツールと同じ作成方法？独自機能は？ →](q23-skills-creation.md)
