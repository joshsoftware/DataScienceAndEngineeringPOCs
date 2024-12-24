import { validateRequest } from "@/auth";
// import NavigateBack from "@/components/admin/NavigateBack";
import UserForm from "@/components/admin/UserForm";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";
export const fetchCache = "force-no-store";
export const revalidate = 0;


export default async function Page() {

    const { user } = await validateRequest();
    if (user) return redirect("/admin/scrapper");

	return (
        <div className="flex flex-col w-full pt-8">
        <div className="flex flex-1 justify-center items-center">
          <UserForm formType="signup" />
        </div>
      </div>
	);
}
