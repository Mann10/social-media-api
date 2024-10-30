![image](https://github.com/user-attachments/assets/c6c04741-0584-40a6-a103-f931b36061be)
### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Mann10/social-media-api.git
   cd SOCIALMEDIAAPI
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the app**

   - The API will be available at `http://127.0.0.1:8000/`
   - Admin dashboard at `http://127.0.0.1:8000/admin`
   - http://127.0.0.1:8000/swagger/

## API Documentation

The API documentation is available via swagger and can be accessed using this link:

http://127.0.0.1:8000/swagger/
