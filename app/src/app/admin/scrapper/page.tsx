import { validateRequest } from "@/auth";
import NavigateBack from "@/components/admin/NavigateBack";
import ConfiguratorForm from "@/components/admin/ConfiguratorForm";
import { Metadata } from "next";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Scrapper | Configurator",
};

const page = async () => {
  const { user } = await validateRequest();

  if (!user) return redirect("/signin");

  return (
    <div className="flex flex-col w-full pt-8">
      <div className="flex justify-start w-full mb-8">
        <NavigateBack href="/admin" />
      </div>
      <div className="flex flex-1 justify-center items-start">
        <ConfiguratorForm />
      </div>
    </div>
  );
};

export default page;
