---
qno: 27
title: "Playbookとは？開発環境構築にしか使っていなかったが、本来の用途と違う？"
category: 07-devin-resources
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/product-guides/playbooks
related: []
estimated: true
---

# Q27. Playbookとは？開発環境構築にしか使っていなかったが、本来の用途と違う？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: Devinリソース](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/product-guides/playbooks ｜ 推定あり

### 結論: **開発環境構築はPlaybookの用途ではない**。それは **Repo Setup** の仕事。Playbookは「**繰り返し依頼する複雑なタスクのための再利用可能なプロンプト**」

### Playbook ライフサイクル

```mermaid
flowchart LR
    Create[作成<br/>Admin UI] --> Edit[編集<br/>手順・例・注意点]
    Edit --> Publish[公開]
    Publish --> Call[呼び出し<br/>Session内で<br/>"@playbook-name"]
    Call --> Exec[Devinが展開<br/>・実行]
    Exec --> Result[PR/結果]
    Result -.改善.-> Edit
    style Create fill:#7ED321,color:#fff
    style Call fill:#4A90E2,color:#fff
    style Result fill:#F5A623,color:#fff
```

「これまで開発環境構築にしか使っていなかった」は、**役割分担がずれていた**可能性が高いです。環境構築は**Repo Setup**、Playbookは**タスク自体の手順書**として使うのが本来の用途。

参考: https://docs.devin.ai/product-guides/creating-playbooks

### Playbookの正体

#### 定義（公式）
> A playbook is like a custom system prompt for a repeated task.

つまり**「同じ種類のタスクを何度も頼むとき、毎回書くプロンプトを定型化したもの」**。

#### 向いているケース
- **同じプロンプトを複数セッションで使い回す**
- **Devinに同じ注意事項を何度もリマインドしている**
- **他のメンバー（または自分の別プロジェクト）でも同じタスクをやる**

#### Playbookの構造（推奨セクション）

```markdown
# <Playbook名>

## Outcome（目的）
何を達成したいか

## Procedure（手順）
1. Setup: ...
2. Main task: ...
3. Delivery: ...
  （各行 action verbで、Mutually Exclusive Collectively Exhaustive）

## Specifications（完了条件・事後条件）
Devin完了後に成立しているべき状態

## Advice（ヒント・priorsの修正）
Devinが間違えがちな点、好みの進め方

## Forbidden Actions（禁止事項）
絶対にやってほしくないこと

## Required from User（ユーザに要求する情報）
事前に必要な入力
```

### ⚠️ 混同しやすい3兄弟との使い分け

Devinには似た役割のものが3つあり、最初は区別が難しい:

| 機能 | 何を書く | いつ参照される | 例 |
|---|---|---|---|
| **Repo Setup** | **環境構築コマンド**（install / migrate / run） | セッション開始時に**自動実行** | `npm ci`、`docker compose up -d db`、`npm run dev` |
| **Knowledge** | プロジェクトの**恒常的な事実・ルール** | 関連トピック検知時に**自動注入** | 「このrepoはESM only」「APIはOpenAPI 3.1」 |
| **Playbook** | **繰り返し行うタスクの手順書** | ユーザが**明示的にアタッチ**して起動 | 「TDDサイクル」「新ライブラリ統合」「DB migration」 |

#### 開発環境構築は **Repo Setup** の仕事

「新規Devinセッション開始時に `npm install && docker compose up -d db && npm run migrate` を実行」は**Repo Setupの8ステップ**（Install / Maintain / Lint / Test / Run / Notes等）に書くべき内容。Playbookに書くと**毎回手動でアタッチする必要**があり本末転倒。

→ **もし「Playbook」に環境構築を書いていたなら、それは Repo Setupに移すべき**。

### Playbookの典型的な用途（本来の使い方）

#### 1. タスク手順の自動化
- **TDD Cycle**: Red → Green → Refactorを固定
- **DB Migration**: スキーマ変更 → migration生成 → dry run → apply → rollback手順
- **Bug Triage**: 再現手順 → 原因特定 → テスト追加 → 修正 → PR
- **Dependency Upgrade**: `npm outdated` → 候補選定 → 段階的更新 → テスト → PR
- **Security Patch**: 脆弱性調査 → 影響範囲 → パッチ → テスト → PR

#### 2. 統合作業の定型化
- **Stripe決済統合**: Stripe SDKをインストール → Webhook設定 → テストカード検証
- **Sentry導入**: パッケージ追加 → DSN設定 → サンプル送信 → アラート確認
- **OpenTelemetry導入**: SDK → exporter → tracer provider → span確認

#### 3. 運用タスク
- **Hotfix Workflow**: `main`→`hotfix/x` → 最小修正 → デプロイ → cherry-pick
- **Release PR**: changelog生成 → version bump → tag → release note
- **Data Migration**: 抽出 → 変換 → 投入 → 整合性チェック

