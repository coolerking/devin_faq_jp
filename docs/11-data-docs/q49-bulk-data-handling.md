---
qno: 49
title: "Devinに大量データを連携させるには？"
category: 11-data-docs
last_verified: "2026-04-16"
sources: []
related: []
estimated: true
---

# Q49. Devinに大量データを連携させるには？

📚 [トップ索引](../../README.md) ｜ [カテゴリ索引: データ入出力・ドキュメント理解](README.md)

---

> **メタ**: 最終確認日 2026/4/16 ｜ 根拠 運用観察・公式ガイドベース ｜ 推定あり

### 結論: **(1) GitHub LFS / リポジトリに保存してclone**、**(2) S3/GCS/Azure BlobをSecrets経由で認証してセッション内からアクセス**、**(3) Google Driveは API/MCP経由**、**(4) ローカルPCは基本アップロード**。**ファイルシステムマウントは限定的**

### 大量データの経路別比較

```mermaid
flowchart TD
    Q{データサイズ}
    Q -->|~数MB| Direct[直接アップロード]
    Q -->|~数十MB| GHRepo[repoにcommit]
    Q -->|~数GB| LFS[GitHub LFS]
    Q -->|数十GB以上| Cloud
    subgraph Cloud[外部ストレージ]
        S3[S3/GCS/Azure Blob]
        Drive[Google Drive]
        DB[(DB)]
    end
    S3 -->|Secrets経由認証| Devin
    Drive -->|MCP/API| Devin
    DB -->|接続文字列| Devin
    Direct --> Devin
    GHRepo --> Devin
    LFS --> Devin
    Devin[Devin Session VM]
    style Cloud fill:#F5A623,color:#fff
    style Devin fill:#4A90E2,color:#fff
```

### 大量データの量別対応

| 容量 | 推奨手段 |
|---|---|
| 〜数MB | **チャット添付 / API Attachment** |
| 数十MB〜数百MB | **API Attachment** または **GitHub LFS** |
| 数百MB〜数GB | **S3/GCS/Azure**等オブジェクトストレージ |
| 数GB〜数十GB | **同上**、**ストリーム処理**が必須 |
| 数十GB〜TB級 | **外部ストレージ連携**、セッション内でパーティション処理 |

### 連携手段の詳細

### 1. AWS S3

#### 認証
**Secretsに登録**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`（例: `ap-northeast-1`）

#### アクセス方法

**方法A: AWS CLI**
```bash
aws s3 ls s3://my-bucket/data/
aws s3 cp s3://my-bucket/data/large.parquet /tmp/
```

**方法B: Pythonのboto3**
```python
import boto3
s3 = boto3.client("s3")
s3.download_file("my-bucket", "data/large.parquet", "/tmp/large.parquet")
```

**方法C: pandasで直接読む**
```python
import pandas as pd
df = pd.read_parquet("s3://my-bucket/data/large.parquet")
```

**方法D: s3fsでファイルシステム的に扱う**
```python
import s3fs
fs = s3fs.S3FileSystem()
files = fs.ls("my-bucket/data/")
with fs.open("my-bucket/data/file.csv", "r") as f:
    ...
```

**方法E: goofysなどでFUSEマウント**（高度）
```bash
apt install goofys
goofys my-bucket /mnt/s3
# /mnt/s3 がS3のローカルファイルシステムとして見える
```
→ **可能だが権限・Linux capsで失敗することもある**、推奨は方法B〜D

#### ベストプラクティス
- **IAM Roleは読み取り専用で限定**（`AmazonS3ReadOnlyAccess`等）
- **Bucket Policy** でDevin用アクセスキーにスコープ制限
- **大きなファイルはストリーム処理**（全件メモリ展開しない）

### 2. Google Cloud Storage (GCS)

#### 認証
- **Service Account JSON** をSecretsに登録（`GOOGLE_APPLICATION_CREDENTIALS_JSON`等）
- セッション内でファイルに書き出し→ 環境変数 `GOOGLE_APPLICATION_CREDENTIALS`に設定

```bash
echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" > /tmp/gcp-key.json
export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json
gsutil cp gs://my-bucket/data/large.parquet /tmp/
```

```python
from google.cloud import storage
client = storage.Client()
bucket = client.get_bucket("my-bucket")
blob = bucket.blob("data/large.parquet")
blob.download_to_filename("/tmp/large.parquet")
```

### 3. Azure Blob Storage

#### 認証
- `AZURE_STORAGE_ACCOUNT` / `AZURE_STORAGE_KEY` をSecretsに
- または **Managed Identity**（Enterprise向け）

```python
from azure.storage.blob import BlobServiceClient
client = BlobServiceClient.from_connection_string(conn_str)
blob = client.get_blob_client("container", "data/file.parquet")
with open("/tmp/file.parquet", "wb") as f:
    f.write(blob.download_blob().readall())
