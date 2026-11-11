# 🔰 RP Stealth Security 超簡単導入ガイド（NON-TECH GUIDE）

プログラミングや専門知識がなくても、既存のWebサイト（WordPress・各種Webサイト）を3分で保護できる導入マニュアルです。

---

## 1. 準備するもの
1. **商用ライセンスキー**: [Stripe決済リンク](https://buy.stripe.com/eVq4gz8ND2Nx9Vscr1f3a00) より購入後、メールで届く `RP9-XXXX-XXXX-XXXX-XXXX`
2. **既存サイトのURL / IP**: 現在運用しているWebサイトの接続先

---

## 2. 最短導入ステップ（Docker利用）

サーバー上で以下のコマンドを実行するだけで、RP Stealth Security の迎撃プロキシが起動します。

```bash
docker run -d \
  --name rp-stealth-shield \
  --restart always \
  -p 80:80 -p 443:443 \
  -e BACKEND_URL="http://127.0.0.1:8080" \
  -e LICENSE_KEY="RP9-YOUR-PURCHASED-KEY" \
  -e MODE="active_deception" \
  rpllc/rp-stealth-shield:latest
```

* `BACKEND_URL`: 現在のWebサーバーのポートや内部URLを指定します。
* `LICENSE_KEY`: メールで送達されたライセンスキーを入力します。

これだけで、すべての不正アクセスは自動的に罠（ステルストラップ）に誘い込まれ、正規ユーザーの通信は何の影響も受けずに通過します。

---

## 3. サポート・お問い合わせ
* 技術サポート: `support@rp-sec.com`
* 特定商取引法に基づく表記: [LEGAL.md](./LEGAL.md)
