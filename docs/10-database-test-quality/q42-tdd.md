---
qno: 42
title: "テスト駆動開発（TDD）は可能？Devinをどう使えばできる？"
category: 10-database-test-quality
last_verified: "2026-04-16"
sources: []
related: []
estimated: false
---

# Q42. テスト駆動開発（TDD）は可能？Devinをどう使えばできる？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: DB・テスト・品質・Review](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 運用観察ベース ｜ 推定なし

### 結論: **可能、かつDevinはTDDと相性が良い**。ただしDevinの標準動作は「実装先行→テスト後付け」寄りなので、**明示的に「TDDモード」で依頼する**仕組みを作ると効く

Devinは**テストを書く・実行する・修正するサイクルが自律で回せる**ので、Red-Green-Refactorループを任せやすい。一方で指示しないと**「実装→テスト」の順**で動きがちなので、**Red-Firstを明示的に指示**する設計が必要です。

### TDDのサイクルとDevinの対応

#### 古典的TDDサイクル（Red → Green → Refactor）

```
1. Red:      失敗するテストを書く（まだ実装がない）
2. Green:    最小の実装でテストを通す
3. Refactor: 重複除去・可読性改善（テストは通り続ける）
```

#### Devin対応マッピング

| フェーズ | Devinができること | 注意点 |
|---|---|---|
| **Red** | 要件からテストケース生成、既存コードの網羅性検証 | **「実装はまだ書かない」と明示** |
| **Green** | テストをパスする最小実装を書く | オーバーエンジニアリングを避けさせる |
| **Refactor** | 重複除去・命名改善・パターン抽出 | **テストが通り続けること**を制約に |

### ⭐ Devinに「TDDモード」で依頼する方法

#### 方法1: Playbook化（最推奨）

**Playbook「TDD Cycle」**を作成すると、ワンコマンドでRed-Green-Refactorループを回せる:

```
名前: TDD for new feature
本文:
  1. 要件を整理して、最小の失敗するテストを書く（まだ実装は書かない）
  2. `npm test` でテストが失敗することを確認（Red）
  3. テストをパスする最小限の実装を書く
  4. `npm test` でテストがパスすることを確認（Green）
  5. リファクタリング: 重複・命名・責務分離を改善
  6. `npm test` でテストが通り続けていることを確認（Refactor）
  7. 次の要件に進む（ステップ1に戻る）
  8. 全要件完了でPR作成
```

→ 「Playbook TDD Cycleで `calculateTax` 関数を実装して」と依頼 → Devinが厳密にRed→Green→Refactorを守って進める。

#### 方法2: Skillに手順を書く

`.agents/skills/tdd/SKILL.md`:
```yaml
---
name: tdd
description: テスト駆動開発のサイクルに従って実装する
---

## 原則
- **必ずテストを先に書く**
- **1サイクル1テスト**: 一度に複数のテストを書かない
- **最小実装**: 仮実装（ベタ書き）から始めて、複数テストで三角測量
- **Refactor時はテスト追加しない**

## サイクル手順

## 1. Red
1. 要件を1つだけ選んで、最小の失敗テストを書く
2. `npm test -- <該当ファイル>` で **失敗すること**を確認
3. **実装コードには一切触れない**

## 2. Green
1. **最小限の実装**（仮実装OK）でテストをパスさせる
2. `npm test` でグリーンを確認
3. 仮実装（ハードコード等）のままでもOK

## 3. Refactor
1. 重複除去、命名改善、責務分離
2. **各変更後に `npm test` で通ることを確認**
3. 新しいテストは追加しない
4. 不安なら小さいコミットに分けて `git commit`

## 完了条件
- すべての要件に対応するテストが書かれている
- すべてのテストがパスする
- カバレッジ80%以上（可能なら）
- Lint/Type check がクリーン

## 禁止事項
- テストを書かずに実装を進める
- Refactor中にテストを追加・変更する
- 一度に複数のテストを書いてまとめて実装する
```

#### 方法3: AGENTS.mdにプロジェクト全体のTDDポリシーを書く

```markdown
## 開発スタイル

このプロジェクトはTDD（テスト駆動開発）を採用しています。

- **新機能追加時は必ずテストを先に書く**
- Red → Green → Refactor のサイクルを守る
- 詳細は `.agents/skills/tdd/SKILL.md` を参照
```

