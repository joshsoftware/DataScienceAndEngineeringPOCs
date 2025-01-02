import { registerUserSchema } from "@/Validators/register";
import { z } from "zod";

export async function POST(req: Request) {
  try {
    const body = await req.json();

    const { password, userEmail, name, contactNumber, domain } = registerUserSchema.parse(body);

      const response = await fetch(`${process.env.API_URL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          contactNumber: contactNumber,
          email: userEmail,
          password: password,
          domain: domain,
        }),
      });

      return new Response(JSON.stringify(response), {
        status: 201,
      });
  } catch (error) {
    console.log("------------------->", error);
    if (error instanceof z.ZodError) {
      return new Response(error.message, { status: 422 });
    }
    return new Response("Failed to Register User", { status: 500 });
  }
}
