// MyForm.js

import React, { useState, useEffect } from 'react';
import { Form, Select, DatePicker, Button } from 'antd';
import { fetchGet } from '../utils/APIUtils';
import EmailList from './EmailList';

const { RangePicker } = DatePicker;

const EmailFilter = () => {
    const [emails, setEmails] = useState([])
    const [form] = Form.useForm();
    const [labelOptions, setLabelOptions] = useState([]);

    useEffect(() => {
        const getLabels = async () => {
            const res = await fetchGet('labels');
            const l = res.map(e => ({ key: e['id'], 'name': e['name'] }));
            console.log('labels', l);
            setLabelOptions(l);
        };
        getLabels()
    }, [])

    const onFinish = (values) => {

        const { labels, dateRange } = values;
        const label = labels;

        const dateFormat = 'YYYY/MM/DD';
        const startDate = dateRange[0].format('YYYY-MM-DD');
        const endDate = dateRange[1].format('YYYY-MM-DD');

        fetchGet(`messages?label=${label}&startDate=${startDate}&endDate=${endDate}`)
            .then(res => {
                console.log(res)
                setEmails(res.messages)
            })

    };

    return (
        <div>
            <div style={{ maxWidth: '600px', margin: '0 auto', xborder: 'solid' }}>
                <h1>Select Batch</h1>
                <Form
                    style={{ display: "xflex" }}
                    form={form}
                    name="custom-form"
                    layout="vertical"
                    onFinish={onFinish}
                    initialValues={{
                        labels: '-',
                        dateRange: [],
                    }}
                >
                    <Form.Item
                        name="labels"
                        label="Labels"
                        rules={[{ required: true, message: 'Please select a label' }]}
                    >
                        <Select placeholder="Select a label">
                            {labelOptions.map(e => <Select.Option value={e['key']}>{e['name']}</Select.Option>)}
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="dateRange"
                        label="Date Range"
                        rules={[{ required: true, message: 'Please select a date range' }]}
                    >
                        <RangePicker />
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form>

            </div>
            <EmailList emails={emails} />
        </div>
    );
};

export default EmailFilter;
