import React, { useState, useEffect } from 'react';
import { Layout } from 'antd';
import { config } from '../conf';
import { fetchGet } from '../utils/APIUtils';
import EmailFilter from './EmailFilter';
import CleanEmails from './CleanEmails';
import LeftNav from './LeftNav';

const { Header, Footer, Sider, Content } = Layout;

const layoutStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0px',
    backgroundColor: '#eee',
    xborder: 'solid'
}

const contentStyle = {
    padding: '0 48px',
    backgroundColor: '#fff',
};

export function Main({ sessionManager }) {
    const [step, setStep] = useState('batch')
    const [currentScreen, setCurrentScreen] = useState('1'); // Initial screen

    return (
        <Layout style={layoutStyle}>
            <LeftNav currentScreen={currentScreen} onScreenChange={setStep} />
            <Content style={contentStyle} >
                {step == 'batch' ? <EmailFilter /> : ""}
                {step == 'clean' ? <CleanEmails /> : ""}

                {/* {sessionManager?.user?.user_id ?
                    <div style={{ "width": "200px", "margin": "auto" }}>
                        <a href={config.url.GAUTH_URL} rel="noopener noreferrer">
                            Authorize
                        </a>
                    </div> : ""} */}

            </Content>
        </Layout>
    )
}



