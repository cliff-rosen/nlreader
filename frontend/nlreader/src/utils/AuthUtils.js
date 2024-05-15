import { fetchGet } from "./APIUtils";

export const login = async (token) => {
    const res = await fetchGet(`login?token=${token}`)
    console.log('login result', res);
    setUserInStorage(res)
}

export const setUserInStorage = (user) => {
    localStorage.setItem("user", JSON.stringify(user));
};

export const getUserFromStorage = () => {
    var userFromStorage;

    try {
        userFromStorage = JSON.parse(localStorage.getItem("user"));
    } catch {
        userFromStorage = { userID: 0, token: "" };
    }
    return userFromStorage;
};


