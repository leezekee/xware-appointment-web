const decodeToken = (token) => {
    return JSON.parse(atob(token.split('.')[1]));
}

export default decodeToken;