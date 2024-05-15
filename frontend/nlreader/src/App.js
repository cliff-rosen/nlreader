import React, { useState, useEffect } from 'react';
import { Routes, Route } from "react-router-dom";
import { useGoogleLogin } from '@react-oauth/google';
import { config } from './conf';
import { fetchGet } from './utils/APIUtils';
import { GoogleLogin } from '@react-oauth/google';
import Auth from './components/Auth';
import { login } from './utils/AuthUtils';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);

  return (

    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/auth_callback" element={<Auth />} />
    </Routes>
  );
}

function Main() {

  const onSuccess = tokenResponse => {
    console.log(tokenResponse)
    login(tokenResponse.credential)
  }

  const glogin = useGoogleLogin({
    onSuccess: tokenResponse => {
      console.log(tokenResponse)

      fetchGet(`login?token=${tokenResponse.credential}`)
        .then(res => console.log('login result', res));
    },
    flow: 'auth-code',
  });

  return <div className="App">
    <h1>Hello</h1>
    <div style={{ "width": "200px", "margin": "auto" }}>
      <GoogleLogin
        onSuccess={onSuccess}
        onError={() => {
          console.log('Login Failed');
        }}
      />
    </div>
    <br />
    <a href={config.url.GAUTH_URL} rel="noopener noreferrer">
      Authorize
    </a>

    {/* <button onClick={() => glogin()}>Sign in with Google 🚀</button> */}

  </div>

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
