import React, { useState, useEffect } from 'react';
import { Layout } from 'antd';
import { config } from '../conf';
import { fetchGet } from '../utils/APIUtils';
import EmailFilter from './EmailFilter';
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
    const [labels, setLabels] = useState([]);
    const [currentScreen, setCurrentScreen] = useState('1'); // Initial screen

    const handleScreenChange = (newScreenKey) => {
        setCurrentScreen(newScreenKey);
        // Optionally, perform additional actions based on the new screen
    };


    useEffect(() => {
        const getLabels = async () => {
            console.log('click');
            const res = await fetchGet('labels');
            const l = res.map(e => ({ key: e['id'], 'name': e['name'] }));
            console.log('labels', l);
            setLabels(l);
        };
        getLabels()
    }, [])


    const columns = [
        {
            title: 'Label',
            dataIndex: 'name',
            key: 'name',
            render: (text) => <a>{text}</a>,
        }
    ];

    return (
        <Layout style={layoutStyle}>
            <LeftNav currentScreen={currentScreen} onScreenChange={setStep} />
            <Content style={contentStyle} >
                STEP: {step}
                {/* {sessionManager?.user?.user_id ?
                    <div style={{ "width": "200px", "margin": "auto" }}>
                        <a href={config.url.GAUTH_URL} rel="noopener noreferrer">
                            Authorize
                        </a>
                    </div> : ""}
 */}

                {/* <button onClick={getLabels}>Get Labels</button> */}
                {step == 'batch' ? <EmailFilter labelOptions={labels} /> : ""}

            </Content>
        </Layout>
    )
}



