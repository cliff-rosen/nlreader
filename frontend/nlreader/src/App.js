import React, { useState, useEffect } from 'react';
import { Routes, Route } from "react-router-dom";
import { useGoogleLogin } from '@react-oauth/google';
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
  const login = useGoogleLogin({
    onSuccess: tokenResponse => console.log(tokenResponse),
    // flow: 'auth-code',
  });

  return <div className="App">
    <h1>Hello</h1>
    <button onClick={() => login()}>Sign in with Google 🚀</button>;
    <br /><br />
    <a href="https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=604005571-miie2779t7p81l65up26sb6dih1q7uoe.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth_callback&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&state=rDOiNTJzzr7UHOhrjyEndqEqnKxxn4&access_type=offline&include_granted_scopes=true" rel="noopener noreferrer">
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