```

### 4. Google Drive

#### 方法A: Google Drive API (OAuth)
- **OAuth Client IDとクライアントシークレット**をSecretsに
- 初回認証でrefresh tokenを取得して保存
- 以後`googleapiclient`経由でファイル操作

#### 方法B: Service Account（推奨）
- **Service Account JSON**を作成
- 共有したいフォルダに**Service Accountのメールをeditor権限で追加**
- Devinセッション内でそのSAを使ってファイル取得

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    "/tmp/sa.json", scopes=["https://www.googleapis.com/auth/drive.readonly"]
)
svc = build("drive", "v3", credentials=creds)
files = svc.files().list().execute()
```

#### 方法C: MCP経由
- **Google Drive MCP server** を Devin側で連携
- MCPを通じてDevinが直接Driveのファイル一覧・取得を指示
- 将来的に最も簡単になる見込み

#### 方法D: 既にDriveにあるものをエクスポート
- **Google Docs → .docx / PDFエクスポート → ローカル → アップロード**
- 少量データ向け

### 5. GitHub (LFS / 大きめファイル)

#### Git LFS（100MB超のファイル用）
- `.gitattributes` で対象拡張子を指定
- commit/pushでLFS経由で保管
- Devinはcloneすれば自動的にLFSファイルも取得

```bash
# .gitattributes
*.parquet filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
```

#### GitHub Releases
- 大きなデータはRelease assetとして添付
- Devinセッション内で`wget`でダウンロード

### 6. データベース

#### 直接接続
**Secretsに接続文字列**:
- `DATABASE_URL` = `postgres://user:pass@host:5432/db`
- `REDIS_URL`
- `MONGODB_URI`

```python
import psycopg2
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
```

#### 注意
- 本番DBへの直接接続は**読み取り専用ユーザ**で
- 大量クエリは**バッチサイズ制御**必須
- **ネットワークアクセス制御**（Devin IPはEnterpriseで設定可）

### 7. 外部HTTP/FTP

```bash
# HTTPSで
wget https://data.example.com/large.csv

# FTPで
curl -u user:pass ftp://data.example.com/file.csv -O

# SFTPで（鍵認証）
scp -i /tmp/id_rsa user@server:/path/file.csv /tmp/
```

### 8. Rclone（統合クライアント）

rcloneは**70+のクラウドサービスを統一インタフェース**で扱える:
- S3 / GCS / Azure / Box / Dropbox / Google Drive / OneDrive / SFTP / WebDAV等

```bash
apt install rclone
# 設定（初回、Secretsを経由して環境変数で）
rclone copy remote:bucket/path /tmp/data/
rclone mount remote:bucket /mnt/remote  # FUSEマウント
```

### 9. ローカルPCからの連携

**基本はアップロード**（Devin側からはローカルPCに直接アクセスできない）:

#### 方法A: Webapp添付
- チャット欄のファイル添付
- ドラッグ&ドロップ

#### 方法B: API Attachment
```bash
curl -X POST https://api.devin.ai/v1/attachments \
  -H "Authorization: Bearer $DEVIN_API_KEY" \
  -F "file=@large.csv"
# → URL取得 → セッションに渡す
```

#### 方法C: ローカルサーバを公開（中級者向け・要セキュリティ対策）
- ngrok/cloudflaredでローカルポートを公開
- Devinセッションから `wget http://xyz.ngrok.io/data.csv`
- **⚠ セキュリティ警告（必読）**:
    - **認証なし公開は厳禁**。必ず BASIC 認証 / 短期トークン（`?token=<random>`）/ mTLS 等で保護する
    - **社内ポリシー・情報セキュリティ規程を事前確認**（ngrok/cloudflared の利用が禁止されている組織が多い）
    - **IP・ホスト名漏洩リスク**: ngrok の公開 URL はログや検索エンジンに残り得る。機密データには使わない
    - **使用後は即切断**（`Ctrl+C` で停止 + トンネル削除）。常時公開は絶対に避ける
    - 業務用途では **Cloudflare Tunnel + Access**（Zero Trust 認証付き）や **Tailscale Funnel**（認証統合）を優先

