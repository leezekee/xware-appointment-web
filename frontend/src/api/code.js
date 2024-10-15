const ResponseCode = Object.freeze({
    SUCCESS: 200200,

    // Custom
    USER_EXISTED: 2004002,          // User already exists
    WRONG_PASSWORD: 2004003,        // Password error
    PASSWORD_NOT_MATCH: 2004001,    // Password not match
    APPOINTMENT_NOT_MATCH: 2004004, // Appointment not match
    TOKEN_REQUIRED: 2004011,        // Token is required
    INVALID_TOKEN: 2004012,         // Invalid token
    USER_NOT_FOUND: 2004041,        // User not found
    APPOINTMENT_NOT_FOUND: 2004042, // Appointment not found
    PERMISSION_DENIED: 2004031      // Permission denied
});

export default ResponseCode;