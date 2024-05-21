import React from 'react';
import { Typography } from 'antd';

export const EmailMessage = ({ email }) => {
    if (!email) {
        return null;
    }
    return (
        <div>
            <div>
                <Typography.Paragraph>
                    <b>Date:</b> {email.message_date}
                </Typography.Paragraph>
                <Typography.Paragraph>
                    <b>Sender:</b> {email.message_sender}
                </Typography.Paragraph>
                <Typography.Paragraph>
                    <b>Subject:</b> {email.message_subject}
                </Typography.Paragraph>

                {/* <div dangerouslySetInnerHTML={{ __html: email.message_body_html }} /> */}

                <div style={{ display: 'flex' }}>
                    <iframe
                        title="Email Content"
                        srcDoc={email.message_body_html}
                        sandbox="allow-scripts allow-same-origin allow-popups allow-forms allow-modals allow-downloads"
                        width="800px"
                        height="800px"
                    />
                    <iframe
                        title="Email Content"
                        srcDoc={email.message_body}
                        sandbox="allow-scripts allow-same-origin allow-popups allow-forms allow-modals allow-downloads"
                        width="800px"
                        height="800px"
                    />
                </div>

            </div>
        </div>
    );
};
