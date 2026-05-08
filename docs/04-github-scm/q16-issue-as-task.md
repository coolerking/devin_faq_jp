---
qno: 16
title: "Issue 1つ = Kanbanボードのタスク1つ？"
category: 04-github-scm
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/integrations/linear-and-jira
related: []
estimated: false
---

# Q16. Issue 1つ = Kanbanボードのタスク1つ？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: GitHub・SCM連携](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/integrations/linear-and-jira ｜ 推定なし

### 結論: **基本Yes、ただし「Issue = 実装単位のタスク」に揃える**必要がある

### レイヤーの整理

| 階層 | 例 | 粒度 | Devin向き？ |
|---|---|---|---|
| **エピック（Epic）** | 「認証機能を作る」 | 1〜3ヶ月 | ❌ 大きすぎる |
| **ストーリー（Story）** | 「ユーザーがGoogleでログインできる」 | 1〜5日 | △ 分解すれば可 |
| **タスク（Task）** | 「Google OAuthのコールバックAPIを実装」 | 半日〜2日 | ✅ **ここが最適** |
| **サブタスク** | 「トークン検証関数を書く」 | 1〜3時間 | △ 細かすぎる場合あり |

Devinに投げる **1 Issue = 1 PR = 1 セッション** は「タスク層」に対応。

### Kanbanボード構成の推奨

```
┌─────────┬────────────┬─────────────┬───────────┬───────────┐
│ Backlog │ To Do      │ In Progress │ In Review │ Done      │
├─────────┼────────────┼─────────────┼───────────┼───────────┤
│ #10     │ #12        │ #14         │ #15 (PR)  │ #11       │
│ #20     │ #13        │             │ #16 (PR)  │ #17       │
│ #30     │ devin-ready│ Devin作業中 │ 人間review│ merged    │
└─────────┴────────────┴─────────────┴───────────┴───────────┘
```

| レーン | 状態 | 誰が動かす |
|---|---|---|
| Backlog | 案として起票だけされた | 人間が整理 |
| To Do | Devinに渡せる状態（`devin-ready`） | 人間が精査して移動 |
| In Progress | Devinが作業中 | 自動 or 人間 |
| In Review | PR作成済み、人間レビュー待ち | 自動（PR化で移動） |
| Done | マージ完了 | 自動（マージで移動） |

**ポイント**:
- 「To Do」に入れる時点でIssueは"Devinが理解できる状態"になっている必要がある
- Backlog → To Doへの移動時に**人間が必ず精査**する（品質の分水嶺）
- In Progress以降はほぼ自動で動く

### GitHub Projectsとの連携

**おすすめ: GitHub Projects (v2) のBoardビュー**
- GitHub純正なので連携が楽
- Automationで状態遷移を自動化:
  - `Issue opened` → Backlog
  - `label:devin-ready` 付与 → To Do
  - `PR opened (linked)` → In Review
  - `PR merged` → Done

**他ツール**:
| ツール | Devin連携 | 備考 |
|---|---|---|
| GitHub Projects | ◎ ネイティブ | 最推奨 |
| Linear | ◎ Integration済み | Devin Webappから直接参照可 |
| Jira | ◎ Integration済み | エンタープライズで定番 |
| Trello | △ | 手動連携 |
| Notion | △ | DB機能使えば可 |

### ストーリー層をどう扱うか

**パターン1: 親Issue + 子Issue**
```
#100 [Epic] 認証機能
  └ #101 [Story] Googleログインできる
      ├ #102 [Task] Google OAuthコールバック実装 ← Devinに投げる
      ├ #103 [Task] トークン保存・セッション管理 ← Devinに投げる
      └ #104 [Task] ログイン画面のUI ← Devinに投げる
```

**パターン2: GitHub ProjectsのフィールドでStory表現**
- Issue自体はタスク粒度で作る
- Project側に `Story` フィールドを追加してグルーピング

### Kanbanカード ≠ Issueになるケース

| Kanbanカード | Issueにする？ |
|---|---|
| 「ミーティング」「レビュー作業」 | ❌ Issueではない（カレンダーで管理） |
| 「環境構築」「調査」 | △ 成果物が出るならIssue化 |
| 「設計ドキュメント作成」 | ○ Issue化してDevinに任せられる |
| 「◯◯について学習する」 | ❌ 個人タスク |
| バグ | ◎ Issue化 |
| 機能追加 | ◎ Issue化 |
| リファクタリング | ◎ Issue化 |

### 1対1運用の週次リズム

```
月曜朝:
  ├ 先週のDoneを振り返る
  ├ Backlogを整理
  └ 今週取り組む5〜10個のIssueをTo Doに移動（devin-readyラベル）

毎日:
  ├ To Doから1〜3個をDevinに投げる（In Progressへ）
  ├ In ReviewのPRをレビュー
  └ 必要に応じて新Issue起票（Backlogへ）

金曜:
  ├ Doneをまとめて振り返り
  └ Knowledge/Playbook更新
```

### まとめ

- Kanbanカード = Issueの対応は、運用上は成立する
- ただし **Issue ≠ ストーリー、Issue = タスク** で揃える
- GitHub Projectsでレーンの自動遷移を設定すると運用が楽
- Kanbanに出てくる全カードをIssue化する必要はない（会議等は除外）

**核心**: **Kanbanカード = Issue は運用上成立するが、「Issue = タスク層（半日〜2日）」に揃えるのが肝**。Epic/Story を直接 Devin に投げず、タスク粒度に分解してから `1 Issue = 1 PR = 1 Session` で流す。

---

[← Q15. DevinはGitHubでどこまで操作できる？Permissionsに依存する？](q15-github-permissions.md) ｜ [Q17. DevinにKanban相当の機能はある？ →](q17-kanban.md)
