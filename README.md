# Devin FAQ JP

日本語で記述された Devin に関する FAQ集。なお本FAQは個人で作成しました。

| | |
|---|---|
| **総質問数** | 70問 |
| **最終確認** | 2026-04-17 |
| **対応 Devin バージョン** | 2026年4月時点（2026/4/16 料金改定反映） |
| **対象読者** | Devin 検討〜エンタープライズ管理者 |
| **記述方針** | 結論→詳細→表→具体例→注意→まとめ（核心） |

> ⚠️ **免責**: 公式情報は変動するため、最新は [docs.devin.ai](https://docs.devin.ai/) を参照。

---

## カテゴリ別索引

| # | カテゴリ | 質問数 | リンク |
|---|---|---|---|
| 01 | Devin入門（What/Who） | 6 | [docs/01-introduction/](docs/01-introduction/README.md) |
| 02 | 料金・プラン | 2 | [docs/02-pricing/](docs/02-pricing/README.md) |
| 03 | 基本操作・セッション | 4 | [docs/03-basic-operations/](docs/03-basic-operations/README.md) |
| 04 | GitHub・SCM連携 | 9 | [docs/04-github-scm/](docs/04-github-scm/README.md) |
| 05 | IDE・エディタ・CLI | 5 | [docs/05-ide-cli/](docs/05-ide-cli/README.md) |
| 06 | コマンド・スキル | 4 | [docs/06-commands-skills/](docs/06-commands-skills/README.md) |
| 07 | Devinリソース | 5 | [docs/07-devin-resources/](docs/07-devin-resources/README.md) |
| 08 | Secrets・API | 3 | [docs/08-secrets-api/](docs/08-secrets-api/README.md) |
| 09 | マルチセッション・複数リポ | 2 | [docs/09-multi-session-repo/](docs/09-multi-session-repo/README.md) |
| 10 | DB・テスト・品質・Review | 9 | [docs/10-database-test-quality/](docs/10-database-test-quality/README.md) |
| 11 | データ入出力・ドキュメント理解 | 5 | [docs/11-data-docs/](docs/11-data-docs/README.md) |
| 12 | セキュリティ・監査・ガバナンス | 5 | [docs/12-security-governance/](docs/12-security-governance/README.md) |
| 13 | クラウド連携・インフラ | 2 | [docs/13-cloud-infra/](docs/13-cloud-infra/README.md) |
| 14 | 外部連携（Slack・PM） | 3 | [docs/14-external-pm/](docs/14-external-pm/README.md) |
| 15 | 組織展開・分析 | 5 | [docs/15-organization-ops/](docs/15-organization-ops/README.md) |
| 16 | セッション停止・復旧 | 1 | [docs/16-session-recovery/](docs/16-session-recovery/README.md) |

---

## 番号順 全Q索引

- [Q1. Devinとは？](docs/01-introduction/q01-devin-overview.md)
- [Q2. DevinはAI？どのAIモデルを使っている？](docs/01-introduction/q02-devin-ai-model.md)
- [Q3. Devinはどんな人向け？（想定ユーザ像）](docs/01-introduction/q03-target-users.md)
- [Q4. Devinユーザに必要な知識・経験は？（必須 / 推奨）](docs/01-introduction/q04-required-knowledge.md)
- [Q5. Devin入門者が最初に読むべきドキュメント・書籍は？](docs/01-introduction/q05-getting-started-docs.md)
- [Q6. Devinの競合サービスやソフトウェアは何？](docs/01-introduction/q06-competitors.md)
- [Q7. Devinの料金体系は？（2026/4/16の改定）](docs/02-pricing/q07-devin-pricing.md)
- [Q8. Ask DevinとSessionの違いは？](docs/03-basic-operations/q08-ask-vs-session.md)
- [Q9. Sessionが待ち状態か判断するには？（アイコンの色で迷った）](docs/03-basic-operations/q09-session-status.md)
- [Q10. セッションの分割粒度はフェーズ単位？もっと細かく？](docs/03-basic-operations/q10-session-granularity.md)
- [Q11. Devinでフルスクラッチ開発する場合の推奨手順は？（1人 × Devin 1対1）](docs/03-basic-operations/q11-fullscratch-flow.md)
- [Q12. DevinはGitHub等のSCM前提か？1対1ならVMストレージだけで十分？](docs/04-github-scm/q12-scm-prerequisite.md)
- [Q13. Devinを使う開発者はGitHubアカウント + Gitの知識・経験が必要？](docs/04-github-scm/q13-developer-git-knowledge.md)
- [Q14. 開発者とDevinはGitHubをどう使い分ける？（フルスクラッチの一般ケース）](docs/04-github-scm/q14-developer-vs-devin-github.md)
- [Q15. DevinはGitHubでどこまで操作できる？Permissionsに依存する？](docs/04-github-scm/q15-github-permissions.md)
- [Q16. Issue 1つ = Kanbanボードのタスク1つ？](docs/04-github-scm/q16-issue-as-task.md)
- [Q17. DevinにKanban相当の機能はある？](docs/04-github-scm/q17-kanban.md)
- [Q18. DevinのIDEはWindsurf？VSCode？](docs/05-ide-cli/q18-windsurf-vs-vscode.md)
- [Q19. 最新のVSCodeはGitHub Copilot Chatが標準でついてくるが、Devinもそうなる？](docs/05-ide-cli/q19-vscode-copilot-bundled.md)
- [Q20. GitHub Copilotと併用すべき？フルスクラッチでの役割分担は？](docs/05-ide-cli/q20-copilot-coexistence.md)
- [Q21. Devin + Copilot併用は初心者向きではない？](docs/05-ide-cli/q21-beginner-fitness.md)
- [Q22. Devinにスキル機能はある？（Claude Code / Codex CLI相当）](docs/06-commands-skills/q22-skills-existence.md)
- [Q23. Devinのスキルは他ツールと同じ作成方法？独自機能は？](docs/06-commands-skills/q23-skills-creation.md)
- [Q24. Devinにスラッシュコマンドはあるか？Ask/Sessionで違いはあるか？](docs/06-commands-skills/q24-slash-commands.md)
- [Q25. カスタムスラッシュコマンドとスキルの違いは「管理場所」だけ？](docs/06-commands-skills/q25-slash-vs-skill.md)
- [Q26. Machine Configurationは Repo Setupのこと？言語別のDevin向きリポ構成は？](docs/07-devin-resources/q26-machine-config.md)
- [Q27. Playbookとは？開発環境構築にしか使っていなかったが、本来の用途と違う？](docs/07-devin-resources/q27-playbook.md)
- [Q28. Repo Setup / Knowledge / Playbookの違いは？（表で整理）](docs/07-devin-resources/q28-resource-comparison.md)
- [Q29. Devin Wikiとは？Codex CLI/Claude CodeのようなローカルRAGか？Ask/Sessionで問い合わせるrepoは事前登録が必要？](docs/07-devin-resources/q29-devin-wiki.md)
- [Q30. Schedule機能とはCronのようなもの？指示はテキスト？使い方・制約・注意点](docs/07-devin-resources/q30-schedule.md)
- [Q31. Secretsの使い方は？（Org/Personalスコープ・同一キー重複時の挙動）](docs/08-secrets-api/q31-secrets.md)
- [Q32. Devin API Keyの使い方は？（API操作・MCP・Skill経由）](docs/08-secrets-api/q32-api-key.md)
- [Q33. API Keyタブの「Legacy」は今後なくなる？変更される？](docs/08-secrets-api/q33-api-legacy.md)
- [Q34. 別々のセッションで並行作業している場合、それぞれのスコープはブランチ/ワークツリーか？](docs/09-multi-session-repo/q34-parallel-sessions.md)
- [Q35. フロント/バックなど複数リポを1セッションで管理できる？](docs/09-multi-session-repo/q35-multi-repo.md)
- [Q36. DBを持つシステムだと、DB用VMと開発用VMを分けて開発する？](docs/10-database-test-quality/q36-database.md)
- [Q37. 繰り返しテストでDBを初期状態に戻すのに有効なDevin機能は？](docs/10-database-test-quality/q37-db-fixture-reset.md)
- [Q38. テスターとしてDevinを扱う場合、結合テスト以降は外部テスト環境を立てるべき？](docs/10-database-test-quality/q38-integration-test-env.md)
- [Q39. Devin Test Modeとは？何ができて、通常とはどう違ってどうすればTest Modeになる？](docs/10-database-test-quality/q39-test-mode.md)
- [Q40. テストの種類ごとに使い方が変わる？（単体〜回帰・負荷・総合）](docs/10-database-test-quality/q40-test-types.md)
- [Q41. 社内LAN内のサーバにDevinからテストできる？SaaS風のP2Pプローブ方式は？](docs/10-database-test-quality/q41-internal-network-test.md)
- [Q42. テスト駆動開発（TDD）は可能？Devinをどう使えばできる？](docs/10-database-test-quality/q42-tdd.md)
- [Q43. Reviewタブはどういう機能？使い方・レビュー範囲・観点](docs/10-database-test-quality/q43-review-tab.md)
- [Q44. 作成中のFAQをDevin Reviewで確認する手順は？](docs/10-database-test-quality/q44-faq-review-procedure.md)
- [Q45. Devinはどんな入力データを認識できる？](docs/11-data-docs/q45-input-data-types.md)
- [Q46. Devinはどんな出力データを作成できる？](docs/11-data-docs/q46-output-data-types.md)
- [Q47. DevinはExcel上の図、Word・PDF上の図をどのくらい理解できる？](docs/11-data-docs/q47-image-pdf-diagrams.md)
- [Q48. Devinに入力するデータで気をつけることは？（APIキー・個人情報・機微情報）](docs/11-data-docs/q48-input-data-cautions.md)
- [Q49. Devinに大量データを連携させるには？](docs/11-data-docs/q49-bulk-data-handling.md)
- [Q50. Devinに入力/アップロードしたデータはいつまで保存される？](docs/12-security-governance/q50-data-retention.md)
- [Q51. Devinのセッション/データを削除するには？（Terminate / Archive / 完全削除の3階層）](docs/12-security-governance/q51-terminate-archive-delete.md)
- [Q52. 組織契約プランで、管理者は一般ユーザのどこまで把握できる？](docs/12-security-governance/q52-org-admin-visibility.md)
- [Q53. Devinは企業の監査に対応している？（SOC 2/GDPR等）](docs/12-security-governance/q53-compliance-audit.md)
- [Q54. AWS S3マウント等でDevinからAWSリソースを利用させる場合、パスワード・セキュリティトークン・pemファイルの扱いは？代替手段は？](docs/13-cloud-infra/q54-aws-credentials.md)
- [Q55. DevinはAWS上で動作している？VPC間接続（Devin社と自組織）は可能？](docs/13-cloud-infra/q55-aws-vpc.md)
- [Q56. 複数Organization（個人契約＋会社契約）で、それぞれ別のSlackワークスペースに連携できる？](docs/14-external-pm/q56-multi-org-slack.md)
- [Q57. Slackワークスペースはプロジェクトごとに分ける必要がある？全社ワークスペース運用の問題点は？](docs/14-external-pm/q57-slack-workspace-strategy.md)
- [Q58. AsanaやBacklogとの連携は可能？](docs/14-external-pm/q58-asana-backlog.md)
- [Q59. 既存の人間主体の開発プロセス/ドキュメントをDevinに把握させ、人とDevinをシームレスに連携させる手順は？](docs/15-organization-ops/q59-existing-process-integration.md)
- [Q60. 標準化ドキュメントリポを渡せば、Devinは準拠したリソース構成を自動生成してくれる？](docs/15-organization-ops/q60-standards-docs-auto-resource.md)
- [Q61. 実例: `internal-standards-docs`（自社旧標準）に準拠したDevinリソース構成の手順は？](docs/15-organization-ops/q61-internal-standards-example.md)
- [Q62. 複数のDevinセッションで協業できる？リーダ→開発者/レビューア/テスター型のマルチエージェント体制は可能？](docs/15-organization-ops/q62-multi-agent-collaboration.md)
- [Q63. セッション操作履歴からユーザ＆Devinの開発生産性を計測できる？（応答時間・思考時間の取得）](docs/15-organization-ops/q63-productivity-metrics.md)
- [Q64. Devinシェルで `git clone` が失敗するのはなぜ？（git-manager.devin.ai/proxy と認証プロキシ／403切り分け）](docs/04-github-scm/q64-clone-failures.md)
- [Q65. 「Devin went to sleep due to session usage settings」と表示されて止まるのはなぜ？対処方法は？](docs/16-session-recovery/q65-session-sleep.md)
- [Q66. Teamsプランで Usage History に他メンバのセッションが見える。自分の作業は丸見え？アーカイブで隠せる？](docs/12-security-governance/q66-session-visibility-teams.md)
- [Q67. 個人プランで登録した GitHub リポジトリや Knowledge / Playbook / Secrets は、企業プランからも使える？](docs/04-github-scm/q67-personal-vs-org-resources.md)
- [Q68. Devin Wiki に未登録のリポジトリを Devin セッションの VM 上に `git clone` して開発に使える？](docs/04-github-scm/q68-clone-without-wiki.md)
- [Q69. Devin CLI を使う場合、Devin セッションの仮想マシンは作成される？CLI を実行している PC で作業？両方可能？](docs/05-ide-cli/q69-devin-cli-modes.md)
- [Q70. Devin と Windsurf のプランは別物？同名の Pro/Max は同じ？](docs/02-pricing/q70-devin-vs-windsurf-plans.md)

---

## カテゴリ別 全Q索引

### 01. Devin入門（What/Who）

Devin の概要・対象者・前提知識・関連ドキュメント・競合

- [Q1. Devinとは？](docs/01-introduction/q01-devin-overview.md)
- [Q2. DevinはAI？どのAIモデルを使っている？](docs/01-introduction/q02-devin-ai-model.md)
- [Q3. Devinはどんな人向け？（想定ユーザ像）](docs/01-introduction/q03-target-users.md)
- [Q4. Devinユーザに必要な知識・経験は？（必須 / 推奨）](docs/01-introduction/q04-required-knowledge.md)
- [Q5. Devin入門者が最初に読むべきドキュメント・書籍は？](docs/01-introduction/q05-getting-started-docs.md)
- [Q6. Devinの競合サービスやソフトウェアは何？](docs/01-introduction/q06-competitors.md)

### 02. 料金・プラン

Devin の料金体系、Windsurf プランとの関係

- [Q7. Devinの料金体系は？（2026/4/16の改定）](docs/02-pricing/q07-devin-pricing.md)
- [Q70. Devin と Windsurf のプランは別物？同名の Pro/Max は同じ？](docs/02-pricing/q70-devin-vs-windsurf-plans.md)

### 03. 基本操作・セッション

Ask Devin / Session の違い、状態判定、粒度、フルスクラッチ手順

- [Q8. Ask DevinとSessionの違いは？](docs/03-basic-operations/q08-ask-vs-session.md)
- [Q9. Sessionが待ち状態か判断するには？（アイコンの色で迷った）](docs/03-basic-operations/q09-session-status.md)
- [Q10. セッションの分割粒度はフェーズ単位？もっと細かく？](docs/03-basic-operations/q10-session-granularity.md)
- [Q11. Devinでフルスクラッチ開発する場合の推奨手順は？（1人 × Devin 1対1）](docs/03-basic-operations/q11-fullscratch-flow.md)

### 04. GitHub・SCM連携

GitHub 等 SCM 連携、権限、Issue/Kanban、clone 失敗、組織リソース移行

- [Q12. DevinはGitHub等のSCM前提か？1対1ならVMストレージだけで十分？](docs/04-github-scm/q12-scm-prerequisite.md)
- [Q13. Devinを使う開発者はGitHubアカウント + Gitの知識・経験が必要？](docs/04-github-scm/q13-developer-git-knowledge.md)
- [Q14. 開発者とDevinはGitHubをどう使い分ける？（フルスクラッチの一般ケース）](docs/04-github-scm/q14-developer-vs-devin-github.md)
- [Q15. DevinはGitHubでどこまで操作できる？Permissionsに依存する？](docs/04-github-scm/q15-github-permissions.md)
- [Q16. Issue 1つ = Kanbanボードのタスク1つ？](docs/04-github-scm/q16-issue-as-task.md)
- [Q17. DevinにKanban相当の機能はある？](docs/04-github-scm/q17-kanban.md)
- [Q64. Devinシェルで `git clone` が失敗するのはなぜ？（git-manager.devin.ai/proxy と認証プロキシ／403切り分け）](docs/04-github-scm/q64-clone-failures.md)
- [Q67. 個人プランで登録した GitHub リポジトリや Knowledge / Playbook / Secrets は、企業プランからも使える？](docs/04-github-scm/q67-personal-vs-org-resources.md)
- [Q68. Devin Wiki に未登録のリポジトリを Devin セッションの VM 上に `git clone` して開発に使える？](docs/04-github-scm/q68-clone-without-wiki.md)

### 05. IDE・エディタ・CLI

Windsurf / VSCode / Copilot / Devin for Terminal の関係と使い分け

- [Q18. DevinのIDEはWindsurf？VSCode？](docs/05-ide-cli/q18-windsurf-vs-vscode.md)
- [Q19. 最新のVSCodeはGitHub Copilot Chatが標準でついてくるが、Devinもそうなる？](docs/05-ide-cli/q19-vscode-copilot-bundled.md)
- [Q20. GitHub Copilotと併用すべき？フルスクラッチでの役割分担は？](docs/05-ide-cli/q20-copilot-coexistence.md)
- [Q21. Devin + Copilot併用は初心者向きではない？](docs/05-ide-cli/q21-beginner-fitness.md)
- [Q69. Devin CLI を使う場合、Devin セッションの仮想マシンは作成される？CLI を実行している PC で作業？両方可能？](docs/05-ide-cli/q69-devin-cli-modes.md)

### 06. コマンド・スキル

Skill / Slash Command / カスタムコマンドの作成方法と使い分け

- [Q22. Devinにスキル機能はある？（Claude Code / Codex CLI相当）](docs/06-commands-skills/q22-skills-existence.md)
- [Q23. Devinのスキルは他ツールと同じ作成方法？独自機能は？](docs/06-commands-skills/q23-skills-creation.md)
- [Q24. Devinにスラッシュコマンドはあるか？Ask/Sessionで違いはあるか？](docs/06-commands-skills/q24-slash-commands.md)
- [Q25. カスタムスラッシュコマンドとスキルの違いは「管理場所」だけ？](docs/06-commands-skills/q25-slash-vs-skill.md)

### 07. Devinリソース

Machine Configuration / Playbook / Knowledge / Wiki / Schedule

- [Q26. Machine Configurationは Repo Setupのこと？言語別のDevin向きリポ構成は？](docs/07-devin-resources/q26-machine-config.md)
- [Q27. Playbookとは？開発環境構築にしか使っていなかったが、本来の用途と違う？](docs/07-devin-resources/q27-playbook.md)
- [Q28. Repo Setup / Knowledge / Playbookの違いは？（表で整理）](docs/07-devin-resources/q28-resource-comparison.md)
- [Q29. Devin Wikiとは？Codex CLI/Claude CodeのようなローカルRAGか？Ask/Sessionで問い合わせるrepoは事前登録が必要？](docs/07-devin-resources/q29-devin-wiki.md)
- [Q30. Schedule機能とはCronのようなもの？指示はテキスト？使い方・制約・注意点](docs/07-devin-resources/q30-schedule.md)

### 08. Secrets・API

Secrets スコープ・API Key・Legacy 表記

- [Q31. Secretsの使い方は？（Org/Personalスコープ・同一キー重複時の挙動）](docs/08-secrets-api/q31-secrets.md)
- [Q32. Devin API Keyの使い方は？（API操作・MCP・Skill経由）](docs/08-secrets-api/q32-api-key.md)
- [Q33. API Keyタブの「Legacy」は今後なくなる？変更される？](docs/08-secrets-api/q33-api-legacy.md)

### 09. マルチセッション・複数リポ

並行セッションのスコープ、複数リポを 1 セッションで扱う方法

- [Q34. 別々のセッションで並行作業している場合、それぞれのスコープはブランチ/ワークツリーか？](docs/09-multi-session-repo/q34-parallel-sessions.md)
- [Q35. フロント/バックなど複数リポを1セッションで管理できる？](docs/09-multi-session-repo/q35-multi-repo.md)

### 10. DB・テスト・品質・Review

DB 運用、テスト戦略、TDD、Test Mode、Review タブ

- [Q36. DBを持つシステムだと、DB用VMと開発用VMを分けて開発する？](docs/10-database-test-quality/q36-database.md)
- [Q37. 繰り返しテストでDBを初期状態に戻すのに有効なDevin機能は？](docs/10-database-test-quality/q37-db-fixture-reset.md)
- [Q38. テスターとしてDevinを扱う場合、結合テスト以降は外部テスト環境を立てるべき？](docs/10-database-test-quality/q38-integration-test-env.md)
- [Q39. Devin Test Modeとは？何ができて、通常とはどう違ってどうすればTest Modeになる？](docs/10-database-test-quality/q39-test-mode.md)
- [Q40. テストの種類ごとに使い方が変わる？（単体〜回帰・負荷・総合）](docs/10-database-test-quality/q40-test-types.md)
- [Q41. 社内LAN内のサーバにDevinからテストできる？SaaS風のP2Pプローブ方式は？](docs/10-database-test-quality/q41-internal-network-test.md)
- [Q42. テスト駆動開発（TDD）は可能？Devinをどう使えばできる？](docs/10-database-test-quality/q42-tdd.md)
- [Q43. Reviewタブはどういう機能？使い方・レビュー範囲・観点](docs/10-database-test-quality/q43-review-tab.md)
- [Q44. 作成中のFAQをDevin Reviewで確認する手順は？](docs/10-database-test-quality/q44-faq-review-procedure.md)

### 11. データ入出力・ドキュメント理解

入出力可能データ、図/表の理解、機微情報、大量データ

- [Q45. Devinはどんな入力データを認識できる？](docs/11-data-docs/q45-input-data-types.md)
- [Q46. Devinはどんな出力データを作成できる？](docs/11-data-docs/q46-output-data-types.md)
- [Q47. DevinはExcel上の図、Word・PDF上の図をどのくらい理解できる？](docs/11-data-docs/q47-image-pdf-diagrams.md)
- [Q48. Devinに入力するデータで気をつけることは？（APIキー・個人情報・機微情報）](docs/11-data-docs/q48-input-data-cautions.md)
- [Q49. Devinに大量データを連携させるには？](docs/11-data-docs/q49-bulk-data-handling.md)

### 12. セキュリティ・監査・ガバナンス

データ保管、削除、監査対応、セッション可視性

- [Q50. Devinに入力/アップロードしたデータはいつまで保存される？](docs/12-security-governance/q50-data-retention.md)
- [Q51. Devinのセッション/データを削除するには？（Terminate / Archive / 完全削除の3階層）](docs/12-security-governance/q51-terminate-archive-delete.md)
- [Q52. 組織契約プランで、管理者は一般ユーザのどこまで把握できる？](docs/12-security-governance/q52-org-admin-visibility.md)
- [Q53. Devinは企業の監査に対応している？（SOC 2/GDPR等）](docs/12-security-governance/q53-compliance-audit.md)
- [Q66. Teamsプランで Usage History に他メンバのセッションが見える。自分の作業は丸見え？アーカイブで隠せる？](docs/12-security-governance/q66-session-visibility-teams.md)

### 13. クラウド連携・インフラ

AWS 連携、VPC、認証情報の取扱い

- [Q54. AWS S3マウント等でDevinからAWSリソースを利用させる場合、パスワード・セキュリティトークン・pemファイルの扱いは？代替手段は？](docs/13-cloud-infra/q54-aws-credentials.md)
- [Q55. DevinはAWS上で動作している？VPC間接続（Devin社と自組織）は可能？](docs/13-cloud-infra/q55-aws-vpc.md)

### 14. 外部連携（Slack・PM）

Slack、Asana、Backlog、PM ツール連携

- [Q56. 複数Organization（個人契約＋会社契約）で、それぞれ別のSlackワークスペースに連携できる？](docs/14-external-pm/q56-multi-org-slack.md)
- [Q57. Slackワークスペースはプロジェクトごとに分ける必要がある？全社ワークスペース運用の問題点は？](docs/14-external-pm/q57-slack-workspace-strategy.md)
- [Q58. AsanaやBacklogとの連携は可能？](docs/14-external-pm/q58-asana-backlog.md)

### 15. 組織展開・分析

プロセス統合、標準化、マルチエージェント、生産性計測

- [Q59. 既存の人間主体の開発プロセス/ドキュメントをDevinに把握させ、人とDevinをシームレスに連携させる手順は？](docs/15-organization-ops/q59-existing-process-integration.md)
- [Q60. 標準化ドキュメントリポを渡せば、Devinは準拠したリソース構成を自動生成してくれる？](docs/15-organization-ops/q60-standards-docs-auto-resource.md)
- [Q61. 実例: `internal-standards-docs`（自社旧標準）に準拠したDevinリソース構成の手順は？](docs/15-organization-ops/q61-internal-standards-example.md)
- [Q62. 複数のDevinセッションで協業できる？リーダ→開発者/レビューア/テスター型のマルチエージェント体制は可能？](docs/15-organization-ops/q62-multi-agent-collaboration.md)
- [Q63. セッション操作履歴からユーザ＆Devinの開発生産性を計測できる？（応答時間・思考時間の取得）](docs/15-organization-ops/q63-productivity-metrics.md)

### 16. セッション停止・復旧

Sleep / Usage Settings / 再開手順

- [Q65. 「Devin went to sleep due to session usage settings」と表示されて止まるのはなぜ？対処方法は？](docs/16-session-recovery/q65-session-sleep.md)

---

## 編集について

- 編集元のモノリス `org/faq.md` は VM 内のみ参照可能（`.gitignore` 済）
- `docs/` 配下は `tools/split.py` が自動生成。直接編集しない
- 新規 Q 追加手順は [CONTRIBUTING.md](CONTRIBUTING.md) 参照

