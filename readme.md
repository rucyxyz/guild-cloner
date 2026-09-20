# Discord Server Cloner Web

ブラウザから操作できる **Discord サーバークローンツール** です。
ロール・カテゴリ・テキスト/ボイスチャンネル・メッセージを、別のサーバーへ丸ごと複製できます。
UIはDiscordのダークテーマを再現し、日本語で使いやすく設計しています。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)

---

## 重要：免責事項（必ずお読みください）

> **本ツールは教育・研究目的で公開されています。**

- 本ツールは **User Token（ユーザートークン）** を使用します。
- **User Tokenを用いた自動化はDiscordの利用規約（ToS）で明確に禁止されています。**
- 使用により **アカウントが永久BANされる可能性** があります。
- トークンが漏洩した場合、**アカウントを完全に乗っ取られます。**
- 本ツールの使用は **完全に自己責任** で行ってください。
- 作者は、本ツールの使用によって生じたいかなる損害・アカウント停止・法的問題についても **一切の責任を負いません。**

**これらに同意できない場合は、本リポジトリを使用しないでください。**

---

## 特徴

- **ブラウザUI** — インストール不要、`http://127.0.0.1:8000` を開くだけ
- **Discordダークテーマ** — 公式クライアントに近い配色で違和感なく操作
- **日本語UI** — 全ラベル・ログ・エラーメッセージを日本語化
- **ローカル完結** — トークンはあなたのPC内のみで使用。外部サーバーへ送信されません
- **リアルタイム進捗** — WebSocketで進行状況を逐次表示
- **選択的クローン** — ロール / カテゴリ / テキスト / ボイス / メッセージを個別にON/OFF
- **メッセージ履歴コピー** — 件数を指定して過去ログを転送（要User Token）

---

## 動作環境

| 項目 | 要件 |
|---|---|
| OS | Windows / macOS / Linux |
| Python | 3.9 以上 |
| ブラウザ | Chrome / Edge / Firefox 最新版 |
| ネットワーク | Discord API に接続できること |
| 必要なもの | 有効なDiscord User Token |

---

## インストール

### Windows (PowerShell) の場合

```powershell
git clone https://github.com/rucyxyz/guild-cloner.git
cd guild-cloner
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux の場合

```bash
git clone https://github.com/rucyxyz/guild-cloner.git
cd guild-cloner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 使い方

### 1. サーバーを起動

```bash
python server.py
```

起動に成功すると以下のように表示されます：

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

> このターミナルは起動中は閉じないでください。閉じるとサーバーが停止します。

### 2. ブラウザで開く

```
http://127.0.0.1:8000
```

### 3. 操作フロー

1. **トークン認証** — 自分のUser Tokenを入力して「認証」をクリック
2. **サーバー選択** — 複製元と複製先（空のサーバー推奨）をプルダウンで選択
3. **複製項目を選択** — ロール / カテゴリ / チャンネル / メッセージ にチェック
4. **「複製を開始」** — 進行状況がリアルタイムでログに表示されます
5. **完了後は必ずDiscordのパスワードを変更** — トークンを強制無効化してください

### 4. 停止

サーバーを起動しているターミナルで `Ctrl + C` を押すと停止します。

---

## 次回以降の起動（3ステップ）

### Windows (PowerShell)

```powershell
cd C:\Users\<あなたの名前>\OneDrive\Desktop\guild-cloner
venv\Scripts\activate
python server.py
```

### macOS / Linux

```bash
cd ~/Desktop/guild-cloner
source venv/bin/activate
python server.py
```

→ ブラウザで `http://127.0.0.1:8000` を開く。

---

## ディレクトリ構成

```
guild-cloner/
├── server.py           # FastAPI バックエンド（API + WebSocket）
├── cloner.py           # Discord クローン処理本体
├── requirements.txt    # 依存パッケージ
├── README.md
├── LICENSE
└── static/
    ├── index.html      # UI 本体
    ├── style.css       # Discord ダークテーマ
    └── app.js          # フロントエンドロジック
```

---

## 設定・カスタマイズ

### メッセージ複製の速度を変更

`cloner.py` 内の `await asyncio.sleep(1.2)` の数値で調整できます。
**短くしすぎるとレート制限・BANの原因になります。**

```python
# メッセージ送信間隔（秒）
await asyncio.sleep(1.2)
```

### ポート番号を変更

`server.py` の末尾：

```python
uvicorn.run(app, host="127.0.0.1", port=8000)  # ← ここ
```

### テーマカラーを変更

`static/style.css` の `:root` 変数を編集：

```css
:root {
  --accent: #5865f2;   /* アクセントカラー（Blurple） */
  --success: #23a55a;  /* 成功色 */
}
```

---

## セキュリティについて

本ツールは **ローカルPC上でのみ動作する** ことを前提に設計されています。

| 項目 | 対策 |
|---|---|
| トークンの送信先 | `127.0.0.1` のみ。外部サーバーへは送信されません |
| ログへの記録 | トークンはログに出力されません |
| 保存 | トークンはサーバー側で保存されません（毎回入力） |
| 公開範囲 | **絶対にインターネットへ公開しないでください** |

### やってはいけないこと

- 本ツールを**クラウド（VPS・Render・Herokuなど）にデプロイする**
- 他人のトークンを入力させる
- トークンを `.env` やソースコードにベタ書きする
- 認証後もトークンを有効なまま放置する

### 使用後の必須作業

1. Discordの **パスワードを変更**（トークンが強制無効化されます）
2. ブラウザのタブを閉じる
3. サーバーを `Ctrl + C` で停止

---

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `venv\Scripts\activate` が実行できない | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` を実行 → `Y` |
| `python` コマンドが見つからない | Pythonインストール時に「Add to PATH」にチェックして再インストール |
| `git` コマンドが見つからない | Git for Windows をインストール：https://git-scm.com/download/win |
| `ログイン失敗` | トークンが正しいか、期限切れでないか確認 |
| `サーバーが見つかりません` | そのアカウントが両方のサーバーに参加しているか確認 |
| `複製元と複製先が同じです` | 別のサーバーIDを指定してください |
| チャンネルが一部作成されない | レート制限の可能性。`asyncio.sleep` を長くしてください |
| メッセージが転送されない | User Token の権限・チャンネル閲覧権限を確認 |
| ブラウザに何も表示されない | `http://` でアクセスしているか（`https` ではない）確認 |
| 画面が更新されない | `Ctrl + Shift + R` でスーパーリロード |

---

## ロードマップ

- [x] ロール複製
- [x] カテゴリ複製
- [x] テキストチャンネル複製
- [x] ボイスチャンネル複製
- [x] メッセージ履歴複製
- [x] WebSocket リアルタイム進捗
- [x] 日本語UI / Discordダークテーマ

---

## ライセンス

本プロジェクトは **MIT License** の下で公開されています。
詳細は [LICENSE](./LICENSE) を参照してください。

ただし、**Discordの利用規約に違反する使用については、ライセンス如何に関わらず作者は一切関与しません。**

---

## 謝辞

- [discord.py-self](https://github.com/dolfies/discord.py-self) — User Token 対応ライブラリ
- [FastAPI](https://fastapi.tiangolo.com/) — 高速Webフレームワーク
- [seregonwar/DiscordServerManager](https://github.com/seregonwar/DiscordServerManager) — 元となったアイデア

---

<div align="center">

**Use at your own risk.**

Made for educational purposes.

</div>
```
