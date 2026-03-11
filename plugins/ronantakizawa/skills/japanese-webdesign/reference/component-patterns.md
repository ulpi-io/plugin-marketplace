# Japanese Web Design Component Patterns

## Detailed UI Component Examples

### 1. Product Card (商品カード)

```html
<div class="jp-product-card">
  <!-- Ranking badges -->
  <div class="card-badges">
    <span class="badge badge-rank">
      <i class="icon-crown"></i> ランキング1位
    </span>
    <span class="badge badge-new">NEW</span>
    <span class="badge badge-sale">SALE</span>
  </div>

  <!-- Product image with hover gallery -->
  <div class="card-image">
    <img src="product-main.jpg" alt="商品名">
    <div class="image-count">1/12</div>
  </div>

  <!-- Product info section -->
  <div class="card-content">
    <!-- Brand and category -->
    <div class="card-meta">
      <span class="brand">ブランド名</span>
      <span class="category">カテゴリ</span>
    </div>

    <!-- Product name (can be long) -->
    <h3 class="card-title">
      【送料無料】商品名 詳細説明 特徴キーワード
    </h3>

    <!-- Rating with count -->
    <div class="card-rating">
      <span class="stars">★★★★☆</span>
      <span class="rating-value">4.2</span>
      <span class="review-count">(1,234件)</span>
    </div>

    <!-- Price section -->
    <div class="card-price">
      <div class="price-original">
        <span class="label">定価:</span>
        <s>¥15,800</s>
      </div>
      <div class="price-current">
        <span class="amount">¥9,980</span>
        <span class="tax">(税込)</span>
      </div>
      <div class="price-discount">
        <span class="percent">37%OFF</span>
        <span class="saved">5,820円お得</span>
      </div>
    </div>

    <!-- Points -->
    <div class="card-points">
      <i class="icon-point"></i>
      <span>99ポイント進呈</span>
    </div>

    <!-- Shipping info -->
    <div class="card-shipping">
      <span class="free-shipping">✓ 送料無料</span>
      <span class="delivery">明日届く</span>
    </div>

    <!-- Stock status -->
    <div class="card-stock">
      <span class="in-stock">在庫あり</span>
      <span class="remaining">残り3点</span>
    </div>
  </div>

  <!-- Action buttons -->
  <div class="card-actions">
    <button class="btn-cart">カートに入れる</button>
    <button class="btn-favorite">♡ お気に入り</button>
  </div>
</div>
```

```css
.jp-product-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  position: relative;
  transition: box-shadow 0.2s;
}

.jp-product-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card-badges {
  position: absolute;
  top: 8px;
  left: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  z-index: 1;
}

.badge {
  padding: 2px 8px;
  font-size: 11px;
  font-weight: bold;
  border-radius: 2px;
}

.badge-rank {
  background: #ffd700;
  color: #333;
}

.badge-new {
  background: #e60012;
  color: #fff;
}

.badge-sale {
  background: #ff6b35;
  color: #fff;
}

.card-price .price-current .amount {
  font-size: 24px;
  font-weight: bold;
  color: #e60012;
}

.card-shipping .free-shipping {
  color: #00a040;
  font-weight: bold;
}

.card-stock .remaining {
  color: #e60012;
  font-weight: bold;
}
```

### 2. Banner Carousel (バナー)

Japanese banners are information-dense with multiple text elements:

```html
<div class="jp-banner">
  <div class="banner-bg" style="background-image: url('banner-bg.jpg')">
    <!-- Multiple text layers -->
    <div class="banner-eyecatch">期間限定</div>
    <div class="banner-main-copy">
      <span class="highlight">最大50%OFF</span>
      <span class="sub">冬の大セール</span>
    </div>
    <div class="banner-period">
      2024年1月15日(月)〜1月31日(水)
    </div>
    <div class="banner-details">
      <ul>
        <li>✓ 全品送料無料</li>
        <li>✓ ポイント5倍</li>
        <li>✓ クーポン併用可</li>
      </ul>
    </div>
    <div class="banner-cta">
      <a href="#" class="btn-banner">セール会場へ →</a>
    </div>
    <div class="banner-disclaimer">
      ※一部対象外商品あり
    </div>
  </div>
</div>
```

