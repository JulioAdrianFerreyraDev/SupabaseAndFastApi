# Application Setup

1. Install the python requirements using:
```pip install -r requirements.txt```
2. Copy the `.env-template` file and rename it to `.env`
3. Change the dummy data for your real data.
4. Be sure the database and the storage are available.
5. Run the server for testing using:
```uvicorn app:app```
6. Open the link.


>
> Requirements:
>
> Python 3.12

# Deploy
Run the server using 
```uvicorn app:app --host 0.0.0.0 --port 8000```