#### 4. ドキュメント生成
- **API Doc Update**: OpenAPIから再生成 → 差分確認 → PR
- **Changelog**: コミット集計 → カテゴリ分類 → PR

#### 5. コードレビュー補助
- **PR Review Prep**: 変更内容要約 → テストカバレッジ確認 → レビュー観点リスト作成

#### 6. データ処理系
- **Data Ingestion to Redshift**: S3 → 前処理 → COPY → 検証
- **Analytics Query生成**: 要件 → SQL → 可視化

### 具体例: TDD Cycle Playbook

```markdown
# TDD Cycle for New Function

## Outcome
与えられた関数要件をテスト駆動開発で実装し、PRを作成する

## Procedure
1. 要件を1つ選択して失敗するテストを1つだけ書く（実装は書かない）
2. `npm test -- <file>` で失敗を確認
3. 最小限の実装（仮実装OK）でパスさせる
4. `npm test` でグリーンを確認
5. 重複除去・命名改善でリファクタ
6. `npm test` で通り続けることを確認
7. 次の要件でStep 1に戻る
8. 全要件達成でlint/typecheckを実行
9. ブランチを作成してcommit、PR作成

## Specifications
- 全要件に対応するテストが存在
- 全テストパス
- lint/typecheck クリーン
- PR作成済み、CIグリーン

## Advice
- 一度に複数テストを書かない
- Refactor中にテスト追加しない
- 仮実装→三角測量で一般化する

## Forbidden Actions
- テストなしで実装を書く
- 既存テストの期待値を変更する
- PRのbaseブランチをmaster/mainに直接commit

## Required from User
- 対象関数名
- 要件リスト
- テストフレームワーク（Jest / Vitest / pytest 等）
```

### 具体例: Dependency Upgrade Playbook

```markdown
# Safe Dependency Upgrade

## Outcome
指定パッケージ群を安全にアップグレードし、テストを通してPR化

## Procedure
1. `npm outdated` で候補確認
2. patch版を一括更新、テスト実行
3. minor版を1つずつ更新、都度テスト
4. major版は**1つずつ独立ブランチ**で検証（別PR）
5. 破壊的変更あれば、該当コードを修正
6. `npm audit` で脆弱性なしを確認
7. PR作成、CHANGELOG相当の変更点を記載

## Specifications
- 全テストパス
- npm audit でhigh以上の脆弱性なし
- PRに更新前後のバージョン表記

## Forbidden Actions
- majorバージョンを複数同時に上げる
- package-lock.jsonを手動編集
```

### Playbookの作成・利用方法

#### 作成
1. Devin Webapp: `Settings > Playbooks > Create a new Playbook`
   URL: https://app.devin.ai/settings/playbooks/create
2. または `.devin.md` ファイルを作成 → セッション開始時にドラッグ&ドロップ

#### 利用（セッションへのアタッチ）
1. 新規セッション作成画面
2. **Playbookドロップダウン**から選択
3. ドロップダウンの横に**青いpill**が表示されればアタッチ成功
4. タスク内容を書いてセッション開始

#### アタッチ中のヒント
- **複数Playbookを同時アタッチ可能**
- インラインで直前に編集もできる（そのセッションだけの調整）

### Playbookの粒度の目安

| 粒度 | 例 | Playbook向き？ |
|---|---|---|
| 超細かい | 「1ファイルにimport追加」 | ✕ Devinが直接やれる |
| 細かい | 「関数の命名変更」 | △ Knowledgeで十分 |
| **中** | **「TDDで新関数実装」** | **◎** |
| **大きい** | **「新しいマイクロサービスをscaffoldしてCI/CDまで」** | **◎** |
| 巨大 | 「新サービス企画から実装・運用まで」 | ✕ 分割すべき |

**目安**: 「**1セッションで完結する、手順化できる複雑タスク**」が最適。

### Knowledgeとの使い分け（よくある混乱）

#### Knowledge向き
- 「このrepoのAPIはOpenAPI 3.1で書く」（**事実**）
- 「lintはbiomeを使う」（**ルール**）
- 「DBテーブル名は複数形」（**規約**）
- 「デプロイは main → staging → prod」（**恒常的情報**）
- 「テスト用アカウントは `test+devin@example.com`」（**認証情報の所在**）

→ **Playbookに書くべきではない**（毎回アタッチしないと伝わらなくなる）

#### Playbook向き
- 「TDDで関数を実装するときの手順」（**タスク手順**）
- 「データ移行ジョブを書くときの流れ」（**タスク手順**）
- 「セキュリティパッチを適用するときの流れ」（**タスク手順**）

→ **タスクを起動するときに選択**して使う

### Repo Setupとの使い分け（本質の整理）

#### Repo Setup向き
- 「`npm ci`」「`docker compose up -d db`」（**環境構築コマンド**）
- 「session開始時に毎回DBリセット」（**毎回の前提条件整備**）
- 「`npm run dev` で起動」（**サービス起動**）

