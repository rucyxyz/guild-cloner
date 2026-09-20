# Discord Server Cloner Web

ブラウザから操作できる **Discord サーバークローンツール** です。
ロール・カテゴリ・テキスト/ボイスチャンネル・メッセージを、別のサーバーへ丸ごと複製できます。
UIはDiscordのダークテーマを再現し、日本語で使いやすく設計しています。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)

---

## 重要：免責事項（必ずお読みください）

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
