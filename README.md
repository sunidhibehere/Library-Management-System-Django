# Library-Management-System-Django
A Simple Library Management System that helps in managing a library.

### Available Functionalities:
1. Members Management (Allows CRUD operations for Library Management)
2. Books Management (Allows CRUD operations for Books)
3. Lending of Books to Members.
4. Returning of Books by Members.
5. Payments for fines and Borrowing Books By Members.

### To run the project locally, follow the following instructions:
- Clone the repository
  ```sql
  git clone https://github.com/hellen-22/Library-Management-System-Django.git
  ```
- Navigate to the project directory.
  ```sql
  cd Library-Management-System-Django
  ```
- Create virtual environment and activate it:
  ```sql
  python3 -m venv venv or python -m venv venv
  ```
  Activate: On Windows
  ```sql
  venv\Scripts\activate
  ```
  On Mac
  ```sql
  source venv\bin\activate
  ```
- Install libraries from the requirements.txt file.
  ```sql
  pip install -r requirement.txt
  ```
- Edit the *.env.sample* file to add your environment variables.
- Set up the database:
  ```sql
  python manage.py migrate
  ```
- Run the server:
  ```sql
  python manage.py runserver
  ```

### Screenshots
Login and Register Pages.
<img width="1440" alt="Screenshot" src="">

<img width="1439" alt="Screenshot" src="">

Dashboard.
<img width="1426" alt="Screenshot" src="">

Members Pages.
<img width="1440" alt="Screenshot" src="">

<img width="1424" alt="Screenshot" src="">

Books Pages.
<img width="1424" alt="Screenshot" src="">

<img width="1423" alt="Screenshot" src="">

Other Pages.
<img width="1439" alt="Screenshot" src="">

<img width="1423" alt="Screenshot" src="">

<img width="1425" alt="Screenshot" src="">