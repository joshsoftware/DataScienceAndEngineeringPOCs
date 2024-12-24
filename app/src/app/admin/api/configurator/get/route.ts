import { validateRequest } from "@/auth";
import { db } from "@/db";
import { configurator, configuratorPayload } from "@/db/schema";
import { z } from "zod";
import { eq } from "drizzle-orm";


export async function POST(req: Request) {
    try {
        const { user } = await validateRequest()
        if (!user) {
            return new Response(JSON.stringify("UnAuthorized"), { status: 400 });
        }
        const body = await req.json();
        const domain: string = body.domain;

        const response = await fetch(`${process.env.API_URL}/organization/${domain}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        const data: any = await response.json();
       
        return new Response(JSON.stringify(data), {
            status: 200
        })

    } catch (error) {
        console.log(error);

        if (error instanceof z.ZodError) {
            return new Response(error.message, { status: 422 });
        }
        return new Response("Failed to get configurator", { status: 500 });
    }
}
