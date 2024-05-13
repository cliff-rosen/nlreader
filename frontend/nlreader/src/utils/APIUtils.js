import { config } from "../conf";
//import { getUserToken } from "./Auth";

export const BASE_API_URL = config.url.API_URL;

function getHeaders() {
  const headers = {
    "Content-Type": "application/json",
  };

  const xheaders = {
    "Content-Type": "multi-part/formdata",
  };
  /*
  const authProperty = getUserToken();

  if (authProperty !== "") {
    headers["Authorization"] = authProperty;
  }
  */
  return headers;
}

/*
    doFetch(method, endpoint, [body])
    returns json from API endpoint
    throws error if:
        fetch status !== 200
        fetch doesn't return parsable json
        parsed json includes "error" property
*/
async function doFetch(method, endpoint, body, isFileUpload) {
  if (method !== "GET" && method !== "POST" && method !== "PUT") {
    console.log("doFetch called with invalid method:", method);
    throw new Error("doFetch called with invalid method:" + method);
  }

  //const headers = getHeaders();
  const options = {
    method,
    //headers,
  };

  if (body) {
    if (isFileUpload) {
      options.body = body;
    } else {
      options.headers = {
        "Content-Type": "application/json",
      };
      options.body = JSON.stringify(body);
    }
  }
  const res = await fetch(`${BASE_API_URL}/${endpoint}`, options);
  const data = await res.json();

  if (res.status === 401) {
    throw new Error("UNAUTHORIZED");
  } else if (res.status !== 200 || data.error) {
    throw new Error(
      `doFetch error. [status=${res.status}, error=${data?.error}]`
    );
  }

  return data;
}

export async function fetchGet(endpoint) {
  console.log("fetchGet", endpoint);
  return doFetch("GET", endpoint);
}

export async function fetchPost(endpoint, body, isFileUpload) {
  console.log("fetchPost", endpoint);
  return doFetch("POST", endpoint, body, isFileUpload);
}

export async function fetchPut(endpoint, body) {
  console.log("fetchPut", endpoint);
  return doFetch("PUT", endpoint, body);
}
