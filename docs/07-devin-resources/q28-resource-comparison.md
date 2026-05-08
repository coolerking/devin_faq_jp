---
qno: 28
title: "Repo Setup / Knowledge / Playbookの違いは？（表で整理）"
category: 07-devin-resources
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/
related: []
estimated: false
---

# Q28. Repo Setup / Knowledge / Playbookの違いは？（表で整理）

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: Devinリソース](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/ (Machine/Knowledge/Playbook) ｜ 推定なし

### 結論: **3つは役割が完全に違う**。混同すると「自動適用されない環境構築」「毎回忘れられる規約」「手動起動不可なタスク定型」といった事故が起きる

### Repo Setup / Knowledge / Playbook の3象限

```mermaid
flowchart TD
    subgraph RS["Repo Setup：環境"]
        RS1[セッション起動時に<br/>自動実行]
        RS2[Install/Lint/Run]
    end
    subgraph KN["Knowledge：事実"]
        KN1[常時参照<br/>ルール・常識]
        KN2[コーディング規約/禁事項]
    end
    subgraph PB["Playbook：タスク手順"]
        PB1[明示呼出し時に展開]
        PB2[反復タスクの手順書]
    end
    Session[Devin Session] --> RS
    Session --> KN
    Session --> PB
    RS -.自動.-> Auto[自動適用]
    KN -.文脈ごと.-> Hit[参照]
    PB -.手動.-> Call[@で呼び出す]
    style RS fill:#7ED321,color:#fff
    style KN fill:#F5A623,color:#fff
    style PB fill:#4A90E2,color:#fff
```

> 覚え方: **環境 = Repo Setup / 事実 = Knowledge / タスク手順 = Playbook**

### ⭐ 1枚で見る比較表（本丸）

| 項目 | **Repo Setup** | **Knowledge** | **Playbook** |
|---|---|---|---|
| **一言で** | 環境構築コマンド集 | 恒常的な事実・ルール集 | 繰り返しタスクの手順書 |
| **書く内容** | シェルコマンド | 自然言語の事実・規約 | 自然言語の手順＋制約 |
| **保存場所** | Devin's Machine設定 | Knowledge管理画面 / AGENTS.md | Playbooks管理画面 / `.devin.md`ファイル |
| **適用タイミング** | **セッション開始時に自動実行** | **関連トピック検知時に自動注入** | **ユーザが手動でアタッチ** |
| **範囲** | Devin's Machine（全セッション） | repo / user / org単位で指定可 | セッション単位（選択制） |
| **起動方法** | 自動（常時） | 自動（文脈に応じて） | 手動（Playbookドロップダウン） |
| **変更頻度** | 低（環境変更時） | 中（プロジェクト規約変更時） | 中（タスクが増えるたび） |
| **共有** | Devin's Machine単位 | Knowledge ACL（user/team/org） | Enterprise playbook化で組織共有 |
| **バージョン管理** | Machine Version History | Knowledge履歴 | Playbook更新履歴 |

### 書く内容の具体例（並べて比較）

| カテゴリ | Repo Setupに書く | Knowledgeに書く | Playbookに書く |
|---|---|---|---|
| **依存インストール** | `npm ci` `pip install -r requirements.txt` | ❌ | ❌ |
| **DB起動** | `docker compose up -d db` `npm run migrate` | ❌ | ❌ |
| **dev server起動** | `npm run dev &` | ❌ | ❌ |
| **環境変数** | `source .envrc`（中身はSecrets） | ❌ | ❌ |
| **lintコマンド** | `npm run lint` | ❌ | ❌ |
| **プロジェクトの技術スタック** | ❌ | 「Next.js 14 / Prisma / PostgreSQL」 | ❌ |
| **命名規則** | ❌ | 「DBテーブル名は複数形 snake_case」 | ❌ |
| **デプロイ手順（事実）** | ❌ | 「main → stagingに自動、prodは手動承認」 | ❌ |
| **テストアカウント** | ❌ | 「`test+devin@example.com` / Secretsにパスワード」 | ❌ |
| **禁止事項** | ❌ | 「masterブランチに直接pushしない」 | （タスク固有はこちらに） |
| **TDDサイクル手順** | ❌ | ❌ | Red→Green→Refactorの各ステップ |
| **DB Migration手順** | ❌ | ❌ | 変更案→dry run→apply→rollback |
| **Dependency Upgrade手順** | ❌ | ❌ | outdated→patch→minor→major各段階 |
| **Bug Triage手順** | ❌ | ❌ | 再現→原因→テスト追加→修正→PR |

### 起動方式の違い（ここが一番重要）

```
Repo Setup:
  [セッション開始] → 自動で実行 → 環境が整った状態でDevinが動き出す
  ※手動アタッチ不要、忘れることがない

Knowledge:
  [セッション中] → Devinがトピックを認識 → 該当Knowledgeを自動注入
  ※「このrepoは ESM only」等が必要な瞬間に思い出される

Playbook:
  [セッション作成画面] → ユーザがドロップダウンから選択 → 青いpillが表示されればアタッチ成功
  ※選ばないと発動しない、用途が明確なタスク専用
```

### 使い分けのフローチャート

```
書きたい内容は「コマンドを実行する」こと？
  Yes → Repo Setup
  No ↓

書きたい内容は「プロジェクトの事実・規約・禁止事項」？
  Yes → Knowledge（チーム全員に関わるならorg scope）
  No ↓

書きたい内容は「特定のタスクを進める手順」？
  Yes → Playbook
  No → AGENTS.md に一般ガイドとして書く
```

### 3つを組み合わせた実例（TDDプロジェクトの場合）

```
Repo Setup（自動実行される）:
  - npm ci
  - docker compose up -d db
  - npm run migrate
  - npm run seed:test
  - npm run dev &

Knowledge（自動注入される）:
  - "このprojectはTDDで進める"
  - "lintはbiome、型はTypeScript strict"
  - "テストはVitest、カバレッジ80%以上"
  - "PRはconventional commitsで"

Playbook（タスクごとに選ぶ）:
  - "TDD Cycle": Red→Green→Refactor を繰り返し
  - "DB Migration": Prismaのschema変更→migrate→検証
  - "Bug Triage": Issue→再現→修正→PR

ユーザ依頼例:
  「Playbook『TDD Cycle』で `calculateTax` を実装して」
  → Repo Setupで環境構築済み
  → Knowledge が「TDD採用・Vitest・biome」を自動注入
  → Playbook が「Red→Green→Refactor」を明示的に指示
  → すべて整った状態でDevinがタスクを進める
```

### 混同しがちな典型的ミスと対処

#### ミス1: Playbookに環境構築を書く
- **症状**: 毎回Playbookをアタッチし忘れると環境が整わない
- **対処**: Repo Setupに移動（自動実行される）

#### ミス2: Knowledgeにタスク手順を書く
- **症状**: Devinが手順を毎回守らない、省略する
- **対処**: Playbookに移動（明示的にアタッチすればDevinが厳密に従う）

#### ミス3: Repo Setupに命名規則を書く
- **症状**: シェルコマンド化できない情報で混乱
- **対処**: Knowledgeに移動（自然言語で書ける）

#### ミス4: AGENTS.mdに全部詰める
- **症状**: ファイルが肥大化、関係ない情報もセッション毎に読み込まれる
- **対処**: 3分類に分けてそれぞれに振る

### スコープ・共有範囲の違い

| 機能 | スコープ選択 | 他人との共有 |
|---|---|---|
| **Repo Setup** | Devin's Machine単位（repoごと） | Machineに紐付くユーザ/チーム全員 |
| **Knowledge** | User / Team / Org / Repo単位 | ACLで細かく制御可 |
| **Playbook** | Personal / Enterprise | Enterprise Playbookで組織共有 |

### 更新・管理のしやすさ

| 観点 | Repo Setup | Knowledge | Playbook |
|---|---|---|---|
| 作成 | Webappで8ステップ入力 | Webapp / AGENTS.md | Webapp / `.devin.md`ファイル |
| 編集 | Webapp（即反映） | Webapp（即反映） | Webapp（即反映）、セッション直前にもインライン編集可 |
| 差分管理 | Machine Version History | 変更履歴あり | 更新履歴あり |
| テスト | 「Finish Setup」で検証 | Ask Devinで動作確認 | 小タスクで試行 |

### 「どれに入れる？」判定早見リスト

| 書きたいこと | 入れ場所 |
|---|---|
| `npm install`、`pip install` | Repo Setup |
| `docker compose up` | Repo Setup |
| migrationコマンド | Repo Setup |
| dev server起動コマンド | Repo Setup |
| 「lintはbiomeを使う」 | Knowledge |
| 「テストカバレッジは80%以上」 | Knowledge |
| 「DBスキーマの命名規則」 | Knowledge |
| 「本番にDevinから接続しない」 | Knowledge |
| 「TDDで進める」（方針） | Knowledge |
| 「TDDサイクルの具体的な手順」 | Playbook |
| 「Dependency Upgradeの手順」 | Playbook |
| 「新しいサービスをscaffoldする手順」 | Playbook |
| 「Stripe決済統合の手順」 | Playbook |
| 「Hotfix workflowの手順」 | Playbook |
| Secretの中身（パスワード等） | Secrets（これも別の4つ目の仕組み） |

### 4つ目の仕組み: Secrets（参考）

厳密には**Secrets**も独立した仕組みで、上記3つと並ぶ4つ目の要素:

| Secrets | |
|---|---|
| 書く内容 | **機密値**（パスワード、APIキー、トークン） |
| 適用 | 環境変数として自動注入 |
| スコープ | User / Org / Repo |
| 特徴 | 値は暗号化保存、ログ・コードに出力されない |

→ **「接続先」はKnowledge、「接続情報（パスワード）」はSecrets**、という分け方。

### 全体像（5階層）

```
┌─────────────────────────────────────────┐
│ Secrets      : 機密値（パスワード等）              │ ← 自動注入（環境変数）
├─────────────────────────────────────────┤
│ Repo Setup   : 環境構築コマンド                 │ ← 自動実行（セッション開始時）
├─────────────────────────────────────────┤
│ Knowledge    : 事実・規約・禁止事項              │ ← 自動注入（文脈に応じて）
├─────────────────────────────────────────┤
│ AGENTS.md    : repo直下の共通ガイド             │ ← 自動読込（常時）
├─────────────────────────────────────────┤
│ Playbook     : 繰り返しタスクの手順書            │ ← 手動アタッチ（選択式）
└─────────────────────────────────────────┘
```

### 「迷ったら」の判定3問

1. **シェルで実行できるコマンドか？** → **Yes: Repo Setup**
2. **プロジェクトに関する常に真な事実か？** → **Yes: Knowledge**
3. **何度もやる複雑タスクの手順か？** → **Yes: Playbook**

どれでもない → AGENTS.mdに書く or そのセッションのプロンプトに直接書く

### まとめ（超短縮版）

| 機能 | 一言 | キーワード |
|---|---|---|
| **Repo Setup** | 環境を整えるコマンド | 自動実行・コマンド |
| **Knowledge** | プロジェクトの知恵袋 | 自動注入・事実 |
| **Playbook** | タスクの段取り書 | 手動アタッチ・手順 |

**初心者へのおすすめ導入順**:
1. **Repo Setupを完成させる**（これができないとどのセッションも時間を浪費する）
2. **AGENTS.mdに最低限のルールを書く**（lint、test、命名など）
3. Knowledgeに**プロジェクトの文脈**を追加（1-3項目で良い）
4. 繰り返しタスクが見えてきたら**Playbookを1-2個作る**
5. 慣れたらSecretsで秘密情報を整理

**核心**: 3つは**役割も起動方式もスコープも全部違う**。それぞれの得意を活かして配置すれば、Devinは**毎回正しい状態で・正しい知識を持って・正しい手順で**動ける。逆にどれか1つにすべてを詰めると、他の2つがサボって本来の力が出ない。

---

[← Q27. Playbookとは？開発環境構築にしか使っていなかったが、本来の用途と違う？](q27-playbook.md) ｜ [Q29. Devin Wikiとは？Codex CLI/Claude CodeのようなローカルRAGか？Ask/Sessionで問い合わせるrepoは事前登録が必要？ →](q29-devin-wiki.md)
