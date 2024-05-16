import React, { useState } from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { Layout, Space, Typography, Menu, MenuProps } from 'antd';
import { GoogleLogin } from '@react-oauth/google';

const { Header } = Layout;
const items = [
    {
        label: 'logout',
        key: 'logout',
    },
]

const Nav = ({ sessionManager }) => {
    console.log("Nav render");
    const navigate = useNavigate();
    const location = useLocation();
    console.log(location)

    const onSuccess = tokenResponse => {
        console.log(tokenResponse)
        sessionManager.login(tokenResponse.credential)
    }

    const onClick = (e) => {
        console.log('click ', e);
        // navigate(`/${e.key}`)
        sessionManager.logout()
    };

    return (
        <Header
            style={{
                display: "flex",
                alignItems: "center",
                paddingTop: 10,
                paddingBottom: 10,
                border: "none",
                background: "white"
            }}
        >
            <Typography.Title level={4} style={{ margin: 0 }}>
                <Link to="/" style={{ textDecoration: "none" }}>
                    NL Reader
                </Link>
            </Typography.Title>

            <div style={{ minWidth: 20 }}></div>

            <div
                style={{
                    flexGrow: 1,
                    color: "red",
                    border: "none",
                }}
            >
            </div>

            <div style={{ flexGrow: 0, fontSize: "1em" }}></div>

            <div style={{ flexGrow: 0, fontSize: "1em" }}>
                {sessionManager?.user?.user_email}
            </div>


            <div style={{ flexGrow: 0, fontSize: "1em" }}>
                {sessionManager?.user?.user_id ?
                    <div>
                        <Menu onClick={onClick} selectedKeys={[location.pathname.substring(1)]} mode="horizontal" items={items} />
                    </div>
                    :
                    <GoogleLogin
                        onSuccess={onSuccess}
                        onError={() => {
                            console.log('Login Failed');
                        }}
                    />
                }
            </div>
        </Header>
    );
};

export default Nav;