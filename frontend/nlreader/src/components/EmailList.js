import React from 'react';
import { Table } from 'antd';

const EmailList = ({ emails }) => {
    // Column definitions
    const columns = [
        {
            title: 'Date',
            dataIndex: 'message_date',
            key: 'message_date',
        },
        {
            title: 'From',
            dataIndex: 'message_sender',
            key: 'message_sender',
        },
        {
            title: 'Subject',
            dataIndex: 'message_subject',
            key: 'message_subject',
        },
        {
            title: 'Body',
            dataIndex: 'message_body',
            key: 'message_body',
        },
    ];

    return <Table dataSource={emails} columns={columns} />;
};

export default EmailList;


