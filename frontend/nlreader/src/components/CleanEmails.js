// MyForm.js

import React, { useState, useEffect } from 'react';
import { Typography } from 'antd';
import { fetchGet } from '../utils/APIUtils';
import EmailList from './EmailList';


const CleanEmails = () => {
    const [emails, setEmails] = useState([])

    useEffect(() => {
        const batch_id = 25
        const getEmails = async () => {
            fetchGet(`batches?batch_id=${batch_id}`)
                .then(res => {
                    console.log(res.messages)
                    setEmails(res.messages)
                })
        };
        console.log('CleanEmails -> useEffect()')
        getEmails()
    }, [])

    return (
        <div>
            <div style={{ maxWidth: '600px', margin: '0 auto', xborder: 'solid' }}>
                <h1>Clean Emails</h1>
                {emails.length > 0 ? <EmailMessage email={emails[0]} /> : ""}
                {/* <EmailList emails={emails} /> */}
            </div>
        </div>
    );
};

export default CleanEmails;

// component that displays an email included date, sender, subject, and body
// uses antd Table component to display the data
// takes in an email object as a prop
const EmailMessage = ({ email }) => {
    return (
        <div>
            <div>
                <Typography.Title level={4}>Email Details</Typography.Title>
                <Typography.Paragraph>
                    <b>From:</b> {email.message_subject}
                </Typography.Paragraph>
                <Typography.Paragraph>
                    <b>Date:</b> {email.message_date}
                </Typography.Paragraph>
                <Typography.Paragraph>
                    <b>Sender:</b> {email.message_sender}
                </Typography.Paragraph>
                <div dangerouslySetInnerHTML={{ __html: email.message_body_html }} />
            </div>
        </div>
    );
}

