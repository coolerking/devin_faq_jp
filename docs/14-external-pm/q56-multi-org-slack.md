---
qno: 56
title: "複数Organization（個人契約＋会社契約）で、それぞれ別のSlackワークスペースに連携できる？"
category: 14-external-pm
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/integrations/slack
related: []
estimated: false
---

# Q56. 複数Organization（個人契約＋会社契約）で、それぞれ別のSlackワークスペースに連携できる？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: 外部連携（Slack・PM）](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/integrations/slack ｜ 推定なし

### 結論: **可能です**。Slack連携は**Organization単位**のため、**各OrgごとにそれぞれのSlackワークスペース**を紐付けられます。ただし**個人ユーザ紐付け時のメアド整合**に注意

参考: https://docs.devin.ai/integrations/slack

### 詳細

### 前提となる仕組み
| 階層 | 設定範囲 | 備考 |
|---|---|---|
| **Org ↔ Slack Workspace** | **Org単位で1対1** | `Settings > Integrations > Slack`で接続 |
| **個別ユーザ紐付け** | 各Slackワークスペースで実施 | 個々のユーザが自身のDevinアカウントと紐付ける |
| **@Devin起動時の振り分け** | Slack WS → 紐付いたDevin Orgに自動振り分け | 混線しない |
| **課金・データ** | Org単位で完全分離 | 個人と会社が混ざらない |

### 可能な構成

```
┌────────────────────────┐       ┌────────────────────────┐
│ Org A（個人契約）      │◄──────│ 個人Slackワークスペース│
│ - 個人が支払い         │       │ #devin-personal        │
│ - Personal Secrets    │       └────────────────────────┘
│ - 個人Knowledge        │
└────────────────────────┘

┌────────────────────────┐       ┌────────────────────────┐
│ Org B（会社契約）      │◄──────│ 会社Slackワークスペース│
│ - 会社が支払い         │       │ #devin-dev             │
│ - Org Secrets (Admin) │       └────────────────────────┘
│ - Org Knowledge        │
└────────────────────────┘
```

→ **個人Slackで @Devin → Org Aのセッション起動**
→ **会社Slackで @Devin → Org Bのセッション起動**
→ 自動で振り分け・課金も各Orgで完結

### 設定手順

### Org A（個人Org）側
既に個人Slack連携済みなら現状維持。未設定なら以下と同じ手順。

### Org B（会社Org）側
1. https://app.devin.ai/ にログイン
2. 右上の **Orgスイッチャー** で **Org Bに切り替え**
3. **Settings > Integrations > Slack** → **Connect** ボタン
4. インストールダイアログで **会社のSlackワークスペース** を選択
5. Devin appを会社ワークスペースにインストール
6. 会社Slack上で自身のDevinユーザを個別認証（メアド整合必要）
7. 会社Slackの任意チャネルで `@Devin hello` → 応答すれば成功

### 個別ユーザの紐付け（各メンバーが実施）
組織メンバー全員が各自:
```
会社Slack内で:
  - Devin Botとの個別認証フロー完了
  - メアドは app.devin.ai/settings のメアドと一致すること
```

### 重要な注意点

### 1. **メアド整合**（最大の落とし穴）
公式docの指示:
> ensure that your Slack email is the same as your email in https://app.devin.ai/settings

個人Slackと会社Slackで**メアドが異なる場合**の選択肢:

| パターン | 説明 | 推奨度 |
|---|---|---|
| **①Devinアカウントを2つ持つ** | 個人メアド用 + 会社メアド用で別々のDevinユーザを作成 | ⭐⭐⭐ 推奨（最もきれい） |
| **②Slack側でメアドエイリアス** | Slack個人設定で追加メアド登録し Devin登録メアドを含める | ⭐⭐ 状況により |
| **③片方のみ連携** | 会社Orgだけ連携、個人Orgは直接Webapp使用 | ⭐ 暫定 |

### 2. **データ・課金の隔離**

| 項目 | 個人Org | 会社Org |
|---|---|---|
| セッション履歴 | 個人のみ | 会社のみ |
| Knowledge | 個人Knowledge | Org Knowledge |
| Secrets | Personal Secrets | Org Secrets（Adminが管理） |
| 使用量・課金 | 個人クレカ | 会社契約 |
| Playbook | 個人作成 | Org全員共有 |
| Admin可視範囲 | 本人のみ | Org Admin全体 |

