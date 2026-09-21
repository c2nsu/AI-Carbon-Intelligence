@echo off
cd /d "C:\Users\scans\OneDrive\Masaüstü\grup projesi"
python -m streamlit run app.py --server.headless true --server.port 8501
pause
