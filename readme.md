# 🎮 Discord Server Cloner Web

ブラウザから操作できる **Discord サーバークローンツール** です。
ロール・カテゴリ・テキスト/ボイスチャンネル・メッセージを、別のサーバーへ丸ごと複製できます。
UIはDiscordのダークテーマを再現し、日本語で使いやすく設計しています。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)

---

## ⚠️ 重要：免責事項（必ずお読みください）

> **本ツールは教育・研究目的で公開されています。**

- 本ツールは **User Token（ユーザートークン）** を使用します。
- **User Tokenを用いた自動化はDiscordの利用規約（ToS）で明確に禁止されています。**
- 使用により **アカウントが永久BANされる可能性** があります。
- トークンが漏洩した場合、**アカウントを完全に乗っ取られます。**
- 本ツールの使用は **完全に自己責任** で行ってください。
- 作者は、本ツールの使用によって生じたいかなる損害・アカウント停止・法的問題についても **一切の責任を負いません。**

**これらに同意できない場合は、本リポジトリを使用しないでください。**

---

## ✨ 特徴

- 🌐 **ブラウザUI** — インストール不要、`http://127.0.0.1:8000` を開くだけ
- 🎨 **Discordダークテーマ** — 公式クライアントに近い配色で違和感なく操作
- 🇯🇵 **日本語UI** — 全ラベル・ログ・エラーメッセージを日本語化
- 🔒 **ローカル完結** — トークンはあなたのPC内のみで使用。外部サーバーへ送信されません
- 📊 **リアルタイム進捗** — WebSocketで進行状況を逐次表示
- 🎭 **選択的クローン** — ロール / カテゴリ / テキスト / ボイス / メッセージを個別にON/OFF
- 📨 **メッセージ履歴コピー** — 件数を指定して過去ログを転送（要User Token）


---

## 🖥 動作環境

| 項目 | 要件 |
|---|---|
| OS | Windows / macOS / Linux |
| Python | 3.9 以上 |
| ブラウザ | Chrome / Edge / Firefox 最新版 |
| ネットワーク | Discord API に接続できること |
| 必要なもの | 有効なDiscord User Token |

---

## 🚀 インストール

### 1. リポジトリをクローン

```bash
git clone https://github.com/rucyxyz/guild-cloner.git
cd guild-cloner-web
```

### 2. 仮想環境を作成

```
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. 依存関係をインストール

```
pip install -r requirements.txt
```
