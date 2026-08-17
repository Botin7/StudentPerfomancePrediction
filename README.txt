To Run System
+ Frontend
 1. npm run dev
+ Backend
 1. Remove folder (venz) 
 2. python -m venv venv (reinstall)
 3. Run venv\Scripts\Activate.ps1    (Terminal)
 4. python -m pip install "uvicorn[standard]" (install unicorn)
 5. py -3.13 -m pip install pandas
 6. py -3.13 -m pip install python-multipart   
 7. Run uvicorn main:app --host 127.0.0.1 --port 8000 --reload (Terminal)
