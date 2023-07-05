import axios from "axios";

const APIManager = function() {
    let baseURL = location.origin;
    if(process.env.NODE_ENV == 'development' )
    {
        baseURL= `http://127.0.0.1:${process.env.PORT}`
    }
    let baseHeader = {};

    const get = async (endPoint, headers, params) => {
        let sendHeaders = Object.assign({}, baseHeader, headers);
        return axios.get(`${baseURL}${endPoint}`, {
            headers: sendHeaders,
            params: params
        })
    }
    
    const post = async (endPoint, headers, params, responseType, body) => {
        let sendHeaders = Object.assign({}, baseHeader, headers);
        return axios.post(`${baseURL}${endPoint}`, body, {
            headers: sendHeaders,
            responseType: responseType,
            params: params
        })
    }

    return {
        get,
        post
    }
}();

export default APIManager;
