<h1>ASDW RSS Feed Parser</h1>
<a href="https://asdw.nbed.ca/alerts/feed/"><img src="https://rss.com/blog/wp-content/uploads/2019/10/social_style_3_rss-512-1.png" height="25px"></a>
<a href="https://github.com/justrals/asdw-rss-feed-parser"><img src="https://img.shields.io/github/stars/justrals/asdw-rss-feed-parser" height="25px"></a>

<h2>What's that?</h2>
<p>It's a script for parsing alerts from the Anglophone School West District RSS feed and sending them in a formatted form via the Telegram Bot API.</p>
<h2>Installation</h2>
<p>You should have Python 3.7 or higher installed before proceeding.</p>

<p>1. Clone the repository</p>

```bash
git clone https://github.com/justrals/asdw-rss-feed-parser.git
cd asdw-rss-feed-parser
```
<p>2. Install dependencies</p>

```bash
pip install -r requirements.txt
```
<p>3. Create .env file with the following content</p>

```bash
TELEGRAM_TOKEN=(your API token from @BotFather)
CHANNEL_ID=(your channel ID, e.g. -1001234567890)
```
<p>4. Run the script</p>

```bash
python main.py
```
