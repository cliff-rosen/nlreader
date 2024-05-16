import React, { useState, useEffect } from 'react';
import { Routes, Route } from "react-router-dom";

import Nav from "./components/Nav";

import { config } from './conf';
import { fetchGet } from './utils/APIUtils';
import { GoogleLogin } from '@react-oauth/google';
import Auth from './components/Auth';
import { useSessionManager } from './utils/AuthUtils';
import './App.css';

import { Table, Layout, Divider } from 'antd';
import EmailFilter from './components/EmailFilter';

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
  const [labels, setLabels] = useState([]);

  const getLabels = async () => {
    console.log('click')
    const res = await fetchGet('labels')
    const l = res.map(e => ({ key: e['id'], 'name': e['name'] }))
    console.log('labels', l)
    setLabels(l)

  }

  const columns = [
    {
      title: 'Label',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <a>{text}</a>,
    }
  ];

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
    <EmailFilter labelOptions={labels} />
  </div>

}

export default App;
