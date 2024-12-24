import { validateRequest } from "@/auth";

export async function GET(req: Request) {
    try {

        const { user } = await validateRequest()

        if (!user) {
            return new Response(JSON.stringify("UnAuthorized"), { status: 400 });
        }

        const data = {
            message: "User is logged in",
            user:  user.sub
        } 

        return new Response(JSON.stringify(data), { status: 200 });
    } catch (error) {
        return new Response("Failed to check session", { status: 500 });
    }
}
