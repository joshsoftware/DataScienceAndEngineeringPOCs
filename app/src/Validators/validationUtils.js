// Common regex patterns
export const regex = {
    domain: /^[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9-]{1,63})+$/
  };
  
  // Common messages
  export const messages = {
    invalidEmail: "Invalid email address.",
    configurator: {
        invalidDomain: "Invalid domain in URL.",
        invalidURL: "Invalid URL.",
        depth: "Depth is required"
    },

    register: {
        passwordMinLength: "Password must be at least 8 characters long",
        passwordMaxLength: "Password must be at most 16 characters long",
        passwordMismatch: "Password doesn't match",
        nameMinLength: "Name should be at least 2 characters long",
        contactNumberInvalid: "Invalid Contact Number",
        contactNumRequired: "Contact number required",
        passwordRequired: "Confirm password required",
        nameRequired: "name required",
        emailRequired: "Email required",
    }
  };
  