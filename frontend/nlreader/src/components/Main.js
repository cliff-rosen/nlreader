import React, { useState } from 'react';
import { config } from '../conf';
import { fetchGet } from '../utils/APIUtils';
import EmailFilter from './EmailFilter';

export function Main({ sessionManager }) {
    const [labels, setLabels] = useState([]);

    const getLabels = async () => {
        console.log('click');
        const res = await fetchGet('labels');
        const l = res.map(e => ({ key: e['id'], 'name': e['name'] }));
        console.log('labels', l);
        setLabels(l);

    };

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
            </div> : ""}


        <button onClick={getLabels}>Get Labels</button>
        <EmailFilter labelOptions={labels} />
    </div>;

}
