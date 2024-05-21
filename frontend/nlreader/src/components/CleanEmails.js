// MyForm.js

import React, { useState, useEffect } from 'react';
import { Button, Divider } from 'antd';
import { fetchGet } from '../utils/APIUtils';
import EmailList from './EmailList';
import { EmailMessage } from './EmailMessage';


const CleanEmails = () => {
    const [emails, setEmails] = useState([])
    const [emailID, setEmailID] = useState(0)

    useEffect(() => {
        const batch_id = 26
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
            <div style={{ xmaxWidth: '600px', margin: '0 auto', xborder: 'solid' }}>
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


