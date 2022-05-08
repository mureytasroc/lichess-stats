export const API_BASE_URL =
  process.env.NODE_ENV === "production"
    ? "https://lichess-stats.org/api"
    : "http://localhost:8000/api";

export function getApiUrl(path) {
  if (/^https?:\/\//.test(path)) {
    const url = new URL(path);
    return url.pathname + url.search;
  }
  return API_BASE_URL + path;
}

export function doApiRequest(path, params, data) {
  let formattedData = data;
  if (!formattedData) {
    formattedData = {};
  }
  formattedData.mode = "cors";
  formattedData.method = "GET";
  if (typeof document !== "undefined") {
    formattedData.headers = formattedData.headers || {};
    if (!(formattedData.body instanceof FormData)) {
      formattedData.headers.Accept = "application/json";
      formattedData.headers["Content-Type"] = "application/json";
    }
  }
  if (formattedData.body && !(formattedData.body instanceof FormData)) {
    formattedData.body = JSON.stringify(formattedData.body);
  }
  const url =
    getApiUrl(path) + (params !== {} ? "?" : "") + new URLSearchParams(params);
  return fetch(url, formattedData).then((response) => response.json());
}
