import axios from "axios";

const APIManager = function() {
    const baseURL = location.origin;
    const baseHeader = {};

    const get = async (endPoint, headers, params) => {
        let sendHeaders = Object.assign({}, baseHeader, headers);
        return axios.get(`${baseURL}${endPoint}`, {
            headers: sendHeaders,
            params: params
        })
    }
    
    const post = async (endPoint, headers, params, body) => {
        let sendHeaders = Object.assign({}, baseHeader, headers);
        console.log(`${baseURL}${endPoint}`);
        return axios.post(`${baseURL}${endPoint}`, body, {
            headers: sendHeaders,
            params: params
        })
    }

    return {
        get,
        post
    }
}();

export default APIManager;
