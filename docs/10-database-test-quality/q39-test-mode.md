---
qno: 39
title: "Devin Test Modeとは？何ができて、通常とはどう違ってどうすればTest Modeになる？"
category: 10-database-test-quality
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/work-with-devin/testing-and-recordings
related: []
estimated: false
---

# Q39. Devin Test Modeとは？何ができて、通常とはどう違ってどうすればTest Modeになる？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: DB・テスト・品質・Review](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/work-with-devin/testing-and-recordings ｜ 推定なし

### 結論: **PR作成後に自動でアプリをE2Eテストし、動画で証跡を残す構造化ワークフロー**

Test Modeは、Devinが「**PRを作った後に、そのアプリを実際に起動してブラウザで操作し、動画録画つきで動作確認する**」専用モード。レビュアーが動画を見て「うん、動いてる」と即マージできることを目的とした仕組み。

参考:
- https://docs.devin.ai/work-with-devin/testing-and-recordings
- https://docs.devin.ai/work-with-devin/computer-use

### 通常モード（Session）との違い

| 観点 | 通常Session | **Test Mode** |
|---|---|---|
| 主目的 | コードを書く・PRを作る | **書いたコードが動くことを証明する** |
| 入力 | Issue / タスク指示 | **作成済みPRの内容** |
| 実行 | コード編集・commit・push | **アプリ起動 → ブラウザ操作 → 録画** |
| 出力 | PR | **テスト計画 + 動画ファイル** |
| ブラウザ | 任意（調査用） | **必須（Computer Useで実操作）** |
| 画面録画 | なし | **自動録画 + アノテーション** |
| 完了条件 | PR作成・CIグリーン | **動画送信まで** |
| 新規Skill提案 | する | **テスト中の学びを強くSkill化** |

→ Test Modeは通常Sessionの**延長線上の特別フェーズ**（別セッションではない、同じセッション内のフェーズ遷移）。

### Test Modeの3フェーズワークフロー

#### Phase 1: Setup（環境準備）
- PRとコードベースを読み、何をテストすべきか理解
- `.agents/skills/` の関連Skillを参照（例: `testing-frontend/SKILL.md`）
- 必要なサービス（DB, Redis）を起動
- ログインが必要なら認証（Secretsから / 対話で要求）
- 環境確認（ローカル / staging / dev）

Repo Setupが済んでいれば**ここが超速くなる**。

#### Phase 2: Test planning（テスト計画）
- **1つの最重要E2Eフロー**を特定（「ログイン→ToDo追加→保存→表示」など）
- **具体的で曖昧性のないステップ**を書く（「右上のSaveボタンをクリック」等）
- コードをトレースしてUIパスを実際に確認
- ユーザに計画をメッセージで送る → 修正依頼可

#### Phase 3: Recording and execution（録画・実行）
- CIがグリーン・レビュー対応が済んでいるのを確認
- **画面録画開始**
- **アノテーション**をつけながらブラウザを操作（「Testing login flow」等のラベル表示）
- **Auto-zoom**: クリック位置に自動でズームイン
- 録画停止 → 動画処理（速度調整・ハイライト）
- **動画を添付ファイルとしてメッセージ送信**

### 何ができるか

#### ✅ できること
- **アプリをVM内で起動**（dev server, docker compose等）
- **ブラウザでUI操作**（Chrome / Playwright / Computer Use）
- **デスクトップGUI操作**（Electronアプリ、IDE、TUI等も）
- **動画録画**（アノテーション・Auto-zoom付き）
- **スクリーンショット**（レイアウト検証）
- **ログイン・認証フロー**（Secrets使用、対話で追加取得）
- **ステージング環境への接続テスト**（URL指定）
- **Skill Suggestions**: テストで得た知見を `.agents/skills/` に残すPR提案

#### ❌ できないこと・不向き
- 網羅的な全ケーステスト（短い1フロー前提）→ それは既存のテストスイートとCIで
- 数十分かかる長時間シナリオ
- 複数ブラウザ/複数OS同時検証（1 VM/1 desktop 1024×768）
- 本番環境での操作（接続させない運用）

### Test Modeに入る方法

#### ⭐ 方法1: PR作成後の「Test the app」ボタン（標準）
PRが作られるとDevinがメッセージで**Test the app ボタン付きの提案**を出す。クリックするとTest Modeに入る。

#### 方法2: Sessionで自然言語で依頼
セッション中のどのタイミングでもOK:
- 「test the changes you just made and send me a recording」
- 「ログイン画面の動作を確認して動画を送って」
- 「checkout flowを最初から最後まで試して」

