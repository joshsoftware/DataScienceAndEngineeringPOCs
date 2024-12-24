import { z } from "zod";
import { messages, regex } from "./validationUtils"

export const configuratorSchema = z.object({
  url: z.string()
  .refine((url) => validateURL(url), {message: messages.configurator.invalidURL})
  .refine((url) => validateDomain(url), {message: messages.configurator.invalidDomain}),

  maxPages: z.number(),
  domain: z.string().optional(),

  depth: z.number({
    message: messages.configurator.depth
  }),
  frequency: z.number()
})


const validateURL = (url: string) => {
  try {
    const website = new URL(url);
    const domain = website.hostname;
    const domainRegex = regex.domain;
    
    if (domainRegex.test(domain)) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}

const validateDomain = async (url: string) => {
  const adminEmail = localStorage.getItem("email")
  if(adminEmail) {
    if(validateURL(url)) {
      const website = new URL(url);
      const websiteDomain =  (website.hostname).replace(/^www\./, '');
      const emailDomain = adminEmail.substring(adminEmail.indexOf('@') + 1);
    
      if(websiteDomain && emailDomain && websiteDomain.toLowerCase() !== emailDomain.toLowerCase()) {
        return false
      }
      return true;
    }
  }
  return false;
}

export type configuratorRequest = z.infer<typeof configuratorSchema>;
