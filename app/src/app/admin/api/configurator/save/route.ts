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
        const {
            url,
            depth,
            frequency,
            domain,
            maxPages
        }: configuratorPayload = body;

        const response = await fetch(`${process.env.API_URL}/register-organization`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json", 
            },
            body: JSON.stringify({
                "url": url.trim(),
                "domain": domain,
                "depth": depth,
                "max_pages": maxPages,
                "frequency": frequency,
                "user": 1
            }),
        });

        if(response) {
            return new Response("Configurator saved successfully.", { status: 200 });
        } else {
            return new Response("Failed to save configurator", { status: 500 });   
        }
        //     const { user } = await validateRequest()
        //     if (!user) {
        //         return new Response(JSON.stringify("UnAuthorized"), { status: 400 });
        //     }
        //     const body = await req.json();
        //     const {
        //         url,
        //         depth,
        //         frequency,
        //         domain,
        //         maxPages
        //     }: configuratorPayload = body;

        //     const existingData = await db
        //     .select()
        //     .from(configurator)
        //     .where(eq(configurator.url, url.trim()))

        //     if (existingData && existingData[0]) {
        //     return new Response("This URL is already in the system.", {
        //         status: 201,
        //     })
        // }

        //     const response = await db.insert(configurator).values({
        //         url: url.trim(),
        //         depth,
        //         frequency,
        //         domain,
        //         maxPages,
        //         userID: user?.id,
        //     }).returning();

        //     if(response) {
        //         return new Response("Configurator saved successfully.", { status: 200 });
        //     }

    } catch (error) {
        console.log(error);

        if (error instanceof z.ZodError) {
            return new Response(error.message, { status: 422 });
        }
        return new Response("Failed to save configurator", { status: 500 });
    }
}
