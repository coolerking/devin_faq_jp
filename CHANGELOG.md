# Changelog

## 2026-08-05

### Q71 追加（71問）

- `docs/02-pricing/q71-personal-pro-email-limit.md` を追加（2026年4月の料金改定後に個人Proプランが選択できない理由と対処）
- `tools/split.py` の `QMAP` に Q71 を追加
- ルート `README.md`・`docs/02-pricing/README.md` の索引を更新（総質問数 70→71、02 料金・プラン 2→3）

## 2026-04-17

### 初版（70問）

- モノリス `org/faq.md`（16,353行・70問）から `docs/` 配下に分割
- カテゴリ 16 件で構成
- `tools/split.py` で自動生成・再生成可能
- トップ `README.md`、各カテゴリ `README.md` を自動生成
- クロス参照を `[QN](#qN)` から相対パスリンクへ書き換え
- YAML frontmatter（最小限: qno, title, category, last_verified, sources, related, estimated）を各 Q ファイルに付与

### 含まれる Q カテゴリ

01. Devin入門（Q1〜Q6）
02. 料金・プラン（Q7, Q70）
03. 基本操作・セッション（Q8〜Q11）
04. GitHub・SCM連携（Q12〜Q17, Q64, Q67, Q68）
05. IDE・エディタ・CLI（Q18〜Q21, Q69）
06. コマンド・スキル（Q22〜Q25）
07. Devinリソース（Q26〜Q30）
08. Secrets・API（Q31〜Q33）
09. マルチセッション・複数リポ（Q34〜Q35）
10. DB・テスト・品質・Review（Q36〜Q44）
11. データ入出力・ドキュメント理解（Q45〜Q49）
12. セキュリティ・監査・ガバナンス（Q50〜Q53, Q66）
13. クラウド連携・インフラ（Q54〜Q55）
14. 外部連携（Slack・PM）（Q56〜Q58）
15. 組織展開・分析（Q59〜Q63）
16. セッション停止・復旧（Q65）
