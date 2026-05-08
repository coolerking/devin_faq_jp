---
qno: 41
title: "社内LAN内のサーバにDevinからテストできる？SaaS風のP2Pプローブ方式は？"
category: 10-database-test-quality
last_verified: "2026-04-16"
sources: []
related: []
estimated: true
---

# Q41. 社内LAN内のサーバにDevinからテストできる？SaaS風のP2Pプローブ方式は？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: DB・テスト・品質・Review](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 運用観察ベース ｜ 推定あり

### 結論: **デフォルトでは不可だが、工夫すれば可能**。標準的な解決策は大きく **(A) VPN/Zero Trust でDevinを社内に入れる** **(B) 社内にプローブを置いて中継** **(C) Enterprise VPCデプロイ**の3系統

Devin VMは**Cognitionのクラウド側で動いていて、社内LANのプライベートIP（192.168.x / 10.x）には直接到達できません**。ですが、**プローブ/トンネル方式で回避する設計**は業界で広く使われており、Devinでも実装可能です。

### なぜデフォルトで届かないか

```
Devin VM (Cognitionクラウド)
   │
   │ (公開インターネット経由)
   │
[社内ファイアウォール/NAT]
   │
   ├ 192.168.10.5  テストサーバ ← ❌ 到達不可
   └ 10.0.0.12     DB           ← ❌ 到達不可
```

- Devin VMのIPは **Cognitionのクラウド側**
- 社内プライベートIP空間には**外から入れない**のが普通
- 社内ルータ/FWに穴を開ければ別だが、セキュリティ上NG

### ⭐ 対策（実用的な順）

#### パターンA: Zero Trust / SaaS型トンネル（最推奨）

**「P2Pプローブ方式」に最も近い**。既存SaaSが成熟していて導入が楽。

```
Devin VM ──[認証済トンネル]── Relay/Controller ──[認証済トンネル]── 社内Probe
                                 (SaaS)                            (192.168.x LAN内)
                                                                       │
                                                                       ├ 192.168.10.5 テストサーバ
                                                                       └ 10.0.0.12 DB
```

**代表的なツール**:

| ツール | 方式 | Devinでの使いやすさ |
|---|---|---|
| **Tailscale** | WireGuard + 認証コントローラ | ◎（LinuxクライアントをVMに入れるだけ） |
| **Cloudflare Tunnel (cloudflared)** | 逆向きトンネル | ◎（Accessで認証、社内にcloudflaredエージェント） |
| **ZeroTier** | P2Pメッシュ | ◯ |
| **ngrok** | リバーストンネル | △（本番向きではない、PoC用） |
| **Twingate** | Zero Trustネットワーク | ◎ |

**具体的な手順（Tailscale例）**:

1. 社内に Tailscale **Subnet Router** を1台立てる（Raspberry Pi / 小さなLinuxでも可）
   ```
   sudo tailscale up --advertise-routes=192.168.10.0/24,10.0.0.0/16
   ```
2. Devin Secretsに `TAILSCALE_AUTH_KEY` を登録（ACLで最小権限）
3. Devin's Machineの Repo Setupで Tailscale クライアントをインストール:
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up --authkey=$TAILSCALE_AUTH_KEY --hostname=devin-$USER
   ```
4. これで Devin VMから 192.168.10.5に直接ping/curl可能
5. AGENTS.mdに「テストは Tailscale 経由で社内機（192.168.10.5）にアクセス」と明記
6. `.agents/skills/test-internal-lan/SKILL.md` にアクセス手順を格納

**メリット**:
- 既存SaaSで運用実績多数、セキュリティも成熟
- ACLで「このDevin VMは特定ホスト/特定ポートのみ」と絞れる
- **P2P / WireGuard ベースで暗号化**、公開IPを晒さない

**デメリット**:
- 社内に**Tailscale Subnet Router等のプローブを1台常駐**させる必要あり
- Tailscaleの契約コスト（Personal/Teamsで異なる）

#### パターンB: リバーストンネル / 逆向きプローブ

**Cloudflare Tunnel / bore / frp / rathole** などを使って、**社内プローブが外に繋ぎにいく**パターン。

```
Devin VM ──HTTP(S)── Relay (SaaS/自前) ◄──tunnel── 社内Probe
                                                     │
                                                     └ 社内サーバ叩く
