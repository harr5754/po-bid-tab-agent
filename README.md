# Aegentik Bid Tab Agent

Turn RFQ packages + bidder proposals into a structured Bid Tab (online + downloadable Excel) in minutes.

**Demo:** Pre-loaded with real M001 data (Absolute Energy + BWFS Industries).  
No API key required for the demo.

---

## Quick Deploy to Streamlit Cloud (with your domain)

### 1. Create GitHub Repository
1. Go to [github.com](https://github.com) → New repository
2. Name it e.g. `bid-tab-agent` (or whatever you prefer)
3. Keep it **Private** or Public (your choice)
4. Do **not** initialize with README (we already have one)
5. Click **Create repository**

### 2. Upload this folder
**Option A – Drag & drop (easiest)**
- On the new empty repo page, click **uploading an existing file**
- Drag the entire contents of this `bid_tab_agent` folder
- Commit the files

**Option B – Git command line**
```bash
git init
git add .
git commit -m "Initial Aegentik Bid Tab Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bid-tab-agent.git
git push -u origin main
```

### 3. Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with the same GitHub account
2. Click **New app**
3. Select your repository and branch (`main`)
4. Set **Main file path** to: `app/main.py`
5. Click **Deploy**

You will get a URL like:  
`https://YOUR_APP_NAME.streamlit.app`

### 4. Point your domain (aegentik.ai)
Streamlit Cloud free tier uses the `.streamlit.app` subdomain.  
For a custom domain / subdomain (e.g. `bidtab.aegentik.ai` or `demo.aegentik.ai`):

- Streamlit Cloud **paid** plans support custom domains directly in the app settings.
- Free tier alternative: Use Cloudflare (or similar) as a reverse proxy / CNAME to the Streamlit URL.

Once deployed, give your daughter only the final link. She never needs to touch GitHub or Streamlit settings.

---

## Local Testing (optional)

```bash
cd bid_tab_agent
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

---

## Features in this version

- Welcome / landing screen branded for Aegentik
- Demo mode with real M001 data (Absolute + BWFS)
- Commercial Summary + Pricing + Terms side-by-side
- Technical compliance comparison
- Manual Review & Correct screen
- Download Excel in Classic or Modern format
- Claude API key field ready (company key – zero extra cost)
- Max 5 bidders support structure

---

## Next development (after she tries the demo)

- Full Claude extraction pipeline for new RFQ uploads
- Closer match of Classic Excel to your existing Bid Tab layout
- Risk flags / recommendation scoring
- GLEX and additional bidders

---

**Powered by Aegentik** · For Crosstrails Engineering demo
