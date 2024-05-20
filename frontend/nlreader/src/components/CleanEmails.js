// MyForm.js

import React, { useState, useEffect } from 'react';
import { Typography, Button, Divider } from 'antd';
import { fetchGet } from '../utils/APIUtils';
import EmailList from './EmailList';


const CleanEmails = () => {
    const [emails, setEmails] = useState([])
    const [emailID, setEmailID] = useState(0)

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

                <div>
                    <Button disabled={emailID == 0 ? true : false} onClick={() => setEmailID(id => id - 1)} type="default" xsize="large" style={{ marginRight: '10px' }}>
                        PREV
                    </Button>
                    <Button disabled={emailID == emails.length - 1 ? true : false} onClick={() => setEmailID(id => id + 1)} type="default" xsize="large">
                        NEXT
                    </Button>
                </div>

                <Divider />

                {emails.length > 0 ? <EmailMessage email={emails[emailID]} /> : ""}
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
    if (!email) {
        return null;
    }
    return (
        <div>
            <div>
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