```css
.jp-banner {
  position: relative;
  overflow: hidden;
}

.banner-eyecatch {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #e60012;
  color: #fff;
  padding: 4px 12px;
  font-weight: bold;
  transform: rotate(-5deg);
}

.banner-main-copy {
  text-align: center;
  padding: 20px;
}

.banner-main-copy .highlight {
  display: block;
  font-size: 48px;
  font-weight: bold;
  color: #e60012;
  text-shadow: 2px 2px 0 #fff, -2px -2px 0 #fff;
}

.banner-period {
  background: rgba(0,0,0,0.7);
  color: #fff;
  text-align: center;
  padding: 8px;
}

.banner-disclaimer {
  font-size: 10px;
  color: #666;
  position: absolute;
  bottom: 4px;
  right: 8px;
}
```

### 3. Information Table (情報テーブル)

```html
<table class="jp-info-table">
  <caption>商品詳細情報</caption>
  <tbody>
    <tr>
      <th>商品名</th>
      <td>高機能ステンレス調理器具セット</td>
    </tr>
    <tr>
      <th>型番</th>
      <td>KT-2024-SS</td>
    </tr>
    <tr>
      <th>サイズ</th>
      <td>
        フライパン: 直径26cm × 深さ5cm<br>
        鍋: 直径20cm × 深さ12cm<br>
        蓋: 直径26cm / 20cm 兼用
      </td>
    </tr>
    <tr>
      <th>重量</th>
      <td>
        フライパン: 約850g<br>
        鍋: 約1,200g<br>
        蓋: 約350g<br>
        <strong>総重量: 約2,400g</strong>
      </td>
    </tr>
    <tr>
      <th>素材</th>
      <td>
        本体: 18-8ステンレス（SUS304）<br>
        底面: アルミニウム三層構造<br>
        持ち手: フェノール樹脂（耐熱温度150℃）
      </td>
    </tr>
    <tr>
      <th>対応熱源</th>
      <td>
        <span class="check">✓</span> ガス火<br>
        <span class="check">✓</span> IH (100V/200V)<br>
        <span class="check">✓</span> ハロゲンヒーター<br>
        <span class="check">✓</span> シーズヒーター<br>
        <span class="cross">✗</span> 電子レンジ不可
      </td>
    </tr>
    <tr>
      <th>生産国</th>
      <td>日本（新潟県燕三条製）</td>
    </tr>
    <tr>
      <th>保証</th>
      <td>メーカー保証2年間（通常使用に限る）</td>
    </tr>
    <tr>
      <th>JANコード</th>
      <td>4901234567890</td>
    </tr>
    <tr>
      <th>取扱説明書</th>
      <td><a href="#">PDFダウンロード (1.2MB)</a></td>
    </tr>
  </tbody>
</table>
```

```css
.jp-info-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.jp-info-table caption {
  background: #333;
  color: #fff;
  padding: 10px;
  text-align: left;
  font-weight: bold;
}

.jp-info-table th,
.jp-info-table td {
  border: 1px solid #ddd;
  padding: 12px;
  vertical-align: top;
}

.jp-info-table th {
  background: #f5f5f5;
  width: 120px;
  font-weight: bold;
  text-align: left;
}

.jp-info-table .check {
  color: #00a040;
}

.jp-info-table .cross {
  color: #e60012;
}
```

### 4. Section Headers (セクションヘッダー)

```html
<!-- Style 1: Boxed header -->
<div class="section-header-boxed">
  <h2>おすすめ商品</h2>
  <a href="#" class="see-all">すべて見る →</a>
</div>

<!-- Style 2: Decorated header -->
<div class="section-header-decorated">
  <span class="deco">★</span>
  <h2>今週の人気ランキング</h2>
  <span class="deco">★</span>
</div>

<!-- Style 3: Tab-style header -->
<div class="section-header-tabs">
  <button class="tab active">新着順</button>
  <button class="tab">人気順</button>
  <button class="tab">価格順</button>
  <button class="tab">レビュー順</button>
</div>

<!-- Style 4: Banner-style header -->
<div class="section-header-banner">
  <div class="banner-content">
    <span class="icon">🎉</span>
    <h2>タイムセール開催中！</h2>
    <span class="countdown">残り 02:34:56</span>
  </div>
</div>
```

