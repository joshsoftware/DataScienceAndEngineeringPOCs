import { validateRequest } from "@/auth";
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
      {/* TODO need once login done  */}
      {/* <div className="flex justify-start w-full mb-8">
          <NavigateBack />
        </div> */}
      <div className="flex flex-1 justify-center items-center">
        <UserForm formType="signin" />
      </div>
    </div>
  );
}
