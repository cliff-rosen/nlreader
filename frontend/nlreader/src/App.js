import React, { useState, useEffect } from 'react';
import { Routes, Route } from "react-router-dom";
import { useGoogleLogin } from '@react-oauth/google';
import { config } from './conf';
import { fetchGet } from './utils/APIUtils';
import { GoogleLogin } from '@react-oauth/google';
import Auth from './components/Auth';
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
    fetchGet(`login?token=${tokenResponse.credential}`)
      .then(res => console.log('login result', res));
  }

  const login = useGoogleLogin({
    onSuccess: tokenResponse => {
      console.log(tokenResponse)
      fetchGet(`login?token=${tokenResponse.credential}`)
        .then(res => console.log('login result', res));
    },
    flow: 'auth-code',
  });

  return <div className="App">
    <h1>Hello</h1>
    <button onClick={() => login()}>Sign in with Google 🚀</button>
    <br /><br />

    <GoogleLogin
      onSuccess={onSuccess}
      onError={() => {
        console.log('Login Failed');
      }}
      useOneTap
    />;

    <br /><br />

    <a href={config.url.GAUTH_URL} rel="noopener noreferrer">
      Authorize
    </a>
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