```

- 社内FWを**一切開けない**のがメリット（outboundのみ）
- 企業のネットワークポリシー上、これしか許可されないケースが多い
- **Cloudflare Tunnel + Access** が現在のデファクト

**Cloudflare Tunnel構成例**:
```
社内:
  cloudflared tunnel create devin-testbed
  cloudflared tunnel route dns devin-testbed testbed.internal.example.com
  cloudflared tunnel run devin-testbed

  → testbed.internal.example.com → 192.168.10.5 にマップ

Devin:
  Secrets に Cloudflare Access の service token を登録
  curl --header "CF-Access-Client-Id: ..." https://testbed.internal.example.com/healthz
```

#### パターンC: Devin Enterpriseの VPC / 専用デプロイ

**Devin Enterprise プラン**では、**お客様のVPC内にDevinのVMを配置する**構成が選択肢になる（要セールス確認）。

- Devin VMが**社内ネットワークの一員**になるので、LAN内ホストに直接アクセス可能
- 大企業・規制業界（金融・医療）向け
- 契約・構築コストは高い

参考: https://docs.devin.ai/enterprise

#### パターンD: 踏み台SSH / Bastion + ポートフォワード

既存の**踏み台サーバ（Bastion host）** が公開IPを持っていれば、**SSHポートフォワーディング**で中継可能。

```
Devin VM ──SSH──► Bastion (公開IP) ──社内LAN──► 192.168.10.5:8080
```

**手順**:
1. 踏み台の SSH keyを Devin Secretsに登録（Devin専用の最小権限ユーザ）
2. Repo Setupで踏み台へのSSH疎通確認
3. `.agents/skills/lan-via-bastion/SKILL.md` にポートフォワード手順:
   ```bash
   ssh -f -N -L 18080:192.168.10.5:8080 devin@bastion.example.com
   # Devin側は localhost:18080 にアクセス
   curl http://localhost:18080/
   ```

**メリット**: ほぼどの社内環境でも実現可能（踏み台は既存インフラを流用）
**デメリット**: SSH key管理が煩雑、複数ホストを叩くとトンネルだらけになる

#### パターンE: Mock化 / コントラクトテストで代替

「本物の社内サーバに届かなくてもテストできる」方向性:

- **Mock Server** をDevin VM内に立てる（WireMock、MSW、Prism等）
- **Contract Test（Pact）** で相手サービスの期待動作を固定
- **VCR / Recorded responses** で本物のレスポンスを録画して再生
- 本番相当テストだけ**人手で社内環境で実行**

**Devin的に使いやすい**: VM内完結、実環境依存なし、高速。
**欠点**: 実機テストの代替にはならない（契約違反の検出が甘くなる）

### 判断フロー

```
社内LAN内のサーバをテストしたい
  ↓
本番相当のテストは年数回しかやらない？
  Yes → パターンE（Mock/Contract）+ 年次だけ人手実機
  No ↓

社内ネットワークポリシーでinbound穴あけ禁止？
  Yes → パターンB（Cloudflare Tunnel/frp等、outboundのみ）
  No ↓

全社的にZero Trustが導入されている？
  Yes → パターンA（Tailscale/Twingate を活用）
  No ↓

既存の踏み台（bastion）がある？
  Yes → パターンD（SSH port forward）
  No ↓

規制業界 / 厳格な要件？
  Yes → パターンC（Devin Enterprise VPC）
```

### セキュリティ上の鉄則

#### 1. 最小権限でトンネルを設計
- **Tailscale ACL**で「Devin VMは 192.168.10.5:8080のみ、かつ GET/POSTのみ」等に絞る
- **Cloudflare Access** のポリシーで「特定のservice tokenのみ許可」

#### 2. 認証情報はDevin Secretsで管理
- Tailscale authkey / Cloudflare service token / SSH keyは**すべてSecrets**
- **ACL付き、期限付き**で発行（可能なら）

#### 3. テスト対象を専用に
- 「**Devinからアクセス可能なホストはテスト用のみ**」と物理分離
- 本番ホストとはVLANを分ける、FWでアクセス元を制限

#### 4. 監査ログ
- Tailscale / Cloudflareの接続ログを有効化
- 「いつ Devin VMが社内機に接続したか」の追跡可能性を確保

#### 5. 本番DBとは絶対繋がない
- トンネル経由でも**本番DBの接続情報はDevin Secretsに入れない**
- テスト用Replicaや別環境のみ

### Devin側の具体的な実装

#### Repo Setup 例（Tailscale経由）

**Install Dependencies**:
```bash
# Tailscale 本体
curl -fsSL https://tailscale.com/install.sh | sh
# VPN接続テストツール
apt-get install -y curl jq
```

**Maintain Dependencies** (毎セッション開始時):
```bash
# Tailscale起動（authkeyはSecretsから）
sudo tailscale up --authkey="$TAILSCALE_AUTH_KEY" --hostname="devin-session" --reset
# 疎通確認
ping -c 1 192.168.10.5 || echo "LAN unreachable"
```

**Additional Notes**:
```
社内LANアクセスは Tailscale 経由。
テストサーバ: testbed.lan.example.com (192.168.10.5)
DB: db.lan.example.com (10.0.0.12)
本番への接続は禁止、Secretsにも本番情報を入れないこと。
```

#### AGENTS.md 例

```markdown
## 社内LAN接続

