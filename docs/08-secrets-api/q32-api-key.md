---
qno: 32
title: "Devin API Keyの使い方は？（API操作・MCP・Skill経由）"
category: 08-secrets-api
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/api-reference/
related: []
estimated: false
---

# Q32. Devin API Keyの使い方は？（API操作・MCP・Skill経由）

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: Secrets・API](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/api-reference/ ｜ 推定なし

### 結論: **API Keyを発行すればDevinを完全にAPIで操作可能**。MCPサーバ（`Devin MCP`）も公式提供されていて、**別のDevinセッションや他のAIエージェントからDevinを操作**できる。Skillからも呼び出し可能

参考:
- https://docs.devin.ai/api-reference/
- https://docs.devin.ai/work-with-devin/devin-mcp

### Devin API Keyとは

#### 概要
- **REST APIでDevinを操作するための認証トークン**
- 個人用・サービスユーザ用の2種類
- **Max / Teams / Enterprise** で利用可（プラン要確認）

#### 発行場所
- Settings > API Keys（個人用）
- Enterprise admin はAPIで**Service User API Key**も発行可

#### 種類

| 種類 | 用途 | 発行方法 |
|---|---|---|
| **Personal API Key / PAT** | 自分の操作を自動化 | Settings > API Keys（※PATは closed beta） |
| **Service User API Key** | CI/CD・Bot・Integration用 | Settings > Service Usersで作成 |

#### 認証方式
```
Authorization: Bearer cog_XXXXXXXX
```

### APIで可能な操作

主なエンドポイント（**v3 API は `{org_id}` をパスパラメータとして必ず含む**。v1 API は個人/サービスユーザキーで `{org_id}` 不要の形式）:

| カテゴリ | エンドポイント（v3） | エンドポイント（v1） | 用途 |
|---|---|---|---|
| **Session** 作成 | `POST /v3/organizations/{org_id}/sessions` | `POST /v1/sessions` | 新規セッション作成 |
| Session 参照 | `GET /v3/organizations/{org_id}/sessions/{session_id}` | `GET /v1/session/{session_id}` | セッション状態確認 |
| Session メッセージ | `POST /v3/organizations/{org_id}/sessions/{session_id}/messages` | `POST /v1/session/{session_id}/message` | 進行中セッションへメッセージ送信 |
| Session 終了 | `DELETE /v3/organizations/{org_id}/sessions/{session_id}` | `DELETE /v1/sessions/{session_id}` | セッション終了 |
| **Schedule** | `POST /v3/organizations/{org_id}/schedules` 他 CRUD | — | スケジュール作成・編集・削除 |
| **Secret** | `POST /v3/organizations/{org_id}/secrets` 他 CRUD | — | Secret 管理（値は出力不可） |
| **Playbook** | v3 CRUD | — | Playbook の作成・更新 |
| **Knowledge** | v3 CRUD | — | Knowledge の作成・更新 |
| **Machine** | v3 経由 | — | Repo Setup / Machine Version 制御 |
| **Tags / Metrics** | v3 経由 | — | 課金・使用量の分析 |

> 最新のパスは公式リファレンスで確認: [Devin API v3](https://docs.devin.ai/api-reference/v3) / [Devin API v1](https://docs.devin.ai/api-reference/v1)

→ **UIでできることはほぼAPI経由でも可能**。

### 典型的なAPI使用例

#### 例1: 外部システムからDevinにタスク依頼
```bash
curl -X POST https://api.devin.ai/v3/organizations/$ORG_ID/sessions \
  -H "Authorization: Bearer $DEVIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "このrepoで最新の依存関係更新を実行してPRを作成",
    "repositories": ["coolerking/mfg_drone"],
    "playbook_id": "playbook-xxxxx"
  }'
```

#### 例2: CI/CDから起動
- GitHub Actions / GitLab CI からdevin Sessionを立ち上げ
- PR作成、Issueトリアージ等を自動化

#### 例3: Slack Botから起動
- SlackコマンドでDevinセッション起動
- 結果をチャンネルに返す

#### 例4: ダッシュボード構築
- 全Sessionの状態を自社ダッシュボードで一覧
- コスト / 進捗 / 失敗率を可視化

### MCP経由でのDevin操作

#### Devin MCPサーバ
> The Devin MCP server provides programmatic access to Devin's functionality.

**MCPサーバ**（`Devin MCP`）を経由して、**他のAIエージェント（Claude Desktop、Cursor、Windsurf、別のDevinセッション等）からDevinを操作**できる。

#### MCPで利用可能な主な機能
- **セッション管理**: 作成・検索・メッセージ送信・完了待ち・イベント確認
- **Playbook管理**: CRUD
- **Knowledge管理**: CRUD
- **Schedule管理**: CRUD
- **Wiki / Semantic Search**: コードベース理解
- **Integration / MCP Status**: 連携状態確認

#### MCP導入イメージ

```
Claude Desktop (ユーザのローカル)
      │
      │ MCP経由
      ▼
   Devin MCP
      │
      │ Devin API
      ▼
  Devin Session (新VM起動・作業)
```

→ **ChatからDevinを起動、結果を取得**が可能。

#### Devin自身もMCPを使える
DevinセッションからもMCP経由で**別のDevinセッションを起動可能**。つまり、**DevinがDevin自身を操作する（親子・再帰的）**構成が実現できる。

### Skill経由でのDevin操作

#### Skillとは（復習）
- repoに置く**タスク手順書**（`.agents/skills/`等）
- Devinが該当シチュエーションで自動参照

#### Skillで「別Devinセッションを起動」
Skill内に**MCPツールの呼び出し手順**を書けば、Devinが**MCP経由で別セッションを起動**できる:

```yaml
---
name: parallel-refactor
description: 大規模リファクタリングを複数サブセッションで並列実行
---

## 手順
1. 対象ファイル群を機能別グループに分割
2. 各グループごとに `devin_mcp` の `create_session` ツールで**別Devinセッションを起動**
3. 各サブセッションにリファクタ指示を送信
4. すべての完了を待機（`wait_on_session`）
5. 結果を集約してPRマージ
```

→ **親セッションが複数の子セッションを並列管理**する「マルチエージェント構成」が実現可能。

### 連鎖のパターン

#### 1. 手動UI → API手動呼び出し
- curl / Postmanでテスト
- 自動化の第一歩

#### 2. CI/CD → API呼び出し
- GitHub Actions等から起動
- 夜間バッチ的なDevin使い

#### 3. 他のエージェント → MCP → Devin
- Claude Desktop / Cursor からDevinを発注
- 複数エージェントの協調

#### 4. Devin → Skill → MCP → 子Devin
- **親Devinが子Devinを起動**
- 並列化・タスク分割
- ただし**各子セッションは別VM**で独立

### 制約・注意事項

#### 💰 コスト
- **API経由でも通常セッションと同じ課金**
- スクリプトで大量起動すると一気に消費
- **上限・アラートをEnterprise側で設定**

#### 🔑 API Key管理
- **最小権限のService User**を作って付与
- 退職者・異動時に**即ローテ**
- **Secretsに登録**して他セッションから呼び出せるようにしてもOK

#### 🔀 並列の注意
- 同じrepoで複数子セッションがPRを作ると**コンフリクト**
- **タスク分割**（ファイル/機能単位で重ならないように）
- マージ順序を親セッションで管理

#### 🔒 認証範囲
- APIキーのスコープ（Personal / Org / Service）を理解
- **Personal API Key**では組織全体の操作はできない場合あり

#### 📊 監査
- API経由のSession起動は**API key attribution**で追跡可能
- Run as（誰のセッションとして計上するか）を明示

#### 🔁 再帰的起動に注意
- Devin→Devinの連鎖が深くなると**コスト爆発+デバッグ困難**
- 深度を明示的に制限する設計にする

### 典型的なユースケース

| ユースケース | 技術 |
|---|---|
| Issueトリアージ自動化 | GitHub webhook → API → Session起動 |
| 夜間バッチ | Schedule + API or 単独Schedule |
| Slackコマンド | Slack Bot → API → Session |
| 外部ダッシュボード | API経由で全Session取得 → 可視化 |
| チームbot | Slack/Teams → MCP/API → Devin |
| マルチエージェント協調 | Claude Desktop + Devin MCP |
| 大規模リファクタリング | 親Devin + 子Devin群（MCP経由） |
| テスト自動化 | CI → API → Devin Test Mode |

### MCP / Skill / APIの使い分け

| 用途 | 推奨手段 |
|---|---|
| **UIで使う人間** | Webアプリ |
| **他のAIエージェントから呼び出す** | **Devin MCP** |
| **CI/CDやBotから呼び出す** | **REST API** |
| **Devinが別Devinを起動** | **MCP経由（Skill内で指示）** |
| **スケジュール実行** | Schedule機能 |
| **Playbook/Knowledge管理** | API or MCP（IaC化したい場合） |

### まとめ

| 観点 | 結論 |
|---|---|
| API Key | **REST APIでDevinを完全操作可能**、Personal / Service の2種 |
| 可能な操作 | Session作成・Schedule・Playbook・Knowledge・Secret等ほぼ全機能 |
| MCP | **Devin MCPサーバ提供**、他AIエージェント・別Devinから操作可 |
| Skill | Skillから**MCPツール呼び出し**で子Devinを起動可能 |
| 典型用途 | CI/CD起動・Slack Bot・マルチエージェント・夜間バッチ |
| 注意 | **コスト・API Keyローテ・並列コンフリクト・再帰爆発**に注意 |

**核心**: API Keyひとつで**Devinは完全に自動化・統合可能**。MCP経由で**他エージェントがDevinを呼ぶ**、**DevinがDevinを呼ぶ**まで拡張できる。初心者はまずAPI Keyで1つのセッション起動スクリプトを書いてみる → 慣れたらMCP連携、という段階導入が推奨。

---

[← Q31. Secretsの使い方は？（Org/Personalスコープ・同一キー重複時の挙動）](q31-secrets.md) ｜ [Q33. API Keyタブの「Legacy」は今後なくなる？変更される？ →](q33-api-legacy.md)