```css
.section-header-boxed {
  background: linear-gradient(90deg, #e60012, #ff6b35);
  color: #fff;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header-boxed h2 {
  margin: 0;
  font-size: 18px;
}

.section-header-decorated {
  text-align: center;
  padding: 20px;
  border-top: 2px solid #333;
  border-bottom: 2px solid #333;
  margin: 20px 0;
}

.section-header-decorated h2 {
  display: inline;
  font-size: 20px;
}

.section-header-decorated .deco {
  color: #ffd700;
  font-size: 24px;
  margin: 0 10px;
}

.section-header-tabs {
  display: flex;
  border-bottom: 2px solid #333;
}

.section-header-tabs .tab {
  padding: 10px 20px;
  background: #f5f5f5;
  border: none;
  cursor: pointer;
}

.section-header-tabs .tab.active {
  background: #333;
  color: #fff;
}
```

### 5. Notice/Alert Boxes (お知らせ)

```html
<!-- Important notice -->
<div class="notice notice-important">
  <div class="notice-icon">⚠️</div>
  <div class="notice-content">
    <h4>【重要】システムメンテナンスのお知らせ</h4>
    <p>
      2024年1月20日(土) 2:00〜6:00の間、システムメンテナンスを実施いたします。
      この間、サービスをご利用いただけません。
    </p>
    <p class="notice-date">2024年1月15日 掲載</p>
  </div>
</div>

<!-- Shipping notice -->
<div class="notice notice-shipping">
  <h4>📦 配送に関するお知らせ</h4>
  <ul>
    <li>年末年始期間（12/29〜1/3）は配送休業となります</li>
    <li>12/27までのご注文は年内発送可能です</li>
    <li>1/4以降順次発送いたします</li>
  </ul>
</div>

<!-- Campaign notice -->
<div class="notice notice-campaign">
  <div class="notice-badge">開催中</div>
  <h4>🎁 新春ポイントアップキャンペーン</h4>
  <p>期間中のお買い物でポイント最大10倍！</p>
  <p class="notice-period">2024年1月1日(月)〜1月15日(月)</p>
  <a href="#" class="notice-link">詳細を見る →</a>
</div>
```

```css
.notice {
  border-radius: 4px;
  padding: 16px;
  margin: 16px 0;
}

.notice-important {
  background: #fff3cd;
  border: 2px solid #ffc107;
  display: flex;
  gap: 12px;
}

.notice-important .notice-icon {
  font-size: 24px;
}

.notice-shipping {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.notice-campaign {
  background: #fce4ec;
  border: 2px solid #e91e63;
  position: relative;
}

.notice-campaign .notice-badge {
  position: absolute;
  top: -10px;
  right: 10px;
  background: #e91e63;
  color: #fff;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: bold;
}

.notice h4 {
  margin: 0 0 8px 0;
}

.notice-date {
  font-size: 12px;
  color: #666;
}

.notice-period {
  font-weight: bold;
  color: #e91e63;
}
```

### 6. Footer (フッター)

Japanese footers are comprehensive with detailed links and company information:

```html
<footer class="jp-footer">
  <!-- Service links -->
  <div class="footer-services">
    <div class="footer-column">
      <h4>お買い物ガイド</h4>
      <ul>
        <li><a href="#">ご注文方法</a></li>
        <li><a href="#">お支払い方法</a></li>
        <li><a href="#">配送・送料について</a></li>
        <li><a href="#">返品・交換について</a></li>
        <li><a href="#">ギフトラッピング</a></li>
        <li><a href="#">領収書・納品書について</a></li>
      </ul>
    </div>
    <div class="footer-column">
      <h4>会員サービス</h4>
      <ul>
        <li><a href="#">新規会員登録</a></li>
        <li><a href="#">マイページ</a></li>
        <li><a href="#">ポイントについて</a></li>
        <li><a href="#">メールマガジン</a></li>
        <li><a href="#">お気に入り</a></li>
        <li><a href="#">購入履歴</a></li>
      </ul>
    </div>
    <div class="footer-column">
      <h4>お問い合わせ</h4>
      <ul>
        <li><a href="#">よくある質問(FAQ)</a></li>
        <li><a href="#">お問い合わせフォーム</a></li>
        <li><a href="#">チャットサポート</a></li>
      </ul>
      <div class="footer-phone">
        <p>お電話でのお問い合わせ</p>
        <p class="phone-number">0120-123-456</p>
        <p class="phone-hours">
          受付時間: 平日9:00〜18:00<br>
          （土日祝日・年末年始を除く）
        </p>
      </div>
    </div>
    <div class="footer-column">
      <h4>会社情報</h4>
      <ul>
        <li><a href="#">会社概要</a></li>
        <li><a href="#">採用情報</a></li>
        <li><a href="#">プレスリリース</a></li>
        <li><a href="#">IR情報</a></li>
      </ul>
    </div>
  </div>

  <!-- Trust badges and certifications -->
  <div class="footer-trust">
    <img src="privacy-mark.png" alt="プライバシーマーク">
    <img src="ssl-badge.png" alt="SSL/TLS暗号化通信">
    <img src="jdma-badge.png" alt="JDMA会員">
  </div>

  <!-- Company details -->
  <div class="footer-company">
    <p>
      <strong>株式会社○○○○</strong><br>
      〒100-0001 東京都千代田区○○1-2-3 ○○ビル5F<br>
      TEL: 03-1234-5678 / FAX: 03-1234-5679<br>
      代表取締役社長: 山田太郎<br>
      設立: 2000年4月1日 / 資本金: 1億円
    </p>
  </div>

  <!-- Legal links -->
  <div class="footer-legal">
    <a href="#">利用規約</a>
    <a href="#">プライバシーポリシー</a>
    <a href="#">特定商取引法に基づく表記</a>
    <a href="#">サイトマップ</a>
  </div>

  <!-- Copyright -->
  <div class="footer-copyright">
    <p>Copyright © 2024 Company Name Inc. All Rights Reserved.</p>
  </div>
</footer>
```