→ どのセッションでも自動で注入され、Devinは常にTDDで動く。

#### 方法4: 依頼プロンプトで明示

```
「TDDで `calculateTax` 関数を実装してください。
 - まず失敗テストを1つ書く（実装はまだ書かない）
 - テストが失敗することを確認
 - 最小実装でパスさせる
 - リファクタ
 - 次の要件（通常の単価、軽減税率、複数商品）も同じサイクルで追加
 - 各サイクルの終わりに `npm test` の結果を見せて」
```

### TDDの3つの流派とDevin対応

#### 1. Classical TDD（古典派、Chicago School）
- 状態ベースのテスト中心
- ユニットテストで**実際の依存**を使う（Mock最小限）
- **Devin相性: ◎** シンプルで依頼しやすい

#### 2. Mockist TDD（ロンドン派）
- インタラクションベースのテスト中心
- **Mock/Stub多用**、外界との会話を検証
- **Devin相性: ◯** Mock指示が細かく必要

#### 3. BDD（振る舞い駆動開発）
- Given-When-Thenでシナリオ記述
- Cucumber / Jest等の `describe/it`
- **Devin相性: ◎** 自然言語に近いので依頼しやすい

### 具体的なTDDセッション実行例

#### 例: `calculateTotal(items)` 関数をTDDで実装

**Devinへの指示**:
```
「TDD Cycle Playbookで `calculateTotal` 関数を実装。
 要件:
 1. 空配列は 0
 2. 1商品は価格そのもの
 3. 複数商品は合計
 4. 税率（10%）を適用
 5. 割引コード `SUMMER10` で10%オフ」
```

**Devinの期待動作**:

##### Cycle 1: 空配列
```typescript
// Red
test('empty array returns 0', () => {
  expect(calculateTotal([])).toBe(0);
});
// 実行 → Error: calculateTotal is not defined
```
```typescript
// Green (最小実装・仮実装)
export function calculateTotal(items: Item[]) {
  return 0;
}
// 実行 → Pass
```
→ Refactor不要、次へ

##### Cycle 2: 1商品
```typescript
// Red
test('single item returns its price', () => {
  expect(calculateTotal([{ price: 100 }])).toBe(100);
});
// 実行 → Fail
```
```typescript
// Green
export function calculateTotal(items: Item[]) {
  if (items.length === 0) return 0;
  return items[0].price;
}
// Pass
```

##### Cycle 3: 複数商品（三角測量）
```typescript
// Red
test('multiple items sum up', () => {
  expect(calculateTotal([{ price: 100 }, { price: 200 }])).toBe(300);
});
// Fail
```
```typescript
// Green
export function calculateTotal(items: Item[]) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
// Pass (Cycle 1, 2もPass継続)
```

##### Cycle 4-5: 税・割引（省略）

##### Refactor
- 定数（税率、割引率）の抽出
- 戦略パターンで割引ロジック分離
- 各変更で `npm test` 実行

### 既存コードへのTDD導入（レガシー改修）

**Characterization Test + TDD**:
```
1. 既存コードの**現状の挙動を固定するテスト**を書く（Characterization Test）
2. そのテストを動かしつつ、リファクタ
3. 新機能は普通にTDDで追加
```

**Devinへの依頼**:
```
「legacy-pricing.ts のリファクタリング。
 1. まず現状の挙動を固定するテストを書く（テストが通る状態を作る）
 2. 安全にリファクタ（毎ステップ `npm test` で確認）
 3. 新要件「送料無料の閾値変更」はTDDで追加」
```

### TDDでDevinを使うメリット

#### 1. 要件をテストコードで明確化できる
- 自然言語のあいまいさをテストで固定
- Devinが「テストを通す」という明確なゴールに向かえる

#### 2. 実装の過剰生成を抑制
- 「テストをパスするだけの最小実装」に絞れる
- Devin特有の親切すぎる実装を抑止

#### 3. 回帰防止
- 各サイクルで全テストが通ることを保証
- 副作用が早期発見できる

#### 4. レビューが楽
- PRに「テスト追加→実装」の流れが記録される
- コミット履歴がRed-Greenで明確

