# 新規 Q 追加・更新手順

このリポジトリは **`org/faq.md`（VM内専用・gitignore済）が source of truth** で、
`docs/` 配下は `tools/split.py` により自動生成される構成。

## 編集の流れ（方針 A）

```
[編集] org/faq.md  ──────►  python tools/split.py  ──────►  docs/ 配下が再生成
                                                              │
                                                              ▼
                                                         git diff で差分確認
                                                              │
                                                              ▼
                                                       PR を作成（org/ は ignore で含まれない）
```

### 1. 新規 Q の追加

1. `org/faq.md` を開く（VM 内のみ参照可）
2. 末尾の最大 Q 番号を確認 → 次の番号で新規 Q セクションを既存と同形式で追加:
   ```markdown
   <a id="qNN"></a>

   ## QNN. （タイトル）
   > **メタ**: 最終確認日 YYYY/M/D ｜ 根拠 https://... ｜ 推定あり/なし

   ### 結論: ...
   ```
3. `tools/split.py` の `QMAP` に Q番号 → (カテゴリディレクトリ, slug) のエントリを追加
4. `python tools/split.py` を実行
5. `docs/` 配下の差分を確認（新ファイル + 索引更新）
6. `git add docs/ tools/split.py` で commit（`org/` は ignore で除外）
7. PR を作成

### 2. 既存 Q の更新

1. `org/faq.md` の対象 Q を編集
2. `python tools/split.py` を実行
3. `git diff docs/` で差分確認
4. commit & PR

### 3. カテゴリ追加

1. `tools/split.py` の `CATEGORIES` に新カテゴリを追加（番号は連番）
2. 該当 Q の `QMAP` エントリで新カテゴリディレクトリ名に変更
3. `python tools/split.py` を実行

## ファイル命名規則

- `q{NN}-{slug}.md`（例: `q07-devin-pricing.md`）
- `NN`: 2 桁ゼロ埋めの Q 番号
- `slug`: kebab-case の英小文字（5 語以内推奨）

## 検証

PR 前に手元で確認:

```bash
# Q ファイル数（70）
find docs -name "q*.md" | wc -l

# UTF-8 妥当性
find docs -name "*.md" -exec python -c "open('$0').read().encode('utf-8')" {} \;

# クロス参照（残存 anchor リンクがないこと）
grep -r '\[Q[0-9]\+[^]]*\](#q[0-9]\+)' docs/ || echo "OK: no anchor xrefs left"

# 索引整合性（README の Q 一覧と実ファイル数が一致）
grep -c '^- \[Q[0-9]' README.md
```

## 禁止事項

- `docs/` 配下を直接編集しない（`tools/split.py` の出力で上書きされる）
- `org/` 配下を `git add` しない（`.gitignore` で防いでいるが、`-f` 強制追加禁止）
- `git push --force` を main に対して行わない

## CHANGELOG

新規 Q 追加・既存 Q の大幅更新時は `CHANGELOG.md` に追記。
