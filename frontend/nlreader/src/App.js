import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetch('/api/messages')
      .then(response => response.json())
      .then(data => setMessages(data))
      .catch(error => console.error('Error fetching messages:', error));
  }, []);

  const handleLogin = () => {
    window.location.href = '/login';
  };

  const handleLogout = () => {
    fetch('/logout', { method: 'POST' })
      .then(() => window.location.reload())
      .catch(error => console.error('Error logging out:', error));
  };

  return (
    <div className="App">
      <h1>Recent Gmail Messages</h1>
      {messages.length > 0 ? (
        <ul>
          {messages.map((message, index) => (
            <li key={index}>{message.snippet}</li>
          ))}
        </ul>
      ) : (
        <p>No messages found. Please <button onClick={handleLogin}>log in</button> to view your messages.</p>
      )}
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
}

export default App;
