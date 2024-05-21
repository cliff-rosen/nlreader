import React, { useEffect } from 'react';
import { Routes, Route } from "react-router-dom";

import Nav from "./components/Nav";

import { GoogleLogin } from '@react-oauth/google';
import Auth from './components/Auth';
import { useSessionManager } from './utils/AuthUtils';
import './App.css';

import { Table, Layout, Divider } from 'antd';
import { Main } from './components/Main';

const { Header, Footer, Sider, Content } = Layout;

const layoutStyle = {
  xmaxWidth: '1200px',
  margin: '0 auto',
  padding: '0px',
  backgroundColor: '#fff',
}

const contentStyle = {
  padding: '0 48px',
  backgroundColor: '#eee',
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


export default App;
