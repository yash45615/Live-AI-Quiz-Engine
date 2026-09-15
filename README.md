# Live AI Quiz Engine

A real-time AI-powered classroom quiz platform built with FastAPI, React, SQLite, SQLAlchemy, WebSockets, and OpenAI.

## Features

- Teacher quiz creation
- AI-powered question generation
- Multiple-choice questions
- Live quiz sessions
- Unique session codes
- Student joining
- Real-time WebSocket communication
- Automatic answer scoring
- Speed-based scoring
- Live leaderboard
- Teacher-controlled question navigation
- Final quiz results
- REST API
- Swagger API documentation
- Automated backend testing
- React frontend
- SQLite database

## Architecture

```text
Teacher
   |
   v
Teacher Dashboard
   |
   v
FastAPI Backend
   |
   +--------------------+
   |                    |
   v                    v
AI Question Service   SQLite
   |                    |
   +---------+----------+
             |
             v
       Quiz Session
             |
             v
         WebSocket
        /    |    \
       /     |     \
Student 1 Student 2 Student 3
       \     |     /
        \    |    /
         Leaderboard
