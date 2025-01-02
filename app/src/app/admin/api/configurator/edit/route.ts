import { validateRequest } from "@/auth";
import { z } from "zod";


export async function POST(req: Request) {
    try {
        const { user } = await validateRequest()
        if (!user) {
            return new Response(JSON.stringify("UnAuthorized"), { status: 400 });
        }
        const body = await req.json();
        const domain: string = body.domain;

        const updateData = {
            url: body.url,
            max_pages: body.max_pages,
            depth: body.depth,
            frequency: body.frequency
        };

        const response = await fetch(`${process.env.API_URL}/organization/${domain}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),

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
        return new Response("Failed to update configurator", { status: 500 });
    }

        // const body = await req.json();
        // const {
        //     url,
        //     depth,
        //     frequency,
        //     domain,
        //     maxPages
        // }: configuratorPayload = body;

        // const response = await db
        // .update(configurator)
        // .set({
        //   url: url.trim(),
        //   depth,
        //   frequency,
        //   domain,
        //   maxPages,
        //   userID: user?.id,
        // })
        // .where(eq(configurator.domain, domain)) // Replace `configuratorId` with your specific condition
        // .returning();

        // if (response) {
        //     return new Response("Configurator edited successfully.", { status: 200 });
        // }

    //  catch (error) {
    //     console.log(error);

    //     if (error instanceof z.ZodError) {
    //         return new Response(error.message, { status: 422 });
    //     }
    //     return new Response("Failed to edit configurator", { status: 500 });
    // }
}
