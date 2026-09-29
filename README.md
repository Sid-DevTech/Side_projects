
# Python Projects

A collection of Python projects. This overview intentionally leaves out the `GenAi/` folder.

## Access Guard

A command-line employee access management project with employee onboarding, role-based tool permissions, access requests, and access revocation.

Source: [Access_Guard/access_guard.py](Access_Guard/access_guard.py)

Run from the project folder:

```powershell
cd Access_Guard
python access_guard.py
```

Uses the Python standard library; no additional packages are required.

## Bank Management

A command-line banking project for creating accounts, signing in with a PIN, checking balances, and making deposits. Account and transaction records are stored in an Excel workbook named `bank_records.xlsx` in the project folder.

Source: [Bank_Mgmt/Bank_mgmt.py](Bank_Mgmt/Bank_mgmt.py)

Install dependencies and run from the project folder:

```powershell
cd Bank_Mgmt
python -m pip install openpyxl rich pyfiglet pwinput
python Bank_mgmt.py
```

## Library Management

A command-line library system for adding, viewing, and searching books, registering users, and issuing books. Book and user records are kept in `book_data.txt` and `reg_user.txt`.

Source: [Lib_mgmt/lib_mgmt.py](Lib_mgmt/lib_mgmt.py)

Install the dependency and run from the project folder:

```powershell
cd Lib_mgmt
python -m pip install colorama
python lib_mgmt.py
```

## Aero Travel Assistant

A Streamlit travel planner that uses Google Gemini to generate a dated itinerary based on destination, trip length, budget, travel group, and schedule. It also displays locations on a map and provides an estimated cost breakdown.

Source: [travel_assistant_web/main.py](travel_assistant_web/main.py)

Create a `.env` file in `travel_assistant_web` with your Gemini API key:

```text
GEMINI_API_KEY=your_api_key
```

Install the listed dependencies and launch the app from its folder:

```powershell
cd travel_assistant_web
python -m pip install -r requirements.txt
streamlit run main.py
```
=======
This repository contains the projects I have made
>>>>>>> f0d2f741dc3c0c97b8988324ba8bc6eda4428df8