### 7. Breadcrumbs (パンくずリスト)

```html
<nav class="jp-breadcrumbs">
  <ol>
    <li><a href="/">ホーム</a></li>
    <li><a href="/category">カテゴリ一覧</a></li>
    <li><a href="/category/kitchen">キッチン用品</a></li>
    <li><a href="/category/kitchen/pans">フライパン・鍋</a></li>
    <li><span>商品名</span></li>
  </ol>
</nav>
```

```css
.jp-breadcrumbs {
  background: #f5f5f5;
  padding: 8px 16px;
  font-size: 12px;
}

.jp-breadcrumbs ol {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  margin: 0;
  padding: 0;
}

.jp-breadcrumbs li:not(:last-child)::after {
  content: ">";
  margin: 0 8px;
  color: #999;
}

.jp-breadcrumbs a {
  color: #0066cc;
  text-decoration: none;
}

.jp-breadcrumbs a:hover {
  text-decoration: underline;
}
```

## Responsive Patterns

### Mobile Product Grid

```css
/* Japanese mobile: Maintain 2 columns */
@media (max-width: 768px) {
  .product-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    padding: 8px;
  }

  .jp-product-card {
    font-size: 11px;
  }

  .jp-product-card .card-title {
    font-size: 12px;
    line-height: 1.4;
    /* Allow 3 lines */
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .jp-product-card .price-current .amount {
    font-size: 16px;
  }

  /* Keep badges but smaller */
  .card-badges .badge {
    font-size: 9px;
    padding: 1px 4px;
  }
}
```

### Mobile Navigation

```html
<!-- Sticky tab navigation (not hamburger) -->
<nav class="mobile-tab-nav">
  <a href="/" class="tab-item active">
    <span class="tab-icon">🏠</span>
    <span class="tab-label">ホーム</span>
  </a>
  <a href="/search" class="tab-item">
    <span class="tab-icon">🔍</span>
    <span class="tab-label">検索</span>
  </a>
  <a href="/categories" class="tab-item">
    <span class="tab-icon">📋</span>
    <span class="tab-label">カテゴリ</span>
  </a>
  <a href="/cart" class="tab-item">
    <span class="tab-icon">🛒</span>
    <span class="tab-label">カート</span>
    <span class="badge">3</span>
  </a>
  <a href="/mypage" class="tab-item">
    <span class="tab-icon">👤</span>
    <span class="tab-label">マイページ</span>
  </a>
</nav>
```

```css
.mobile-tab-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  display: flex;
  justify-content: space-around;
  border-top: 1px solid #ddd;
  padding: 8px 0;
  z-index: 1000;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #666;
  font-size: 10px;
  position: relative;
}

.tab-item.active {
  color: #e60012;
}

.tab-item .tab-icon {
  font-size: 20px;
}

.tab-item .badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #e60012;
  color: #fff;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
}
```
