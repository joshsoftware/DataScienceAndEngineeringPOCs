import { useMutation } from "@tanstack/react-query";
import axios, { AxiosError } from "axios";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { LoginUserRequest, RegisterUserRequest } from "@/Validators/register";
import { useState } from "react";

export const useUser = () => {

    const router = useRouter();

    const [disableSubmit,setDisableSubmit] = useState(false);
    const { mutate:signup, isPending:isSigningUp } = useMutation({
        mutationKey: ["signup-user"],
        mutationFn: async (payload: RegisterUserRequest) => {
          payload.domain = "joshsoftware.com"
          const response = await axios.post("/admin/api/signup", payload);
          return response.data;
        },
        onSuccess: async (res) => {
        localStorage.setItem("userEmail", res.userEmail)
          toast.success("User Registered Successfully");
          router.push("/admin/signin")
        },
        onError: (error) => {
          if (error instanceof AxiosError) {
            if (error.response?.status === 422) {
              return toast.error("Failed to Register User", {
                description: error.message,
              });
            }
            else if(error.response?.status === 409){
              return toast.error("User already exists, please sign in", {
                action: {
                  label: "Signin",
                  onClick: () => router.push("/admin/signin"),
                }
              });
            }
          }
          return toast.error(
            "Failed to Register User, please try again in some time",
          );
        },
        onSettled: () => {
          setDisableSubmit(false);
        }
    });

    const { mutate:signin, isPending:isSigningIn } = useMutation({
      mutationKey: ["signin-user"],
      mutationFn: async (payload: LoginUserRequest) => {
        const response = await axios.post("/admin/api/signin", payload);
        console.log(response);
        return response.data;
      },
      onSuccess: async (res) => {
        toast.success("User sign in Successfully");
        localStorage.setItem("email",res.email);
        router.push("/admin/scrapper")
      },
      onError: (error) => {
        if (error instanceof AxiosError) {
          if (error.response?.status === 422) {
            return toast.error("Failed to sign in User", {
              description: error.message,
            });
          }
          else if(error.response?.status === 404){
            return toast.error("User does not exists", {
              action: {
                label: "Signup",
                onClick: () => router.push("/admin/signup"),
              }
            });
          }
          else if(error.response?.status === 401){
            return toast.error("Incorrect username or password");
          }
        }
        return toast.error(
          "Failed to sign in User, please try again in some time",
        );
      },
      onSettled: () => {
        setDisableSubmit(false);
      }
  });

    const signupUser = (data: RegisterUserRequest) => {
        setDisableSubmit(true);
        signup(data);
    }

    const signinUser = (data: LoginUserRequest) => {
      setDisableSubmit(true);
      signin(data);
    }

    // const GetSignInUser = async () => {
    //   const { user } = await validateRequest()
    //   if(user) {
    //     return user;
    //   }
    //   return null;
    // }

    return {
        signupUser,
        signinUser,
        isPending: isSigningUp || isSigningIn,
        disableSubmit
    }

}