#### 方法D: 一度クラウドにアップ → Devin取得
- S3/Drive/Boxにアップロード → Devinが取得
- 大容量の定番

### 10. MCP経由（今後の主流）

Devin MCPで接続できる例:
- **Google Drive MCP**
- **Slack MCP**
- **GitHub MCP**
- **Postgres MCP**
- **S3 MCP**
- **Notion MCP**

→ **Devin MCPを通じて「取得・検索・書き込み」を自然言語で指示**できる。

### 大量データ処理のコツ

### コツ1: ストリーミング処理
```python
# 全件メモリ展開ではなくチャンク処理
for chunk in pd.read_csv("huge.csv", chunksize=10000):
    process(chunk)
```

### コツ2: パーティション化
- 時系列データは日別/月別に分割して保管
- Devinには「2024-01のデータだけ」のように指示

### コツ3: クエリ寄せ
- データをDevinに全部引き渡すのではなく、**DBサイドで絞ってから**渡す
- ` WHERE created_at > '2024-01-01' LIMIT 10000 `等

### コツ4: 圧縮
- `gzip/xz` で転送量削減
- Parquet/ORC等の列指向形式で大幅圧縮

### コツ5: サンプリング
- まずは**10%サンプル**で設計、本番は最後

### 典型パターン

### パターンA: S3 + pandas
```python
# セッション内
import pandas as pd
import boto3
# S3からdaily dataを全部読み込む
df = pd.concat([
    pd.read_parquet(f"s3://bucket/data/{d}.parquet")
    for d in date_range
])
# 分析
result = df.groupby("region").sum()
# 結果をS3に書き戻す
result.to_parquet("s3://bucket/output/result.parquet")
```

### パターンB: 大きなGitHub repoのクローン
```bash
# Shallow cloneで速く
git clone --depth=1 https://github.com/org/huge-repo.git
# 必要な部分だけ
git clone --filter=blob:none --sparse https://github.com/org/huge-repo.git
```

### パターンC: Webスクレイピング + 蓄積
```python
# Devinがスクレイピング → S3保存 → 次回はS3から読む
```

### セキュリティ・監査

- **すべての外部アクセスはSecretsで認証**（ハードコーディング禁止）
- **Enterprise**では**VPC内で完結**させる設定可
- **監査ログ**でどのセッションが何のデータにアクセスしたか追跡可
- **IAM/RBAC**で最小権限

### まとめ

| データソース | 推奨手段 |
|---|---|
| **AWS S3** | **Secrets + boto3 / aws CLI / s3fs** |
| **GCS** | **Service Account JSON + google-cloud-storage / gsutil** |
| **Azure Blob** | **接続文字列 + azure-storage-blob** |
| **Google Drive** | **Service Account or OAuth or MCP** |
| **GitHub大容量** | **LFS / Releases** |
| **DB** | **接続文字列Secrets + psycopg2/pymysql等** |
| **HTTP/FTP/SFTP** | **wget/curl/scp + 鍵はSecrets** |
| **統合クライアント** | **rclone**（70+サービス対応） |
| **ローカルPC** | **Webapp添付 / API Attachment / 一度クラウド経由** |
| **MCP経由** | **Google Drive/Slack/Notion/DB等**（今後の主流） |

| 量 | 戦略 |
|---|---|
| 〜MB | チャット添付 |
| 〜百MB | Attachment / LFS |
| GB〜TB | **S3/GCS/Azure** + **ストリーム処理** |

**核心**: 大量データは「**外部ストレージに置いて、Secrets経由で認証してDevinから取りに行く**」が基本。ローカルPCからは**アップロード一方通行**、**双方向同期はクラウド経由**。**S3+boto3** が最も汎用的で、**rclone**は統合クライアントとして強力。**MCP**が今後の主流。

---

[← Q48. Devinに入力するデータで気をつけることは？（APIキー・個人情報・機微情報）](q48-input-data-cautions.md) ｜ [Q50. Devinに入力/アップロードしたデータはいつまで保存される？ →](../12-security-governance/q50-data-retention.md)
