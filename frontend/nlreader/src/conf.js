const prod = {
    url: {
        API_URL: "https://nlreader-api.ironcliff.ai",
        GAUTH_URL: "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=604005571-miie2779t7p81l65up26sb6dih1q7uoe.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth_callback&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&state=rDOiNTJzzr7UHOhrjyEndqEqnKxxn4&access_type=offline&include_granted_scopes=true"
    },
};

const dev = {
    url: {
        API_URL: "http://127.0.0.1:5001",
        GAUTH_URL: "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=604005571-miie2779t7p81l65up26sb6dih1q7uoe.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth_callback&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&state=rDOiNTJzzr7UHOhrjyEndqEqnKxxn4&access_type=offline&include_granted_scopes=true"
    },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
