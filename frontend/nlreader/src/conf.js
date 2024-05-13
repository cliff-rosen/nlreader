const prod = {
    url: {
        API_URL: "https://nlreader-api.ironcliff.ai"
    },
};

const dev = {
    url: {
        API_URL: "http://127.0.0.1:5001"
    },
};

export const config = process.env.NODE_ENV === "development" ? dev : prod;
