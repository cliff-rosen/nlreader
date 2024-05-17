import React from 'react';
import { Table } from 'antd';

const EmailList = ({ emails }) => {
    // Column definitions
    const columns = [
        {
            title: 'Date',
            dataIndex: 'date',
            key: 'date',
        },
        {
            title: 'From',
            dataIndex: 'sender',
            key: 'sender',
        },
        {
            title: 'Subject',
            dataIndex: 'subject',
            key: 'subject',
        },
        {
            title: 'Body',
            dataIndex: 'body',
            key: 'body',
        },
    ];

    return <Table dataSource={emails} columns={columns} />;
};

export default EmailList;
