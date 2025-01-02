import { validateRequest } from "@/auth";
import NavigateBack from "@/components/admin/NavigateBack";
import EmbeddedCodeCard from "@/components/admin/embeddedCodeCard";
import { Metadata } from "next";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Embedded card",
};

const page = async () => {
  const { user } = await validateRequest();

	if (!user) return redirect("/admin/signin");

  return (
    <div className="flex flex-col w-full pt-8">
      <div className="flex justify-start w-full mb-8">
        <NavigateBack href="/admin/scrapper" />
      </div>
      <div className="flex flex-1 justify-center items-start">
        <EmbeddedCodeCard />
      </div>
    </div>
  );
};

export default page;
