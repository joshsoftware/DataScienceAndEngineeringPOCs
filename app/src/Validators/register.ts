import { z } from "zod";
import { messages } from "./validationUtils"

export const registerUserSchema = z.object({
  name: z.string().min(2, messages.register.nameMinLength,),

  contactNumber: z.string()
    .min(1, messages.register.contactNumRequired)
    .regex(/^\+?[1-9]\d{1,11}$/, messages.register.contactNumberInvalid),

  userEmail: z.string()
    .min(1, messages.register.emailRequired)
    .email(messages.invalidEmail,),

  password: z.string()
    .min(8, messages.register.passwordMinLength)
    .max(16, messages.register.passwordMaxLength),

  confirmPassword: z.string().min(1, messages.register.passwordRequired),

  domain: z.string().optional()

}).refine(data => data.password === data.confirmPassword, {
  message: messages.register.passwordMismatch,
  path: ["confirmPassword"]
});

export const loginUserSchema = z.object({
  userEmail: z.string()
    .min(1, messages.register.emailRequired)
    .email(messages.invalidEmail),

  password: z.string()
    .min(8, messages.register.passwordMinLength)
    .max(16, messages.register.passwordMaxLength),
})

export type LoginUserRequest = z.infer<typeof loginUserSchema>;

export type RegisterUserRequest = z.infer<typeof registerUserSchema>;
