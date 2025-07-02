1. Clone the project


git clone https://github.com/yourusername/fastapi-product-service.git
cd fastapi-product-service

2. Create virtual environment
   
python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. PostgreSQL & Redis Setup (Local)
Install and run:

PostgreSQL → create DB: productdb, user: postgres, password: root

Redis → run with redis-server

5. Docker Setup

docker-compose up

6. Open Swagger UI: http://localhost:8000/docs

Authentication (Basic Auth)
Admin: admin / admin123


User: user / user123

7. Running Tests
Make sure Redis and DB are running locally:

# from project root
$env:PYTHONPATH="."; pytest         
