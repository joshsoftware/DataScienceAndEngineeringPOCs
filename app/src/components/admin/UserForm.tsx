"use client";

import { tertiaryFont } from "@/fonts";
import { Input } from "./ui/input";
import { Button, buttonVariants } from "./ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/admin/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { RegisterUserRequest, LoginUserRequest, registerUserSchema, loginUserSchema } from "@/Validators/register";

import { useUser } from "@/hooks/useUser";
import Link from "next/link";

interface UserFormProps {
  formType: "signin" | "signup";
}

const UserForm = (props: UserFormProps) => {

  const { formType } = props;

  const { disableSubmit, isPending, signupUser, signinUser } = useUser();

  const registerForm = useForm<RegisterUserRequest>({
    resolver: zodResolver(registerUserSchema),
    defaultValues: {
      name: "",
      contactNumber: "",
      userEmail: "",
      password: "",
      confirmPassword: ""
    },
    mode: "all",
  });

  const loginForm = useForm<LoginUserRequest>({
    resolver: zodResolver(loginUserSchema),
    defaultValues: {
      userEmail: "",
      password: ""
    },
    mode: "all",
  });

  // For register
  const onRegisterSubmit = (data: RegisterUserRequest) => signupUser(data);
  // For login 
  const onLoginSubmit = (data: LoginUserRequest) => signinUser(data);

  return (
    <div className="flex flex-col gap-2 w-full justify-center items-center">
      {
        formType === "signup" ? 
        <Form {...registerForm}>
          <form
            onSubmit={registerForm.handleSubmit(onRegisterSubmit)}
            className="w-full max-w-sm flex flex-col gap-4 justify-center items-center"
          >
            <h1 className="text-3xl font-bold">Sign Up</h1>
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <div className="pb-1.5">
                <FormField
                  control={registerForm.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel> Name</FormLabel>
                      <FormControl>
                        <Input {...field} type="input" placeholder="Enter your Name" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="gap-1.5">
                <FormField
                  control={registerForm.control}
                  name="contactNumber"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel> Contact Number</FormLabel>
                      <FormControl>
                        <Input {...field} type="input" placeholder="Enter Contact Number" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            </div>
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <FormField
                control={registerForm.control}
                name="userEmail"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input {...field} placeholder="Enter your Email" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid w-full max-w-sm items-center gap-1.5">
              <FormField
                control={registerForm.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input {...field} type="password" placeholder="Enter your Password" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <FormField
                control={registerForm.control}
                name="confirmPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel> Confirm Password</FormLabel>
                    <FormControl>
                      <Input {...field} type="password" placeholder="Confirm your password" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <Button
              isLoading={disableSubmit || isPending}
              disabled={disableSubmit || isPending}
              type="submit"
              className="bg-[#668D7E] hover:bg-[#668D7E] text-white w-full"
            >Sign Up
            </Button>
          </form>
        </Form> :

          <Form {...loginForm}>
            <form
              onSubmit={loginForm.handleSubmit(onLoginSubmit)}
              className="w-full max-w-sm flex flex-col gap-4 justify-center items-center"
            >
              <h1 className="text-3xl font-bold">Sign In
              </h1>
              <div className="grid w-full max-w-sm items-center gap-1.5">
                <FormField
                  control={loginForm.control}
                  name="userEmail"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input {...field} placeholder="Enter your Email" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className="grid w-full max-w-sm items-center gap-1.5">
                <FormField
                  control={loginForm.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input {...field} type="password" placeholder="Enter your Password" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <Button
                isLoading={disableSubmit || isPending}
                disabled={disableSubmit || isPending}
                type="submit"
                className="bg-[#668D7E] hover:bg-[#668D7E] text-white w-full"
              >Sign In
              </Button>
            </form>
          </Form>
      }
      
      <div>
        {formType === "signup" ? "Already have an account?" : "Don't have account? "}
        <Link
          href={formType === "signup" ? "/admin/signin" : "/admin/signup"}
          aria-disabled={disableSubmit || isPending}
          className={`${disableSubmit || isPending ? 'pointer-events-none' : ''} ${buttonVariants({
            variant: "link",
            className: "text-[#668D7E] hover:text-[#668D7E] font-bold"
          })}`}
        >
          {formType === "signup" ? "Sign In" : "Sign Up"}
        </Link>
      </div>
    </div>
  );
};

export default UserForm;