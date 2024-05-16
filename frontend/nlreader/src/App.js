import React, { useState, useEffect } from 'react';
import { Routes, Route } from "react-router-dom";

import Nav from "./components/Nav";

import { config } from './conf';
import { fetchGet } from './utils/APIUtils';
import { GoogleLogin } from '@react-oauth/google';
import Auth from './components/Auth';
import { useSessionManager } from './utils/AuthUtils';
import './App.css';

import { Layout, Divider } from 'antd';

const { Header, Footer, Sider, Content } = Layout;

const layoutStyle = {
  maxWidth: '1200px',
  margin: '0 auto',
  padding: '0px',
  backgroundColor: '#fff',
}

const contentStyle = {
  padding: '0 48px',
  backgroundColor: '#fff',
};

function App() {
  const sessionManager = useSessionManager();
  const [messages, setMessages] = useState([]);

  console.log('sessionManager', sessionManager)

  return (
    <Layout style={layoutStyle}>
      <Nav sessionManager={sessionManager} />
      <Content style={contentStyle} >
        <Divider />
        <Routes>
          <Route path="/" element={<Main sessionManager={sessionManager} />} />
          <Route path="/auth_callback" element={<Auth />} />
        </Routes>
      </Content>
    </Layout>
  );
}


function Main({ sessionManager }) {

  const getLabels = async () => {
    console.log('click')
    const res = await fetchGet('labels')
    console.log('labels', res)
  }

  return <div className="App">
    <h1>Hello</h1>

    <br />

    {sessionManager?.user?.user_id ?
      <div style={{ "width": "200px", "margin": "auto" }}>
        <a href={config.url.GAUTH_URL} rel="noopener noreferrer">
          Authorize
        </a>
      </div> : ""
    }


    <button onClick={getLabels}>Get Labels</button>

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
