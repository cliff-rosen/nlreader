// MyForm.js

import React, { useState } from 'react';
import { Form, Select, DatePicker, Button } from 'antd';
import moment from 'moment';
import { fetchGet } from '../utils/APIUtils';

const { RangePicker } = DatePicker;

const EmailFilter = ({ labelOptions }) => {
    const [emails, setEmails] = useState([])
    const [form] = Form.useForm();

    const onFinish = (values) => {

        const { labels, dateRange } = values;
        const label = labels;

        const dateFormat = 'YYYY/MM/DD';
        const startDate = dateRange[0].format('YYYY-MM-DD');
        const endDate = dateRange[1].format('YYYY-MM-DD');

        fetchGet(`emails?label=${label}&startDate=${startDate}&endDate=${endDate}`)
            .then(res => console.log(res))

    };

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <Form
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
            <br />

        </div>
    );
};

export default EmailFilter;
