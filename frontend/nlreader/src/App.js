import React, { useState, useEffect } from 'react';
import './App.css';
import { useGoogleLogin } from '@react-oauth/google';

function App() {
  const [messages, setMessages] = useState([]);

  const login = useGoogleLogin({
    onSuccess: tokenResponse => console.log(tokenResponse),
    flow: 'auth-code',
  });

  return (
    <div className="App">
      <h1>Hello</h1>
      <button onClick={() => login()}>Sign in with Google 🚀</button>;
    </div>

  );
}

{/* <GoogleOAuthProvider clientId={REACT_APP_GOOGLE_CLIENT_ID}>
  <div>
    <h2>Social Login</h2>
    <GoogleLogin
      onSuccess={handleGoogleSuccess}
      onFailure={handleGoogleFailure}
      cookiePolicy={'single_host_origin'}
      scope="https://www.googleapis.com/auth/gmail.readonly"
      useOneTap
    />
    {error && <p>{error}</p>}
  </div>
</GoogleOAuthProvider> */}


export default App;
