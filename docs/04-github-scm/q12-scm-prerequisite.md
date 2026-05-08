---
qno: 12
title: "DevinはGitHub等のSCM前提か？1対1ならVMストレージだけで十分？"
category: 04-github-scm
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/integrations/github
related: []
estimated: false
---

# Q12. DevinはGitHub等のSCM前提か？1対1ならVMストレージだけで十分？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: GitHub・SCM連携](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/integrations/github ｜ 推定なし

### 結論: **SCM（GitHub等）を前提にした方が圧倒的に良い**。1対1でもVMストレージだけで運用するのは**非推奨**

### なぜSCMが前提なのか

Devinの設計思想そのものが「**人間とAIのコラボはPR/コミット単位で行う**」という前提で作られている。以下の機能がすべてSCM連携を前提:

| 機能 | SCMがないとどうなる |
|---|---|
| PR作成 | 使えない |
| CI連携 | 使えない |
| コードレビューのやりとり | できない |
| Devin Review（自動レビュー） | 使えない |
| ブランチ管理 | VM上の作業ブランチだけになる |
| セッション間のコード共有 | できない |
| Repo Setup / Knowledge / Playbook | 機能はするが効果半減 |
| Integrations（Linear / Jira / Slack等） | 連携価値が激減 |

### VMストレージだけで運用した場合の致命的な問題

1. **セッション終了でVMが破棄される** — `/home/ubuntu/` に置いたコードは次セッションで見えない
2. **別セッションから過去の成果物を参照できない** — 毎回ゼロから作り直し
3. **履歴・差分・ロールバックができない**
4. **人間がコードをレビューする手段がない**
5. **バックアップがない**
6. **Devinのセルフ改善ループ（Knowledge / Playbook）の効果が激減**

### 1対1運用こそSCMの恩恵が大きい

- 自分の作業の**履歴管理**（昨日の自分がどこまでやったか）
- Devinと自分の**作業の分離**
- **ロールバック**がワンクリック
- **別マシンから続きの作業ができる**

### 一時作業用セッション（このFAQ作成セッションなど）は例外か？

成果物をファイルとしてVMに置いてユーザに渡すだけの用途なら、VM完結もアリ。ただし:
- セッションを閉じたら `/home/ubuntu/*` は消える
- 保存手段として以下のいずれかが必要:
  1. ユーザがダウンロード（message_userのattachmentで送る）
  2. GitHub Issue / Gist / repoに pushする
  3. Knowledgeとして登録する
  4. Notion / Confluence等の外部ドキュメントにコピー

### 推奨構成（1対1開発）

```
[人間] ⇄ [GitHub（SCM）] ⇄ [Devin Session（VM）]
           ↑
           └─ ここが"真実の情報源（Source of Truth）"
```

- **コードの置き場**: GitHub（SCM）
- **Devinへの指示**: Webapp / Slack / IDE拡張
- **Devinの作業場**: セッションVM（一時的、毎回破棄）
- **Devinが学んだこと**: Knowledge / Playbook（Devin側に永続化）
- **日々の成果**: PR → マージ → SCMに蓄積

### SCMがどうしても使えない場合の選択肢

- GitLab（セルフホスト含む）
- Bitbucket
- Azure DevOps
- オンプレGit + Webhook（Enterprise契約で相談）

完全にSCMなしで運用するのはDevinの想定外の使い方。

### まとめ

- DevinはSCM前提の設計。**SCMなしは非推奨**
- 1対1でもSCMを使うべき
- VMストレージはセッション終了で消える一時領域
- 一時作業用セッションは例外的にVM完結もアリだが、**最終成果物は必ず外に出す**

**核心**: **Devin は SCM（GitHub等）前提の設計**。VM ストレージ単独の運用は履歴・レビュー・マージの観点で非推奨。

---

[← Q11. Devinでフルスクラッチ開発する場合の推奨手順は？（1人 × Devin 1対1）](../03-basic-operations/q11-fullscratch-flow.md) ｜ [Q13. Devinを使う開発者はGitHubアカウント + Gitの知識・経験が必要？ →](q13-developer-git-knowledge.md)