→ **自動実行される**ので手動アタッチ不要

#### Playbook向き
- 「DB migrationを書く手順」（**タスクの進め方**）
- 「新ライブラリを統合する手順」（**タスクの進め方**）

→ 環境は整っている前提で、**タスク自体の手順**を書く

### Playbookの設計原則

#### 1. 手順は imperative
- ✅「Run `npm test`」「Commit with message」
- ❌「Maybe run tests」「Try to commit」

#### 2. MECE（もれなく、ダブりなく）を狙う
- 各ステップが**重複せず、全体をカバー**
- If/elseや loopも書ける（条件分岐）

#### 3. 制約を明示する
- **Forbidden Actions** で「やってはいけないこと」を明示
- **Specifications** で「完了の定義」を明示

#### 4. priorsを修正する
- Devinの**標準動作を変えたい**部分を**Advice**に書く
- 例: 「親切な過剰実装はせず、要件通りだけ」

#### 5. 過度に細かくしない
- Devinの**問題解決能力を殺さない**程度に
- 手順 10-20ステップ、優れたPlaybookは50ステップ超のこともある

### これまでの使い方は間違い？

| あなたがPlaybookに書いていたもの | 本来の置き場所 | 対処 |
|---|---|---|
| `npm install` 等の環境構築コマンド | **Repo Setup** の「Install Dependencies」 | Repo Setupに移動 |
| DB起動・migration | **Repo Setup** の「Install/Maintain Dependencies」 | Repo Setupに移動 |
| dev server起動 | **Repo Setup** の「Run Local App」 | Repo Setupに移動 |
| 環境変数の設定 | **Secrets** + Repo Setup（`.envrc` 等） | Secretsに移動 |
| プロジェクトの命名規則 | **Knowledge** or **AGENTS.md** | Knowledgeに移動 |

→ **Playbookに環境構築を書くと、毎回手動アタッチが必要で非効率**。自動実行されるRepo Setupに移すと**全セッションで自動適用**になる。

### 移行の手順（今のPlaybookを整理する）

#### Step 1: 現状のPlaybookを分類
既存Playbookの内容を3つに分類:
1. 環境構築コマンド → **Repo Setup** へ
2. プロジェクト事実・ルール → **Knowledge** or AGENTS.mdへ
3. 純粋なタスク手順 → **Playbookに残す**

#### Step 2: Repo Setupを整備
- Settings > Devin's Machine > Modify repo setup
- 8ステップに環境構築コマンドを配分
- Finish Setupで Machine Snapshotを更新

#### Step 3: Knowledge / AGENTS.mdに事実を移す
- 命名規則、使用ライブラリ、デプロイ手順などを整理
- Knowledgeは管理画面から登録、AGENTS.mdはrepo直下に置く

#### Step 4: 本来のタスクPlaybookを作成
- TDD Cycle / Dependency Upgrade / DB Migrationなど、**繰り返すタスク**を定型化
- 5-10個程度でスタート

#### Step 5: チーム共有
- 成功したPlaybookはEnterprise playbook化で組織共有
- 類似タスクが増えたらPlaybookを増やす

### まとめ

| 観点 | 結論 |
|---|---|
| Playbookの正体 | **繰り返しタスクのための再利用可能プロンプト**（カスタムシステムプロンプト） |
| 開発環境構築に使うべきか | **❌ 違う**、それは **Repo Setup** の仕事 |
| プロジェクト事実・ルール | **❌ 違う**、それは **Knowledge** or AGENTS.md |
| 正しい用途 | **TDD Cycle / Bug Triage / Dependency Upgrade / 統合作業 / 運用タスク** 等 |
| 発動方法 | **手動アタッチ**（セッション開始時にドロップダウンから選択） |
| 構造 | Procedure / Specifications / Advice / Forbidden Actions / Required from User |
| 使いどころの判断 | 「**同じプロンプトを2回以上書いていたら**Playbook化」 |

**今のPlaybookの見直し推奨アクション**:
1. 既存Playbookを開いて、**環境構築コマンドは Repo Setupへ移動**
2. **プロジェクトの事実・ルールは Knowledgeへ移動**
3. 残った「タスク手順」だけをPlaybookとして残す
4. 必要に応じて TDD Cycle、DB Migration などの**新規タスクPlaybook**を追加

**核心メッセージ**: Playbookは「**タスクを繰り返すための道具**」であって、「環境を整える道具」ではない。**環境 = Repo Setup、事実 = Knowledge、タスク手順 = Playbook** の三角形を理解すると、Devinの本来の力が引き出せます。

**核心**: **Playbookは繰り返し運用手順のテンプレート**。Org / Personal スコープで粒度を管理できる。

---

[← Q26. Machine Configurationは Repo Setupのこと？言語別のDevin向きリポ構成は？](q26-machine-config.md) ｜ [Q28. Repo Setup / Knowledge / Playbookの違いは？（表で整理） →](q28-resource-comparison.md)
