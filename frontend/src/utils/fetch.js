export default function doApiRequest(path, params, data) {
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
  const url = path + (params !== {} ? "?" : "") + new URLSearchParams(params);
  return fetch(url, formattedData).then((response) => response.json());
}
