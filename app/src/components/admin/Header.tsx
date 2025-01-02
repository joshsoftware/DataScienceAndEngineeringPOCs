"use client";
import { primaryFont } from "@/fonts";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import Image from "next/image";
import Link from "next/link";
import { toast } from "sonner";
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react";

const Header =  () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  const { mutate: isUserLoggedIn } = useMutation({
    mutationKey: ["isUserLoggedIn"],
    mutationFn: async () => {
      const response = await axios.get("/admin/api/checkSession");
      return response.data;
    },
    onSuccess: (res: any) => {
      setIsLoggedIn(true);
    },
    onError: (error: any) => {
      setIsLoggedIn(false);
    },
  });

  useEffect(() => {
    // Trigger the mutation on mount
    isUserLoggedIn();
  }, [isUserLoggedIn]);

  const router = useRouter()

  const logoutUser = () => {
    logOut();
  }

  const { mutate: logOut } = useMutation({
    mutationKey: ["logOut"],
    mutationFn: async () => {

      const response = await axios.post("/admin/api/signout");
      return response.data;
    },
    onSuccess: async (res: any) => {
      toast.success("signed out successfully.");
      router.push("/admin/signin")
    },
    onError: (error) => {
      return toast.error(error?.message ??
        "Failed to log out"
      );
    },
  });

  return (
    <header
      className={
        `flex justify-between items-center bg-[#ffffff] border-b-2,
        ${primaryFont.className}`
      }
    >
      <div className="container flex items-center py-3">
        <Link href={"/admin"} className="text-3xl text-black">
          Scrapper {isLoggedIn}
        </Link>
        <div className="flex justify-center items-center w-full">
          <Image
            src={"/JoshLogo.svg"}
            className="self-center"
            width={131}
            height={100}
            alt="Josh Logo"
          />
        </div>
        {
          isLoggedIn &&
          <button onClick={logoutUser} className="text-2xl text-gray-600">
            sign out
          </button>
        }
      </div>
    </header>
  );
};

export default Header;
