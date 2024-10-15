import sha256 from 'js-sha256';

const encrypt = (_raw) => {
    return sha256(_raw);
}

export default encrypt;