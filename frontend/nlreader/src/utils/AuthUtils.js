import { useState } from "react";
import { fetchGet } from "./APIUtils";


export const getUserToken = () => {
    var user;

    try {
        user = JSON.parse(localStorage.getItem("user"));
        console.log('getUserToken', user)
    } catch {
        user = { userID: -1, token: "" };
    }
    if (user.user_id > 0) {
        return "Bearer " + user.token;
    }
    return "";
};

export const useSessionManager = () => {
    const [user, setUser] = useState(getUserFromStorage());

    const login = async (token) => {
        const res = await fetchGet(`login?token=${token}`)
        console.log('login result', res);
        setUser(res.user)
        setUserInStorage(res.user)
    }

    const logout = () => {
        const user = { user: { user_id: 0 } }
        setUserInStorage(user)
        setUser(user)
    }

    return { user, login, logout }

}

const getUserFromStorage = () => {
    var userFromStorage;

    try {
        userFromStorage = JSON.parse(localStorage.getItem("user"));
    } catch {
        userFromStorage = { userID: 0, token: "" };
    }
    return userFromStorage;
};

const setUserInStorage = (user) => {
    localStorage.setItem("user", JSON.stringify(user));
};
