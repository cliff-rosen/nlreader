import React from 'react';
import { Table } from 'antd';

const EmailList = ({ emails }) => {
    // Sample data
    const data = [
        {
            key: '1',
            date: '2024-05-01',
            subject: 'Math',
        },
        {
            key: '2',
            date: '2024-05-02',
            subject: 'Science',
        },
        {
            key: '3',
            date: '2024-05-03',
            subject: 'History',
        },
    ];

    // Column definitions
    const columns = [
        {
            title: 'Date',
            dataIndex: 'date',
            key: 'date',
        },
        {
            title: 'Subject',
            dataIndex: 'subject',
            key: 'subject',
        },
    ];

    return <Table dataSource={emails} columns={columns} />;
};

export default EmailList;
