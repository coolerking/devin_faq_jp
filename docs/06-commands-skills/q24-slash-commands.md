---
qno: 24
title: "Devinにスラッシュコマンドはあるか？Ask/Sessionで違いはあるか？"
category: 06-commands-skills
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/product-guides/skills
related: []
estimated: false
---

# Q24. Devinにスラッシュコマンドはあるか？Ask/Sessionで違いはあるか？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: コマンド・スキル](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/product-guides/skills ｜ 推定なし

### 結論: **両方Yes**。スラッシュコマンドは存在し、**Ask Devinと Sessionで使えるコマンドが異なる**ほか、組織ごとに**カスタムコマンドも作れる**

参考: https://docs.devin.ai/work-with-devin/slash-commands

### 使い方

Devinのチャット入力欄で `/` をタイプすると候補メニューが表示される（Claude Code等と同じUX）:
1. `/` を入力 → 候補一覧がポップアップ
2. 絞り込み or 矢印キーで選択
3. Enterで確定すると**プロンプトテンプレートが展開される**
4. 中身をカスタマイズしてから送信

**特徴**: Devinのスラッシュコマンドは **「事前定義のプロンプトテンプレートを挿入する」仕組み**。スラッシュコマンド自体がアクションを実行するわけではなく、**入力補助**として機能する（＝ユーザが中身を編集してから送信できる）。

### 組込みスラッシュコマンド（Built-in）

| コマンド | 用途 | 使うタイミング |
|---|---|---|
| **`/plan`** | 実装前に設計・計画を立てさせる | 大きめのタスク開始時 |
| **`/implement`** | 明確な機能・変更を実装させる | 仕様が固まった後 |
| **`/review`** | コードレビュー（品質・ベスプラ・バグ検出） | PR作成前の自己チェック |
| **`/test`** | テスト作成・既存テスト実行・カバレッジ分析 | テスト強化 |
| **`/think-hard`** | 複雑な問題に深く熟考させる | 難しい設計判断・バグ原因特定 |

### Ask Devinと Sessionでコマンドの違い

**Ask Devinで使えるコマンド**（読み取り専用・コード変更不可）:

| コマンド | Ask Devinでの扱い |
|---|---|
| **`/plan`** | ✅ **本領発揮**（Plan modeと親和性高い） |
| **`/think-hard`** | ✅ 熟考モードに入る |
| **`/review`** | △ コード変更は発生しないが、分析はできる |
| `/implement` | ❌ 実装不可（SessionへのHandoffが必要） |
| `/test` | ❌ VMが必要なのでSessionへ昇格すべき |

**Sessionで使えるコマンド**（VMあり・実装可）:

| コマンド | Sessionでの扱い |
|---|---|
| `/plan` | ✅ 実装前の計画フェーズ |
| `/implement` | ✅ **本領発揮**（実装モード） |
| `/review` | ✅ 実コードをツールで読んでレビュー |
| `/test` | ✅ **本領発揮**（テスト実行可） |
| `/think-hard` | ✅ 深い思考＋実行 |

### 使い分けのベストプラクティス

```
Ask Devin: /plan で計画
    ↓ Handoff（Ask Devinが自動でプロンプト生成）
Session: /implement で実装
    ↓ 完了前に
Session: /review で自己レビュー
    ↓ 必要なら
Session: /test でテスト強化
```

### カスタムスラッシュコマンド（組織独自）

**管理場所**: Devin Webapp `Settings > Customization`（https://app.devin.ai/customization）
**権限**: `ManageOrgSettings`（組織管理者）

**できること**:
- デフォルトコマンドの編集（デフォルトに戻すことも可）
- カスタムコマンドの新規作成
- 既存カスタムの編集・削除

**カスタムコマンド例**:

| 例 | 用途 |
|---|---|
| `/deploy` | チーム独自のデプロイ手順 |
| `/security-review` | 組織のセキュリティ観点レビュー項目 |
| `/onboard` | 新メンバー向けコードベース理解ガイド |
| `/release-note` | PRから自動でリリースノート生成 |
| `/migrate` | DBマイグレーション作成の定型手順 |

**利用範囲**:
- 作成: 組織管理者のみ
- 使用: 組織の全メンバーが使える
- ユーザー個人レベルのカスタムは**ない**（組織単位）

### Claude Code等との違い早見表

| 観点 | Claude Code | Codex CLI | **Devin** |
|---|---|---|---|
| スラッシュコマンドの存在 | ✅ | ✅ | ✅ |
| 動作 | コマンド実行 | コマンド実行 | **プロンプトテンプレート展開**（編集して送信） |
| ビルトイン | `/ultrathink`等 | あり | `/plan` `/implement` `/review` `/test` `/think-hard` |
| カスタムコマンド | ユーザー/プロジェクト単位 | ✅ | **組織単位** |
| Ask / Sessionで挙動変わる | N/A（1モード） | N/A | **変わる** |

**特徴的な違い**:
- Devinのスラッシュコマンドは **"編集可能なテンプレート"** なので送信前にカスタマイズできる
- Claude Codeはコマンドが**即実行**される傾向
- Devinはスラッシュコマンド以外に **`@` メンション**（Knowledge / Skills / Playbooks参照）も併用する設計

### Skills・Playbooks・スラッシュコマンドの使い分け

| 機能 | 実体 | 発火方法 | 保存場所 | 向いてる用途 |
|---|---|---|---|---|
| **Slash Commands** | プロンプトテンプレート | `/command` | 組織設定 | **プロンプト定型化**（入力補助） |
| **Skills** | 手順書（Markdown） | 自動 or `@skills:name` | repo内 `.agents/skills/` | **再現性が必要な手順** |
| **Playbooks** | 大規模ワークフロー | 明示的に選択 | Devin側 or `.devin.md` | **複雑な一連の作業** |

**判断フロー**:
```
プロンプトを毎回書くのが面倒
    → Slash Command

repo固有の手順を固定化したい
    → Skill

複数ステップのワークフロー全体を再現したい
    → Playbook
```

### まとめ

- ✅ Devinにスラッシュコマンドあり（`/plan` `/implement` `/review` `/test` `/think-hard`）
- ✅ **組織カスタムコマンド**も作れる（`Settings > Customization`）
- ✅ **Ask Devinでは `/plan` `/think-hard`が中心**、実装系はSessionへHandoff
- ✅ **Sessionでは全コマンドが本領発揮**
- Devinは「**テンプレート展開型（送信前に編集可）**」なのが独自性
- Skills / Playbooks / Slash Commandsは**使い分け**が重要

**核心**: **ユーザ定義スラッシュコマンドでプロンプトをテンプレート化**。繰り返し指示を圧縮でき、品質も安定する。

---

[← Q23. Devinのスキルは他ツールと同じ作成方法？独自機能は？](q23-skills-creation.md) ｜ [Q25. カスタムスラッシュコマンドとスキルの違いは「管理場所」だけ？ →](q25-slash-vs-skill.md)
