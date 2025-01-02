import { cookies } from "next/headers";
import { cache } from "react";
import { jwtVerify } from "jose";

const SECRET_KEY = new TextEncoder().encode(process.env.JWT_SECRET_KEY);

export const validateRequest = cache(
	async (): Promise<{ user: any } | { user: null; session: null }> => {
		const cookiesInstance = await cookies();
		const token = cookiesInstance.get("access_token")?.value ?? null;
		if (!token) {
			return {
				user: null,
				session: null
			};
		}

		try {
			const { payload } = await jwtVerify(token, SECRET_KEY, {
				algorithms: ["HS256"],
			});
			if (payload) {
				return {
					user: payload
				};
			}
			return {
				user: null,
				session: null
			};
		} catch { }
		return {
			user: null,
			session: null
		};
	}
);

function parseJwtResponse(responseString: string) {
    return Object.fromEntries(
        responseString.split(' ').map(pair => {
            const [key, value] = pair.split('=');
            const cleanedValue: any = value.replace(/'/g, '');
            if (cleanedValue === 'True') return [key, true];
            if (cleanedValue === 'False') return [key, false];
            if (!isNaN(cleanedValue)) return [key, Number(cleanedValue)];
            return [key, cleanedValue];
        })
    );
}

