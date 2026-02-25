# 🚀 Distributed Task Processing & Job Queue System  
### With Retry Mechanism & Fault Tolerance

A production-style distributed job queue system built using **FastAPI** and **Redis**, implementing priority-based scheduling, concurrent worker execution, retry logic, and dead-letter handling for robust background task processing.

---

## 📌 Overview

This system allows asynchronous job submission through REST APIs.  
Jobs are stored in Redis and processed by background worker threads with fault-tolerant retry mechanisms.

Designed to simulate real-world distributed task processing systems used in scalable backend architectures.

---

## 🏗 Architecture

Client → FastAPI API → Redis Priority Queue → Worker Threads → Retry / Dead Letter Queue

---

## ⚙️ Features

- ✅ Asynchronous job submission via REST API
- ✅ Priority-based job scheduling using Redis Sorted Sets
- ✅ Concurrent worker processing
- ✅ Automatic retry mechanism for failed jobs
- ✅ Dead-letter queue for permanently failed tasks
- ✅ Real-time job status tracking
- ✅ Background worker lifecycle management (FastAPI lifespan)
- ✅ Fault-tolerant design

---

## 🧠 How It Works

1. Client submits job via `/submit`
2. Job is stored in Redis queue
3. Background worker thread continuously polls queue
4. Job is processed
5. If failure occurs:
   - Retries decrease
   - Job re-queued
6. If retries exhausted:
   - Job moved to Dead Letter Queue
7. Status updated in Redis

---

## 🛠 Tech Stack

- FastAPI
- Redis
- Docker
- Python
- Threading
- Pydantic

---

## 📂 Project Structure


distributed-job-queue/
│
├── app/
│ ├── main.py
│ ├── producer.py
│ ├── worker.py
│ ├── queue_manager.py
│ ├── redis_client.py
│ └── models.py
│
├── requirements.txt
└── README.md


---
1️⃣ Architecture Diagram 

Client
↓
FastAPI
↓
Redis Queue
↓
Worker Thread
↓
Retry / Dead Letter Queue



2️⃣ Swagger Screenshot

<img width="1915" height="842" alt="image" src="https://github.com/user-attachments/assets/698326e5-33ee-4e03-b8a9-80505e5c556f" />

<img width="1917" height="952" alt="image" src="https://github.com/user-attachments/assets/e277ef48-a494-4ac7-b454-b8b31ae83d11" />



## 🚀 How to Run

### 1️⃣ Start Redis (Docker)

```bash
docker run -d -p 6379:6379 redis
2️⃣ Activate Virtual Environment
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run FastAPI
uvicorn app.main:app --reload
🌐 API Endpoints
Submit Job
POST /submit

Request Body:

{
  "payload": {
    "task": "Example job"
  }
}
Check Job Status
GET /status/{task_id}

Possible Status Values:

queued

processing

retrying

completed

failed

🔥 Production Concepts Implemented

Distributed queue system

Priority scheduling

Background worker lifecycle management

Fault tolerance

Retry logic

Dead letter queue pattern

Redis-based job persistence

📈 Future Improvements

Multi-worker scaling

Rate limiting

Monitoring dashboard

Metrics & logging

Kubernetes deployment

👩‍💻 Author

Radhika Kakad
