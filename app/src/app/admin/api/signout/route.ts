import { validateRequest } from "@/auth";
import { cookies } from "next/headers";

export async function POST(req: Request) {
    try {
        // Validate the request to ensure a session exists
        const { user } = await validateRequest()

        if (!user) {
            return new Response("No active session found", { status: 401 });
        }

        const cookiesSession = await cookies();
        cookiesSession.delete("access_token");
        
        return new Response("User logged out successfully", { status: 200 });
    } catch (error) {
        console.error("Logout error:", error);

        return new Response("Failed to log out", { status: 500 });
    }
}
