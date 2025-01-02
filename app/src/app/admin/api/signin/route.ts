import { validateRequest } from "@/auth";
import { loginUserSchema } from "@/Validators/register";
import { NextResponse } from "next/server";
import { z } from "zod";

interface RegisterResponse {
    message: string;
    data: {
        access_token: string;
    };
}

export async function POST(req: Request) {
    try {
        const { user } = await validateRequest();
        const body = await req.json();
        const { password, userEmail } = loginUserSchema.parse(body);

        if (!process.env.API_URL) {
            throw new Error("API_URL environment variable is not set");
        }

        const response = await fetch(`${process.env.API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: userEmail,
                password: password,
            }),
        });

        const data: RegisterResponse = await response.json();
        if (!response.ok) {
            throw new Error(data.message || response.statusText || "Something went wrong");
        }

        const response1 = NextResponse.json({
            message: "",
            success: true,
            email: userEmail
        });

        response1.cookies.set("access_token", data.data.access_token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            path: "/",
        });

        return response1;
    } catch (error: any) {
        console.error("Error during login:", error);

        if (error instanceof z.ZodError) {
            return NextResponse.json({ error: error.issues }, { status: 400 });
        }
        return NextResponse.json({ error: error.message || "Failed to Register User" }, { status: 500 });
    }
}