**絶対に混ざらない**が、**誤って個人Slackで会社業務タスクを投げるリスク**は残る → **チャネル命名と運用ルール**で区別推奨。

### 3. **Admin権限**
| Org | 実施者 |
|---|---|
| 個人Org | 本人（Owner） |
| 会社Org | **Admin**が実施（一般ユーザは接続操作不可） |

会社Orgで自分がAdminでない場合は、Admin（IT/DevOps担当）にSlack連携を依頼。

### 4. **Slack側の個別カスタマイズも独立**
各Orgで独立に設定:
- **Slack通知**（PR完了・エラー時の通知）
- **Dedicated Devin Channel**（Devin専用チャネル指定）
- **`@Devin`のリネーム**（例: `@DevinCorp` / `@DevinPersonal`）
- **Inline keywords**（`!ask`/`!deep`/`!plan`等）

### 具体的推奨セットアップ

```
[個人環境]
  Devinアカウント: your-personal@example.com
  └─ Org A（個人契約、個人支払い）
      └─ Slack: personal-workspace.slack.com
          └─ #devin-personal（@DevinPersonalにリネーム）

[会社環境]
  Devinアカウント: you@company.co.jp
  └─ Org B（会社契約、会社支払い）
      └─ Slack: company-workspace.slack.com
          └─ #devin-dev（@DevinCorpにリネーム）
          └─ #devin-support
```

**各Slackから投げたタスクは、必ず対応するOrgの課金・リソースのみを消費**。

### よくある落とし穴と対処

| 症状 | 原因 | 対処 |
|---|---|---|
| 会社Slackで `@Devin` が反応しない | Devinユーザの個別紐付け未完了 | Slack上で個別認証フロー実施 |
| 個人/会社Slackで同じアカウントが紐付く | 同一メアドで両方認証した | 片方を別メアドのDevinアカウントに切り替え |
| 会社Slackで個人Orgのタスクが起動 | Devin側Org切り替えが古い | `Settings > Integrations > Slack`でDisconnect→Reconnect |
| 課金が意図しないOrgに来る | Slack WS紐付け先のOrgが誤り | 誤Org側でDisconnect → 正しいOrgでConnect |
| 片方のSlackで接続済みなのに片方はエラー | メアド不一致 | `app.devin.ai/settings`確認、Slackメアド整合 |
| 会社SlackでInstallボタンが押せない | Slackワークスペースの管理者承認が必要 | Slack管理者にアプリインストール承認を依頼 |
| Enterprise Grid構成で悩む | Slack Enterprise Gridは複数WSの束 | 特定WS限定インストール or Grid全体で可（要調整） |

### まとめ

| 観点 | 回答 |
|---|---|
| **2Org × 2Slackの独立運用は可能?** | **✅ 可能**、Devin公式サポート範囲 |
| **セッション・課金・データ混線は?** | **❌ 混ざらない**、Org単位で完全分離 |
| **個人Slackから会社Orgを呼び出せる?** | **❌ できない**、WS紐付けOrgで固定 |
| **設定単位** | **Org単位**（Adminまたは個人Owner） |
| **最大の注意点** | **メアド整合**（app.devin.ai/settingsとSlackのメアドを合わせる or Devinアカウント2つ運用） |
| **推奨構成** | **Devinアカウント2つ + Slack WS別々紐付け**、チャネル・@名もリネームで区別 |

**核心**: 「Slack連携はOrg単位で独立」の設計のため、**個人Slack→個人Org、会社Slack→会社Org** の2系統運用は自然にできる。唯一の注意は**個人ユーザのメアド整合**だけなので、**Devinアカウントを2つ（個人メアド用・会社メアド用）に分ける**のが最もトラブルフリーです。

---

[← Q55. DevinはAWS上で動作している？VPC間接続（Devin社と自組織）は可能？](../13-cloud-infra/q55-aws-vpc.md) ｜ [Q57. Slackワークスペースはプロジェクトごとに分ける必要がある？全社ワークスペース運用の問題点は？ →](q57-slack-workspace-strategy.md)
