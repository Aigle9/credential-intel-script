
---  

## 2) Publishing via GitHub (recommended)  

Option A: GitHub Repository (long-term, versioned, easy to share)  

1) Create a new repository  
- Go to GitHub → New repository  
- Name: credential-intel-scripts  
- Public  
- Initialize with a README (you can replace later)  

2) Add your scripts  
- Either push via git or use the GitHub UI to upload the five .py files  

3) Add README.md  
- Add the README content from above (or customize)  

4) Get raw file URLs  
- After pushing, the raw URLs look like:  
  - https://raw.githubusercontent.com/your-username/credential-intel-scripts/main/script_top_credential_malware_monitoring.py  
  - https://raw.githubusercontent.com/your-username/credential-intel-scripts/main/script_gir_mapping.py  
  - https://raw.githubusercontent.com/your-username/credential-intel-scripts/main/script_credentials_bruteforce_detector.py  
  - https://raw.githubusercontent.com/your-username/credential-intel-scripts/main/script_phishing_indicator_extractor.py  
  - https://raw.githubusercontent.com/your-username/credential-intel-scripts/main/script_info_breach_notifier.py  

Notes:  
- If you enable GitHub Pages, you can also serve HTML/PT docs and link to the raw scripts from a docs site.  

Option B: GitHub Repository with GitHub Pages (docs site)  

1) In the repo, create a docs/ folder or a docs/ index.html for a simple site.  
2) Enable GitHub Pages in the repository settings (Source: main branch /docs folder).  
3) Link to the script pages from the docs site, e.g. https://your-username.github.io/credential-intel-scripts/script_top_credential_malware_monitoring.py  

---  

## 3) Publishing via GitHub Gists (quick, per-script)  

If you prefer snippety, individual URLs quickly:  

1) Go to GitHub Gists: https://gist.github.com/  
2) Create five public gists, one for each script.  
3) Paste the full script content into each gist.  # credential-intel-script