このrepoのテストには社内サーバへのアクセスが必要です。

## 接続方法
- Tailscale で社内ネットワークに接続済み（Repo Setup で自動起動）
- 疎通確認: `tailscale status` で online になっていること

## テスト対象
- API サーバ: https://testbed.lan.example.com
- DB: postgres://db.lan.example.com:5432/testdb

## 禁止事項
- 本番環境（prod.*）への接続は絶対禁止
- Secretsには本番認証情報を登録しない
```

#### Skill 例

`.agents/skills/test-internal-lan/SKILL.md`:
```yaml
---
name: test-internal-lan
description: 社内LAN越しのE2Eテスト実行手順
---

## 事前確認
1. `tailscale status` で `online` になっていることを確認
2. `curl -I https://testbed.lan.example.com/healthz` で200を確認

## 実行
1. `npm run test:integration -- --env=lan-testbed`
2. 失敗時: `tailscale status` でVPN切断を疑う、`sudo tailscale up --reset`

## トンネルが切れたとき
- Secrets の TAILSCALE_AUTH_KEY が期限切れ → 新しいkeyを発行してSecrets更新
```

### プローブ常駐サーバの要件（社内に置くマシン）

| 要件 | 推奨 |
|---|---|
| OS | Linux（Ubuntu / Raspberry Pi OS等） |
| スペック | CPU 1コア / RAM 512MB〜 でも可（軽量） |
| ネットワーク | Outbound only (HTTPS 443) |
| 常時起動 | ◎（不在時にもDevinがテスト可） |
| 監視 | エージェント停止時にアラート |
| 更新 | 自動アップデート（Tailscale / cloudflared） |

### Devin的な活用イメージ

```
ユーザ: 「社内のテストサーバ（192.168.10.5）のAPIが最新化されたので、
         retryロジックに副作用がないかE2Eで確認して動画送って」

Devin:
  1. Tailscaleで社内LANに接続（Repo Setup済み）
  2. curl で testbed.lan.example.com に疎通確認
  3. test-internal-lan Skill を参照
  4. Playwright でテストシナリオ実行
  5. Test Mode で録画
  6. 結果動画を添付してPR化
```

→ **社内LANにDevinを「招き入れる」設計**ができれば、クラウドVMからでも社内システムを自由にテストできる。

### まとめ

| 観点 | 結論 |
|---|---|
| デフォルトで社内LANに届く？ | **❌ 届かない**（DevinはCognitionクラウド側） |
| 可能な解決策 | **(A) Zero Trust / VPN** / **(B) リバーストンネル** / **(C) Enterprise VPC** / **(D) 踏み台SSH** / **(E) Mock化** |
| 初心者推奨 | **パターンE（Mock）** で回避 or **パターンA（Tailscale）** |
| 大企業推奨 | **パターンB（Cloudflare Tunnel）** or **パターンC（Devin Enterprise VPC）** |
| 常駐プローブが必要？ | **パターンA/B/Dは必要**（社内に1台Linux機） |
| セキュリティ設計 | **最小権限ACL**、**Secrets管理**、**テスト専用ホスト分離**、**本番接続禁止** |
| Devin側の実装 | **Repo Setup + Secrets + Skill + AGENTS.md** の4点セット |

**核心**: SaaSのP2Pプローブ方式と同じ思想で **「社内に小さなエージェントを置いて、Devin VMから認証済みトンネルで中継する」** 設計が実用解。Tailscale / Cloudflare Tunnelがデファクト。初心者が短期で踏み込むのは重いので、**まずはMock化でしのぐ**→ **必要になったらTailscale導入**が段階的導入の王道です。

---

[← Q40. テストの種類ごとに使い方が変わる？（単体〜回帰・負荷・総合）](q40-test-types.md) ｜ [Q42. テスト駆動開発（TDD）は可能？Devinをどう使えばできる？ →](q42-tdd.md)
