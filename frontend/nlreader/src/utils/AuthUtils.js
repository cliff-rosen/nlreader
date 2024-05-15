import { useState } from "react";
import { fetchGet } from "./APIUtils";


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


export const useSessionManager = () => {
    const [user, setUser] = useState(getUserFromStorage());

    const login = async (token) => {
        const res = await fetchGet(`login?token=${token}`)
        console.log('login result', res);
        setUser(res)
        setUserInStorage(res)
    }


    return { user, login }

}  