#### 方法3: PR 作成後の自動トリガー
PR 作成後に**ボタンを押さなくても自動で Test Mode に入る**トリガー設定。公式ドキュメント（`docs.devin.ai/work-with-devin/testing-and-recordings`）で最新の提供状況を確認すること（本 FAQ 最終更新 2026/4/16 時点では自動トリガーは "coming soon" の記載あり）。

### 前提設定（Test Modeを使うために）

#### 1. Desktop modeを有効化（組織設定）
```
Settings > Customization > Browser interaction
  → Enable desktop mode: ON
```
- 組織管理者のみ変更可
- 全プランで利用可能

#### 2. Repo Setupの整備
- 依存インストール、DB起動、dev server起動コマンドを登録
- **これがないとTest Mode Phase 1で時間を食う**
- 例:
  ```
  npm ci
  docker compose up -d db
  npm run migrate
  npm run dev
  ```

#### 3. `.agents/skills/` にテスト用Skillを置く（推奨）
例: `.agents/skills/testing-frontend/SKILL.md`
```yaml
---
name: testing-frontend
description: フロントエンドPR前にdev serverを起動してページを検証
---

## Setup
1. `npm install`
2. `docker-compose up -d postgres`
3. `npx prisma migrate dev`
4. `npm run dev`
5. `http://localhost:3000` でReadyを待つ

## Verify
1. git diffで変更ページを特定
2. ブラウザで各ページを開く
3. コンソールエラー / レイアウト崩れ / リンク切れをチェック
4. Desktop (1280px) / Mobile (375px) でスクリーンショット
```
→ Test ModeのPhase 1-2でDevinがこれを自動参照する

#### 4. ログイン情報・認証情報をSecretsに登録
- `TEST_USER_EMAIL` / `TEST_USER_PASSWORD`
- 初回の対話で要求 → Secretsに保存 → 次回以降自動使用

### 出力される動画の特徴

- **アノテーション**: 重要な瞬間にテキストラベル表示（「Login successful」等）
- **Auto-zoom**: クリックしている箇所に自動ズームイン、アイドル時は引く
- **速度調整**: 待ち時間は早送り、重要操作は通常速度
- **短尺**: レビュアーが数十秒〜1分程度で見られる長さに圧縮
- **配信**: セッション内に添付ファイルとして送信（WebappやSlackで再生可）

### よくあるトラブルと対処

| 症状 | 原因 | 対処 |
|---|---|---|
| Test the app ボタンが出ない | コード変更のあるPRが作られていない | 「testして動画送って」と自然言語で依頼 |
| 録画が失敗 | アプリがテスト中にクラッシュ / 動画処理タイムアウト | 「Try recording again」で再試行依頼 |
| アプリにアクセスできない | ログイン壁 / VPN要 | Secretsに認証情報登録 / Interactive Browserで手動認証 / Repo Setupを整備 |
| テストが的外れ | Test計画が曖昧 | Phase 2の計画時にユーザから修正指示を入れる |

### 良い依頼 / 悪い依頼

#### ✅ 良い依頼
- 「checkout flowをテスト: カートにアイテム追加→checkout→フォーム入力→注文確認ページで合計額が正しいことを確認」
- 「dark mode toggleを設定ページでテスト: テキストが読めるか、要素が消えないか」
- 「CSV エクスポートがダウンロードされ、ヘッダーが正しいか確認」

#### ❌ 悪い依頼
- 「全部テストして」
- 「アプリが動くか確認」
- 「壊れてないかチェック」

### Skill Suggestionsとの連携

Test Mode中に得た知見（「このrepoのdev serverは立ち上げに30秒かかる」「ログインにはXを入力する」等）から、**Skill化のPRを自動提案**してくれる。これがDevinの独自機能の強みで、**テストを繰り返すたびにTest Mode自体が賢くなる**。

### まとめ

1. **Test Mode = PR作成後の自動E2E検証＋動画提出フェーズ**
2. 通常Sessionとの違い: **コードを書く** vs **書いたコードが動くことを証明する**
3. Phase 1-3（Setup→計画→録画実行）の構造化フロー
4. 開始方法: **「Test the app」ボタン** / 「testして動画送って」 / 近日自動化
5. 前提: **Desktop mode有効化** + **Repo Setup整備** + **テスト用Skill** + **Secrets登録**
6. 出力: **アノテーション・Auto-zoom付き動画**（数十秒〜1分程度）
7. Skill Suggestionsと連動してテスト知見をSkill化、**使うほど賢くなる**

**核心**: **Test Mode は PR 完成後の E2E 検証用モード**。通常モードとは別の権限・動線を持ち、明示的に遷移する。

---

[← Q38. テスターとしてDevinを扱う場合、結合テスト以降は外部テスト環境を立てるべき？](q38-integration-test-env.md) ｜ [Q40. テストの種類ごとに使い方が変わる？（単体〜回帰・負荷・総合） →](q40-test-types.md)
