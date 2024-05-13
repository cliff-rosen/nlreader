import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { fetchGet } from '../utils/APIUtils';

export default function Auth() {
    console.log('Auth')

    const [queryParams, setQueryParams] = useState({});
    const location = useLocation();

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const params = {};
        for (const [key, value] of searchParams) {
            params[key] = value;
        }
        var code = params['code']
        console.log('code:', code)
        setQueryParams(params);

        const getTokenFromCode = async (i_code) => {
            const t = await fetchGet(`get_token_from_auth_code?code=${i_code}`);
            console.log(t);
        };

        getTokenFromCode(code);

    }, [location]); // Depend on location to re-run this effect if location changes

    return (
        <div>
            <h1>Query Parameters</h1>
            <pre>{JSON.stringify(queryParams, null, 2)}</pre>
        </div>
    );
}
