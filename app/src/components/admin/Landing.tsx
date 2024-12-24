"use client";

import { primaryFont } from "@/fonts";
import { cn } from "@/lib/utils";
import Image from "next/image";
import { Button, buttonVariants } from "./ui/button";
import { useRouter } from "next/navigation";
import Link from "next/link";

const Landing = () => {

  return (
    <div className="flex flex-col md:flex-row w-full h-full justify-between gap-4 pt-16">
      <div className="w-full flex flex-col gap-4 justify-center items-start">
        <h1 className={cn(primaryFont.className, "text-3xl text-[#3f51b5] ")}>
          Welcome
        </h1>
        <h1 className={cn(primaryFont.className, "text-5xl")}>
          Heading
        </h1>
        <p>  
          description.......
          </p>
         <div className="w-full flex gap-3">
        <Link
          href={"/signin"}
          className={buttonVariants({
            className: "!bg-[#3f51b5] !hover:bg-[#303f9f] text-white",
          })}
        >
          Configure Organization
        </Link>

        {/* <Link
          href={"/analyse"}
          className={buttonVariants({
            className: "!bg-[#3f51b5] !hover:bg-[#303f9f] text-white",
          })}
        >
          View Analysis
        </Link> */}
        </div>
      </div>
      <Image
        src={"/landing_graphics.png"}
        className="self-center"
        width={500}
        height={538}
        alt="Josh Logo"
      />
    </div>
  );
};

export default Landing;
