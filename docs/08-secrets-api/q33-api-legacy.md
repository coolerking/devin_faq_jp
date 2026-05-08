---
qno: 33
title: "API Keyタブの「Legacy」は今後なくなる？変更される？"
category: 08-secrets-api
last_verified: "2026-04-16"
sources:
  - https://docs.devin.ai/api-reference/authentication
related: []
estimated: false
---

# Q33. API Keyタブの「Legacy」は今後なくなる？変更される？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: Secrets・API](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 https://docs.devin.ai/api-reference/authentication ｜ 推定なし

### 結論: **Yes、Legacy API Keyは「deprecated（廃止予定）」**。新規開発は**v3 + Service User API Key（`cog_` prefix）に移行すべき**。現行のLegacyは**当面動作し続ける**が、新機能はサポートされない

参考: https://docs.devin.ai/api-reference/authentication

### Legacyと 新方式の違い

| 項目 | **Legacy（旧、廃止予定）** | **新（現行推奨）** |
|---|---|---|
| 対象API | **v1 / v2** | **v3** |
| Key prefix | 旧形式（`cog_` 以外のレガシー・プレフィックス） | **`cog_`** 統一（Service User API Key / Personal Access Tokenともに） |
| 発行場所 | Settings > API Keys | Settings > Service Users / API Keys |
| RBAC（権限制御） | ❌ 非対応 | ✅ 対応 |
| Session attribution | ❌ 非対応 | ✅ `create_as_user_id` で人のセッションとして記録 |
| Cursor-based pagination | ❌ 非対応 | ✅ 対応 |
| Impersonation | ❌ | ✅ `ImpersonateOrgSessions`権限で他ユーザとしてsession作成 |
| 新機能サポート | **なし** | **継続追加** |

### 推奨される移行方針

#### 1. 新規開発は**Service User API Key（`cog_`）** で開始
```bash
# 新方式
curl -X POST https://api.devin.ai/v3/organizations/$ORG_ID/sessions \
  -H "Authorization: Bearer cog_XXXXXXXXXX"
```

#### 2. 既存のLegacy Keyがある場合
- **移行ガイド**を参照: https://docs.devin.ai/api-reference/getting-started/migration-guide
- v1/v2コード → v3に書き換え
- 旧プレフィックスのLegacy Key → `cog_` で発行し直し
- **できるだけ早めに移行**（いつ廃止でも動けるように）

#### 3. 人間としてAPI呼びたい場合
- **Personal Access Token（PAT）** が用意されているが **closed beta**（本FAQ最終更新 2026/4/16 時点，`https://docs.devin.ai/api-reference/personal-access-tokens` にて明記）
- SSO / Enterprise アカウントでは**利用不可**
- 必要なら support@cognition.aiに連絡してfeature flag 有効化を依頼
- それ以外は**Service User API Key**を作って運用

### Service User（推奨される新しい扱い）

#### メリット
- **非人間アカウント**として独立した監査可能なIdentity
- **RBAC**で最小権限に絞れる
- 退職者・異動の影響を受けない
- **Enterprise Service User**はorg横断で使える

#### 設定手順（概略）
1. `Settings > Service Users` で新規作成
2. Role（権限）を割当
3. API Key発行 → **1回だけ表示**されるのでその場で保存
4. `cog_` プレフィックスのKeyを `Authorization: Bearer` で利用

### Legacyはいつ実際になくなる？

公式の明示的な期限は**現時点で非公開**ですが:
- **"deprecation period"**（廃止猶予期間）中は動く
- 新機能が追加されない＝徐々に使い物にならなくなる
- ドキュメント上は **v3 + service user** への移行を明確に推奨

→ **「今すぐ止まる」ことはないが、「いつかは必ず止まる」**前提で動くのが安全。

### 実装への影響（やるべきこと）

#### ⭐ すぐやる
1. **新規のCI/CD、Bot、Integration開発はすべて`cog_` Service User Key**で実装
2. 既存で Legacy Key（`cog_` 以外）を使っているスクリプトをリストアップ
3. **v1/v2エンドポイント依存**を v3に書き換え計画

#### 近いうちにやる
4. **Secretsに登録している Legacy Key** を新Keyに差し替え
5. GitHub Actions等のsecretsを更新
6. Legacy Keyをrevoke（破棄）

#### 継続監視
7. リリースノートで**deprecation期限が発表**されたら即対応
8. 年1回はAPI Keyの棚卸し

### よくある落とし穴

#### 1. Legacy / 新が混在して混乱
- 新旧で**エンドポイントのパス構造**が違う（v2 vs v3）
- **プロジェクト内で統一**、移行中はコメントで明示

#### 2. Legacy Keyをそのまま永続化
- 「動いているからいいや」で放置→ある日突然動かなくなる
- **計画的移行**必須

#### 3. PATが使えると思っていた
- PATは**closed beta**、SSOでは使えない
- 人間の操作はUIで、プログラム操作はService Userで

#### 4. Service User Keyを**チーム全員で共有**
- ちゃんと**RBACで絞る**、用途別に分ける（CI用・Bot用・Dashboard用）

#### 5. Key漏洩対策忘れ
- v3用 Service User Key / Legacy Key どちらも `cog_` prefix。**コードにベタ書きしない**
- Devin Secretsか環境変数で管理
- 漏洩時は**即revoke**

### まとめ

| 観点 | 結論 |
|---|---|
| Legacy API Keyの将来 | **deprecated（廃止予定）**、当面動くが新機能なし |
| 新方式 | **v3 + Service User API Key（`cog_` prefix）** |
| 推奨行動 | **新規開発は新方式、既存は計画的に移行** |
| PAT（人間用） | **closed beta**（本FAQ最終更新 2026/4/16 時点）、SSO不可、まだ限定利用 |
| 廃止日 | **未公開**、ただし「いつかは必ず止まる」前提で動く |
| 移行ガイド | https://docs.devin.ai/api-reference/getting-started/migration-guide |

**今後の方針**:
1. 新しいAPI連携は**必ず`cog_` Service User Keyで実装**
2. 既存Legacy Keyは**リストアップ→計画的移行**
3. リリースノート購読で**廃止期限を逃さない**

**核心**: Legacyは**今後なくなる方向**。今からは`cog_` Service User Keyに寄せて運用するのが正解。既存スクリプトは時間があるうちに移行しておくのが安全です。

---

[← Q32. Devin API Keyの使い方は？（API操作・MCP・Skill経由）](q32-api-key.md) ｜ [Q34. 別々のセッションで並行作業している場合、それぞれのスコープはブランチ/ワークツリーか？ →](../09-multi-session-repo/q34-parallel-sessions.md)
