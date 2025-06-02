💨 Minesweeper Web App

This is a simple web-based Minesweeper game built using Django (backend) and HTMX (frontend). I created it as a way to practice real-time UI updates, event-driven logic, and progressive enhancement without heavy JavaScript frameworks.

🚀 Features

Classic Minesweeper gameplay with hidden mines and flagging.

Clean UI with HTMX-powered cell updates (no full-page reloads).

Real-time updates using Server-Sent Events (SSE) for multiplayer support.

Flag/unflag cells with right-click or long-press.

Exploding a mine ends the game.

🎯 Why I Made It

To improve my Django skills with a non-CRUD project.

To explore how HTMX and SSE can replace traditional front-end frameworks in certain apps.

To practice event-based architecture and state management in a web app.

Because Minesweeper is fun and a great test case for grid-based logic.

⚙️ How It Works

The game board is stored in server-side memory (board variable).

Clicking a cell triggers a Django view via HTMX.

The server determines the new state (empty, mine, flagged).

The updated cell is re-rendered and returned to the browser.

The server uses Server-Sent Events to push updates to all connected clients when cells are opened or flagged.

🛠️ Technologies Used

🐍 Django – Backend framework for routing and logic

⚡ HTMX – For AJAX and DOM updates without writing JavaScript

🌐 HTML/CSS – Minimal styling for a clean grid UI

📡 Server-Sent Events (SSE) – For pushing cell updates to all clients in real time

🧪 How to Run Locally

# Clone the repo
git clone https://github.com/YOUR_USERNAME/minesweeper-app.git
cd minesweeper-app

# Create and activate a virtualenv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py runserver

Open http://localhost:8000 in your browser and start playing.

📸 Screenshot

Add a screenshot here if you have one

🤛‍♂️ Future Improvements

Add user login and high score tracking

Timer and difficulty settings

Proper game-over and victory screens

Mobile-friendly controls

📄 License

MIT License. See LICENSE for details.