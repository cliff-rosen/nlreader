// MyForm.js

import React, { useState, useEffect } from 'react';
import { fetchGet } from '../utils/APIUtils';
import EmailList from './EmailList';


const CleanEmails = () => {
    const [emails, setEmails] = useState([])

    useEffect(() => {
        const batch_id = 3
        const getEmails = async () => {
            fetchGet(`batches?batch_id=${batch_id}`)
                .then(res => {
                    console.log(res.messages)
                    setEmails(res.messages)
                })
        };
        getEmails()
    }, [])

    return (
        <div>
            <div style={{ maxWidth: '600px', margin: '0 auto', xborder: 'solid' }}>
                <h1>Clean Emails</h1>
                <EmailList emails={emails} />
            </div>
        </div>
    );
};

export default CleanEmails;
