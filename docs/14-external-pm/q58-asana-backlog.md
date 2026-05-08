---
qno: 58
title: "AsanaやBacklogとの連携は可能？"
category: 14-external-pm
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/integrations/
  - https://developers.asana.com
related: []
estimated: false
---

# Q58. AsanaやBacklogとの連携は可能？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: 外部連携（Slack・PM）](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/integrations/ / https://developers.asana.com ｜ 推定なし

### 結論: **両方とも連携可能**、ただし **Native統合ではなくMCP経由**。Asanaは公式MCPサーバ、BacklogはNulab公式MCPサーバあり

参考: https://docs.devin.ai/integrations/overview

### Devinの Project Management 統合状況

| ツール | 統合方法 | 公式サポート |
|---|---|---|
| **Jira** | **Native統合** | ⭐⭐⭐ Devin公式 |
| **Linear** | **Native統合** | ⭐⭐⭐ Devin公式 |
| **Asana** | **MCP経由**（Asana公式MCPサーバ） | ⭐⭐ Asana側公式 |
| **Backlog** | **MCP経由**（Nulab公式MCPサーバ） | ⭐⭐ Nulab側公式 |

### Asana 連携（MCP経由）

### Asana公式MCPサーバ V2
- **エンドポイント**: `https://mcp.asana.com/v2/mcp`
- **認証**: OAuth（Asanaアカウントで承認）
- **プロトコル**: Streamable HTTP
- **重要**: Asana MCP V1 の廃止予定日と V2 移行方針は **Asana 公式開発者ドキュメント（[developers.asana.com](https://developers.asana.com/docs/mcp-server)）** に掲載された告知を一次ソースとして確認のこと（本 FAQ 最終更新 2026/4/16 時点では V2 推奨）

### Devin側での設定手順
```
1. Devin Webapp → Settings > MCP Marketplace / Integrations
2. Add Custom MCP Server（または marketplace から Asana 選択）
3. URL: https://mcp.asana.com/v2/mcp
4. OAuth承認 → Asanaワークスペースと紐付け
5. セッションから Asana 操作が可能に
```

### できること
- タスクの作成・更新・検索・完了
- プロジェクト状況確認
- アサイン変更
- セクション・サブタスク管理
- レポート生成

### プロンプト例
```
@Devin
AsanaのMarketingプロジェクトで「Q2キャンペーン」タスクを作成、
期限4/30、自分にアサイン、サブタスクに「コピー作成」「画像準備」追加
```

### Backlog 連携（MCP経由）

### Nulab公式 Backlog MCP サーバ
- **リポジトリ**: https://github.com/nulab/backlog-mcp-server
- **ライセンス**: MIT License（OSS）
- **言語**: TypeScript
- **提供**: Nulab（Backlog開発元）公式
- **配布**: npm + Docker

### Devin側での設定手順
```
1. Devin Secrets に登録:
   - BACKLOG_API_KEY  （Backlog管理画面 > 個人設定 > API から発行）
   - BACKLOG_DOMAIN   （例: yourspace.backlog.jp または yourspace.backlog.com）

2. Devin Webapp → Settings > MCP Marketplace

3. Add Custom MCP Server、以下のconfig例：
```

```json
{
  "mcpServers": {
    "backlog": {
      "command": "npx",
      "args": ["-y", "@nulab/backlog-mcp-server"],
      "env": {
        "BACKLOG_DOMAIN": "yourspace.backlog.com",
        "BACKLOG_API_KEY": "{{secret:BACKLOG_API_KEY}}"
      }
    }
  }
}
```

### できること
- Issue（課題）のCRUD
- プロジェクト・スペース情報取得
- Wikiの読み書き
- ファイル添付
- マイルストーン・バージョン管理
- コメント追加
- ステータス・担当者変更

### プロンプト例
```
@Devin
Backlogの「Webサイトリニューアル」プロジェクトで
「ログイン画面改修」の子課題として「UIデザイン」「実装」「テスト」を作成、
マイルストーン v2.0 に紐付けて
```

### 代替案: MCPを使わない接続

### パターン1: API直接叩く（Secrets + HTTP）
- **Asana**: REST API + Personal Access Tokenを Secretsに
- **Backlog**: REST API + APIキー を Secretsに
- Devinが `curl` / `requests` で直接呼ぶ

**メリット**: シンプル、追加ツール不要
**デメリット**: プロンプトで毎回API仕様を指示する必要あり

```
以下のSecretsを使ってBacklogのREST APIを呼び出し、
プロジェクト「PROJ」の未完了Issueを一覧化して:
- BACKLOG_DOMAIN
- BACKLOG_API_KEY
```

### パターン2: Slack/Teams経由
- Asana/Backlogの通知を受けたSlackチャネルで `@Devin` に指示
- 完了したらSlack返信で関係者に共有
- **チケット更新自体は手動**（Devinはアドバイスのみ）

### パターン3: GitHub経由（Backlog⇔GitHub連携時）
- BacklogのIssueキーがGitHubコミット/PRに含まれる場合
- GitHub側でDevinがPR作成 → Backlogが自動更新
- **Backlog-GitHub連携を有効化**している組織向け

### 比較マトリクス

| 観点 | Jira/Linear（Native） | Asana（MCP） | Backlog（MCP） |
|---|---|---|---|
| **接続設定** | UI数クリック | MCP設定必要 | MCP設定必要 |
| **OAuth対応** | ✅ | ✅ | ❌（APIキー） |
| **日本語UI** | △ | △ | ⭐ 完全対応 |
| **エンタープライズ導入** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐（日本法人多数） |
| **セッション内操作** | チケット→Devin起動も可 | MCP tool経由 | MCP tool経由 |
| **自動チケット起動** | ✅（新規作成で起動） | 手動 | 手動 |
| **監査ログ** | Org Admin可視 | MCP側＋Devin側 | MCP側＋Devin側 |
| **MCP追加コスト** | 不要 | 不要（Asana側提供） | 不要（OSS） |
| **SSO連携** | ✅ | ✅（Asana側） | Backlog次第 |
| **双方向性** | 強（trigger起動可） | 中（MCP経由のみ） | 中（MCP経由のみ） |

### よくある注意点

| 観点 | 内容 |
|---|---|
| **MCP導入の主導者** | Org Adminが `Settings > MCP Marketplace` で追加 |
| **APIキーの扱い** | Backlog APIキー等は **Devin Secrets**、Slackに貼らない |
| **レートリミット** | Asana / Backlog 双方のAPIレート制限あり、大量操作で注意 |
| **双方向ではない** | Backlog/Asana からDevinを起動する自動トリガーは無い（Jira/Linearのような新規チケット→Devin自動起動は非対応） |
| **権限範囲** | MCP経由でも、トークン所有者の権限を超えた操作は不可 |
| **トラブル時** | MCPサーバ側のログ確認、OAuth再認証、API互換性確認 |
| **Asana V1廃止** | **2026年5月11日に廃止予定**（本FAQ最終更新 2026/4/16 時点で未来日）、以降は V2 必須 |
| **Backlog Classic/Premium** | 両プラン対応、料金プランによってAPI制限異なる |

### 設定の全体像

```mermaid
flowchart TD
    subgraph Devin
        SES[Devin Session]
        SEC[Devin Secrets]
        MCP[MCP Server登録]
    end

    subgraph 外部PM
        ASANA[Asana]
        BL[Backlog]
        JIRA[Jira Native]
    end

    SEC -->|APIキー/OAuth Token| MCP
    MCP -->|mcp.asana.com/v2/mcp| ASANA
    MCP -->|@nulab/backlog-mcp-server| BL
    SES -->|ツール呼び出し| MCP

    SES -.Native統合.-> JIRA

    style SES fill:#e1f5ff
    style MCP fill:#fff9c4
    style JIRA fill:#c8e6c9
```

### まとめ

| 観点 | 回答 |
|---|---|
| **Asana連携** | ✅ 可能（MCP経由、Asana公式V2サーバ） |
| **Backlog連携** | ✅ 可能（MCP経由、Nulab公式MCP） |
| **Native対応は?** | ❌ 現時点では Jira/Linearのみ |
| **日本企業で実用的?** | ⭐ Backlogは日本企業で広く使われているため現実的 |
| **セットアップ難易度** | 中（Native統合より一手間、但し難易度は低い） |
| **推奨** | **日本法人: Backlog MCP**、**グローバル共通: Asana MCP**、**PM中心開発: Jira/Linear Native** |
| **落とし穴** | 「双方向自動トリガー」は無い、**新規チケット→Devin自動起動**なら Jira/Linearが優位 |

**核心**: **Asana/Backlog どちらも MCP 経由で十分実用**。Backlogは日本語環境の強みがあり、Nulab公式OSSで安定供給されているため、**日本企業なら Backlog MCPが現実的な選択肢**。ただし「チケット作成と同時にDevinタスク起動」のような**深い統合**は Jira/Linear Nativeの方が優位です。

---

[← Q57. Slackワークスペースはプロジェクトごとに分ける必要がある？全社ワークスペース運用の問題点は？](q57-slack-workspace-strategy.md) ｜ [Q59. 既存の人間主体の開発プロセス/ドキュメントをDevinに把握させ、人とDevinをシームレスに連携させる手順は？ →](../15-organization-ops/q59-existing-process-integration.md)