### TDDでDevinが苦手なケースと対処

#### 苦手1: UIのTDD
- UIテスト（Storybook / Visual Regression）はTDDと相性が悪い
- **対処**: **単体テストだけTDD**、UIはTest ModeでE2E検証

#### 苦手2: 大きすぎる要件を一気に渡す
- 「この機能全部TDDで」→ Devinがサイクルを省略しがち
- **対処**: **要件を小さく分解**、1セッションで3-5サイクル程度に絞る

#### 苦手3: Mock/Stubの設計
- ロンドン派TDDで複雑なMock階層を組ませると事故る
- **対処**: **インタフェース設計を先に人間がレビュー**、DevinはMock実装から任せる

#### 苦手4: 仕様変更時の既存テスト修正
- 「Redを維持したまま既存テストを変えて」が難しい
- **対処**: **1テストずつ変更→Greenを確認**、を明示的に指示

### TDD × Devin 機能の組み合わせ表

| 機能 | TDDでの役割 |
|---|---|
| **Session** | サイクル実行本体 |
| **Playbook** | ⭐ Red→Green→Refactorを固定化 |
| **Skill（.agents/skills/tdd/）** | ⭐ 手順の定型化、全セッション共有 |
| **AGENTS.md** | プロジェクト全体のTDDポリシー宣言 |
| **Repo Setup（Set up Tests）** | `npm test` 等の即時実行可能化 |
| **Devin Review** | PRのRed-Green順序を自動確認 |
| **Test Mode** | UIのE2Eは別途動画検証 |

### 推奨セットアップ手順（TDD開始時）

1. **AGENTS.mdに TDD ポリシー明記**
2. **`.agents/skills/tdd/SKILL.md` を作成**
3. **Playbook「TDD Cycle」をDevin Webappで作成**
4. **Repo Setupの「Set up Tests」に `npm test -- --watch=false` を登録**
5. **テストフレームワーク整備**（Jest / Vitest / pytest / RSpec等）
6. **最初のサイクルを1つDevinに依頼して動きを確認**
7. **Slack連携**（あれば）で「サイクル完了」の通知をオンに

### 依頼プロンプトの良し悪し

#### ✅ 良い依頼
- 「TDD Cycle Playbookで `formatPrice` を実装。要件は: 1) 整数→`¥1,000`形式, 2) 小数→四捨五入, 3) 負の数→括弧表記。1要件1サイクルで進めて」
- 「legacy-auth.ts をTDDでリファクタ。まずは現状固定テストを書いてから、cycle式に改善」

#### ❌ 悪い依頼
- 「TDDで決済システム全部作って」（要件が大きすぎる）
- 「テストも書いといて」（TDDじゃなく後付けテストになる）

### まとめ

| 観点 | 結論 |
|---|---|
| Devin × TDDは可能か | ✅ **可能、むしろ得意領域** |
| 標準動作 | 放置すると「実装→テスト」順になる、**明示指示が必要** |
| 推奨仕組み | **Playbook「TDD Cycle」** + **Skill** + **AGENTS.md** |
| 最小実装 | 最初はPlaybookだけでも効く |
| 苦手領域 | UIのTDD、大きい要件の一括TDD、複雑なMock設計 |
| 粒度 | **1セッション = 数サイクル**で回す、要件を小さく分解 |
| 組み合わせ | Devin Reviewで順序確認、Test ModeでUI検証は別系統 |

**初心者向けの始め方**:
1. 小さい関数（ユーティリティ関数など）から始める
2. AGENTS.mdに「TDDで進める」と宣言
3. Playbookを1つ作って、それ経由で依頼する
4. 慣れたら機能単位・クラス単位に拡大

**核心**: **「Devinに任せるTDD」は「人間がやるTDDを指示で再現する」こと**。Playbook/Skillで手順を固定化しておけば、Devinは忠実にサイクルを守る。放置すると実装先行になるので、**TDDモードの明示が最大のコツ**。

---

[← Q41. 社内LAN内のサーバにDevinからテストできる？SaaS風のP2Pプローブ方式は？](q41-internal-network-test.md) ｜ [Q43. Reviewタブはどういう機能？使い方・レビュー範囲・観点 →](q43-review-tab.md)
